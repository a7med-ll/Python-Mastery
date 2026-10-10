import re
import uuid
from functools import lru_cache

import numpy as np
import pymupdf
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)
from sentence_transformers import CrossEncoder, SentenceTransformer


#---------------------------------------------------------------------------------------------------------
# PDF EXTRACTION
#---------------------------------------------------------------------------------------------------------

def extract_pdf_pages(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text()   # --> full extractable text from current page

        blocks = page.get_text("blocks")   # --> layout-aware text blocks from PyMuPDF

        paragraphs = [
            block[4].strip()
            for block in blocks
            if block[4].strip()
        ]   # --> keep only non-empty text blocks

        pages.append({
            "page": page_number,
            "text": text,
            "paragraphs": paragraphs
        })

    document.close()

    return pages


#---------------------------------------------------------------------------------------------------------
# FIXED-SIZE CHUNKING
#---------------------------------------------------------------------------------------------------------

def fixed_size_chunking(pages, chunk_size=300, overlap=50):
    chunks = []

    for page in pages:

        text = page["text"]
        page_number = page["page"]

        start = 0
        chunk_number = 1

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]   # --> fixed character slice

            chunks.append({
                "chunk_id": f"p{page_number}-c{chunk_number}",
                "page": page_number,
                "text": chunk_text,
                "strategy": "fixed"
            })

            start += chunk_size - overlap   # --> preserve overlap between chunks

            chunk_number += 1

    return chunks


#---------------------------------------------------------------------------------------------------------
# PARAGRAPH-AWARE CHUNKING
#---------------------------------------------------------------------------------------------------------

def paragraph_chunking(pages, max_chunk_size=500):
    chunks = []

    for page in pages:

        page_number = page["page"]
        paragraphs = page["paragraphs"]

        current_chunk = ""
        chunk_number = 1

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            # --> keep adding blocks while the chunk stays inside the size limit
            if len(current_chunk) + len(paragraph) <= max_chunk_size:

                current_chunk += paragraph + "\n\n"

            else:

                # --> save the completed chunk before starting another
                if current_chunk:

                    chunks.append({
                        "chunk_id": f"p{page_number}-c{chunk_number}",
                        "page": page_number,
                        "text": current_chunk.strip(),
                        "strategy": "paragraph"
                    })

                    chunk_number += 1

                current_chunk = paragraph + "\n"

        # --> save anything left after the final paragraph
        if current_chunk:

            chunks.append({
                "chunk_id": f"p{page_number}-c{chunk_number}",
                "page": page_number,
                "text": current_chunk.strip(),
                "strategy": "paragraph"
            })

    return chunks


#---------------------------------------------------------------------------------------------------------
# LOCAL MODEL CACHING
#---------------------------------------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_embedding_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )   # --> converts text into 384-dimensional embeddings


@lru_cache(maxsize=1)
def get_reranker_model():

    return CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )   # --> reranks retrieved chunks using query-to-passage relevance


@lru_cache(maxsize=1)
def get_nli_model():

    return CrossEncoder(
        "cross-encoder/nli-deberta-v3-small"
    )   # --> checks whether evidence supports or contradicts a claim


#---------------------------------------------------------------------------------------------------------
# EMBEDDING GENERATION
#---------------------------------------------------------------------------------------------------------

def generate_embeddings(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = get_embedding_model().encode(
        texts
    )

    for chunk, embedding in zip(chunks, embeddings):

        chunk["embedding"] = embedding

    return chunks


#---------------------------------------------------------------------------------------------------------
# BASIC COSINE SEARCH
#---------------------------------------------------------------------------------------------------------

def cosine_similarity(vector_a, vector_b):

    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )


def semantic_search(query, chunks, top_k=3):

    query_embedding = get_embedding_model().encode(
        query
    )

    results = []

    for chunk in chunks:

        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "text": chunk["text"],
            "score": float(score)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


#---------------------------------------------------------------------------------------------------------
# QDRANT CONFIGURATION
#---------------------------------------------------------------------------------------------------------

qdrant_client = QdrantClient(
    url="http://localhost:6333"
)

COLLECTION_NAME = "p4_09_documents"


def create_collection():

    collections = qdrant_client.get_collections().collections

    collection_names = [
        collection.name
        for collection in collections
    ]

    # --> create collection only when it does not already exist
    if COLLECTION_NAME not in collection_names:

        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def recreate_collection():

    # --> used mainly by evaluation when a clean collection is required
    if qdrant_client.collection_exists(
        COLLECTION_NAME
    ):

        qdrant_client.delete_collection(
            collection_name=COLLECTION_NAME
        )

    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


#---------------------------------------------------------------------------------------------------------
# QDRANT INDEXING
#---------------------------------------------------------------------------------------------------------

def index_chunks(chunks, document_id, filename):
    points = []

    for chunk in chunks:

        # --> deterministic ID prevents duplicate copies of the same chunk
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{document_id}:{chunk['strategy']}:{chunk['chunk_id']}"
            )
        )

        points.append(
            PointStruct(
                id=point_id,
                vector=chunk["embedding"].tolist(),
                payload={
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_id": chunk["chunk_id"],
                    "page": chunk["page"],
                    "text": chunk["text"],
                    "strategy": chunk["strategy"]
                }
            )
        )

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


#---------------------------------------------------------------------------------------------------------
# QDRANT SEARCH
#---------------------------------------------------------------------------------------------------------

def search_qdrant(query, document_id, strategy=None, top_k=3):

    query_embedding = get_embedding_model().encode(
        query
    ).tolist()

    conditions = [
        FieldCondition(
            key="document_id",
            match=MatchValue(
                value=document_id
            )
        )
    ]   # --> always restrict search to the current PDF

    if strategy:

        conditions.append(
            FieldCondition(
                key="strategy",
                match=MatchValue(
                    value=strategy
                )
            )
        )

    response = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=Filter(
            must=conditions
        ),
        limit=top_k,
        with_payload=True
    )

    return response.points


#---------------------------------------------------------------------------------------------------------
# CROSS-ENCODER RERANKING
#---------------------------------------------------------------------------------------------------------

def rerank_results(query, results, top_k=3):

    if not results:
        return []

    pairs = [
        [query, result.payload["text"]]
        for result in results
    ]   # --> compare the query against each retrieved passage

    scores = get_reranker_model().predict(
        pairs
    )

    reranked = list(
        zip(results, scores)
    )

    reranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return reranked[:top_k]


#---------------------------------------------------------------------------------------------------------
# FILTER WEAK RETRIEVAL RESULTS
#---------------------------------------------------------------------------------------------------------

MIN_RERANK_SCORE = 1.0   # --> project-specific starting threshold from adversarial testing


def filter_relevant_results(
    reranked_results,
    min_score=MIN_RERANK_SCORE
):

    return [
        (result, rerank_score)
        for result, rerank_score in reranked_results
        if float(rerank_score) >= min_score
    ]   # --> remove low-quality evidence cards individually


#---------------------------------------------------------------------------------------------------------
# CLAIM EXTRACTION
#---------------------------------------------------------------------------------------------------------

def extract_claim(query):

    cleaned_query = query.strip()

    if not cleaned_query:
        return None


    #-----------------------------------------------------------------------------------------------------
    # Explicit claim before another question
    # Example:
    # "Atlas retains documents permanently. What is the policy?"
    #-----------------------------------------------------------------------------------------------------

    sentences = re.split(
        r"(?<=[.!?])\s+",
        cleaned_query
    )   # --> sentence split without breaking decimal values such as 99.9

    if len(sentences) > 1:

        first_sentence = sentences[0].strip()

        if len(first_sentence.split()) >= 3:

            return first_sentence.rstrip(".?!")


    #-----------------------------------------------------------------------------------------------------
    # WHY DOES / HOW DOES
    # Example:
    # "Why does Atlas use an LLM API?"
    #-----------------------------------------------------------------------------------------------------

    implicit_patterns = [
        r"^why does\s+(.+?)\?$",
        r"^how does\s+(.+?)\?$",
    ]

    for pattern in implicit_patterns:

        match = re.match(
            pattern,
            cleaned_query,
            flags=re.IGNORECASE
        )

        if match:

            return match.group(1).strip()


    #-----------------------------------------------------------------------------------------------------
    # WHY IS / HOW IS
    #-----------------------------------------------------------------------------------------------------

    match = re.match(
        r"^(why|how)\s+is\s+(.+?)\?$",
        cleaned_query,
        flags=re.IGNORECASE
    )

    if match:

        return f"{match.group(2).strip()} is true"


    #-----------------------------------------------------------------------------------------------------
    # WHY ARE / HOW ARE
    #-----------------------------------------------------------------------------------------------------

    match = re.match(
        r"^(why|how)\s+are\s+(.+?)\?$",
        cleaned_query,
        flags=re.IGNORECASE
    )

    if match:

        return f"{match.group(2).strip()} are true"


    #-----------------------------------------------------------------------------------------------------
    # SINCE / GIVEN THAT
    #-----------------------------------------------------------------------------------------------------

    match = re.match(
        r"^(since|given that)\s+(.+?)(?:,|\?)",
        cleaned_query,
        flags=re.IGNORECASE
    )

    if match:

        return match.group(2).strip()


    return None   # --> normal factual question does not need NLI premise checking


#---------------------------------------------------------------------------------------------------------
# SENTENCE-LEVEL EVIDENCE
#---------------------------------------------------------------------------------------------------------

def split_evidence_sentences(text):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]   # --> NLI checks focused sentences instead of whole mixed-topic chunks


#---------------------------------------------------------------------------------------------------------
# NLI LABEL MAPPING
#---------------------------------------------------------------------------------------------------------

def get_nli_labels():

    model = get_nli_model()

    return {
        int(key): str(value).lower()
        for key, value in model.model.config.id2label.items()
    }   # --> read label order directly from the model configuration


#---------------------------------------------------------------------------------------------------------
# NLI SUPPORT / CONTRADICTION CHECK
#---------------------------------------------------------------------------------------------------------

NLI_CONFIDENCE_THRESHOLD = 0.70


def classify_evidence(query, reranked_results, top_n=3):

    claim = extract_claim(
        query
    )

    if claim is None:

        return {
            "label": "not_checked",
            "score": None,
            "claim": None,
            "evidence_rank": None,
            "evidence_text": None
        }


    # --> only use passages already considered relevant by the reranker
    relevant_results = filter_relevant_results(
        reranked_results
    )

    if not relevant_results:

        return {
            "label": "not_enough_evidence",
            "score": None,
            "claim": claim,
            "evidence_rank": None,
            "evidence_text": None
        }


    selected_results = relevant_results[:top_n]

    evidence_items = []


    # --> break each relevant chunk into smaller sentence-level evidence units
    for rank, (result, rerank_score) in enumerate(
        selected_results,
        start=1
    ):

        sentences = split_evidence_sentences(
            result.payload["text"]
        )

        for sentence in sentences:

            evidence_items.append({
                "rank": rank,
                "text": sentence
            })


    if not evidence_items:

        return {
            "label": "not_enough_evidence",
            "score": None,
            "claim": claim,
            "evidence_rank": None,
            "evidence_text": None
        }


    pairs = [
        [
            item["text"],   # --> document evidence
            claim           # --> user claim being verified
        ]
        for item in evidence_items
    ]


    logits = get_nli_model().predict(
        pairs
    )


    if np.ndim(logits) == 1:

        logits = np.array([
            logits
        ])


    labels = get_nli_labels()


    best_entailment = {
        "score": 0.0,
        "rank": None,
        "text": None
    }

    best_contradiction = {
        "score": 0.0,
        "rank": None,
        "text": None
    }


    # --> evaluate every sentence separately
    for item, row in zip(
        evidence_items,
        logits
    ):

        exp_scores = np.exp(
            row - np.max(row)
        )

        probabilities = (
            exp_scores / exp_scores.sum()
        )


        for index, probability in enumerate(
            probabilities
        ):

            label = labels.get(
                index,
                ""
            )

            probability = float(
                probability
            )


            if "entail" in label:

                if probability > best_entailment["score"]:

                    best_entailment = {
                        "score": probability,
                        "rank": item["rank"],
                        "text": item["text"]
                    }


            elif "contrad" in label:

                if probability > best_contradiction["score"]:

                    best_contradiction = {
                        "score": probability,
                        "rank": item["rank"],
                        "text": item["text"]
                    }


    #-----------------------------------------------------------------------------------------------------
    # SUPPORTED
    # Direct support wins before contradiction from another related sentence.
    #-----------------------------------------------------------------------------------------------------

    if best_entailment["score"] >= NLI_CONFIDENCE_THRESHOLD:

        return {
            "label": "supported",
            "score": best_entailment["score"],
            "claim": claim,
            "evidence_rank": best_entailment["rank"],
            "evidence_text": best_entailment["text"]
        }


    #-----------------------------------------------------------------------------------------------------
    # CONTRADICTED
    #-----------------------------------------------------------------------------------------------------

    if best_contradiction["score"] >= NLI_CONFIDENCE_THRESHOLD:

        return {
            "label": "contradicted",
            "score": best_contradiction["score"],
            "claim": claim,
            "evidence_rank": best_contradiction["rank"],
            "evidence_text": best_contradiction["text"]
        }


    #-----------------------------------------------------------------------------------------------------
    # NOT ENOUGH EVIDENCE
    #-----------------------------------------------------------------------------------------------------

    return {
        "label": "not_enough_evidence",
        "score": max(
            best_entailment["score"],
            best_contradiction["score"]
        ),
        "claim": claim,
        "evidence_rank": None,
        "evidence_text": None
    }