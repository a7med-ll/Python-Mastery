# P4-09 suite: run 3

**11/12 passed (91.7%). Score: 9/10**, up from 10/12 (83.3%) and 8/10. All twelve original questions were executed through the browser against localhost:8501 after loading pending app changes. The same indexed PDF was reused. No app source edits or LLM API added.

The uptime regression is fixed: case 10 now reports insufficient evidence rather than contradiction. Case 12 remains a high-severity factual-grounding error: Yusuf completed training, yet the app contradicts this true premise at 99.17% confidence. The displayed page 4 evidence explicitly confirms his training. Training completion and access eligibility are different facts.

The score uses the same scope and rubric as previous runs: complete cited evidence suffices for normal retrieval questions; premise-handling and unsupported/out-of-domain cases require correct status. This is a small synthetic suite pass rate, not calibrated model accuracy or production readiness. The app supplies evidence, rather than generated answers or arithmetic. The fixture includes explicit multi-hop bridging and ambiguity statements.

| Case | Category | Previous | Now | Top vector | Top rerank | NLI | Confidence |
|---|---|---|---|---:|---:|---|
| 1 | exact | PASS | PASS | 0.6458 | 8.8665 | not shown | not shown |
| 2 | paraphrase | PASS | PASS | 0.6399 | 6.3026 | not shown | not shown |
| 3 | combined | PASS | PASS | 0.622 | 6.3 | not shown | not shown |
| 4 | contradiction | PASS | PASS | 0.7127 | 7.0173 | contradicted | 99.79% |
| 5 | wrong_page | PASS | PASS | 0.8068 | 6.8622 | not shown | not shown |
| 6 | unrelated | PASS | PASS | not shown | not shown | not shown | not shown |
| 7 | ambiguous | PASS | PASS | 0.3529 | 1.8908 | not shown | not shown |
| 8 | cross_page | PASS | PASS | 0.612 | 7.8051 | not shown | not shown |
| 9 | numeric | PASS | PASS | 0.7545 | 7.0004 | not shown | not shown |
| 10 | unsupported | FAIL | PASS | not shown | not shown | not_enough_evidence | not shown |
| 11 | implicit_false | PASS | PASS | 0.627 | 5.6317 | contradicted | 99.94% |
| 12 | exception | FAIL | FAIL | 0.7627 | 8.8309 | contradicted | 99.17% |

## Remaining limitations

1. **High, observed:** false contradiction for a supported training claim (case 12). Inspect local NLI per-class outputs and label mapping using direct entailment, contradiction and neutral control pairs before changing aggregation again. The UI evidence establishes the error, not its root cause.
2. **Medium, observed:** budget context remains split between chunks ending in The and starting budget excludes. Reusing the stored index preserves this boundary issue.
3. **Low, observed:** rejected cases do not display retrieval scores; NLI confidence is hidden for the insufficient-evidence case. Values remain unavailable, not zero.

Initial model loading exceeded the browser wait on cases 1 and 4; final completed output was then captured. All 12 cases are represented, with complete browser snapshots in the JSON file.

## Detailed records

### 1 - exact: PASS

Question: Who is the project owner of Atlas?

Expected: Lina Faris; p1.

Actual: Cited evidence. Correct project-owner evidence.

NLI: not shown; confidence: None; evidence rank: None.

Notes: Correct project-owner evidence.

Rank 1; page 2; p2-c2; vector 0.6458; rerank 8.8665.

budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4

Rank 2; page 1; p1-c1; vector 0.5944; rerank 8.4931.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.

Rank 3; page 2; p2-c1; vector 0.5568; rerank 6.5638.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 2 - paraphrase: PASS

Question: How long are uploaded Atlas files kept before removal?

Expected: 30 days, not permanent; p1.

Actual: Cited evidence. Correct current retention policy; weak third hit removed.

NLI: not shown; confidence: None; evidence rank: None.

Notes: Correct current retention policy; weak third hit removed.

Rank 1; page 1; p1-c2; vector 0.6399; rerank 6.3026.

The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4

Rank 2; page 2; p2-c1; vector 0.5653; rerank 4.1031.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 3 - combined: PASS

Question: What is the Atlas budget including its contingency reserve?

Expected: AED 52,000 = 48,750 + 3,250; p2.

Actual: Cited evidence. Both budget values and exclusion clause retrieved; arithmetic remains for the reader.

NLI: not shown; confidence: None; evidence rank: None.

Notes: Both budget values and exclusion clause retrieved; arithmetic remains for the reader.

Rank 1; page 2; p2-c2; vector 0.6220; rerank 6.3000.

budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4

Rank 2; page 2; p2-c1; vector 0.5652; rerank 5.5102.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 4 - contradiction: PASS

Question: Atlas retains uploaded documents permanently. What is its retention policy?

Expected: Contradicted; 30 days; p1.

Actual: Contradiction banner. Claim checked: Atlas retains uploaded documents permanently

NLI: contradicted; confidence: 99.79; evidence rank: 1.

Notes: Correct contradiction; NLI confidence 99.79%.

Rank 1; page 1; p1-c2; vector 0.7127; rerank 7.0173.

The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4

Rank 2; page 2; p2-c1; vector 0.6333; rerank 2.8714.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 5 - wrong_page: PASS

Question: According to page 3, what is the current Atlas PDF upload limit?

Expected: 12 MB on p1; correct false page reference; p3 explicitly says so.

Actual: Cited evidence. Correct 12 MB value on page 1 and page-reference correction on page 3.

NLI: not shown; confidence: None; evidence rank: None.

Notes: Correct 12 MB value on page 1 and page-reference correction on page 3.

Rank 1; page 1; p1-c2; vector 0.8068; rerank 6.8622.

The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4

Rank 2; page 3; p3-c2; vector 0.5913; rerank 4.4803.

No access password, API key or administrator credential is included in this document. Page 3 contains access policy. The current PDF upload limit is stated on page 1, not page 3.
Fictional test data | Physical PDF page 3 of 4

Rank 3; page 2; p2-c1; vector 0.6236; rerank 4.4107.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 6 - unrelated: PASS

Question: What is the capital of France?

Expected: Abstain: no supporting document evidence; p4.

Actual: No sufficiently relevant evidence was found in the indexed document.

NLI: not shown; confidence: None; evidence rank: None.

Notes: FIXED: explicit no-sufficient-evidence warning replaces irrelevant evidence cards.

### 7 - ambiguous: PASS

Question: Who is the owner?

Expected: Clarify or distinguish Lina (project) and Noor (document); p1/p2.

Actual: Cited evidence. Correct owner distinction; only the relevant card is retained.

NLI: not shown; confidence: None; evidence rank: None.

Notes: Correct owner distinction; only the relevant card is retained.

Rank 1; page 2; p2-c2; vector 0.3529; rerank 1.8908.

budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4

### 8 - cross_page: PASS

Question: Is Samira Nasser eligible for Atlas PDF access, and why?

Expected: Yes; Cedar membership + completed training; p3 and p4.

Actual: Cited evidence. Correct Cedar policy and training record on pages 3 and 4. Fixture contains an explicit bridging statement, so this is not proof of general reasoning.

NLI: not shown; confidence: None; evidence rank: None.

Notes: Correct Cedar policy and training record on pages 3 and 4. Fixture contains an explicit bridging statement, so this is not proof of general reasoning.

Rank 1; page 3; p3-c1; vector 0.6120; rerank 7.8051.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Access rules and exception
Atlas allows PDF access to members of the Cedar team only when their training is complete. A
Cedar member without completed training is not eligible.
Members of the Birch team cannot access Atlas PDFs, even if their training is complete.
Contractors cannot access Atlas PDFs.
Samira Nasser is a Cedar team member. Her training completion status is recorded on page 4.

Rank 2; page 4; p4-c1; vector 0.5821; rerank 7.4978.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Training register and unsupported matters
Samira Nasser completed the required training on 9 March 2027. Combining this record with
the access rules on page 3 establishes her eligibility for Atlas PDF access.
Yusuf Karim is a Birch team member and completed training on 8 March 2027. Completed
training does not override the Birch access restriction.
No customer satisfaction percentage, uptime guarantee, investment return, or comparison

### 9 - numeric: PASS

Question: What is the current maximum Atlas PDF upload size in MB?

Expected: 12 MB; reject historical 8 MB; p1/p2.

Actual: Cited evidence. Correct current 12 MB limit ahead of obsolete 8 MB.

NLI: not shown; confidence: None; evidence rank: None.

Notes: Correct current 12 MB limit ahead of obsolete 8 MB.

Rank 1; page 1; p1-c2; vector 0.7545; rerank 7.0004.

The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4

Rank 2; page 2; p2-c1; vector 0.5847; rerank 3.8451.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 10 - unsupported: PASS

Question: Atlas achieved 99.9 percent uptime last year. What evidence proves this?

Expected: Not enough evidence; no uptime guarantee/performance reported; p4.

Actual: The indexed document does not provide enough evidence to verify the premise in this question. Claim checked: Atlas achieved 99.9 percent uptime last year.

NLI: not_enough_evidence; confidence: None; evidence rank: None.

Notes: FIXED: unsupported uptime receives not_enough_evidence. Decimal value remains intact. No retrieval scores or confidence are displayed for this rejected case.

### 11 - implicit_false: PASS

Question: Why does Atlas use an LLM API?

Expected: Correct premise: no LLM API; p1.

Actual: Contradiction banner. Claim checked: Atlas use an LLM API

NLI: contradicted; confidence: 99.94; evidence rank: 1.

Notes: FIXED: implicit premise extracted as Atlas use an LLM API and correctly contradicted at 99.94%.

Rank 1; page 1; p1-c1; vector 0.6270; rerank 5.6317.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.

### 12 - exception: FAIL

Question: Yusuf Karim completed training. Can he access Atlas PDFs?

Expected: No; Birch restriction overrides completed training; p3/p4.

Actual: Contradiction banner. Claim checked: Yusuf Karim completed training

NLI: contradicted; confidence: 99.17; evidence rank: 1.

Notes: FAIL persists: training completion is explicit on page 4, but the app says that exact claim is contradicted at 99.17% confidence. Access restriction does not negate training completion.

Rank 1; page 4; p4-c1; vector 0.7627; rerank 8.8309.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Training register and unsupported matters
Samira Nasser completed the required training on 9 March 2027. Combining this record with
the access rules on page 3 establishes her eligibility for Atlas PDF access.
Yusuf Karim is a Birch team member and completed training on 8 March 2027. Completed
training does not override the Birch access restriction.
No customer satisfaction percentage, uptime guarantee, investment return, or comparison

Rank 2; page 3; p3-c1; vector 0.5648; rerank 4.0253.

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Access rules and exception
Atlas allows PDF access to members of the Cedar team only when their training is complete. A
Cedar member without completed training is not eligible.
Members of the Birch team cannot access Atlas PDFs, even if their training is complete.
Contractors cannot access Atlas PDFs.
Samira Nasser is a Cedar team member. Her training completion status is recorded on page 4.