# Manual retrieval and premise tests

Upload **atlas_adversarial.pdf**, select **Index Document**, and submit one question at a time. Page numbers below are physical PDF pages. These are expected behaviors, not claims that a new test run passed. The app displays evidence rather than generating a narrative answer.

| Response / test | Question | Expected evidence and review criteria |
| --- | --- | --- |
| Normal retrieval | Who is the project owner of Atlas? | Lina Faris; pages 1–2. Distinguish the document owner and Atlas Blue. |
| Paraphrase | How long are uploaded Atlas files kept before removal? | Current retention: 30 days, page 1; historical 90 days is superseded. |
| SUPPORTED | Yusuf Karim completed training. Can he access Atlas PDFs? | Training premise supported by page 4; access prohibited by Birch rule on page 3. A supported premise does not mean access is allowed. |
| CONTRADICTED | Atlas retains uploaded documents permanently. What is its retention policy? | Page 1 says 30 days and explicitly denies permanent retention. Verification sentence must concern retention. This case failed grounding in the saved Atlas run. |
| Implicit false premise | Why does Atlas use an LLM API? | Contradicted: page 1 says Atlas does not use an LLM API. |
| NOT ENOUGH EVIDENCE | Atlas achieved 99.9 percent uptime last year. What evidence proves this? | Insufficient evidence; page 4 supplies no uptime measurement. Missing evidence does not establish the claim is false. |
| Unrelated / abstention | What is the capital of France? | No relevant document evidence; abstain. |
| Wrong page | According to page 3, what is the current Atlas PDF upload limit? | 12 MB on page 1. Inspect actual citation; do not accept the question's page reference. |
| Misleading reference | What is the current maximum Atlas PDF upload size in MB? | 12 MB, page 1; do not mistake superseded 8 MB on page 2 for the current limit. |
| Cross-page | Is Samira Nasser eligible for Atlas PDF access, and why? | Cedar membership/access rule on page 3 plus completed training on page 4. Both are needed. |

For a second fixture, index **boreal_final_challenge.pdf** and ask: “Noor Karim completed safety training. Is Noor allowed to drive a Boreal vehicle?” Training is supported on page 3, but a suspended permit prevents driving. Ask “According to page 2, what is the current Boreal delivery fee?” and check that the current AED 27.50 fee is cited from page 1, not the obsolete AED 22.00 fee.

Other PDFs: **automotive_retrieval_test.pdf** is a demo fixture; **sample.pdf** is a reference sample. `../data/sample.pdf` remains the evaluator's original input and has not been relocated.

Record the label, actual verification sentence, cited page/chunk, and retrieved evidence. Scores alone do not establish correctness. Existing results are in `../evaluation/`; no adversarial suite was rerun during repository preparation.
