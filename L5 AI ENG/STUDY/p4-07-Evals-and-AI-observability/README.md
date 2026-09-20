# P4-07 — Evals and AI Observability

## Purpose

This study task builds a conceptual understanding of how AI systems are evaluated before release and observed after deployment. It focuses on **golden datasets, LLM-as-judge evaluation, prompt regression testing, prompt/response logging, tracing, and token usage/cost**. It is deliberately **not a build project**. The evidence is a clear explanation, in your own words, of the concepts and trade-offs below.

## Learning outcomes

By the end, you should be able to explain:

- why software tests alone are insufficient for probabilistic AI behavior;
- the difference between evaluation, testing, monitoring, and observability;
- what a golden dataset contains and how it should be versioned;
- how exact-match, rule-based, semantic, human, and model-based graders differ;
- how pointwise, pairwise, and reference-based evaluation differ;
- what LLM-as-judge can measure and which biases it can introduce;
- how to calibrate an automated judge against human labels;
- how prompt regression testing prevents silent quality loss;
- why aggregate scores must be supplemented with slices and failure analysis;
- how logs, metrics, traces, and feedback complement one another;
- what to record for prompts, responses, retrieval, tools, models, and errors;
- how token usage, latency, and cost should be attributed across a trace;
- why privacy, security, retention, and access controls are essential for AI telemetry;
- how offline evaluation and production observation form a continuous improvement loop.

---

## 1. Evaluation and observability answer different questions

### Evaluation

**Evaluation** asks whether the system's behavior meets defined quality requirements.

Examples:

- Is the answer factually correct?
- Did the output match the required schema?
- Was the response grounded in the retrieved evidence?
- Did the model select the correct tool?
- Did the assistant refuse an unsafe request appropriately?
- Is the new prompt better than the current prompt?

### Observability

**Observability** asks what happened inside a running system and provides enough evidence to explain its behavior.

Examples:

- Which prompt and model version produced the answer?
- Which documents were retrieved?
- Which tools were called, and how long did they take?
- Where did an error occur?
- How many tokens and how much money did the request consume?
- Was latency caused by retrieval, model generation, a queue, or a tool?

### Monitoring

**Monitoring** watches known signals and alerts when they cross expected boundaries.

Examples:

- error rate exceeds 2%;
- p95 latency exceeds five seconds;
- average input tokens double;
- daily model spend exceeds budget;
- groundedness score drops below the release threshold.

### Testing

**Testing** verifies expected behavior under defined conditions. Deterministic software tests remain important for:

- parsers;
- access-control checks;
- schema validators;
- tool execution;
- prompt-template rendering;
- cost calculations;
- retry and timeout logic.

AI evaluation adds methods for outputs that can be valid in more than one form.

### How the four connect

```text
offline evaluation
      ↓ release gate
production system
      ↓ telemetry
monitoring and traces
      ↓ failures and feedback
new evaluation cases
      ↓
next offline evaluation
```

Evaluation says whether behavior is acceptable. Observability supplies the evidence needed to diagnose and improve it.

---

## 2. Why AI evaluation is different

### Outputs are often non-deterministic

The same input can produce different wording or even different decisions because of sampling, provider changes, model updates, tool results, or nondeterministic infrastructure.

A test such as:

```text
assert actual_output == one_expected_paragraph
```

is too strict for many valid natural-language tasks and too weak for semantic correctness if the expected string is itself incomplete.

### Many outputs can be correct

A summarization request, support answer, or rewritten email can have many acceptable responses. Evaluation must define the qualities that matter instead of one exact sentence.

### One response has several quality dimensions

A response can be:

- fluent but incorrect;
- correct but unsupported by supplied evidence;
- grounded but incomplete;
- safe but unhelpful;
- structurally valid but semantically wrong;
- accurate but too slow or expensive.

One score should not silently combine unrelated properties.

### The system is larger than the model

An AI application may include:

- prompt assembly;
- retrieval;
- reranking;
- model generation;
- tool selection and execution;
- structured-output parsing;
- safety checks;
- post-processing;
- user-interface behavior.

Evaluate components separately and the end-to-end system together.

---

## 3. Define the evaluation target

### Begin with a task specification

Before choosing metrics, define:

- intended users;
- supported tasks;
- acceptable and unacceptable outputs;
- authoritative sources;
- safety requirements;
- latency and cost budgets;
- cases where the system should abstain or ask a question;
- consequences of false positives and false negatives.

A metric without a task definition measures whatever the test happened to contain.

### Unit of evaluation

The unit might be:

- one classification;
- one assistant turn;
- a multi-turn conversation;
- one retrieved chunk;
- a complete RAG answer;
- a tool-call trajectory;
- an entire user task or business outcome.

Choose a unit aligned with real success. A correct individual message does not prove that a multi-step task succeeded.

### Quality dimensions

Common dimensions include:

- correctness;
- relevance;
- completeness;
- groundedness;
- citation support;
- instruction following;
- format compliance;
- safety;
- tone and style;
- tool-selection accuracy;
- task completion;
- latency;
- token usage and cost.

Each dimension needs an operational definition.

### Thresholds and trade-offs

Define what is required to ship. Examples:

- no regression greater than an allowed margin;
- schema validity above a threshold;
- zero critical permission failures;
- higher task success without unacceptable latency growth;
- improved quality for priority slices, not only the overall average.

A threshold should reflect product risk rather than a convenient round number.

---

## 4. Golden datasets

### What a golden dataset is

A **golden dataset** is a curated collection of representative evaluation cases with trusted labels, reference information, rubrics, or expected behavior.

A case may contain:

- input or conversation history;
- relevant user and environment metadata;
- expected output or acceptable-output criteria;
- retrieved evidence or an authoritative reference;
- required and prohibited behaviors;
- grading method;
- category and difficulty labels;
- provenance and reviewer information.

“Golden” means carefully curated, not permanently perfect.

### Sources of cases

Cases can come from:

- domain experts;
- anonymized production interactions;
- known incidents and bug reports;
- support tickets;
- manually authored edge cases;
- adversarial testing;
- synthetic generation followed by human review;
- public benchmarks when they match the task.

Real production failures are especially valuable because they reveal assumptions missed during initial design.

### Representative distribution

The dataset should cover:

- frequent requests;
- high-impact rare cases;
- easy and difficult inputs;
- ambiguous and incomplete requests;
- multiple languages or regions where applicable;
- short and long context;
- each supported tool or workflow;
- answerable and unanswerable questions;
- benign and adversarial inputs;
- cases requiring refusal or escalation.

A dataset containing only ordinary happy paths creates false confidence.

### Golden answer versus grading criteria

Some tasks have one exact answer, such as a category label or computed number. Open-ended tasks usually benefit from a rubric or reference facts instead of one required wording.

For example:

```text
Required facts:
- refund window is 30 days
- proof of purchase is required

Must not claim:
- opened software is always refundable

Style:
- concise and helpful
```

This allows different valid phrasings while preserving factual requirements.

### Positive, negative, and contrastive examples

Include:

- clear successes;
- clear failures;
- near-misses;
- irrelevant but plausible evidence;
- answers that sound polished but are wrong;
- answers that are correct but violate format or policy.

Near-misses help graders learn and test meaningful boundaries.

### Versioning

Version the dataset together with:

- case IDs;
- label and rubric revisions;
- provenance;
- additions and removals;
- reviewer decisions;
- source-document versions;
- evaluation code and grader prompts.

Historical results are not comparable if the dataset or rubric changed silently.

### Prevent leakage

Keep evaluation cases separate from:

- fine-tuning data;
- prompt examples;
- few-shot demonstrations;
- optimization feedback shown repeatedly to model developers.

Near-duplicate leakage can make a system appear to generalize when it has only adapted to the benchmark.

### A living dataset

Add production failures, new features, and newly important risks. Retire obsolete cases transparently. Maintain a stable core suite for long-term comparison and a rotating or hidden suite to reduce overfitting.

---

## 5. Grading methods

### Deterministic graders

Deterministic checks are best when correctness has an exact machine-readable definition.

Examples:

- exact match after safe normalization;
- regular-expression checks;
- JSON Schema or Pydantic validation;
- required-key presence;
- numeric tolerance;
- successful code tests;
- tool name and argument comparison;
- citation identifier existence;
- authorization outcome.

These graders are fast, reproducible, and inexpensive.

### Reference-based metrics

Text-overlap metrics compare a response with reference text. They can be useful for constrained tasks but may penalize valid paraphrases and reward surface overlap without correctness.

Use them only when overlap represents the desired quality.

### Semantic similarity

Embedding similarity can identify related meaning, but a high score does not prove factual correctness, completeness, or policy compliance. It is a useful signal, not a universal grader.

### Human evaluation

Humans are essential when quality requires domain judgment, subtle safety decisions, or product preference.

Reliable human evaluation needs:

- a clear rubric;
- examples at score boundaries;
- trained reviewers;
- blinded model or variant identity where possible;
- multiple labels for ambiguous cases;
- adjudication for disagreements;
- measurement of inter-rater agreement.

Human judgment is not automatically objective. Reviewers can disagree or drift over time.

### Model-based evaluation

An LLM can grade responses using a rubric, reference material, or pairwise comparison. This is often called **LLM-as-judge**.

It offers scale and flexibility but must be validated rather than treated as ground truth.

### Outcome-based evaluation

When possible, evaluate actual task outcomes:

- Was the ticket resolved?
- Did the correct database record change?
- Did code pass tests?
- Did the user complete the workflow?
- Was escalation required later?

Outcome metrics can be more meaningful than prose-quality scores, though outcomes may be delayed and influenced by factors outside the model.

---

## 6. LLM-as-judge

### What it means

An evaluator model receives some combination of:

- the original task;
- candidate response;
- reference answer or evidence;
- grading rubric;
- optional competing response;

and returns a score, label, preference, and sometimes an explanation.

### Pointwise evaluation

A pointwise judge scores one response independently.

Example:

```text
Score factual correctness from 1 to 5 using the supplied evidence.
```

Pointwise scores are easy to aggregate, but numerical scales can be inconsistently interpreted.

### Pairwise evaluation

A pairwise judge chooses between response A and response B, possibly allowing a tie.

Pairwise judgment can be easier than assigning an absolute score, but it is vulnerable to presentation order and requires an aggregation strategy across comparisons.

### Reference-based evaluation

The judge compares the candidate with trusted reference facts, an ideal answer, or source evidence. This helps constrain the judgment, but the reference itself must be correct and sufficiently complete.

### Reference-free evaluation

The judge uses only the task and rubric. This may be necessary for open-ended qualities such as tone, but it increases dependence on the judge's own knowledge and preferences.

### Rubric design

A strong rubric should:

- define one dimension at a time where practical;
- describe what each score or label means;
- identify critical failures;
- distinguish factual correctness from writing quality;
- specify how to treat missing information;
- include boundary examples;
- require evidence for the judgment;
- produce a structured result.

Avoid vague prompts such as “rate how good this is.”

---

## 7. LLM-judge limitations

### Position bias

In pairwise evaluation, a judge may prefer the first or second response because of its position. A simple test is to swap A and B and measure how often the verdict changes.

### Verbosity and style bias

A longer, more polished response may be preferred even when a shorter response is equally or more correct. Grade factual and stylistic dimensions separately.

### Self-preference or family bias

A judge may favor outputs with patterns similar to its own provider or model family. Avoid assuming neutrality merely because the judge differs from the candidate.

### Knowledge and reasoning limitations

A judge can confidently misgrade a response if the task exceeds its knowledge, reasoning, language, or domain capability.

### Prompt sensitivity

Small rubric or formatting changes can affect judgments. The judge prompt, model, settings, and parsing logic are versioned components of the evaluation system.

### Contamination and correlated errors

Candidate and judge models may share training data, assumptions, or blind spots. Agreement between models is not independent proof of correctness.

### Judge drift

A provider can update a judge model or alias. Evaluation results may shift even when the application does not change. Use pinned versions where available and rerun calibration when the judge changes.

---

## 8. Calibrating an LLM judge

### Use a human-labeled calibration set

Create cases spanning:

- clear passes and failures;
- boundary cases;
- each important task slice;
- intentionally misleading answers;
- different answer lengths and styles;
- order-swapped pairs.

Compare judge outputs with expert labels.

### Measure agreement

Possible measurements include:

- accuracy for categorical labels;
- precision and recall for failure detection;
- correlation for ordered scores;
- Cohen's kappa or related agreement measures;
- consistency under repeated grading;
- flip rate when candidate order changes.

High consistency does not necessarily mean high validity. A judge can repeat the same biased decision reliably.

### Reduce bias

Possible controls include:

- randomizing and swapping pair order;
- hiding provider and model names;
- normalizing superficial formatting;
- grading separate dimensions independently;
- using clear reference evidence;
- allowing ties and uncertainty;
- using multiple judges for high-risk cases;
- sending low-confidence or disagreement cases to humans.

### Do not use the judge's explanation as proof

A plausible rationale can accompany an incorrect grade. Validate the decision itself against human labels and deterministic evidence.

---

## 9. Prompt regression testing

### What a regression is

A **regression** occurs when a change makes previously acceptable behavior worse.

Potential causes include:

- editing a prompt;
- changing few-shot examples;
- changing a model or model version;
- modifying retrieval or chunking;
- adding a tool;
- changing structured-output schemas;
- updating safety instructions;
- altering conversation-memory logic.

### Treat prompts as versioned artifacts

Track:

- prompt ID and version;
- template text;
- variables and rendering logic;
- few-shot examples;
- linked tool schemas;
- expected model family;
- change rationale;
- evaluation results.

A prompt hidden inside application code without a version is difficult to compare or roll back.

### Regression workflow

```text
proposed change
    ↓
run stable golden dataset
    ↓
compare candidate with baseline
    ↓
inspect overall metrics and slices
    ↓
review changed cases
    ↓
ship, revise, or reject
```

### Paired comparison

Run baseline and candidate on the same cases. Paired analysis reduces noise because both variants face identical inputs.

Record:

- wins, losses, and ties;
- newly fixed cases;
- newly broken cases;
- quality by slice;
- latency, token, and cost differences.

### Non-determinism

For unstable tasks, consider repeated trials and report distributions or confidence intervals instead of one run. Keep sampling settings controlled when the goal is regression detection.

### Release gates

Examples of gates:

- no critical safety or authorization failure;
- deterministic tests all pass;
- overall task score does not regress beyond tolerance;
- priority slices meet minimum thresholds;
- latency and cost stay within budget;
- new capability improves its target cases.

An improved average must not hide a severe failure in a critical slice.

### Inspect examples, not only scores

A one-point change can come from label noise, judge drift, or a genuine product problem. Review representative wins and losses before deciding.

---

## 10. Component and end-to-end evaluation

### Retrieval

Evaluate:

- Hit Rate@k;
- Recall@k;
- Precision@k;
- MRR or nDCG;
- permission-filter correctness;
- source freshness;
- reranking quality.

### Generation

Evaluate:

- correctness;
- groundedness;
- completeness;
- citation support;
- style;
- abstention when evidence is insufficient.

### Tool calling

Evaluate:

- correct tool selection;
- correct arguments;
- avoidance of unnecessary tools;
- multi-step ordering;
- recovery from tool errors;
- respect for confirmation and authorization boundaries.

### Structured output

Evaluate:

- parse rate;
- schema validity;
- field-level correctness;
- business-rule validity;
- retry rate;
- behavior when no valid result exists.

### End-to-end task

Evaluate whether the full user goal was completed safely. Strong component metrics can still combine into a poor workflow.

---

## 11. Offline and online evaluation

### Offline evaluation

Offline evaluation runs against a controlled dataset. It is:

- repeatable;
- suitable for release gates;
- safe for testing failures;
- useful for comparing variants.

Its weakness is representativeness. A fixed dataset cannot fully capture future users or changing production data.

### Shadow evaluation

A candidate runs on copied production inputs without affecting users. Its outputs are evaluated against the live system or later outcomes.

Shadowing reveals real traffic behavior but requires strong privacy controls and careful handling of duplicate side effects.

### A/B testing

Users are assigned to variants, and product outcomes are compared. Randomization helps causal comparison, but experimentation must respect risk, sample size, exposure, and stopping rules.

### Production feedback

Signals may include:

- explicit ratings;
- corrections;
- regenerated responses;
- task completion;
- escalation;
- citation clicks;
- user abandonment;
- downstream success or failure.

These are imperfect proxies. For example, no complaint does not prove correctness.

### Convert incidents into tests

When a meaningful production failure occurs:

1. preserve a safely redacted trace;
2. identify the failure layer;
3. create a reproducible evaluation case;
4. verify that the proposed fix passes;
5. retain the case to prevent recurrence.

---

## 12. AI observability fundamentals

### Logs

Logs are discrete records of events. They may describe:

- request received;
- retrieval completed;
- tool call failed;
- response validation failed;
- model request was rate-limited.

Logs are useful for details but difficult to understand as an end-to-end flow without correlation.

### Metrics

Metrics are numerical time-series summaries such as:

- request rate;
- error rate;
- p95 latency;
- input and output token totals;
- daily cost;
- cache-hit rate;
- tool failure rate;
- evaluation-score trends.

Metrics support dashboards and alerts but usually lack case-level detail.

### Traces

A trace represents one end-to-end request or workflow as a tree or graph of timed operations called **spans**.

```text
user request trace
├── prompt assembly
├── retrieval
│   ├── query embedding
│   ├── vector search
│   └── reranking
├── model response
├── tool call
│   └── external API
└── response validation
```

Traces show where time, tokens, cost, and failures occurred.

### Events

Events record notable occurrences within a span, such as:

- first streamed token;
- retry attempt;
- tool approval requested;
- safety refusal;
- output parser failure.

### Feedback and evaluation labels

Feedback is not a replacement for telemetry. Link ratings, human labels, and automated evaluation results to the relevant trace or response ID so behavior can be analyzed with its context.

---

## 13. Trace design

### Correlation identifiers

Useful identifiers include:

- trace ID;
- span ID and parent span ID;
- application request ID;
- conversation and turn ID;
- user or tenant identifier in a privacy-safe form;
- model-provider request ID;
- prompt version;
- deployment version.

These identifiers connect application logs with model, retrieval, and tool operations.

### Span attributes

A model span may record:

- provider and model identifier;
- operation name;
- prompt/template version;
- streaming status;
- input and output token counts;
- request and first-token timestamps;
- completion status;
- finish reason;
- retry count;
- cost estimate;
- error type.

Do not place sensitive prompt text into attributes intended for unrestricted indexing.

### Retrieval spans

Useful retrieval data includes:

- index and embedding-model version;
- original and rewritten query identifiers;
- filter summary;
- candidate count;
- retrieved chunk IDs and scores;
- reranked order;
- selected context IDs;
- latency per stage.

### Tool spans

Record:

- tool name and version;
- validated argument summary;
- authorization decision;
- execution status;
- latency and retry count;
- result size or safe summary;
- external service correlation ID;
- error category.

Avoid logging secrets or sensitive full arguments by default.

### Nested and multi-agent traces

Complex workflows may branch, run tools in parallel, or invoke sub-agents. Preserve parent–child relationships and links so that all work can be attributed to the originating request.

---

## 14. Prompt and response logging

### Why teams log content

Prompt and response content can help:

- reproduce failures;
- audit behavior;
- create evaluation cases;
- inspect retrieval grounding;
- diagnose prompt rendering;
- understand user needs.

### Why full logging is risky

Prompts and responses may contain:

- personally identifiable information;
- credentials or API keys;
- private documents;
- health, financial, or legal information;
- proprietary code;
- malicious instructions;
- data subject to deletion or residency requirements.

Observability storage can become a second sensitive data system.

### Data-minimization choices

Depending on risk, record:

- no content, only metadata;
- hashes or stable identifiers;
- redacted excerpts;
- sampled full content;
- encrypted content with restricted access;
- references to content stored in a governed system;
- short retention for debugging data.

The choice should follow the use case, law, contracts, and threat model.

### Redaction

Redaction can detect and remove known sensitive patterns before storage, but it is imperfect. Apply controls at several layers:

- input filtering;
- structured field allowlists;
- secret detection;
- access control;
- encryption;
- retention limits;
- audit logs;
- deletion workflows.

### Sampling

Logging every full interaction may be too costly or risky. Sampling strategies include:

- uniform sampling;
- higher sampling for errors;
- higher sampling for new deployments;
- targeted sampling for important slices;
- full metadata with limited content capture.

Sampling must be recorded so analysts do not mistake the sample for the entire traffic distribution.

---

## 15. Token usage and cost

### Token categories

Providers may report categories such as:

- input tokens;
- output tokens;
- cached input tokens;
- reasoning-related tokens;
- audio, image, or other modality units;
- embedding tokens.

Names and billing rules differ. Preserve provider-native usage fields as well as normalized summaries.

### Cost attribution

Cost can occur in:

- the main generation;
- query rewriting;
- embeddings;
- reranking;
- LLM-as-judge evaluation;
- tool or search APIs;
- retries;
- failed or abandoned requests;
- batch or background work.

Attribute cost at the span, request, conversation, feature, tenant, and deployment levels where appropriate.

### Estimated and billed cost

An application may estimate cost from tokens and a pricing table. This is not automatically identical to provider billing because of:

- pricing changes;
- service tiers;
- cached-token rules;
- batch discounts;
- multimodal units;
- rounding;
- provider-specific charges.

Version the pricing table used for each estimate and reconcile with billing data.

### Cost-quality trade-off

Do not optimize cost alone. Track quality against cost:

- quality per request cost;
- task success per dollar;
- incremental quality gained by reranking or a larger model;
- cost by successful versus failed task;
- cost regressions caused by longer prompts or retries.

A cheaper system that fails more often may be more expensive at the product level.

---

## 16. Latency and reliability metrics

### Latency measures

Track distributions rather than only averages:

- end-to-end latency;
- queue time;
- retrieval latency;
- tool latency;
- model time to first token;
- total model duration;
- inter-token latency or output rate;
- validation and post-processing time;
- p50, p95, and p99 values.

### Streaming latency

For streaming experiences, separate:

- request start;
- connection established;
- first meaningful output;
- final event;
- user cancellation.

Fast first output can coexist with slow total completion.

### Reliability measures

Track:

- timeout rate;
- rate-limit rate;
- provider and model errors;
- retry count and recovered requests;
- invalid structured-output rate;
- tool failures;
- cancelled requests;
- incomplete generations;
- fallback usage;
- queue rejection or overload.

### Retry inflation

A successful final response can hide two failed attempts. Track attempt-level and request-level success separately, including tokens, cost, and latency spent on retries.

---

## 17. Dashboards and alerts

### Operational dashboard

Useful operational views include:

- traffic and concurrency;
- latency percentiles;
- error and retry rates;
- provider/model availability;
- queue depth;
- tool and retrieval health.

### Quality dashboard

Useful quality views include:

- evaluation scores over time;
- task success;
- groundedness and citation support;
- refusal and abstention behavior;
- human feedback;
- quality by prompt, model, language, product, or other slice.

### Cost dashboard

Useful cost views include:

- input and output tokens;
- cost per feature and tenant;
- cost per successful task;
- cache effectiveness;
- retry waste;
- budget trend and forecast.

### Alerts must be actionable

An alert should identify:

- what changed;
- which users or components are affected;
- severity;
- likely owner;
- useful trace links;
- immediate mitigation or runbook.

Too many unactionable alerts create alert fatigue.

### Quality alerts require care

Quality labels may arrive slowly, be sampled, or contain judge noise. Use sufficient sample sizes, confidence bounds, and sustained-change rules before treating a small fluctuation as an incident.

---

## 18. Drift and production change

### Input drift

Users may begin asking different questions because of new products, seasons, incidents, or changing interfaces. Compare production input distributions with the evaluation dataset.

### Knowledge drift

Policies and documents change. A model can behave consistently while its information becomes stale. Monitor source freshness and retrieval index updates.

### Model or provider drift

Behavior can change when:

- a model alias updates;
- safety behavior changes;
- an SDK or API version changes;
- serving parameters change;
- a fallback model receives more traffic.

Record the actual model and configuration used.

### Evaluation drift

A rubric or judge may no longer represent product expectations. Periodically revalidate automated graders with human review.

---

## 19. Security and governance

### Access control

Limit telemetry access by role. A dashboard viewer may need aggregate metrics but not raw prompts or private documents.

### Retention and deletion

Define retention by data type. Ensure that user deletion and source-deletion requirements also cover logs, traces, evaluation datasets, caches, and exported debugging artifacts.

### Encryption

Protect telemetry in transit and at rest. Manage encryption keys and access logs according to the sensitivity of recorded content.

### Prompt injection in telemetry

Retrieved documents, user prompts, and tool outputs are untrusted text. Observability interfaces should render them safely rather than interpreting HTML, Markdown, links, or commands as trusted instructions.

### Evaluation-data governance

Golden datasets can contain valuable production examples and human labels. Track consent, provenance, allowed uses, access, and whether cases may be used for evaluation, training, or both.

---

## 20. Common misconceptions

### “A high benchmark score proves the product is good”

False. The benchmark may not represent actual users, risks, tools, data, or workflows.

### “Golden datasets never change”

False. They require versioning, review, new incident cases, and protection against overfitting.

### “LLM-as-judge is ground truth”

False. It is an automated measurement instrument that must be calibrated and monitored for bias and drift.

### “A judge explanation proves the grade”

False. A fluent rationale can justify an incorrect decision.

### “One aggregate number is enough”

False. Averages hide failures in important slices and mix different quality dimensions.

### “If the model did not change, evaluation is unnecessary”

False. Prompts, retrieval, tools, data, SDKs, providers, and traffic can change behavior.

### “Observability means logging every prompt forever”

False. Good observability uses deliberate metadata, sampling, redaction, access controls, and retention.

### “The HTTP request succeeded, so the AI task succeeded”

False. Transport success says nothing about correctness, grounding, safety, or task completion.

### “Average latency describes user experience”

False. Tail latency and time to first meaningful output often matter more.

### “Token count equals cost”

Not by itself. Pricing varies by provider, model, token category, service tier, caching, and modality.

### “User feedback is unbiased ground truth”

False. Feedback is sparse and influenced by user expectations, interface design, and selection effects.

---

## 21. A practical evaluation and observability loop

1. Define the task, users, risks, and success criteria.
2. Build a versioned golden dataset from expert cases, realistic traffic, and known failures.
3. Choose the simplest valid grader for each dimension.
4. Calibrate LLM judges against human labels where they are used.
5. Establish a baseline for quality, latency, tokens, and cost.
6. Run paired prompt and pipeline regression tests before release.
7. Gate releases on overall metrics, important slices, and zero-tolerance failures.
8. Trace production requests across retrieval, models, and tools.
9. Monitor latency, errors, tokens, cost, and sampled quality.
10. Protect telemetry with minimization, redaction, access control, and retention.
11. Turn incidents and reviewed production failures into new test cases.
12. Recalibrate graders and refresh datasets as the product and traffic change.

This creates a feedback system rather than a one-time benchmark.

---

## 22. Knowledge check

You should now be able to answer these questions in your own words:

1. How do evaluation, testing, monitoring, and observability differ?
2. Why is exact string matching unsuitable for many generative tasks?
3. What belongs in a golden dataset case?
4. Why should golden datasets contain negative and near-miss examples?
5. How do deterministic, human, semantic, and LLM-based graders differ?
6. What is the difference between pointwise and pairwise judging?
7. What are position, verbosity, and self-preference biases?
8. How would you calibrate an LLM judge against humans?
9. Why does consistent judging not necessarily mean valid judging?
10. What is prompt regression testing?
11. Why should baseline and candidate prompts run on the same cases?
12. Why are slices necessary in addition to an overall average?
13. What information do logs, metrics, and traces each provide?
14. What spans would you expect in a RAG-and-tool workflow?
15. Why is logging full prompts and responses a security risk?
16. How can token and cost usage be attributed to a complete request?
17. Why should retries be visible even when the final request succeeds?
18. How do time to first token and total latency differ?
19. How can production incidents improve the golden dataset?
20. Why must automated judges and evaluation datasets be monitored for drift?

# P4-07 — Evals and AI Observability is completed with the provided readme notes
