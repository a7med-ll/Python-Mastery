# P4-04 — Embeddings and Vector Databases

## Purpose

This study task builds a conceptual model of how embeddings represent meaning and how vector databases retrieve semantically related information. It is deliberately **not a build project**: the evidence is an explanation, in your own words, of the ideas below.

## Learning outcomes

By the end, you should be able to explain:

- what an embedding is and what an embedding model learns;
- why embeddings are vectors rather than human-readable labels;
- how vector dimensions, model choice, and normalization affect retrieval;
- cosine similarity and cosine distance;
- when embeddings are useful and when exact matching is better;
- how a vector database stores vectors, source data, identifiers, and metadata;
- the difference between exact and approximate nearest-neighbor search;
- how HNSW and inverted-file-style indexes trade recall for speed;
- how metadata filtering changes retrieval;
- how dense, sparse, lexical, and hybrid search differ;
- how result fusion and reranking improve retrieval;
- the conceptual differences among Chroma, Qdrant, and pgvector;
- why retrieval quality must be evaluated rather than assumed.

---

## 1. Embedding fundamentals

### What an embedding is

An **embedding** is a numerical vector that represents an item in a learned geometric space. The item might be:

- a word, token, sentence, paragraph, or document;
- an image or region of an image;
- audio;
- a product, user, or event;
- source code;
- another structured or unstructured object.

A simplified text embedding might look like:

```text
[0.18, -0.42, 0.07, 0.91, ...]
```

Real embeddings often contain hundreds or thousands of dimensions. Individual dimensions normally do not have simple human-readable meanings. The useful information lies in the overall pattern and the relationships among vectors.

### What the space represents

An embedding model is trained so that items related according to its training objective tend to receive geometrically related vectors. For text embeddings, semantically similar passages often appear near one another even when they do not use exactly the same words.

For example:

- “reset my password” may be near “I cannot sign in”;
- “car insurance claim” may be near “report vehicle damage”;
- “Python list comprehension” may be near “compact loop syntax in Python.”

The geometry is learned, not manually programmed. “Near” therefore means similar according to the model and its training—not universally equivalent, factually identical, or appropriate for every application.

### Embeddings are model-specific

Vectors produced by different embedding models do not normally share a compatible coordinate space. Even if two models output the same number of dimensions, dimension 42 in one model does not necessarily correspond to dimension 42 in another.

The following must normally use the same compatible embedding model and configuration:

- stored document vectors;
- query vectors compared with those documents;
- the distance metric expected by the index;
- any preprocessing that changes the embedded text.

Changing the embedding model often requires re-embedding the stored corpus and rebuilding or updating its vector index.

### Dimensionality

The **dimension** of an embedding is the number of numerical components in the vector. A 768-dimensional embedding contains 768 values.

Higher dimensionality can provide more representational capacity, but it also increases:

- storage;
- memory use;
- data-transfer size;
- index size;
- distance-computation cost.

More dimensions do not automatically mean better retrieval. Model training, domain fit, multilingual support, input limits, chunking, distance metric, and evaluation quality can matter more.

---

## 2. Similarity and distance

### Why a comparison function is needed

An embedding becomes useful when the application can compare it with other embeddings. A **similarity** function gives larger scores to vectors judged more alike. A **distance** function gives smaller scores to vectors judged closer.

Common choices include:

- cosine similarity or cosine distance;
- dot product or inner product;
- Euclidean distance.

The correct choice depends on how the embedding model was trained and how the vector system defines its scoring operators.

### Cosine similarity

Cosine similarity measures the angle between two vectors:

\[
\operatorname{cosine\_similarity}(A,B)
=
\frac{A \cdot B}{\lVert A \rVert\lVert B \rVert}
\]

It compares direction after accounting for vector magnitude.

For non-zero vectors:

- a value near `1` means the vectors point in similar directions;
- a value near `0` means they are approximately orthogonal;
- a value near `-1` means they point in opposite directions.

The practical score range observed from a particular embedding model may be much narrower. A universal rule such as “anything above 0.8 is relevant” is unsafe without evaluation on that model and dataset.

### Cosine distance

Many systems expose **cosine distance** rather than cosine similarity:

\[
\operatorname{cosine\_distance}(A,B)
=
1 - \operatorname{cosine\_similarity}(A,B)
\]

With similarity, larger is closer. With distance, smaller is closer. Confusing the two can reverse rankings or produce an incorrect threshold.

### Normalization and dot product

A vector is normalized when its length is scaled to one. For unit-normalized vectors, cosine similarity and dot product produce the same ranking because the vector magnitudes are fixed.

Without normalization, dot product reflects both direction and magnitude. That may be intended for a model trained for dot-product retrieval, but it is not interchangeable with cosine similarity by default.

### Similarity is not certainty

A high similarity score means the model placed two items near one another. It does not prove that:

- they state the same fact;
- one answers the other;
- either one is correct;
- the result is safe to use;
- the score is calibrated as a probability.

Similarity scores are ranking signals. Their meaning must be tested in the target retrieval task.

---

## 3. When to use embeddings

### Strong use cases

Embeddings are useful when the task depends on meaning, behavior, or learned resemblance rather than exact strings.

Typical uses include:

- semantic search;
- retrieval for RAG systems;
- document or support-ticket clustering;
- recommendation and “similar item” features;
- duplicate or near-duplicate detection;
- classification using similarity to labeled examples;
- anomaly detection in representation space;
- matching questions with answers;
- cross-lingual retrieval when the model supports it;
- multimodal retrieval when compatible models map modalities into related spaces.

### When exact or structured search is better

Embeddings are not the best first tool for every query. Exact, lexical, or relational search is usually stronger for:

- order numbers, account IDs, SKUs, and ISBNs;
- exact quotations;
- email addresses and filenames;
- rare names and error codes;
- numeric ranges;
- dates and timestamps;
- equality conditions;
- joins and transactional constraints;
- legally required exact wording.

An exact identifier should not be retrieved by “meaning.” If the user asks for invoice `INV-10482`, an indexed exact lookup is more reliable than nearest-neighbor search.

### Embeddings and generation are different

An embedding model produces a vector representation. A generative model produces tokens or other content. Embeddings do not generate an answer by themselves.

In a retrieval-augmented system:

1. an embedding model converts the query into a vector;
2. a search system retrieves relevant records;
3. the application supplies selected records to a generative model;
4. the generative model produces the answer.

Each stage can fail independently.

---

## 4. Preparing data for embedding

### The unit of retrieval

A vector normally represents the text passed to the embedding model. If an entire book is embedded as one vector, the result compresses many unrelated topics into a single representation. If every sentence is embedded separately, individual chunks may lose essential context.

The **chunk** is therefore the practical unit of retrieval.

### Chunking

Chunking divides source material into retrievable pieces. Useful boundaries may follow:

- headings and sections;
- paragraphs;
- sentences;
- code functions or classes;
- table rows or logical groups;
- conversational turns;
- fixed token windows when structural boundaries are unavailable.

Chunk size creates a precision–context tradeoff:

- smaller chunks can produce precise matches but may omit surrounding meaning;
- larger chunks preserve context but may dilute the relevant signal and consume more prompt space.

Overlap can preserve information across boundaries, but excessive overlap increases storage and returns redundant results.

### Preserve source relationships

Each chunk should normally retain metadata such as:

- source document ID;
- chunk ID;
- parent section or heading;
- original position;
- title and source URL;
- author or owner;
- creation and update time;
- tenant or access-control scope;
- language, category, or document type;
- embedding-model version.

Retrieval may return a chunk, but the application often needs the metadata to cite the source, reconstruct context, enforce permissions, or refresh stale embeddings.

### Input preprocessing

Preprocessing might remove boilerplate, normalize whitespace, preserve headings, extract text from markup, or attach useful context before embedding.

Aggressive cleaning can remove meaning. For example, deleting punctuation may damage code, removing headings may erase topic context, and stripping numbers may destroy identifiers. Preprocessing choices should be evaluated with the retrieval task.

### Data freshness

When source content changes, its embedding can become stale. A production ingestion process needs a strategy for:

- detecting changes;
- updating changed chunks;
- deleting removed chunks;
- avoiding duplicates;
- tracking embedding versions;
- rebuilding indexes when required;
- handling partial ingestion failures.

---

## 5. Vector-database fundamentals

### What a vector database stores

A vector record commonly contains:

```text
id + vector + original content or reference + metadata
```

For example:

```json
{
  "id": "handbook-12-section-4",
  "vector": [0.18, -0.42, 0.07, 0.91],
  "text": "Employees may carry forward five days of leave.",
  "metadata": {
    "document_id": "handbook-12",
    "section": "Leave policy",
    "department": "HR",
    "version": 3
  }
}
```

Some products store the source text directly. Others primarily store vectors and references to data held elsewhere. The design affects consistency, updates, permissions, backup, and retrieval latency.

### Collections, points, and rows

Different systems use different names:

- Chroma groups records in **collections**;
- Qdrant stores **points** inside collections;
- pgvector stores vector values in ordinary PostgreSQL **rows**.

The terminology differs, but each system needs a way to associate a vector with an identity and application data.

### The basic query flow

1. Receive a query.
2. Apply the same compatible embedding process used for indexed content.
3. Produce a query vector.
4. Apply metadata or access-control filters.
5. Compare the query vector with stored vectors.
6. Retrieve the nearest candidates.
7. Optionally combine, rerank, deduplicate, or expand them.
8. Return records with scores and metadata.

The database performs retrieval; it does not decide whether the retrieved content is sufficient to answer the user's question.

---

## 6. Exact and approximate nearest-neighbor search

### Exact search

Exact nearest-neighbor search compares the query against all eligible vectors and returns the true nearest results under the chosen metric.

Advantages:

- perfect recall for the defined metric;
- simple behavior;
- useful as a quality baseline;
- effective for smaller filtered datasets.

Disadvantages:

- computation grows with the number and dimensionality of vectors;
- latency can become expensive at large scale.

### Approximate nearest-neighbor search

Approximate nearest-neighbor search uses an index to avoid examining every vector. It can dramatically improve latency, but may miss some results that exact search would rank in the top `k`.

This introduces a **speed–recall tradeoff**:

- more aggressive search is faster but may miss relevant neighbors;
- broader search examines more candidates and improves recall at additional cost.

Approximate does not mean randomly wrong. It means the system deliberately trades guaranteed exactness for scalable retrieval performance.

### Recall

For vector indexing, recall commonly measures how many of the true exact top results are recovered by the approximate search.

If exact search identifies 10 relevant nearest neighbors and the approximate index returns 9 of them, recall against that exact set is 90%.

High index recall does not guarantee high user relevance. The exact nearest neighbors can still be poor if the embeddings, chunks, metric, or query do not represent the task well.

---

## 7. Vector indexes

### Why indexing is needed

A vector index organizes vectors so that likely neighbors can be found without a complete scan. Unlike a traditional B-tree, a vector index is designed for high-dimensional proximity rather than ordered scalar values.

Index selection depends on:

- corpus size;
- query latency target;
- memory budget;
- update frequency;
- filter selectivity;
- required recall;
- index build time;
- supported distance metrics.

### HNSW

**Hierarchical Navigable Small World** indexing constructs a multilayer graph. Search navigates from coarse upper layers toward promising regions and then explores nearby nodes in lower layers.

Typical strengths:

- strong speed–recall performance;
- fast queries;
- good support for nearest-neighbor retrieval.

Typical costs:

- substantial memory use;
- slower index construction;
- tuning affects build time, query time, memory, and recall.

Common conceptual tuning controls determine:

- how densely nodes are connected during construction;
- how many candidates are considered while building;
- how broadly the graph is explored during search.

Names and defaults vary by product.

### Inverted-file-style indexes and IVFFlat

An inverted-file-style index partitions vectors into clusters or lists. A query first finds promising clusters and then searches only a subset of them.

Typical strengths:

- smaller memory footprint than HNSW in many settings;
- faster index construction;
- tunable number of searched partitions.

Typical costs:

- quality depends on representative training or clustering data;
- recall may be lower at similar latency;
- an index built with poor list configuration can underperform;
- inserts and data-distribution changes may require careful maintenance.

In pgvector, IVFFlat divides vectors into lists and searches selected lists. Increasing the number of probes generally improves recall while increasing query cost.

### Indexes depend on the distance function

An index prepared for cosine distance is not automatically the same as one prepared for Euclidean distance or inner product. The query operator and index configuration must agree with the metric.

---

## 8. Similarity search

### Top-k retrieval

A common query asks for the `k` nearest results:

```text
return the five stored vectors closest to the query vector
```

`k` controls how many results are returned, not whether those results are relevant. If the collection has no good match, nearest-neighbor search still returns the least-distant items unless a threshold or rejection rule prevents it.

### Score thresholds

A threshold can reject weak matches, but it must be calibrated for:

- the embedding model;
- the distance metric;
- the dataset;
- query type;
- business tolerance for false matches and missed results.

One global threshold may not work across languages, content types, or query categories.

### Metadata filtering

Metadata filters restrict eligible records before or during vector retrieval.

Examples:

- `tenant_id = current_tenant`;
- `language = "en"`;
- `document_type = "policy"`;
- `published_at >= a required date`;
- `department IN the user's allowed departments`.

Filtering improves precision and enforces scope, but it interacts with approximate indexes. A highly selective filter can leave too few candidates after approximate search. Systems may need filter-aware indexes, iterative scans, oversampling, or a different query plan.

Access control must not rely only on metadata suggested by the model. The application must derive security filters from authenticated permissions.

### Reranking

Vector search is often used as a fast candidate generator. A more expensive reranker then evaluates a smaller candidate set with stronger query–document interaction.

Conceptual pipeline:

1. retrieve 50 candidates quickly;
2. rerank those 50 with a stronger model;
3. keep the best 5;
4. send only the selected evidence downstream.

Reranking can improve relevance, but adds latency and cost. It cannot recover a relevant document that the first-stage retriever never included.

---

## 9. Dense, sparse, and lexical retrieval

### Dense vectors

Dense embeddings contain values in most dimensions. They are well suited to semantic similarity and paraphrases.

Strengths:

- matches related meaning across different wording;
- can generalize beyond exact keywords;
- may support multilingual or multimodal similarity.

Weaknesses:

- can miss exact identifiers and rare terms;
- may retrieve conceptually related but operationally wrong content;
- scores are model-dependent and difficult to interpret globally.

### Sparse retrieval

Sparse representations contain many zero values and relatively few non-zero dimensions. Traditional lexical methods such as BM25 reward matching terms using document and corpus statistics. Learned sparse models can also map text into high-dimensional term-like spaces.

Strengths:

- strong exact-term behavior;
- effective for identifiers, names, acronyms, and rare vocabulary;
- often easier to inspect through matched terms.

Weaknesses:

- can miss paraphrases and conceptual similarity;
- depends more directly on vocabulary overlap.

### Lexical search is not merely “old semantic search”

Lexical and dense retrieval capture different evidence. One should not be treated as an obsolete replacement for the other.

For the query `ERR_AUTH_104`, lexical matching may be ideal. For `I cannot access my account after changing phones`, dense retrieval may find relevant authentication guidance even without exact word overlap.

---

## 10. Hybrid search

### What hybrid search means

Hybrid search combines more than one retrieval signal. In text search, it commonly combines:

- dense semantic retrieval;
- sparse or keyword retrieval;
- metadata filters;
- optional reranking.

The goal is to preserve semantic recall while recovering exact terms that dense embeddings may overlook.

### Why raw scores cannot always be added

Dense and lexical systems often produce scores on different scales with different meanings. Adding raw scores directly can let one retriever dominate for accidental numerical reasons.

Common combination strategies include:

- normalized weighted-score fusion;
- Reciprocal Rank Fusion;
- learned ranking models;
- reranking a union of candidates.

### Reciprocal Rank Fusion

Reciprocal Rank Fusion combines rankings rather than raw scores. A document receives a contribution based on its position in each ranked list:

\[
\operatorname{RRF}(d)
=
\sum_r \frac{1}{k + \operatorname{rank}_r(d)}
\]

Here, `r` represents a retriever and `k` is a constant that reduces the impact of very small rank differences.

RRF is useful when score scales are difficult to compare. It still requires evaluation because the candidate depths, retrievers, and fusion constant affect results.

### Hybrid search example

For a product query such as `wireless noise-cancelling headphones model WH-1000XM5`:

- dense retrieval captures the meaning of wireless noise-cancelling headphones;
- lexical retrieval captures the exact model identifier;
- filters can restrict availability, region, or product category;
- reranking can choose the best final results.

---

## 11. Chroma, Qdrant, and pgvector

### Chroma

Chroma is designed around collections of records and embeddings. A collection can use an embedding function so that text queries are embedded and compared with stored vectors. Queries can also supply embeddings directly, and records can be restricted with metadata or document filters.

Conceptual strengths:

- straightforward developer experience;
- natural fit for local experimentation and application-level retrieval;
- convenient association of documents, embeddings, IDs, and metadata;
- simple collection query interface.

Questions to evaluate before production use include deployment model, persistence, scale, tenancy, backup, observability, and the exact search capabilities required.

### Qdrant

Qdrant is a dedicated vector-search engine with collections and points. It supports dense, sparse, named, and multi-vector representations, along with filtering and advanced query pipelines.

Conceptual strengths:

- purpose-built vector retrieval;
- rich payload filtering;
- multiple vector representations on one point;
- dense–sparse hybrid queries;
- prefetching, fusion, and multistage retrieval patterns.

It is a separate service, so teams must operate or consume that service and design synchronization with the system of record.

### pgvector

pgvector is a PostgreSQL extension that adds vector types, distance operators, and vector indexes to PostgreSQL.

Conceptual strengths:

- vectors live beside relational application data;
- SQL, joins, transactions, constraints, backups, and PostgreSQL operations remain available;
- exact nearest-neighbor search works without an approximate index;
- HNSW and IVFFlat support approximate retrieval;
- PostgreSQL full-text search can be combined with vector search for hybrid retrieval.

The tradeoff is that vector workload tuning shares a database with relational workload concerns. Indexes, memory, vacuuming, filters, query planning, and scaling need PostgreSQL-aware operation.

### Comparison

| Question | Chroma | Qdrant | pgvector |
| --- | --- | --- | --- |
| Primary shape | Embedding-oriented application database | Dedicated vector-search service | PostgreSQL extension |
| Data organization | Collections and records | Collections and points | Tables and rows |
| Relational joins | Not its primary model | Not its primary model | Native PostgreSQL strength |
| Dense similarity search | Yes | Yes | Yes |
| Sparse/hybrid strategy | Product capabilities should be checked for the chosen deployment | Native dense/sparse and hybrid query patterns | Combine vector search with PostgreSQL full-text search and fusion |
| Operational fit | Simple embedding-centric workflows | Specialized vector retrieval at service scale | Teams already centered on PostgreSQL |

This table is conceptual, not a universal ranking. The best choice depends on the existing stack, corpus size, query load, filtering, tenancy, consistency, operational expertise, and measured retrieval quality.

---

## 12. Common misconceptions

### “Embeddings store the original meaning perfectly”

False. An embedding is a lossy learned representation optimized for a model objective. Some details are emphasized and others are discarded.

### “A cosine score is a probability”

False. It is a geometric comparison. A score of `0.8` does not automatically mean an 80% chance of relevance.

### “Similar means correct”

False. A retrieved passage can be topically similar but factually wrong, outdated, contradictory, or unauthorized.

### “A vector database is required for every RAG system”

False. Small corpora may work with exact in-memory search, and some use cases are better served by full-text search, relational queries, or an existing search engine.

### “Approximate search returns random results”

False. It uses an index to find likely neighbors efficiently, accepting the possibility of missing some exact nearest results.

### “HNSW is always better than IVFFlat”

False. HNSW often offers a strong speed–recall tradeoff but can use more memory and take longer to build. Workload, data size, update pattern, filters, and operational limits decide the better index.

### “More retrieved chunks always improve the answer”

False. Larger `k` can add irrelevant or conflicting context, increase cost, and hide the best evidence.

### “Hybrid search means vector search plus metadata filtering”

Not usually. Filtering restricts eligibility. Hybrid text retrieval normally combines semantic and lexical ranking signals, often followed by fusion or reranking.

---

## 13. Retrieval quality and evaluation

### Build a labeled evaluation set

Retrieval quality should be measured on representative queries with known relevant results. Include:

- paraphrased questions;
- exact identifiers;
- rare terms and acronyms;
- ambiguous queries;
- multilingual queries if supported;
- queries with no relevant result;
- time-sensitive questions;
- permission-restricted content;
- queries requiring multiple pieces of evidence.

### Retrieval metrics

Useful metrics include:

- **Recall@k:** whether relevant items appear within the top `k`;
- **Precision@k:** how many of the top `k` are relevant;
- **Mean Reciprocal Rank:** how early the first relevant result appears;
- **nDCG:** ranking quality when relevance has multiple grades;
- **latency:** time required for retrieval;
- **index recall:** approximate results compared with exact nearest neighbors;
- **no-answer accuracy:** whether weak results are rejected when evidence is absent.

Metrics should be interpreted alongside qualitative error analysis. A single average can hide failures for rare terms, long documents, particular languages, or access-control filters.

### Variables to test

Evaluate changes to:

- embedding model;
- chunk size and overlap;
- text preprocessing;
- query rewriting;
- distance metric;
- exact versus approximate search;
- index parameters;
- metadata filtering;
- top `k` and score thresholds;
- dense, lexical, and hybrid retrieval;
- fusion method;
- reranker and reranking depth.

Change one major variable at a time when possible so that improvements can be attributed correctly.

### End-to-end retrieval correctness

A strong retrieval system requires all relevant layers to work:

1. source data is complete and current;
2. chunks preserve useful meaning;
3. embeddings fit the domain;
4. stored and query vectors are compatible;
5. filters enforce the correct scope and permissions;
6. the index meets latency and recall targets;
7. hybrid fusion or reranking improves ordering;
8. weak or absent evidence is handled explicitly;
9. downstream generation stays grounded in retrieved evidence.

A fast nearest-neighbor query is only one part of this chain.

# P4-04 — Embeddings and Vector Databases is completed with the provided readme notes
