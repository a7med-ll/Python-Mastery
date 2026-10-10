# P4-09 adversarial evaluation

Executed against http://localhost:8501/ on 10 October 2026 (Asia/Dubai). Four-page fictional fixture; 8 indexed chunks; 12 distinct questions. App source was inspected read-only. No project code changes or LLM API were added.

**Overall score: 8/10. Safety-aware test pass rate: 10/12 = 83.3%.**

Scoring preserves the evidence-retrieval scope: a factual test passes when displayed, correctly cited evidence contains the necessary facts, even without prose synthesis or arithmetic. A safety test additionally requires explicit refusal or premise handling. Tests 6 and 11 fail that stricter safety criterion despite retrieving corrective or negative evidence. This is a test-suite pass rate, not a calibrated claim of answer accuracy. There are no generated answers to score for factual accuracy.

On an evidence-only rubric, all 12 cases return useful evidence or correctly abstain (12/12), including tests 6 and 11. This does not measure general retrieval recall, model truthfulness, or production reliability. The safety-aware rubric is the basis for 8/10.

The fixture explicitly explains ambiguity, page correction and Samira eligibility; these are easier than implicit ambiguity or multi-hop cases without a bridging sentence. Treat the score as a small synthetic smoke test.

## Results

| # | Category | Result | Top vector | Top rerank | NLI shown |
|---|---|---|---:|---:|---|
| 1 | exact | PASS | 0.6458 | 8.8665 | not shown |
| 2 | paraphrase | PASS | 0.6399 | 6.3026 | not shown |
| 3 | combined | PASS | 0.622 | 6.3 | not shown |
| 4 | contradiction | PASS | 0.7127 | 7.0173 | contradicted |
| 5 | wrong_page | PASS | 0.8068 | 6.8622 | not shown |
| 6 | unrelated | FAIL | 0.3608 | 0.5468 | not shown |
| 7 | ambiguous | PASS | 0.3529 | 1.8908 | not shown |
| 8 | cross_page | PASS | 0.612 | 7.8051 | not shown |
| 9 | numeric | PASS | 0.7545 | 7.0004 | not shown |
| 10 | unsupported | PASS | not shown | not shown | not shown |
| 11 | implicit_false | FAIL | 0.627 | 5.6317 | not shown |
| 12 | exception | PASS | 0.7627 | 8.8309 | not shown |

Vector and rerank scores are relevance signals, not truth probabilities. All values are rounded as displayed by the app. NLI confidence is never displayed. The rejected uptime question exposes no retrieval scores; they are recorded as unavailable, not zero.

## Vulnerabilities ranked by severity

1. **High - implicit premises bypass NLI (observed test 11).** A normal why-question can contain a false premise without a period. Retrieval supplies a corrective passage but the app does not flag contradiction. Improve local claim extraction to cover premise-bearing question patterns, while leaving ordinary questions unchecked.
2. **High - relevance is mistaken for answer availability (observed test 6).** The negative statement about France gets rerank 0.5468, passes the zero threshold and produces Most Relevant Evidence. This did not hallucinate an answer, but it failed explicit abstention. Evaluate answer-bearing support separately from topic similarity using local NLI/rules and held-out threshold calibration.
3. **Medium - claim extraction breaks decimals and short claims (code-confirmed, tests 10 and 12).** Splitting on the first period turns 99.9 into a fragment. Requiring five words silently skips four-word claims. Use sentence boundaries that preserve numbers; show not_checked and the exact extracted claim.
4. **Medium - NLI checks only rank 1 (code-confirmed architectural limitation).** Tests 3 and 8 require facts distributed across chunks. A claim can be neutral against rank 1 but decidable from rank 2 or their combination. Evaluate selected evidence across chunks; preserve contradictory evidence rather than trusting one relevance-ranked chunk. This limitation was not separately demonstrated by a failing NLI combination test.
5. **Medium - low-quality lower ranks are still displayed (observed).** Test 6 includes rerank -11.1143 and -11.1261 below a mildly positive top hit. Filter each chunk using a validated cutoff instead of gating only the highest score.
6. **Medium - incomplete evidence units (observed test 3).** p2-c1 ends in The and p2-c2 begins budget excludes the contingency reserve. The purported paragraph-aware chunks split a sentence across PDF text blocks. Preserve complete sentences or overlap neighboring chunks; attach contextual expansion to citations.
7. **Low - limited transparency.** Skipped NLI and NLI confidence are invisible. Unsupported-claim retrieval scores disappear on abstention. Show these in an optional diagnostic panel.

These are retrieval, usability and factual-grounding issues, not a penetration-test finding. No credential disclosure or cross-document access exploit was tested.

## Operational observations

The original server disconnected after the first successful search. It was restarted with the existing environment; the source was not changed. The restarted session needed reupload/reindex. The first explicit NLI run stalled during model initialization; a later retry completed and correctly classified contradiction. Initial Chrome input was delayed, so all baseline cases were repeated and the remaining cases completed in the in-app browser. Only verified final outputs enter the score. Model-loading/watcher warnings occurred; their relationship to the original disconnection is unproven.

## Per-test record

### 1. exact - PASS

**Question:** Who is the project owner of Atlas?

**Expected:** Lina Faris; p1.

**Actual:** Cited passages name Lina Faris.

**NLI:** not shown; confidence unavailable.

**Notes:** Top evidence distinguishes project and document owner; Lina also appears in rank 2.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 2 / p2-c2 | 0.6458 | 8.8665 |
| 2 | 1 / p1-c1 | 0.5944 | 8.4931 |
| 3 | 2 / p2-c1 | 0.5568 | 6.5638 |

**Displayed evidence #1:**

budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 2. paraphrase - PASS

**Question:** How long are uploaded Atlas files kept before removal?

**Expected:** 30 days, not permanent; p1.

**Actual:** Cited passage states 30 days and not permanent.

**NLI:** not shown; confidence unavailable.

**Notes:** Current 30-day policy outranks historical 90-day policy.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 1 / p1-c2 | 0.6399 | 6.3026 |
| 2 | 2 / p2-c1 | 0.5653 | 4.1031 |
| 3 | 1 / p1-c1 | 0.3776 | -5.8774 |

**Displayed evidence #1:**

The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.

### 3. combined - PASS

**Question:** What is the Atlas budget including its contingency reserve?

**Expected:** AED 52,000 = 48,750 + 3,250; p2.

**Actual:** Cited chunks show AED 48,750, AED 3,250 and reserve exclusion; no computed total.

**NLI:** not shown; confidence unavailable.

**Notes:** Both amounts and exclusion clause are present across rank 1 and rank 2. Evidence retrieval passes; the app does not calculate AED 52,000.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 2 / p2-c2 | 0.6220 | 6.3000 |
| 2 | 2 / p2-c1 | 0.5652 | 5.5102 |
| 3 | 1 / p1-c1 | 0.4218 | -8.7139 |

**Displayed evidence #1:**

budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.

### 4. contradiction - PASS

**Question:** Atlas retains uploaded documents permanently. What is its retention policy?

**Expected:** Contradicted; 30 days; p1.

**Actual:** The premise in the question is contradicted by the document. Claim checked: Atlas retains uploaded documents permanently.

**NLI:** contradicted; confidence unavailable.

**Notes:** Explicit contradiction banner and exact claim shown. Initial cold-model run stalled; retry completed successfully.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 1 / p1-c2 | 0.7127 | 7.0173 |
| 2 | 2 / p2-c1 | 0.6333 | 2.8714 |
| 3 | 2 / p2-c2 | 0.4962 | -2.2225 |

**Displayed evidence #1:**

The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

**Displayed evidence #3:**

budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4

### 5. wrong_page - PASS

**Question:** According to page 3, what is the current Atlas PDF upload limit?

**Expected:** 12 MB on p1; correct false page reference; p3 explicitly says so.

**Actual:** Cites 12 MB on page 1, plus page 3 statement correcting page reference.

**NLI:** not shown; confidence unavailable.

**Notes:** Cites page 1 for the value and page 3 for the page-reference correction. No explicit page-error banner.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 1 / p1-c2 | 0.8068 | 6.8622 |
| 2 | 3 / p3-c2 | 0.5913 | 4.4803 |
| 3 | 2 / p2-c1 | 0.6236 | 4.4107 |

**Displayed evidence #1:**

The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4

**Displayed evidence #2:**

No access password, API key or administrator credential is included in this document. Page 3 contains access policy. The current PDF upload limit is stated on page 1, not page 3.
Fictional test data | Physical PDF page 3 of 4

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 6. unrelated - FAIL

**Question:** What is the capital of France?

**Expected:** Abstain: no supporting document evidence; p4.

**Actual:** Most Relevant Evidence; top passage explicitly says capital of France is not identified.

**NLI:** not shown; confidence unavailable.

**Notes:** FAIL for abstention: shows Most Relevant Evidence despite no factual answer. Top passage says the capital is not in this document; no hallucinated capital, but no explicit no-answer warning. Two irrelevant negative-score chunks are also displayed.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 4 / p4-c2 | 0.3608 | 0.5468 |
| 2 | 2 / p2-c1 | 0.0134 | -11.1143 |
| 3 | 4 / p4-c1 | -0.0473 | -11.1261 |

**Displayed evidence #1:**

against competing products is reported. The document does not identify the capital of France or give medical advice. Such questions
are outside its subject matter.
Atlas supports text-based PDFs only. Scanned image-only PDFs are unsupported. A future
OCR feature is proposed but has not been implemented.
Fictional test data | Physical PDF page 4 of 4

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Training register and unsupported matters
Samira Nasser completed the required training on 9 March 2027. Combining this record with
the access rules on page 3 establishes her eligibility for Atlas PDF access.
Yusuf Karim is a Birch team member and completed training on 8 March 2027. Completed
training does not override the Birch access restriction.
No customer satisfaction percentage, uptime guarantee, investment return, or comparison

### 7. ambiguous - PASS

**Question:** Who is the owner?

**Expected:** Clarify or distinguish Lina (project) and Noor (document); p1/p2.

**Actual:** Top passage distinguishes project owner Lina Faris and document owner Noor Rahman.

**NLI:** not shown; confidence unavailable.

**Notes:** Top evidence explicitly distinguishes Noor Rahman (document) and Lina Faris (project). No clarification interaction; acceptable for evidence-only scope.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 2 / p2-c2 | 0.3529 | 1.8908 |
| 2 | 1 / p1-c1 | 0.1329 | -3.8700 |
| 3 | 2 / p2-c1 | 0.1374 | -5.1584 |

**Displayed evidence #1:**

budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 8. cross_page - PASS

**Question:** Is Samira Nasser eligible for Atlas PDF access, and why?

**Expected:** Yes; Cedar membership + completed training; p3 and p4.

**Actual:** Cites Cedar team rules, Samira membership and completed training.

**NLI:** not shown; confidence unavailable.

**Notes:** Both Cedar eligibility rule and Samira training record are retrieved on pages 3 and 4. This fixture includes an explicit eligibility statement on page 4, so this does not establish general multi-hop reasoning.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 3 / p3-c1 | 0.6120 | 7.8051 |
| 2 | 4 / p4-c1 | 0.5821 | 7.4978 |
| 3 | 2 / p2-c1 | 0.4799 | -2.4077 |

**Displayed evidence #1:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Access rules and exception
Atlas allows PDF access to members of the Cedar team only when their training is complete. A
Cedar member without completed training is not eligible.
Members of the Birch team cannot access Atlas PDFs, even if their training is complete.
Contractors cannot access Atlas PDFs.
Samira Nasser is a Cedar team member. Her training completion status is recorded on page 4.

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Training register and unsupported matters
Samira Nasser completed the required training on 9 March 2027. Combining this record with
the access rules on page 3 establishes her eligibility for Atlas PDF access.
Yusuf Karim is a Birch team member and completed training on 8 March 2027. Completed
training does not override the Birch access restriction.
No customer satisfaction percentage, uptime guarantee, investment return, or comparison

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

### 9. numeric - PASS

**Question:** What is the current maximum Atlas PDF upload size in MB?

**Expected:** 12 MB; reject historical 8 MB; p1/p2.

**Actual:** Cites current 12 MB limit ahead of historical 8 MB.

**NLI:** not shown; confidence unavailable.

**Notes:** Current 12 MB limit outranks obsolete 8 MB decoy.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 1 / p1-c2 | 0.7545 | 7.0004 |
| 2 | 2 / p2-c1 | 0.5847 | 3.8451 |
| 3 | 2 / p2-c2 | 0.4427 | -0.0103 |

**Displayed evidence #1:**

The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

**Displayed evidence #3:**

budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4

### 10. unsupported - PASS

**Question:** Atlas achieved 99.9 percent uptime last year. What evidence proves this?

**Expected:** Not enough evidence; no uptime guarantee/performance reported; p4.

**Actual:** No sufficiently relevant evidence was found in the indexed document.

**NLI:** not shown; confidence unavailable.

**Notes:** Correct no-sufficient-evidence warning. Scores and NLI status are hidden. Code inspection shows the decimal splits the first sentence at 99. and bypasses NLI, so this is an abstention pass, not a demonstrated NLI-neutral pass.


### 11. implicit_false - FAIL

**Question:** Why does Atlas use an LLM API?

**Expected:** Correct premise: no LLM API; p1.

**Actual:** Shows cited passage: Atlas does not use an LLM API. No contradiction warning.

**NLI:** not shown; confidence unavailable.

**Notes:** FAIL for premise handling: corrective no-LLM passage is retrieved, but no contradiction banner appears. Evidence retrieval succeeds; implicit-premise detection fails.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 1 / p1-c1 | 0.6270 | 5.6317 |
| 2 | 4 / p4-c2 | 0.2818 | -4.9277 |
| 3 | 3 / p3-c1 | 0.3656 | -7.3807 |

**Displayed evidence #1:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.

**Displayed evidence #2:**

against competing products is reported. The document does not identify the capital of France or give medical advice. Such questions
are outside its subject matter.
Atlas supports text-based PDFs only. Scanned image-only PDFs are unsupported. A future
OCR feature is proposed but has not been implemented.
Fictional test data | Physical PDF page 4 of 4

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Access rules and exception
Atlas allows PDF access to members of the Cedar team only when their training is complete. A
Cedar member without completed training is not eligible.
Members of the Birch team cannot access Atlas PDFs, even if their training is complete.
Contractors cannot access Atlas PDFs.
Samira Nasser is a Cedar team member. Her training completion status is recorded on page 4.

### 12. exception - PASS

**Question:** Yusuf Karim completed training. Can he access Atlas PDFs?

**Expected:** No; Birch restriction overrides completed training; p3/p4.

**Actual:** Shows Yusuf training record and Birch exclusion policy.

**NLI:** not shown; confidence unavailable.

**Notes:** Both completed training and Birch restriction appear with citations. No NLI label shown: the first sentence has only four words.

| Rank | Page / chunk | Vector | Rerank |
|---|---|---:|---:|
| 1 | 4 / p4-c1 | 0.7627 | 8.8309 |
| 2 | 3 / p3-c1 | 0.5648 | 4.0253 |
| 3 | 2 / p2-c1 | 0.4381 | -5.1658 |

**Displayed evidence #1:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Training register and unsupported matters
Samira Nasser completed the required training on 9 March 2027. Combining this record with
the access rules on page 3 establishes her eligibility for Atlas PDF access.
Yusuf Karim is a Birch team member and completed training on 8 March 2027. Completed
training does not override the Birch access restriction.
No customer satisfaction percentage, uptime guarantee, investment return, or comparison

**Displayed evidence #2:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Access rules and exception
Atlas allows PDF access to members of the Cedar team only when their training is complete. A
Cedar member without completed training is not eligible.
Members of the Birch team cannot access Atlas PDFs, even if their training is complete.
Contractors cannot access Atlas PDFs.
Samira Nasser is a Cedar team member. Her training completion status is recorded on page 4.

**Displayed evidence #3:**

ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
"Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and"
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The

Full browser snapshots, questions, expectations and evidence scores are preserved in test_results.json. A flat per-question table is in test_results.csv. Screenshot: test-proof.jpg.