import hashlib

from rag import (
    extract_pdf_pages,
    fixed_size_chunking,
    paragraph_chunking,
    generate_embeddings,
    recreate_collection,
    index_chunks,
    search_qdrant,
)


# --------------------------------------------------------------------------------------------------
# Hand-labelled test cases
# --------------------------------------------------------------------------------------------------

TEST_CASES = [
    {
        "question": "What is machine learning?",
        "fixed_relevant_chunks": ["p1-c1", "p1-c2"],
        "paragraph_relevant_chunks": ["p1-c1"]
    },

    {
        "question": "What is supervised learning?",
        "fixed_relevant_chunks": ["p1-c2", "p1-c3"],
        "paragraph_relevant_chunks": ["p1-c2"]
    },

    {
        "question": "What is unsupervised learning?",
        "fixed_relevant_chunks": ["p1-c3"],
        "paragraph_relevant_chunks": ["p1-c2"]
    },

    {
        "question": "What is an embedding?",
        "fixed_relevant_chunks": ["p2-c1", "p2-c2"],
        "paragraph_relevant_chunks": ["p2-c1"]
    },

    {
        "question": "What is semantic search?",
        "fixed_relevant_chunks": ["p2-c2", "p2-c3"],
        "paragraph_relevant_chunks": ["p2-c2"]
    },

    {
        "question": "What does cosine similarity compare?",
        "fixed_relevant_chunks": ["p2-c2", "p2-c3"],
        "paragraph_relevant_chunks": ["p2-c3"]
    },

    {
        "question": "Why can embedding search return the wrong topic?",
        "fixed_relevant_chunks": ["p2-c4", "p2-c5"],
        "paragraph_relevant_chunks": ["p2-c4"]
    },

    {
        "question": "What is the difference between training and validation data?",
        "fixed_relevant_chunks": ["p1-c4", "p1-c5"],
        "paragraph_relevant_chunks": ["p1-c3"]
    },

    {
        "question": "How can machine learning help with document search?",
        "fixed_relevant_chunks": ["p1-c6", "p1-c7"],
        "paragraph_relevant_chunks": ["p1-c4"]
    },

    {
        "question": "What are the limitations of semantic retrieval?",
        "fixed_relevant_chunks": ["p2-c4", "p2-c5"],
        "paragraph_relevant_chunks": ["p2-c4"]
    }
]


# --------------------------------------------------------------------------------------------------
# Precision@K
# --------------------------------------------------------------------------------------------------

def precision_at_k(results, relevant_chunks, k):

    top_results = results[:k]   # --> take only top K retrieved results

    relevant_count = sum(
        1
        for result in top_results
        if result.payload["chunk_id"] in relevant_chunks   # --> exact relevant chunk match
    )

    return relevant_count / k   # --> relevant retrieved / total retrieved


# --------------------------------------------------------------------------------------------------
# Generate document ID
# --------------------------------------------------------------------------------------------------

def generate_document_id(pdf_path):

    with open(pdf_path, "rb") as file:

        file_bytes = file.read()

    # --> same PDF always generates the same document ID
    return hashlib.sha256(file_bytes).hexdigest()


# --------------------------------------------------------------------------------------------------
# Evaluation
# --------------------------------------------------------------------------------------------------

def run_evaluation():

    pdf_path = "data/sample.pdf"
    filename = "sample.pdf"

    # --> generate unique document ID from PDF content
    document_id = generate_document_id(pdf_path)


    # --------------------------------------------------------------------------------------------------
    # Extract PDF
    # --------------------------------------------------------------------------------------------------

    pages = extract_pdf_pages(pdf_path)


    # --------------------------------------------------------------------------------------------------
    # Fixed-size chunking
    # --------------------------------------------------------------------------------------------------

    fixed_chunks = fixed_size_chunking(
        pages
    )

    fixed_chunks = generate_embeddings(
        fixed_chunks
    )


    # --------------------------------------------------------------------------------------------------
    # Paragraph-aware chunking
    # --------------------------------------------------------------------------------------------------

    paragraph_chunks = paragraph_chunking(
        pages
    )

    paragraph_chunks = generate_embeddings(
        paragraph_chunks
    )


    # --------------------------------------------------------------------------------------------------
    # Create clean Qdrant collection
    # --------------------------------------------------------------------------------------------------

    recreate_collection()   # --> removes stale / duplicate points before evaluation


    # --------------------------------------------------------------------------------------------------
    # Index fixed-size chunks
    # --------------------------------------------------------------------------------------------------

    index_chunks(
        fixed_chunks,
        document_id=document_id,
        filename=filename
    )


    # --------------------------------------------------------------------------------------------------
    # Index paragraph-aware chunks
    # --------------------------------------------------------------------------------------------------

    index_chunks(
        paragraph_chunks,
        document_id=document_id,
        filename=filename
    )


    # --------------------------------------------------------------------------------------------------
    # Evaluation header
    # --------------------------------------------------------------------------------------------------

    print("\n======================================")
    print("P4-09 Retrieval Evaluation")
    print("======================================")

    print(f"Fixed chunks: {len(fixed_chunks)}")
    print(f"Paragraph chunks: {len(paragraph_chunks)}")


    fixed_scores = []
    paragraph_scores = []


    # --------------------------------------------------------------------------------------------------
    # Run each labelled question
    # --------------------------------------------------------------------------------------------------

    for test in TEST_CASES:

        question = test["question"]

        fixed_relevant = test["fixed_relevant_chunks"]
        paragraph_relevant = test["paragraph_relevant_chunks"]


        # ----------------------------------------------------------------------------------------------
        # Search fixed-size chunks only
        # ----------------------------------------------------------------------------------------------

        fixed_results = search_qdrant(
            question,
            document_id=document_id,
            strategy="fixed",
            top_k=3
        )


        # ----------------------------------------------------------------------------------------------
        # Search paragraph-aware chunks only
        # ----------------------------------------------------------------------------------------------

        paragraph_results = search_qdrant(
            question,
            document_id=document_id,
            strategy="paragraph",
            top_k=3
        )


        # ----------------------------------------------------------------------------------------------
        # Calculate Precision@3
        # ----------------------------------------------------------------------------------------------

        fixed_precision = precision_at_k(
            fixed_results,
            fixed_relevant,
            3
        )

        paragraph_precision = precision_at_k(
            paragraph_results,
            paragraph_relevant,
            3
        )


        # --> store scores for final average
        fixed_scores.append(fixed_precision)
        paragraph_scores.append(paragraph_precision)


        # ----------------------------------------------------------------------------------------------
        # Print individual test results
        # ----------------------------------------------------------------------------------------------

        print("\n--------------------------------------")

        print(f"Question: {question}")

        print(f"Fixed relevant chunks: {fixed_relevant}")
        print(f"Paragraph relevant chunks: {paragraph_relevant}")


        # --> show retrieved fixed-size chunk IDs
        print(
            "Fixed retrieved:",
            [
                result.payload["chunk_id"]
                for result in fixed_results
            ]
        )


        # --> show retrieved paragraph chunk IDs
        print(
            "Paragraph retrieved:",
            [
                result.payload["chunk_id"]
                for result in paragraph_results
            ]
        )


        print(f"Fixed P@3: {fixed_precision:.2f}")
        print(f"Paragraph P@3: {paragraph_precision:.2f}")


    # --------------------------------------------------------------------------------------------------
    # Average Precision@3
    # --------------------------------------------------------------------------------------------------

    avg_fixed = sum(fixed_scores) / len(fixed_scores)

    avg_paragraph = sum(paragraph_scores) / len(paragraph_scores)


    # --------------------------------------------------------------------------------------------------
    # Final results
    # --------------------------------------------------------------------------------------------------

    print("\n======================================")
    print("Final Results")
    print("======================================")

    print(f"Fixed-size Average P@3: {avg_fixed:.2f}")
    print(f"Paragraph Average P@3: {avg_paragraph:.2f}")


    # --------------------------------------------------------------------------------------------------
    # Compare strategies
    # --------------------------------------------------------------------------------------------------

    if avg_paragraph > avg_fixed:

        print("\nWinner: Paragraph-aware chunking")

    elif avg_fixed > avg_paragraph:

        print("\nWinner: Fixed-size chunking")

    else:

        print("\nResult: Both strategies performed equally")


# --------------------------------------------------------------------------------------------------
# Run evaluation
# --------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    run_evaluation()