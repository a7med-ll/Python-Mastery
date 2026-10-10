# New Boreal PDF — final challenge

Tested through the localhost Streamlit browser UI on 10 October 2026. Twelve questions were submitted individually and completed outputs captured. No application code was changed and no LLM API was added.

**Grounded result: 8/12 passed (66.7%). System score: 7/10.** Score is the grounded pass rate scaled to ten and rounded to a whole number; this small fixture is not a production reliability estimate.

**Comparable evidence/status-only result: 9/12 (75.0%).** The stricter grounded result additionally requires the newly displayed NLI verification sentence to support the classification. A correct label with an unrelated verification sentence fails grounding. This distinction keeps comparisons with earlier reports honest.

The app returns cited evidence, not a generated answer. Passing requires sufficient displayed evidence to establish the expected answer; calculations and prose synthesis are not required. Vector/rerank scores are model scores, not probabilities. “Not shown” means the UI did not display a value; it does not mean zero.

## Findings and severity

- **High — missing cross-page link (case 8):** the shipment-to-route relation is retrieved but the route-to-destination relation is absent. The system cannot establish Amber Quay.
- **High — ungrounded NLI contradiction (case 11):** a generic fictional-document sentence is presented as verification at 99.64% confidence despite a relevant weekend policy being available.
- **Medium — combined-fact retrieval incomplete (case 3):** fee amounts are missing from displayed chunks, so the fragile-parcel total cannot be derived.
- **Medium — ambiguity and chunk boundary (case 7):** the role definition ends before the name, and the other role/name is absent.
- **Medium — obsolete policy outranks current policy (case 9):** the superseded 15 kg rule ranks above the current 18.5 kg rule. Case passes because the current rule is present, but ordering can mislead readers.

Potential improvements within the existing scope: overlap or preserve sentence boundaries when chunking; retrieve neighboring chunks and expand retrieval for linked entities; prefer current policy metadata; require topical relevance before selecting NLI verification evidence. These are recommendations only; no changes were made.

New fixture: four text-based pages, indexed into eight chunks. All displayed evidence belonged to the new PDF; no cross-document leakage was observed in this suite. [Download Boreal PDF](../examples/boreal_final_challenge.pdf).

## All twelve cases

### 1. exact — PASS

**Question:** Who is the Boreal service coordinator?

**Expected answer/evidence:** Mira Haddad; page 1. Do not confuse Tarek Amin, coordinator of Boreal Express.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c1; vector **0.5610**, rerank **7.0182**.

```text
BOREAL / OPERATIONS MANUAL
Current service schedule
Boreal delivery program - revision 3, effective 1 September 2028. This is a fictional operations
document. Physical PDF page numbers are the citation reference.
The Boreal service coordinator is Mira Haddad. The depot is Harbor East. Standard deliveries
leave the depot at 06:40 each weekday.
Boreal delivery fee is AED 27.50 per parcel. There is an additional AED 4.25 fragile-handling
```

Rank 2 — page 2, p2-c1; vector **0.4752**, rerank **5.0862**.

```text
BOREAL / OPERATIONS MANUAL
Revision history and identifiers
Revision 1, superseded on 1 September 2028: the standard fee was AED 22.00 and the parcel
weight limit was 15 kg. Revision 3 governs current shipments.
Boreal Express is a separate service coordinated by Tarek Amin. Boreal Express leaves the
North Gate depot at 07:15. These details do not describe the Boreal delivery program.
In this manual, lead can mean the service coordinator or the safety lead. The Boreal safety lead
```

**Notes:** Mira Haddad correctly retrieved; separate Express coordinator appears as a distractor.

### 2. paraphrase — PASS

**Question:** How many working days does normal Boreal transit take?

**Expected answer/evidence:** Two business days; page 1.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c2; vector **0.5692**, rerank **6.5319**.

```text
fee for a fragile parcel. Fees exclude tax. This document does not specify a tax rate. Boreal accepts parcels up to and including 18.5 kg. Parcels heavier than 18.5 kg are rejected.
Normal transit takes two business days.
Standard delivery is not available on weekends. An approved emergency shipment may run on
a Saturday; emergency service is a separate service.
Fictional evaluation fixture | Page 1 of 4
```

**Notes:** Two business days correctly retrieved.

### 3. combined — FAIL

**Question:** What is the fee before tax for fragile parcel BX-52, and is its weight allowed?

**Expected answer/evidence:** AED 31.75 = 27.50 + 4.25; 18.5 kg is accepted inclusively. Pages 1 and 2. Evidence must include fragile status, weight and fee/limit rules; no computed answer required for evidence-only scope.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c2; vector **0.6034**, rerank **4.2748**.

```text
fee for a fragile parcel. Fees exclude tax. This document does not specify a tax rate. Boreal accepts parcels up to and including 18.5 kg. Parcels heavier than 18.5 kg are rejected.
Normal transit takes two business days.
Standard delivery is not available on weekends. An approved emergency shipment may run on
a Saturday; emergency service is a separate service.
Fictional evaluation fixture | Page 1 of 4
```

Rank 2 — page 2, p2-c2; vector **0.4706**, rerank **3.8901**.

```text
is Hala Saleh. Shipment BX-47 was sent using the Boreal service. Its route code is R7. It is not a Boreal
Express shipment.
Shipment BX-52 uses route R4. BX-52 is a fragile parcel weighing 18.5 kg. The current service
schedule contains the rules for its fee and acceptance.
Fictional evaluation fixture | Page 2 of 4
```

**Notes:** FAIL: parcel weight and fragile status retrieved, but AED 27.50 and AED 4.25 fee values omitted. Cannot derive fee from displayed evidence. Arithmetic generation was not required.

### 4. contradiction — PASS

**Question:** Boreal accepts parcels weighing twenty kilograms. Is that allowed by the current weight rule?

**Expected answer/evidence:** Contradicted: rejects weights over 18.5 kg; page 1.

**NLI:** contradicted. Confidence: 92.64%.

**Actual verification sentence (rank 2):** Parcels heavier than 18.5 kg are rejected.


**Actual status output:**

```text
Search
The premise in the question is contradicted by the document.
Claim checked:
Boreal accepts parcels weighing twenty kilograms
Evidence used for verification:
Parcels heavier than 18.5 kg are rejected.
NLI confidence: 92.64% | Evidence rank: 2
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 2, p2-c2; vector **0.3999**, rerank **3.9765**.

```text
is Hala Saleh. Shipment BX-47 was sent using the Boreal service. Its route code is R7. It is not a Boreal
Express shipment.
Shipment BX-52 uses route R4. BX-52 is a fragile parcel weighing 18.5 kg. The current service
schedule contains the rules for its fee and acceptance.
Fictional evaluation fixture | Page 2 of 4
```

Rank 2 — page 1, p1-c2; vector **0.5958**, rerank **3.8733**.

```text
fee for a fragile parcel. Fees exclude tax. This document does not specify a tax rate. Boreal accepts parcels up to and including 18.5 kg. Parcels heavier than 18.5 kg are rejected.
Normal transit takes two business days.
Standard delivery is not available on weekends. An approved emergency shipment may run on
a Saturday; emergency service is a separate service.
Fictional evaluation fixture | Page 1 of 4
```

Rank 3 — page 2, p2-c1; vector **0.5741**, rerank **3.3844**.

```text
BOREAL / OPERATIONS MANUAL
Revision history and identifiers
Revision 1, superseded on 1 September 2028: the standard fee was AED 22.00 and the parcel
weight limit was 15 kg. Revision 3 governs current shipments.
Boreal Express is a separate service coordinated by Tarek Amin. Boreal Express leaves the
North Gate depot at 07:15. These details do not describe the Boreal delivery program.
In this manual, lead can mean the service coordinator or the safety lead. The Boreal safety lead
```

**Notes:** Correct contradiction grounded in rejection of weights above 18.5 kg.

### 5. wrong_page — PASS

**Question:** According to page 4, at what time do standard Boreal deliveries leave?

**Expected answer/evidence:** 06:40 on weekdays, supported on page 1, not page 4. Cite actual source.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c1; vector **0.6616**, rerank **6.2742**.

```text
BOREAL / OPERATIONS MANUAL
Current service schedule
Boreal delivery program - revision 3, effective 1 September 2028. This is a fictional operations
document. Physical PDF page numbers are the citation reference.
The Boreal service coordinator is Mira Haddad. The depot is Harbor East. Standard deliveries
leave the depot at 06:40 each weekday.
Boreal delivery fee is AED 27.50 per parcel. There is an additional AED 4.25 fragile-handling
```

Rank 2 — page 1, p1-c2; vector **0.5744**, rerank **3.7421**.

```text
fee for a fragile parcel. Fees exclude tax. This document does not specify a tax rate. Boreal accepts parcels up to and including 18.5 kg. Parcels heavier than 18.5 kg are rejected.
Normal transit takes two business days.
Standard delivery is not available on weekends. An approved emergency shipment may run on
a Saturday; emergency service is a separate service.
Fictional evaluation fixture | Page 1 of 4
```

Rank 3 — page 2, p2-c1; vector **0.4967**, rerank **2.1040**.

```text
BOREAL / OPERATIONS MANUAL
Revision history and identifiers
Revision 1, superseded on 1 September 2028: the standard fee was AED 22.00 and the parcel
weight limit was 15 kg. Revision 3 governs current shipments.
Boreal Express is a separate service coordinated by Tarek Amin. Boreal Express leaves the
North Gate depot at 07:15. These details do not describe the Boreal delivery program.
In this manual, lead can mean the service coordinator or the safety lead. The Boreal safety lead
```

**Notes:** 06:40 weekday departure retrieved with page 1 citation despite requested page 4.

### 6. unrelated — PASS

**Question:** Who won the 2026 World Cup?

**Expected answer/evidence:** Abstain: no relevant evidence in this operations manual. Do not answer from outside knowledge.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
No sufficiently relevant evidence was found in the indexed document.
```

**Actual retrieved output and displayed scores:**

No evidence chunks or vector/rerank scores shown.
**Notes:** Correctly abstains on an unrelated question.

### 7. ambiguous — FAIL

**Question:** Who is the Boreal lead?

**Expected answer/evidence:** Distinguish Mira Haddad (service coordinator, page 1) and Hala Saleh (safety lead, page 2), or clarify the role. Evidence must expose both meanings.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 2, p2-c1; vector **0.4856**, rerank **4.0784**.

```text
BOREAL / OPERATIONS MANUAL
Revision history and identifiers
Revision 1, superseded on 1 September 2028: the standard fee was AED 22.00 and the parcel
weight limit was 15 kg. Revision 3 governs current shipments.
Boreal Express is a separate service coordinated by Tarek Amin. Boreal Express leaves the
North Gate depot at 07:15. These details do not describe the Boreal delivery program.
In this manual, lead can mean the service coordinator or the safety lead. The Boreal safety lead
```

**Notes:** FAIL: retrieves the ambiguity description but truncates before Hala Saleh; Mira Haddad also absent. Neither complete role distinction nor clarification.

### 8. cross_page — FAIL

**Question:** Where does Boreal shipment BX-47 terminate?

**Expected answer/evidence:** Amber Quay: BX-47 uses R7 (page 2), R7 terminates at Amber Quay (page 3). Both link and destination must be retrieved.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 2, p2-c2; vector **0.6886**, rerank **5.1270**.

```text
is Hala Saleh. Shipment BX-47 was sent using the Boreal service. Its route code is R7. It is not a Boreal
Express shipment.
Shipment BX-52 uses route R4. BX-52 is a fragile parcel weighing 18.5 kg. The current service
schedule contains the rules for its fee and acceptance.
Fictional evaluation fixture | Page 2 of 4
```

Rank 2 — page 4, p4-c1; vector **0.7104**, rerank **1.9525**.

```text
BOREAL / OPERATIONS MANUAL
Operating records
Parcel BX-52 passed its packaging inspection on 3 September 2028. Packaging inspection is
separate from driver permit checks.
On 4 September 2028, the Boreal depot logged 64 dispatched parcels and 3 returned parcels.
Returned parcels are counted separately from dispatched parcels.
Forty-one of the dispatched parcels used route R7, and twenty-three used route R4. These
route counts total sixty-four.
```

**Notes:** FAIL: BX-47 → R7 retrieved, but R7 → Amber Quay omitted. Dispatch counts do not complete the route lookup.

### 9. numeric — PASS

**Question:** What is the current maximum Boreal parcel weight in kilograms?

**Expected answer/evidence:** 18.5 kg inclusive; page 1, not obsolete 15 kg on page 2.

**NLI:** not shown / not checked. Confidence: not shown.

**Actual status output:**

```text
Search
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 2, p2-c1; vector **0.5504**, rerank **5.3782**.

```text
BOREAL / OPERATIONS MANUAL
Revision history and identifiers
Revision 1, superseded on 1 September 2028: the standard fee was AED 22.00 and the parcel
weight limit was 15 kg. Revision 3 governs current shipments.
Boreal Express is a separate service coordinated by Tarek Amin. Boreal Express leaves the
North Gate depot at 07:15. These details do not describe the Boreal delivery program.
In this manual, lead can mean the service coordinator or the safety lead. The Boreal safety lead
```

Rank 2 — page 2, p2-c2; vector **0.3195**, rerank **4.1523**.

```text
is Hala Saleh. Shipment BX-47 was sent using the Boreal service. Its route code is R7. It is not a Boreal
Express shipment.
Shipment BX-52 uses route R4. BX-52 is a fragile parcel weighing 18.5 kg. The current service
schedule contains the rules for its fee and acceptance.
Fictional evaluation fixture | Page 2 of 4
```

Rank 3 — page 1, p1-c2; vector **0.5584**, rerank **2.9465**.

```text
fee for a fragile parcel. Fees exclude tax. This document does not specify a tax rate. Boreal accepts parcels up to and including 18.5 kg. Parcels heavier than 18.5 kg are rejected.
Normal transit takes two business days.
Standard delivery is not available on weekends. An approved emergency shipment may run on
a Saturday; emergency service is a separate service.
Fictional evaluation fixture | Page 1 of 4
```

**Notes:** PASS with ranking risk: obsolete 15 kg appears first; current 18.5 kg inclusive rule appears only in rank 3.

### 10. unsupported — PASS

**Question:** Boreal achieved 98.7 percent on-time delivery in September 2028. What evidence verifies this?

**Expected answer/evidence:** Not enough evidence: no on-time percentage reported (page 4); absence of measurement does not contradict achieved performance.

**NLI:** not_enough_evidence. Confidence: not shown.

**Actual status output:**

```text
Search
The indexed document does not provide enough evidence to verify the premise in this question.
Claim checked:
Boreal achieved 98.7 percent on-time delivery in September 2028
```

**Actual retrieved output and displayed scores:**

No evidence chunks or vector/rerank scores shown.
**Notes:** Correctly reports insufficient evidence; absence of a measurement is not treated as contradiction.

### 11. implicit_false — FAIL

**Question:** Why does Boreal provide standard weekend delivery?

**Expected answer/evidence:** Contradicted: standard service not available on weekends; separate approved Saturday emergency service does not change that rule. Page 1.

**NLI:** contradicted. Confidence: 99.64%.

**Actual verification sentence (rank 2):** This is a fictional operations
document.


**Actual status output:**

```text
Search
The premise in the question is contradicted by the document.
Claim checked:
Boreal provide standard weekend delivery
Evidence used for verification:
This is a fictional operations
document.
NLI confidence: 99.64% | Evidence rank: 2
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 1, p1-c2; vector **0.6031**, rerank **3.5961**.

```text
fee for a fragile parcel. Fees exclude tax. This document does not specify a tax rate. Boreal accepts parcels up to and including 18.5 kg. Parcels heavier than 18.5 kg are rejected.
Normal transit takes two business days.
Standard delivery is not available on weekends. An approved emergency shipment may run on
a Saturday; emergency service is a separate service.
Fictional evaluation fixture | Page 1 of 4
```

Rank 2 — page 1, p1-c1; vector **0.6107**, rerank **1.8280**.

```text
BOREAL / OPERATIONS MANUAL
Current service schedule
Boreal delivery program - revision 3, effective 1 September 2028. This is a fictional operations
document. Physical PDF page numbers are the citation reference.
The Boreal service coordinator is Mira Haddad. The depot is Harbor East. Standard deliveries
leave the depot at 06:40 each weekday.
Boreal delivery fee is AED 27.50 per parcel. There is an additional AED 4.25 fragile-handling
```

**Notes:** FAIL grounding: correct contradiction label, but verification uses “This is a fictional operations document.” at 99.64% confidence. Weekend prohibition is displayed separately.

### 12. supported_exception — PASS

**Question:** Noor Karim completed safety training. Is Noor allowed to drive a Boreal vehicle?

**Expected answer/evidence:** Training premise SUPPORTED (page 3); driving not allowed because permit suspended. Retrieve the two-requirement rule and Noor record; do not contradict the completed-training premise.

**NLI:** supported. Confidence: 99.25%.

**Actual verification sentence (rank 1):** Noor Karim completed safety training on 12 August 2028.


**Actual status output:**

```text
Search
The premise in the question is supported by the document.
Claim checked:
Noor Karim completed safety training
Evidence used for verification:
Noor Karim completed safety training on 12 August 2028.
NLI confidence: 99.25% | Evidence rank: 1
```

**Actual retrieved output and displayed scores:**

Rank 1 — page 3, p3-c2; vector **0.8284**, rerank **9.4955**.

```text
Noor Karim works as a Boreal driver. Noor Karim completed safety training on 12 August 2028. Noor Karim has a suspended permit.
Salim Rashid holds a current permit. Salim Rashid has not completed safety training. Permit
possession does not waive training.
Fictional evaluation fixture | Page 3 of 4
```

Rank 2 — page 3, p3-c1; vector **0.4343**, rerank **1.8107**.

```text
BOREAL / OPERATIONS MANUAL
Routes and eligibility policy
Route R7 terminates at Amber Quay. Route R4 terminates at Stone Pier. Route R9 terminates
at Maple Yard.
Drivers may operate a Boreal vehicle only if they hold a current permit and their safety training
is complete. Either missing requirement prevents driving.
Completing safety training does not itself issue a permit. A suspended permit is not a current
permit.
```

**Notes:** Training premise correctly supported; suspended permit and driving requirements also retrieved.

## Audit files

- [CSV results](boreal_final_results.csv)
- [Structured results including raw browser output](boreal_final_results.json)
- [Untouched browser snapshots](browser_records_boreal_final.json)
- [Final browser proof](boreal-final-proof.jpg)
