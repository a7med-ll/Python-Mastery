# P4-05 — RAG Pipeline Design

## Purpose

This study task builds a conceptual model of **Retrieval-Augmented Generation (RAG)**: how an application retrieves external evidence and gives it to a language model before the model answers. It is deliberately **not a build project**. The evidence is an explanation, in your own words, of chunking strategies, retrieval pipelines, reranking, and retrieval-quality evaluation.

## Learning outcomes

By the end, you should be able to explain:

- what RAG is and what problem it solves;
- how parametric memory differs from retrieved external knowledge;
- the offline ingestion path and the online query path;
- why document parsing and chunking determine what can be retrieved;
- the trade-offs among fixed-size, structure-aware, semantic, and hierarchical chunking;
- how lexical, dense, filtered, and hybrid retrieval differ;
- why candidate generation and reranking are separate stages;
- how query rewriting, decomposition, and routing can improve retrieval;
- how retrieved evidence should be selected and assembled into model context;
- why retrieval relevance, answer correctness, and groundedness are different properties;
- how to evaluate retrieval with Hit Rate, Recall@k, Precision@k, MRR, and nDCG;
- how to diagnose common RAG failures instead of treating RAG as one opaque step.

---

## 1. RAG fundamentals

### What RAG means

**Retrieval-Augmented Generation** is a pattern in which a system retrieves information from an external knowledge source and supplies selected evidence to a generative model as part of the input used to answer a query.

At a high level:

```text
user question
    ↓
retrieve relevant evidence
    ↓
assemble evidence into context
    ↓
generate an answer grounded in that evidence
```

The model still generates the final response. Retrieval does not replace generation; it gives generation access to information that may be more current, private, domain-specific, or traceable than knowledge stored in model parameters.

### Parametric and non-parametric memory

A pretrained model stores patterns and some factual associations in its parameters. This is often called **parametric memory**. It is:

- compressed rather than directly inspectable;
- difficult to update one fact at a time;
- not guaranteed to recall a fact accurately;
- not a dependable source of citations or provenance.

A RAG knowledge base acts as **non-parametric memory**. Its documents can be added, removed, inspected, versioned, permissioned, and cited without retraining the language model.

RAG combines the two:

- the model contributes language understanding and generation;
- the retrieval system contributes selected external evidence.

### What RAG can improve

Well-designed RAG can improve:

- access to current or frequently changing information;
- use of private organizational knowledge;
- traceability through source links or citations;
- domain coverage without full model retraining;
- factual grounding when relevant evidence is available;
- control over which knowledge sources may support an answer.

### What RAG does not guarantee

RAG does not automatically guarantee truth. The system may:

- retrieve the wrong passages;
- miss the correct passage;
- retrieve stale or conflicting sources;
- truncate important evidence;
- pass too much irrelevant context;
- misinterpret good evidence;
- make an unsupported claim despite the evidence;
- attach a citation that does not support the claim.

RAG reduces some failure modes and introduces others. It must be evaluated as a pipeline.

---

## 2. The complete RAG lifecycle

### Offline ingestion path

The offline path prepares knowledge for retrieval:

```text
source acquisition
    → parsing and normalization
    → document segmentation
    → chunking
    → metadata enrichment
    → embedding and/or lexical indexing
    → index storage
    → validation and refresh
```

This path may run once, on a schedule, or whenever sources change.

### Online query path

The online path handles a user request:

```text
question
    → query understanding or rewriting
    → candidate retrieval
    → filtering and fusion
    → reranking
    → context selection and assembly
    → generation
    → citations and response checks
```

### Why the two paths must agree

The online query must be compatible with the offline index. Important agreements include:

- the same or compatible embedding model for stored chunks and dense queries;
- a matching distance metric and vector index;
- metadata names and types that query filters understand;
- compatible tokenization for lexical search;
- stable source and chunk identifiers;
- consistent tenant and permission data;
- a refresh policy that prevents deleted or outdated content from remaining searchable.

Changing the embedding model, chunk representation, or schema may require reprocessing and reindexing the corpus.

---

## 3. Source ingestion and document preparation

### Source acquisition

A knowledge base may contain:

- web pages;
- PDFs and word-processing documents;
- support articles;
- database rows;
- tickets and conversations;
- code and API documentation;
- policies, contracts, or manuals;
- transcripts and other extracted text.

The pipeline should retain source identity, ownership, update time, and access rules from the beginning.

### Parsing is part of retrieval quality

Retrieval cannot recover information that parsing destroyed. Common parsing failures include:

- headers mixed into body text on every page;
- table rows converted into meaningless word sequences;
- columns read in the wrong order;
- headings separated from their content;
- footnotes inserted into unrelated paragraphs;
- scanned pages without OCR;
- code losing indentation;
- diagrams omitted without alternative descriptions.

Before tuning embeddings, inspect the actual text produced by the parser.

### Normalization

Normalization can remove repeated navigation, repair whitespace, standardize encodings, and identify structural elements. It should not erase information needed for meaning or exact retrieval.

For example, aggressive normalization can damage:

- case-sensitive identifiers;
- code;
- version strings;
- mathematical notation;
- table relationships;
- legal wording.

### Metadata

Useful chunk metadata can include:

- document and chunk identifiers;
- title and section path;
- source URL or file path;
- author or owner;
- creation and update timestamps;
- product, region, language, or version;
- content type;
- tenant and access-control information;
- links to adjacent, parent, or child chunks.

Metadata supports filtering, citations, refresh, deletion, debugging, and access control. It is not merely decorative information.

---

## 4. Chunking strategies

### Why chunking matters

Most source documents are too large and topically broad to retrieve as one unit. A **chunk** is the unit that gets indexed, ranked, retrieved, and usually placed into the model context.

Chunking balances two competing goals:

- **specificity:** the chunk should focus on the information needed by the query;
- **completeness:** the chunk should retain enough surrounding context to be understandable.

Chunks that are too large can dilute relevance and consume the context budget. Chunks that are too small can lose definitions, conditions, references, and relationships.

### Fixed-size chunking

Fixed-size chunking splits text after a chosen number of characters or tokens, often with overlap.

Advantages:

- simple and deterministic;
- fast to apply;
- easy to compare in experiments;
- useful as a baseline.

Limitations:

- boundaries may cut sentences, tables, or logical sections;
- unrelated ideas may share a chunk;
- a heading may be separated from its body;
- the best size varies by content and query type.

### Sliding windows and overlap

An overlapping window repeats some text in adjacent chunks. Overlap can preserve information near a boundary, but excessive overlap creates:

- duplicate search results;
- a larger index;
- more embedding cost;
- less diverse context;
- repeated evidence in the final prompt.

Overlap is a boundary-recovery tool, not a universal quality setting. It should be evaluated rather than maximized.

### Structure-aware chunking

Structure-aware chunking follows natural document boundaries such as:

- headings and subheadings;
- paragraphs;
- list items;
- table sections;
- code functions or classes;
- conversation turns;
- individual records in structured data.

It usually preserves meaning better than arbitrary cuts. Long sections may still need secondary splitting.

### Semantic chunking

Semantic chunking attempts to split where the topic or meaning changes. It may use sentence embeddings, similarity changes, classifiers, or a language model.

Potential benefits:

- more coherent chunks;
- less mixing of unrelated topics;
- boundaries that follow meaning rather than size alone.

Potential costs:

- more preprocessing time and complexity;
- nondeterministic or model-dependent boundaries;
- harder debugging;
- no guarantee of better retrieval on the target queries.

### Hierarchical or parent–child chunking

Hierarchical chunking indexes small child passages for precise matching while retaining links to a larger parent section.

A common flow is:

1. retrieve a focused child chunk;
2. identify its parent section;
3. provide the parent or selected neighboring chunks to the model.

This separates the best unit for **matching** from the best unit for **reading**.

### Contextualized chunks

A small passage may contain phrases such as “this policy” or “the second option” whose meaning depends on its document. A contextualized representation adds limited document or section context to the chunk before indexing it.

For example:

```text
Document: Employee Travel Policy
Section: International expense limits
Context: This passage defines hotel reimbursement rules for international travel.

[original chunk text]
```

The added context can improve retrieval, but it must be accurate and should not replace the original source text.

### Chunk size is an evaluated parameter

There is no universally correct chunk size. The best choice depends on:

- document structure;
- answer granularity;
- embedding-model input limits;
- expected query length;
- whether facts span sections;
- context-window and latency budgets;
- whether parent expansion or reranking is used.

Evaluate several strategies with representative questions. Do not select a size only because it is common in a tutorial.

---

## 5. Representations and indexes

### Lexical representation

Lexical search matches terms and usually ranks them with a method such as BM25. It is strong for:

- names and identifiers;
- technical terms;
- error codes;
- quotations;
- rare words;
- queries whose wording appears in the source.

### Dense representation

Dense retrieval embeds queries and chunks into a vector space. It can match related meaning even when the wording differs.

It is strong for:

- natural-language questions;
- paraphrases;
- conceptual similarity;
- vocabulary mismatch between query and source.

It can be weaker for exact strings, numbers, and rare identifiers.

### Sparse learned representation

Learned sparse representations retain a large token-oriented vector with many zero values. They can combine learned expansion with lexical-style matching, depending on the model and system.

They are distinct from both classic term search and dense embeddings.

### Hybrid retrieval

Hybrid retrieval obtains candidates from more than one method, commonly lexical and dense search, then combines their rankings.

This helps because exact-match and semantic signals fail differently. A product code may favor lexical search, while a paraphrased policy question may favor dense search.

Raw scores from different retrieval methods are usually not directly comparable. Rank-based fusion such as Reciprocal Rank Fusion can combine ordered lists without assuming that their score scales mean the same thing.

---

## 6. Query understanding

### The user's question is not always the best search query

Conversation history, ambiguity, shorthand, and multiple intentions can make the original question unsuitable for direct retrieval.

Example:

```text
Previous turn: What plans support SSO?
Current turn: What does the cheapest one cost?
```

The second sentence needs conversational context before it becomes a useful retrieval query.

### Query rewriting

Query rewriting turns the request into a clearer, standalone search query. It may:

- resolve pronouns from conversation history;
- expand abbreviations;
- preserve exact entities and identifiers;
- remove irrelevant conversational wording;
- add a missing product or domain name.

A rewrite can also harm retrieval by changing the user's meaning. The original query should remain available for comparison and debugging.

### Query decomposition

A multi-part question may require multiple searches.

For example, “Compare the cancellation policy and data-retention policy for plans A and B” may be decomposed into focused subqueries. Their evidence is then combined before generation.

Decomposition is helpful when one embedding cannot represent all parts well, but it increases latency and creates an evidence-assembly problem.

### Query expansion and multiple queries

The retriever may search several paraphrases, related terms, or likely document formulations. This can increase recall but may introduce off-topic candidates.

### Hypothetical answer retrieval

Some systems generate a hypothetical answer or passage and embed that text as a retrieval query. The generated passage may be closer in style to the stored documents than the short user question.

The hypothetical content is only a retrieval aid. It is not evidence and must never be treated as a factual source.

### Routing

A router chooses which knowledge source or retrieval strategy should handle the request.

Possible routes include:

- exact database lookup for an order number;
- lexical search for an error code;
- vector search for a conceptual question;
- a policy index for compliance questions;
- no retrieval for casual conversation;
- refusal or clarification when the request is outside scope.

Good routing prevents every query from being forced through the same index.

---

## 7. Candidate retrieval

### Candidate generation optimizes recall

The first retrieval stage should produce a manageable candidate set that is likely to contain the relevant evidence. It usually favors **recall**: avoid losing the correct passage too early.

Candidate generation may use:

- dense nearest-neighbor search;
- lexical or sparse search;
- hybrid search;
- metadata filters;
- several rewritten queries;
- searches over multiple indexes;
- parent, child, or neighboring-chunk expansion.

### Top-k

`k` is the number of results requested from a retriever.

- A very small `k` can miss relevant evidence.
- A very large `k` increases latency and reranking cost.
- Sending every candidate to the model can add noise and exceed the context budget.

The candidate count, reranking depth, and final context count are separate settings.

### Metadata filtering

Filters can restrict candidates by attributes such as:

- tenant;
- user permissions;
- product or document type;
- language;
- date range;
- version;
- region;
- publication status.

Filters improve relevance and enforce scope, but security-sensitive filtering must be guaranteed by the retrieval and authorization layer. It cannot rely on the model choosing to ignore forbidden text.

### Pre-filtering and post-filtering

**Pre-filtering** restricts eligible records before or during nearest-neighbor search. **Post-filtering** retrieves broadly and removes disallowed or mismatched records afterward.

Post-filtering can return too few results when many top candidates are removed. The database's filtering behavior should therefore be understood and tested.

### Similarity thresholds

A threshold can reject weak matches, but similarity scores are model- and dataset-specific. A fixed score should not be interpreted as a universal probability of relevance.

Thresholds should be calibrated on labeled examples, including questions for which the knowledge base contains no answer.

---

## 8. Reranking

### Retrieval and reranking solve different problems

Initial retrieval searches a large corpus efficiently. A **reranker** applies a more expensive relevance model to a much smaller candidate set.

```text
large corpus
    ↓ fast retriever
candidate set
    ↓ accurate reranker
ordered shortlist
```

The retriever is optimized for speed and recall. The reranker is optimized for precision and ordering.

### Bi-encoders and cross-encoders

Dense retrieval commonly uses a **bi-encoder** pattern: query and chunk are encoded separately, allowing chunk vectors to be precomputed.

A **cross-encoder** reads the query and candidate together and predicts their relevance. It can model detailed interactions between their tokens, but it must run for each query–candidate pair and is therefore slower.

### Language-model reranking

A language model can score, compare, or select candidates using task-specific instructions. This can handle nuanced criteria but may be:

- slower and more expensive;
- less deterministic;
- difficult to calibrate;
- vulnerable to instructions contained in untrusted retrieved text.

### Reranking depth

If only the first 20 candidates are reranked, a relevant chunk initially ranked 21st cannot be rescued. Reranking depth is therefore a recall–latency trade-off.

### Diversity and deduplication

The highest-scoring chunks may repeat the same passage because of overlap or document duplication. Context selection should consider:

- exact and near-duplicate removal;
- source diversity;
- topic coverage;
- maximal marginal relevance or similar diversity methods;
- whether adjacent chunks should be merged;
- whether several pieces are needed to answer a multi-part question.

The goal is not simply the individually highest scores. It is the most useful evidence set.

---

## 9. Context construction

### Retrieval results are not yet a prompt

After reranking, the system must construct a context package for the model. This stage may:

- choose the final chunks;
- merge overlapping neighbors;
- restore document headings;
- order chunks by relevance, source, or chronology;
- attach source identifiers;
- fit evidence into a token budget;
- remove duplicates;
- preserve exact quotations and tables where needed.

### Context budget

The prompt must share a finite context window among:

- system and developer instructions;
- conversation history;
- the current request;
- retrieved evidence;
- tool results;
- space for the model's answer.

More retrieved text is not automatically better. Irrelevant evidence can distract the model, create conflicts, raise cost, and hide the strongest passage.

### Ordering effects

Models may not use every context position equally well. Important evidence should not be buried in a long collection of weak passages. The ordering strategy should be tested rather than assumed.

### Source labels and citations

Every supplied passage should have a stable source identifier. The generator can then associate claims with specific evidence.

A citation is useful only when:

1. the cited source exists;
2. the cited passage supports the claim;
3. the source is authoritative enough for the task;
4. the citation points to the correct location;
5. the answer does not overstate what the source says.

### Retrieved text is untrusted input

External documents may contain malicious or irrelevant instructions such as “ignore previous rules.” Retrieval does not convert source text into trusted system instructions.

The application should:

- clearly delimit retrieved evidence;
- instruct the model to treat it as data, not authority over behavior;
- keep permissions and tool authorization outside model control;
- sanitize unsafe active content;
- restrict which sources enter sensitive workflows;
- test indirect prompt-injection attacks.

---

## 10. Grounded generation

### The generator's task

A grounded-answer instruction typically asks the model to:

- answer from the supplied evidence;
- distinguish evidence from inference;
- cite supporting sources;
- avoid unsupported details;
- say when evidence is insufficient or conflicting;
- ask for clarification when the question is ambiguous.

### Groundedness and correctness are different

An answer is **grounded** when its claims are supported by the provided context. It is **correct** when those claims are true relative to the world or an authoritative reference.

An answer can be grounded but wrong if the retrieved source is wrong or stale. It can be correct but ungrounded if the model states a true fact that does not appear in the supplied evidence.

Both properties matter.

### Abstention

A robust RAG system should sometimes respond that it lacks enough evidence. This requires evaluation with **unanswerable queries**, not only questions known to have an answer.

Without such testing, the system may learn or be prompted to produce a confident response for every request.

### Conflicting evidence

When sources disagree, the pipeline may need to consider:

- source authority;
- version and timestamp;
- jurisdiction or region;
- product version;
- whether one source supersedes another;
- whether the conflict must be surfaced to the user.

Similarity ranking alone cannot determine policy authority.

---

## 11. Evaluating retrieval quality

### Begin with a labeled evaluation set

A retrieval evaluation set normally contains:

- representative user questions;
- the documents or chunks considered relevant;
- questions with multiple valid evidence passages;
- hard negatives that resemble the answer but do not support it;
- unanswerable and out-of-scope questions;
- important slices such as language, product, source type, and query difficulty.

Labels may come from domain experts, production feedback, or carefully reviewed synthetic questions. Synthetic data is useful for coverage, but it can favor the method that generated it and should be validated.

### Hit Rate at k

**Hit Rate@k** asks whether at least one relevant item appears in the first `k` results.

For one query:

```text
1 if a relevant result appears in the top k
0 otherwise
```

The dataset score is the average across queries. It is easy to understand, but it does not measure how many relevant items were found or where within the top `k` they appeared.

### Recall at k

**Recall@k** measures the fraction of all known relevant items retrieved in the top `k`:

\[
\operatorname{Recall@k}
=
\frac{\text{relevant items retrieved in top }k}
{\text{all relevant items}}
\]

Recall is especially important during candidate generation. If the correct evidence is absent, later reranking and generation cannot recover it.

### Precision at k

**Precision@k** measures the fraction of the first `k` retrieved items that are relevant:

\[
\operatorname{Precision@k}
=
\frac{\text{relevant items retrieved in top }k}
{k}
\]

Precision matters when irrelevant context distracts the generator or consumes limited tokens.

### Mean Reciprocal Rank

For a query, **reciprocal rank** is the inverse of the position of the first relevant result:

\[
\operatorname{RR}
=
\frac{1}{\text{rank of first relevant result}}
\]

**Mean Reciprocal Rank (MRR)** averages this value across queries. It rewards placing the first useful result near the top, but it ignores additional relevant results after that first one.

### nDCG

**Normalized Discounted Cumulative Gain (nDCG)** is useful when results have graded relevance rather than a simple relevant/not-relevant label. It:

- gives more credit to highly relevant documents;
- rewards placing useful results earlier;
- compares the observed ranking with the ideal ranking.

It is helpful when one passage directly answers the question while another is only partially useful.

### Evaluate at the correct unit

Ground truth may exist at document, section, passage, or fact level. A chunk-level metric can unfairly mark a neighboring passage wrong even when it comes from the correct section, while a document-level metric may hide poor chunk selection.

The evaluation unit should match what the generator needs.

### Retrieval metrics do not measure the final answer

Strong retrieval does not guarantee a good answer. End-to-end evaluation should separately assess:

- answer correctness;
- groundedness or faithfulness to evidence;
- completeness;
- citation correctness;
- appropriate abstention;
- safety;
- latency and cost.

Separating retrieval and generation metrics makes failures diagnosable.

---

## 12. Evaluation design

### Compare one variable at a time

Useful experiments compare:

- chunk sizes and overlap;
- fixed, structural, semantic, and parent–child chunking;
- embedding models;
- lexical, dense, and hybrid retrieval;
- metadata filters;
- query rewriting or decomposition;
- candidate counts;
- rerankers and reranking depth;
- context-selection and ordering strategies.

If many stages change together, an improvement cannot be attributed to a specific cause.

### Use slices, not only one average

An overall metric can hide serious weaknesses. Report results for slices such as:

- exact identifiers versus conceptual questions;
- short versus multi-part queries;
- recent versus old documents;
- common versus rare topics;
- tables versus prose;
- each language, product, region, or tenant;
- answerable versus unanswerable queries.

### Offline evaluation

Offline evaluation is repeatable and useful during development. It can compare pipeline variants against a fixed labeled dataset.

Its weakness is representativeness: a clean benchmark may not reflect real user language, corpus changes, or production traffic.

### Online evaluation

Production signals can include:

- user corrections or satisfaction;
- answer abandonment;
- follow-up reformulations;
- citation clicks;
- escalation to a human;
- task completion;
- sampled expert review;
- controlled A/B tests.

Behavioral signals are not perfect relevance labels. For example, a citation click can mean trust, curiosity, or doubt.

### Regression testing

Every major change to parsing, chunking, models, indexing, filters, or prompting should rerun a stable evaluation set. Track:

- quality by metric and slice;
- latency percentiles;
- token and model cost;
- index size;
- ingestion time;
- failure and timeout rates.

A pipeline change is not an improvement if a small average gain causes an unacceptable regression for a critical group of queries.

---

## 13. Failure diagnosis

### No correct evidence was retrieved

Possible causes:

- the source was never ingested;
- parsing lost the information;
- chunk boundaries separated necessary context;
- the index is stale;
- query rewriting changed the intent;
- the embedding model is a poor domain match;
- `k` is too small;
- an incorrect filter excluded the source;
- approximate search missed a neighbor;
- lexical retrieval was required for an exact term.

### Correct evidence was retrieved but ranked too low

Possible causes:

- weak first-stage ranking;
- overly broad query expansion;
- duplicate chunks crowding the list;
- hybrid fusion weights or candidate pools are unsuitable;
- the reranker was not used or did not see enough candidates;
- the relevance label depends on context absent from the chunk.

### Correct evidence reached the prompt but the answer was wrong

Possible causes:

- too much distracting context;
- conflicting sources;
- important content was truncated;
- poor evidence ordering;
- instructions did not require grounding;
- the model made an unsupported inference;
- the question required synthesis across several chunks;
- source formatting was confusing.

This is primarily a context-construction or generation failure, not a retrieval-recall failure.

### The answer is correct but the citation is wrong

Possible causes:

- source labels were lost during context assembly;
- citations were generated from memory rather than constrained identifiers;
- several chunks were merged without provenance;
- the cited passage is topically related but does not entail the claim.

Citation correctness needs its own evaluation.

### The system should not have answered

Possible causes:

- no threshold or evidence-sufficiency check;
- unanswerable cases were absent from evaluation;
- prompts rewarded always providing an answer;
- retrieved passages matched the topic but not the requested fact;
- the generator used parametric memory beyond the allowed evidence.

---

## 14. Production concerns

### Freshness and deletion

A production knowledge base needs a lifecycle:

1. detect source creation, update, or deletion;
2. identify affected chunks;
3. reprocess only what changed when practical;
4. update lexical and vector indexes consistently;
5. prevent old and new versions from competing unintentionally;
6. verify that deleted content is no longer retrievable.

### Permissions

Access control should be applied before protected content reaches the language model. Required properties may include:

- tenant isolation;
- document- or row-level permissions;
- group membership checks;
- auditable access decisions;
- protection against metadata-filter bypass;
- cache separation between users and tenants.

Prompt instructions are not authorization controls.

### Latency and cost

Latency can accumulate across:

- query rewriting;
- embedding generation;
- several searches;
- reranking;
- parent expansion;
- context processing;
- answer generation.

The slowest high-percentile requests matter more to user experience than the average alone. Cache only when identity, freshness, and permissions make reuse safe.

### Observability

Useful traces record:

- original and rewritten queries;
- chosen route and filters;
- retrieved identifiers and scores;
- fusion and reranking results;
- selected context and token counts;
- source versions;
- generation settings;
- citations;
- latency and cost per stage;
- user feedback and evaluation labels.

Sensitive document content and user data require appropriate redaction and retention controls.

---

## 15. Common misconceptions

### “RAG eliminates hallucinations”

False. RAG can provide evidence, but retrieval and generation can both fail. Unsupported generation remains possible.

### “A vector database is the RAG pipeline”

False. A vector index is one component. Parsing, chunking, metadata, query handling, retrieval, reranking, context construction, generation, permissions, and evaluation are also part of the system.

### “Larger chunks always preserve more useful context”

False. Larger chunks may mix topics, weaken matching, and waste prompt tokens. The right unit depends on the data and questions.

### “More overlap always improves recall”

False. Some overlap can protect boundaries, while too much creates duplicates and reduces evidence diversity.

### “The nearest vector is the correct answer”

False. Vector similarity is a ranking signal, not proof of relevance, truth, or authority.

### “Reranking can recover anything”

False. A reranker can reorder only the candidates it receives. It cannot recover evidence absent from the candidate set.

### “If retrieval metrics improve, the answer must improve”

False. The generator may still ignore, misread, or overstate evidence. Context construction and answer quality must also be evaluated.

### “If the answer is correct, the RAG system is working”

Not necessarily. The model may have answered from parametric memory while ignoring the retrieved evidence. Test groundedness and citation support.

### “One global pipeline is best for every query”

False. Exact lookups, conceptual questions, multi-hop comparisons, and unanswerable requests may require different routes.

---

## 16. A practical mental model

For every RAG answer, reason through these layers:

1. **Source:** Does the knowledge base contain authoritative, current information?
2. **Parsing:** Was that information extracted correctly?
3. **Chunking:** Does at least one retrievable unit preserve the needed meaning?
4. **Representation:** Can lexical, dense, sparse, or hybrid search express the match?
5. **Query:** Did rewriting and routing preserve the user's intent?
6. **Candidate retrieval:** Did the relevant evidence enter the candidate set?
7. **Reranking:** Was the evidence placed high enough?
8. **Context selection:** Did the model receive the right evidence without excessive noise?
9. **Generation:** Does every material claim follow from the evidence?
10. **Citation:** Does each reference actually support its claim?
11. **Authorization:** Was every retrieved source allowed for this user?
12. **Evaluation:** Do labeled tests and production signals support the quality claim?

This model turns “the RAG answer is bad” into a specific, testable diagnosis.

---

## 17. Knowledge check

You should now be able to answer these questions in your own words:

1. What information does RAG add that a language model may not reliably provide alone?
2. Why does RAG improve grounding without guaranteeing correctness?
3. What is the difference between the offline ingestion path and online query path?
4. Why can a parsing failure look like an embedding failure?
5. What trade-off does chunk size create?
6. When is overlap useful, and when does it become harmful?
7. How do fixed-size, structure-aware, semantic, and parent–child chunking differ?
8. Why might hybrid retrieval outperform dense retrieval alone?
9. Why are raw lexical and vector scores not automatically comparable?
10. What is the difference between candidate retrieval and reranking?
11. Why can a reranker not repair low candidate recall?
12. What should metadata filters do, and why are they security-sensitive?
13. Why should retrieved documents be treated as untrusted input?
14. What is the difference between groundedness and correctness?
15. How do Recall@k, Precision@k, Hit Rate@k, MRR, and nDCG differ?
16. Why should retrieval and final-answer quality be evaluated separately?
17. What test cases verify that the system abstains appropriately?
18. How would you diagnose a correct chunk that was retrieved but not used by the model?

# P4-05 — RAG Pipeline Design is completed with the provided readme notes
