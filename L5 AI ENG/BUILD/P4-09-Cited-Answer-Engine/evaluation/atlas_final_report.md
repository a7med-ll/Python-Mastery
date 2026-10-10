# Original Atlas suite — final rerun

Tested through the localhost Streamlit browser UI on 10 October 2026. Twelve questions were submitted individually and completed outputs captured. No application code was changed and no LLM API was added.

**Grounded result: 11/12 passed (91.7%). System score: 9/10.** Score is the grounded pass rate scaled to ten and rounded to a whole number; this small fixture is not a production reliability estimate.

**Comparable evidence/status-only result: 12/12 (100.0%).** The stricter grounded result additionally requires the newly displayed NLI verification sentence to support the classification. A correct label with an unrelated verification sentence fails grounding. This distinction keeps comparisons with earlier reports honest.

The app returns cited evidence, not a generated answer. Passing requires sufficient displayed evidence to establish the expected answer; calculations and prose synthesis are not required. Vector/rerank scores are model scores, not probabilities. “Not shown” means the UI did not display a value; it does not mean zero.

## Findings and severity

- **High — ungrounded NLI contradiction (case 4):** permanent retention gets the correct label, but an unrelated contingency-budget sentence is presented as its verification at 99.91% confidence. Confidence cannot substitute for relevant evidence.
- **Resolved in this run:** Yusuf’s completed training is supported, with the Birch access restriction retrieved separately (case 12). All twelve original evidence/status checks pass.

The original fixture remains downloadable as [Atlas PDF](../examples/atlas_adversarial.pdf).

## All twelve cases

### 1. exact — PASS

**Question:** Who is the project owner of Atlas?

**Expected answer/evidence:** Lina Faris; p1.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 2, p2-c2; vector **0.6458**, rerank **8.8665**.

```text
budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4
```

Rank 2 — page 1, p1-c1; vector **0.5944**, rerank **8.4931**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.
```

Rank 3 — page 2, p2-c1; vector **0.5568**, rerank **6.5638**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
Atlas Blue is not the Atlas retrieval pilot.
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The
```

**Notes:** Owner correctly retrieved, including distinction from nearby names.

### 2. paraphrase — PASS

**Question:** How long are uploaded Atlas files kept before removal?

**Expected answer/evidence:** 30 days, not permanent; p1.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c2; vector **0.6399**, rerank **6.3026**.

```text
The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4
```

Rank 2 — page 2, p2-c1; vector **0.5653**, rerank **4.1031**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
Atlas Blue is not the Atlas retrieval pilot.
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The
```

**Notes:** Current 30-day retention retrieved.

### 3. combined — PASS

**Question:** What is the Atlas budget including its contingency reserve?

**Expected answer/evidence:** AED 52,000 = 48,750 + 3,250; p2.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 2, p2-c2; vector **0.6220**, rerank **6.3000**.

```text
budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4
```

Rank 2 — page 2, p2-c1; vector **0.5652**, rerank **5.5102**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
Atlas Blue is not the Atlas retrieval pilot.
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The
```

**Notes:** Both AED 48,750 and AED 3,250 retrieved; enough evidence to derive AED 52,000.

### 4. contradiction — FAIL

**Question:** Atlas retains uploaded documents permanently. What is its retention policy?

**Expected answer/evidence:** Contradicted; 30 days; p1.

**NLI:** contradicted. Confidence: 99.91%.

**Actual verification sentence (rank 2):** Its contingency reserve is AED 3,250.


**Actual status output:**

```text
Search
The premise in the question is contradicted by the document.
Claim checked:
Atlas retains uploaded documents permanently
Evidence used for verification:
Its contingency reserve is AED 3,250.
NLI confidence: 99.91% | Evidence rank: 2
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c2; vector **0.7127**, rerank **7.0173**.

```text
The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4
```

Rank 2 — page 2, p2-c1; vector **0.6333**, rerank **2.8714**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
Atlas Blue is not the Atlas retrieval pilot.
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The
```

**Notes:** Correct contradiction label and retention evidence, but verification uses unrelated sentence: “Its contingency reserve is AED 3,250.” Grounding failure despite 99.91% confidence.

### 5. wrong_page — PASS

**Question:** According to page 3, what is the current Atlas PDF upload limit?

**Expected answer/evidence:** 12 MB on p1; correct false page reference; p3 explicitly says so.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c2; vector **0.8068**, rerank **6.8622**.

```text
The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4
```

Rank 2 — page 3, p3-c2; vector **0.5913**, rerank **4.4803**.

```text
No access password, API key or administrator credential is included in this document. Page 3 contains access policy. The current PDF upload limit is stated on page 1, not page 3.
Fictional test data | Physical PDF page 3 of 4
```

Rank 3 — page 2, p2-c1; vector **0.6236**, rerank **4.4107**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
Atlas Blue is not the Atlas retrieval pilot.
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The
```

**Notes:** Current 12 MB limit and actual source pages retrieved despite incorrect page premise.

### 6. unrelated — PASS

**Question:** What is the capital of France?

**Expected answer/evidence:** Abstain: no supporting document evidence; p4.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
No sufficiently relevant evidence was found in the indexed document.
```

**Actual retrieved output and displayed scores:**

No evidence chunks or vector/rerank scores shown.
**Notes:** Correctly abstains on an unrelated question.

### 7. ambiguous — PASS

**Question:** Who is the owner?

**Expected answer/evidence:** Clarify or distinguish Lina (project) and Noor (document); p1/p2.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 2, p2-c2; vector **0.3529**, rerank **1.8908**.

```text
budget excludes the contingency reserve. In the current Atlas pilot, the maximum number of retrieved candidates is 10, and the reranker
returns 3 evidence chunks.
The word owner can refer to the project owner or the document owner. The document owner is
Noor Rahman; the Atlas project owner is Lina Faris.
Fictional test data | Physical PDF page 2 of 4
```

**Notes:** Evidence distinguishes project owner Lina Faris and document owner Noor Rahman.

### 8. cross_page — PASS

**Question:** Is Samira Nasser eligible for Atlas PDF access, and why?

**Expected answer/evidence:** Yes; Cedar membership + completed training; p3 and p4.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 3, p3-c1; vector **0.6120**, rerank **7.8051**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Access rules and exception
Atlas allows PDF access to members of the Cedar team only when their training is complete. A
Cedar member without completed training is not eligible.
Members of the Birch team cannot access Atlas PDFs, even if their training is complete.
Contractors cannot access Atlas PDFs.
Samira Nasser is a Cedar team member. Her training completion status is recorded on page 4.
```

Rank 2 — page 4, p4-c1; vector **0.5821**, rerank **7.4978**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Training register and unsupported matters
Samira Nasser completed the required training on 9 March 2027. Combining this record with
the access rules on page 3 establishes her eligibility for Atlas PDF access.
Yusuf Karim is a Birch team member and completed training on 8 March 2027. Completed
training does not override the Birch access restriction.
No customer satisfaction percentage, uptime guarantee, investment return, or comparison
```

**Notes:** Policy and Samira’s membership/training record both retrieved.

### 9. numeric — PASS

**Question:** What is the current maximum Atlas PDF upload size in MB?

**Expected answer/evidence:** 12 MB; reject historical 8 MB; p1/p2.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c2; vector **0.7545**, rerank **7.0004**.

```text
The current upload limit is 12 MB per PDF. The current retention period is 30 days. Uploaded documents are not retained permanently.
Atlas encrypts stored documents at rest. This document does not state that Atlas holds ISO
27001 certification.
Fictional test data | Physical PDF page 1 of 4
```

Rank 2 — page 2, p2-c1; vector **0.5847**, rerank **3.8451**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Historical settings and nearby names
Historical record, superseded: before 1 February 2027, Atlas allowed 8 MB per PDF and
retained files for 90 days. These are not the current limits.
A separate project named Atlas Blue is owned by Omar Salim. Atlas Blue launches on 21 April
Atlas Blue is not the Atlas retrieval pilot.
The Atlas retrieval pilot has a budget of AED 48,750. Its contingency reserve is AED 3,250. The
```

**Notes:** Current 12 MB limit retrieved; historical 8 MB is identified as superseded.

### 10. unsupported — PASS

**Question:** Atlas achieved 99.9 percent uptime last year. What evidence proves this?

**Expected answer/evidence:** Not enough evidence; no uptime guarantee/performance reported; p4.

**NLI:** not_enough_evidence. Confidence: not shown.

**Actual status output:**

```text
Search
The indexed document does not provide enough evidence to verify the premise in this question.
Claim checked:
Atlas achieved 99.9 percent uptime last year
```

**Actual retrieved output and displayed scores:**

No evidence chunks or vector/rerank scores shown.
**Notes:** Correctly reports insufficient evidence; decimal 99.9 preserved in checked claim.

### 11. implicit_false — PASS

**Question:** Why does Atlas use an LLM API?

**Expected answer/evidence:** Correct premise: no LLM API; p1.

**NLI:** contradicted. Confidence: 99.6%.

**Actual verification sentence (rank 1):** Atlas does not use an LLM API.


**Actual status output:**

```text
Search
The premise in the question is contradicted by the document.
Claim checked:
Atlas use an LLM API
Evidence used for verification:
Atlas does not use an LLM API.
NLI confidence: 99.60% | Evidence rank: 1
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c1; vector **0.6270**, rerank **5.6317**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Current Atlas specification
This is a fictional test document. All names, dates and amounts are synthetic. Physical PDF
page numbers are authoritative.
Atlas is a text-based document retrieval pilot operated by Meridian Lab. Its project owner is
Lina Faris. The launch date is 17 March 2027.
Atlas uses Qdrant for vector storage, a local cross-encoder for reranking, and a local NLI model
to check explicit claims. Atlas does not use an LLM API.
```

**Notes:** Correct contradiction grounded in “Atlas does not use an LLM API.”

### 12. exception — PASS

**Question:** Yusuf Karim completed training. Can he access Atlas PDFs?

**Expected answer/evidence:** No; Birch restriction overrides completed training; p3/p4.

**NLI:** supported. Confidence: 98.9%.

**Actual verification sentence (rank 1):** Yusuf Karim is a Birch team member and completed training on 8 March 2027.


**Actual status output:**

```text
Search
The premise in the question is supported by the document.
Claim checked:
Yusuf Karim completed training
Evidence used for verification:
Yusuf Karim is a Birch team member and completed training on 8 March 2027.
NLI confidence: 98.90% | Evidence rank: 1
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 4, p4-c1; vector **0.7627**, rerank **8.8309**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Training register and unsupported matters
Samira Nasser completed the required training on 9 March 2027. Combining this record with
the access rules on page 3 establishes her eligibility for Atlas PDF access.
Yusuf Karim is a Birch team member and completed training on 8 March 2027. Completed
training does not override the Birch access restriction.
No customer satisfaction percentage, uptime guarantee, investment return, or comparison
```

Rank 2 — page 3, p3-c1; vector **0.5648**, rerank **4.0253**.

```text
ATLAS / ADVERSARIAL RETRIEVAL FIXTURE
Access rules and exception
Atlas allows PDF access to members of the Cedar team only when their training is complete. A
Cedar member without completed training is not eligible.
Members of the Birch team cannot access Atlas PDFs, even if their training is complete.
Contractors cannot access Atlas PDFs.
Samira Nasser is a Cedar team member. Her training completion status is recorded on page 4.
```

**Notes:** Training premise correctly supported; Birch access restriction also retrieved. Earlier false contradiction is fixed.

## Audit files

- [CSV results](atlas_final_results.csv)
- [Structured results including raw browser output](atlas_final_results.json)
- [Untouched browser snapshots](browser_records_atlas_final.json)
- [Final browser proof](atlas-final-proof.jpg)
