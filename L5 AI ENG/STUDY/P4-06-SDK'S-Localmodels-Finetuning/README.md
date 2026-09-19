# P4-06 — SDKs, Local Models, and When to Fine-Tune

## Purpose

This study task builds a conceptual understanding of three decisions AI engineers repeatedly face: how provider SDKs represent model requests and responses, when running a model locally or self-hosting is justified, and when fine-tuning is a better tool than prompting or Retrieval-Augmented Generation (RAG). It is deliberately **not a build project**. The evidence is a clear explanation of the concepts and trade-offs below.

## Learning outcomes

By the end, you should be able to explain:

- what an AI SDK does and what it does not do;
- the common parts of model requests and responses across providers;
- the important conceptual differences among the Anthropic, OpenAI, and Google GenAI SDKs;
- how synchronous, asynchronous, streaming, and realtime interactions differ;
- why a streaming response is a sequence of typed events rather than one finished message;
- why provider-neutral abstractions can help but can also hide capabilities;
- what fine-tuning changes inside a model;
- when prompting, RAG, tools, fine-tuning, or a combination is appropriate;
- what supervised fine-tuning data represents;
- how LoRA reduces the number of trainable parameters at a high level;
- the difference between running a model locally and operating a production inference service;
- the roles of Ollama and vLLM;
- when privacy, control, latency, scale, and total cost justify self-hosting;
- why evaluation must precede and follow every adaptation or deployment decision.

---

## 1. Begin with the problem, not the model

### Four different kinds of change

Many weak AI-system designs begin by choosing a technique before identifying what must change. Separate these needs:

1. **Behavior change:** The model should follow a style, format, classification rule, or workflow more consistently.
2. **Knowledge access:** The system needs current, private, or traceable facts.
3. **Action:** The system must read or modify external state through tools.
4. **Deployment control:** The organization needs a particular privacy, latency, hardware, licensing, or operational arrangement.

These needs point to different solutions:

| Need | Typical first approach |
|---|---|
| Clearer instructions or a few examples | Prompting |
| Current/private/source-backed facts | RAG or tools |
| Exact operations on external systems | Tool calling |
| Repeated task behavior at scale | Consider fine-tuning |
| On-device, offline, or controlled infrastructure | Local or self-hosted inference |

The approaches can be combined. A fine-tuned model may still use RAG, and a self-hosted model may still call tools.

---

## 2. What an SDK is

### SDK versus API

An **API** defines how software communicates with a service: endpoints, authentication, request bodies, response bodies, errors, and protocols.

An **SDK** is a language-specific library that wraps that API. It usually provides:

- client initialization;
- authentication handling;
- typed request and response objects;
- serialization and deserialization;
- synchronous and asynchronous interfaces;
- streaming helpers;
- error classes;
- automatic retry behavior for selected failures;
- pagination or file-upload helpers;
- versioned access to provider features.

The SDK does not make model output correct, authorize business actions, or replace application-level validation.

### Why use an official SDK

An official SDK can reduce boilerplate and track new API capabilities. It also makes common failures easier to handle consistently.

However, engineers should still understand the underlying HTTP and streaming behavior because:

- SDK versions can differ;
- abstractions sometimes expose only part of the API;
- debugging often requires inspecting raw status codes and request identifiers;
- streaming and timeout behavior depends on transports;
- migration may change object shapes or method names.

### Pin and observe dependencies

Production applications should treat SDK versions as dependencies, not invisible infrastructure. Good practice includes:

- pinning or constraining versions;
- reading release and migration notes;
- testing upgrades against evaluation suites;
- logging the SDK and API version where useful;
- avoiding undocumented response fields;
- isolating provider-specific code behind a small internal boundary.

---

## 3. The common model-request shape

### Core request elements

Although names differ, model requests commonly include:

- a model identifier;
- instructions or a system-level directive;
- user input or conversation content;
- multimodal parts such as text, images, audio, or files;
- generation limits;
- sampling controls where supported;
- tool definitions and tool-selection settings;
- structured-output configuration;
- streaming or background-execution options;
- metadata and safety-related identifiers.

Conceptually:

```text
Request
├── model
├── instructions
├── input / messages / contents
│   ├── role
│   └── content parts
├── tools
├── output constraints
├── generation controls
└── transport/lifecycle options
```

### Roles are not identical across providers

Providers commonly distinguish user and model/assistant turns, but system or developer instructions may be represented differently:

- as a top-level field;
- as a specially typed message;
- as configuration outside the conversation list.

Do not assume that copying a message array from one provider preserves the same instruction hierarchy in another.

### Content is often multimodal and typed

A message is not always one string. It may contain an ordered list of parts such as:

- text;
- image references or bytes;
- audio;
- documents;
- tool calls;
- tool results;
- reasoning or other provider-specific blocks;
- citations or annotations.

Code that assumes `response[0].text` will often break as soon as tools, refusals, multiple candidates, or multimodal output are introduced.

### Generation limits

Output-token limits bound how much the model may generate. They are not the same as the model's total context window.

The total context may include:

- instructions;
- conversation history;
- user content;
- retrieved documents;
- tool definitions and results;
- generated output;
- provider-specific internal or reasoning tokens.

### Sampling controls

Controls such as temperature and top-p influence token selection, but they do not create factual guarantees. Not every model or endpoint exposes the same controls, ranges, or semantics.

Provider migration should not assume that equal numeric values produce equal behavior.

---

## 4. The common model-response shape

### A response is more than text

A completed response may include:

- a unique response or message identifier;
- status and timestamps;
- one or more output items;
- text and other content blocks;
- tool-call requests;
- refusal or safety information;
- citations or annotations;
- finish or stop reasons;
- token-usage information;
- errors or incomplete-response details;
- model and service metadata.

The application should inspect types and status rather than assuming every response contains a normal text answer.

### Stop reasons

A generation can stop because it:

- completed normally;
- reached an output limit;
- requested a tool;
- encountered a safety refusal;
- matched a stop sequence;
- failed or was cancelled;
- remains queued or incomplete.

These outcomes require different handling. A length-limited response is not automatically a successful complete answer.

### Usage data

Usage objects can report input, output, total, cached, or reasoning-related tokens, depending on the provider and model. Usage is important for:

- cost monitoring;
- context budgeting;
- detecting unexpectedly large prompts;
- comparing pipeline designs;
- capacity planning.

Do not assume every provider counts or reports tokens in exactly the same way.

### Request identifiers

Provider request IDs and application correlation IDs are valuable for tracing failures. Logs should avoid exposing API keys or sensitive prompts, while preserving enough metadata to diagnose latency, retries, and provider errors.

---

## 5. Anthropic, OpenAI, and Google GenAI SDKs

### Shared mental model

All three SDK families allow an application to:

1. create a client;
2. authenticate with a key or supported cloud identity;
3. select a model;
4. provide instructions and input;
5. receive a typed response or event stream;
6. inspect text, tools, status, and usage;
7. handle errors and retries.

The concepts transfer, but the object models do not match field-for-field.

### Anthropic SDK

Anthropic's core conversational interface uses the **Messages API**. Important concepts include:

- a message request with model, messages, and an output-token limit;
- content represented as typed blocks;
- a system instruction supplied separately from ordinary user/assistant turns;
- tool-use and tool-result blocks;
- stop reasons and usage data;
- SDK helpers for synchronous and asynchronous streaming.

The streaming interface can expose text deltas as well as lifecycle and content-block events. Tool input and other block types mean that not every event is printable text.

### OpenAI SDK

OpenAI's current general model interface centers on the **Responses API**. Important concepts include:

- `input` and optional `instructions`;
- an `output` array whose items may be messages, tool calls, or other typed results;
- a convenience `output_text` property in supported SDKs;
- built-in tools, custom function calls, and MCP tools;
- structured text configuration;
- response status, usage, and incomplete details;
- server-sent streaming events such as text deltas and completion events.

Applications should not assume that the first output item is always an assistant text message because output ordering and types depend on what the model did.

### Google GenAI SDK

The Google GenAI SDK provides access to Gemini APIs. Important concepts include:

- model input represented through content and typed parts;
- user and model conversation turns;
- multimodal content within parts;
- normal generation, streaming, and realtime/live interfaces;
- candidates and associated content in generation responses;
- typed streaming events or response chunks, depending on the API used;
- configuration for tools, output formats, safety, and generation behavior.

Current Google documentation distinguishes its newer interaction-oriented interface from the older content-generation interface. The lesson is broader than one method name: verify which API surface a code example targets before mixing request or streaming patterns.

### Conceptual comparison

| Concept | Anthropic | OpenAI | Google GenAI |
|---|---|---|---|
| Primary conversational abstraction | Messages | Responses and typed output items | Interactions or content/parts, depending on API |
| Instruction placement | Separate system field | Instructions or supported message/input forms | System instruction/configuration |
| Output representation | Typed content blocks | Typed output items and content | Candidates, content/parts, or typed interaction events |
| Streaming | SSE events and SDK stream helpers | SSE typed response events | SSE/stream chunks; Live API uses a realtime connection |
| Tool use | Tool-use blocks | Function/custom and built-in tool items | Function/tool parts and API-specific events |

This table is a conceptual map, not a drop-in translation guide. Always consult the documentation matching the installed SDK version.

---

## 6. Streaming

### What streaming changes

Without streaming, the client waits for a completed response object. With streaming, the server sends incremental events while work is in progress.

Streaming can improve **time to first visible output**, but it does not necessarily reduce total generation time.

```text
Non-streaming:
request ───────── wait ─────────> complete response

Streaming:
request ──> event ─> delta ─> delta ─> done
```

### Server-Sent Events

Many HTTP streaming APIs use **Server-Sent Events (SSE)**. The connection remains open while the server sends a sequence of events.

Events may describe:

- response creation;
- content-block creation;
- text deltas;
- tool-input deltas;
- completed content;
- usage updates;
- errors;
- final response completion.

The client must process events in order and handle types it recognizes.

### Deltas are not complete objects

A text delta is only a new fragment. A streamed JSON or tool argument may be syntactically incomplete until later events arrive.

Therefore:

- accumulate fragments using the SDK's event model;
- do not validate partial JSON as if it were final;
- do not execute a tool from incomplete arguments;
- inspect the final stop status;
- preserve the final assembled response for logging and evaluation where appropriate.

### Streaming errors

An ordinary HTTP error may occur before streaming begins. A failure can also arrive after a successful connection and partial output.

The application must decide:

- whether partial text is shown or discarded;
- whether a request is safe to retry;
- how duplicate output is prevented;
- how cancellation is propagated;
- whether the UI marks an interrupted answer as incomplete.

### Backpressure and disconnects

If the producer sends events faster than the client can process them, buffering grows. Slow consumers need backpressure-aware handling.

If the user disconnects, the application should cancel upstream work when supported instead of wasting compute and cost.

### Streaming versus realtime

One-way response streaming is different from a realtime bidirectional session.

- **SSE streaming:** one request produces incremental server events.
- **Realtime/WebSocket-style interaction:** client and server can exchange incremental audio, text, or events over a persistent connection.

Use realtime protocols for low-latency, bidirectional experiences such as voice, not merely because text should appear token by token.

---

## 7. Reliable SDK integration

### Authentication

API keys and credentials should be stored server-side in a secret manager or protected environment—not embedded in client applications, source control, screenshots, or logs.

### Timeouts

Use explicit timeouts appropriate to the operation:

- connection timeout;
- first-byte or first-event timeout;
- read timeout;
- total deadline;
- separate longer deadlines for batch or background work.

An unlimited wait is not a reliability strategy.

### Retries

Retries can help with transient network errors, rate limits, or selected server failures. Use:

- exponential backoff;
- jitter;
- a maximum attempt or time budget;
- provider retry guidance;
- idempotency protections where supported.

Do not retry every failure. Invalid requests, authentication errors, and policy refusals usually require a change rather than repetition.

### Rate limits

Rate limits may be expressed through requests, tokens, concurrent work, or other provider-specific units. Applications should queue, shed load, or degrade gracefully instead of creating synchronized retry storms.

### Validation

Even typed SDK responses contain probabilistic model output. Validate:

- required structured fields;
- enumerated values;
- identifiers and ranges;
- tool arguments;
- business invariants;
- permissions before side effects.

### Provider abstraction

A thin internal interface can reduce vendor coupling for shared tasks such as basic text generation, but the lowest common denominator can hide:

- provider-specific tools;
- caching controls;
- distinct reasoning or safety settings;
- event types;
- multimodal features;
- background execution;
- response metadata.

A good abstraction normalizes stable application needs while allowing explicit provider-specific capabilities.

---

## 8. Fine-tuning fundamentals

### What fine-tuning changes

Fine-tuning continues training a pretrained model on a task-specific dataset. It changes model parameters so that desired behaviors become more likely for inputs similar to the training distribution.

Fine-tuning can adapt:

- response style and tone;
- classification behavior;
- domain-specific terminology;
- repeated output structure;
- tool-selection patterns;
- task-specific transformations;
- compact task instructions demonstrated across many examples.

### Fine-tuning is not a database

Model weights are a poor replacement for a source of frequently changing or auditable facts. Fine-tuned knowledge is:

- difficult to update surgically;
- difficult to cite;
- not guaranteed to be recalled exactly;
- capable of becoming stale;
- mixed probabilistically with prior model behavior.

Use RAG or tools for current facts, exact records, private documents, and provenance.

### Supervised fine-tuning

In supervised fine-tuning, training examples demonstrate desired input–output behavior.

Conceptually:

```text
input:  representative user request and context
target: ideal assistant response or action pattern
```

The model learns statistical patterns across examples. It does not store the dataset as an exact lookup table.

### Dataset quality dominates quantity

Training data should be:

- representative of production inputs;
- correct and consistently labeled;
- diverse across relevant cases;
- balanced across important classes and behaviors;
- free from secrets and unauthorized data;
- separated from evaluation data;
- aligned with the desired prompt and response format.

Inconsistent examples teach inconsistent behavior more efficiently.

---

## 9. Prompting, RAG, tools, or fine-tuning?

### Start with prompting

Prompting is usually the cheapest and fastest first intervention when:

- instructions fit comfortably in context;
- a few examples establish the behavior;
- the task changes frequently;
- the base model already has the capability;
- request volume does not justify training operations.

Prompting remains transparent and easy to revise.

### Use RAG for knowledge access

RAG is usually appropriate when the answer depends on:

- current information;
- private documents;
- a large changing corpus;
- citations and provenance;
- user- or tenant-specific knowledge;
- removal or correction of individual sources.

RAG changes context, not model weights.

### Use tools for exact state and actions

Tools are appropriate when the system must:

- retrieve a precise account or order record;
- perform calculations;
- query a transactional database;
- send a message or update a system;
- access live external state;
- perform a deterministic operation.

The model chooses or fills an interface; application code validates and executes it.

### Consider fine-tuning for repeated behavior

Fine-tuning becomes a serious candidate when:

- a stable task has many high-quality examples;
- prompting has reached a measured quality ceiling;
- the desired behavior repeats at substantial volume;
- prompts contain long demonstrations that could be learned;
- consistent style, classification, or formatting is difficult with prompting alone;
- a smaller adapted model can meet quality targets more economically;
- latency or token savings justify training and maintenance.

### Combine techniques

Examples:

- fine-tune a model to select tools reliably, then use tools for live data;
- fine-tune a response style, then use RAG for current facts;
- use prompting for instructions, RAG for evidence, and structured output for validation;
- serve a LoRA adapter on a self-hosted base model while retrieving from a private index.

Fine-tuning does not eliminate the need for good prompts, retrieval, tools, or validation.

### Decision table

| Question | Prompting | RAG | Tools | Fine-tuning |
|---|---:|---:|---:|---:|
| Changes behavior without training | Yes | Indirectly | Indirectly | No |
| Supplies current/private facts | Only if included | Yes | Yes | Poor fit |
| Provides source provenance | Limited | Yes | Yes | No |
| Performs external actions | No | No | Yes | No |
| Changes model weights | No | No | No | Yes |
| Easy to update one fact | Yes, for tiny context | Yes | Yes | No |
| Requires a training dataset | No | No | No | Yes |

---

## 10. When not to fine-tune

Do not begin with fine-tuning when:

- the real problem is missing or stale knowledge;
- the prompt has not been improved and evaluated;
- only a few unreviewed examples exist;
- requirements change weekly;
- the base model lacks a required tool or modality;
- the task requires exact deterministic rules;
- failures come from parsing, retrieval, or authorization;
- there is no stable evaluation set;
- the organization cannot maintain datasets, training jobs, versions, and rollback.

Fine-tuning a pipeline failure often makes the failure harder to inspect.

---

## 11. LoRA at a high level

### Full fine-tuning

Full fine-tuning updates many or all parameters of the base model. For large models, this can require substantial accelerator memory, storage, training compute, and operational effort.

### Low-Rank Adaptation

**LoRA** stands for **Low-Rank Adaptation**. At a high level, it:

1. keeps the original pretrained weight matrices frozen;
2. introduces small trainable low-rank matrices into selected layers;
3. learns an update represented by those smaller matrices;
4. applies that update alongside, or merges it with, the original weights for inference.

For a frozen weight matrix \(W\), the adapted transformation is often described conceptually as:

\[
W' = W + \Delta W
\]

with the update factorized as:

\[
\Delta W = BA
\]

where \(A\) and \(B\) have a much smaller internal rank than the full weight matrix.

### Why low rank helps

Instead of training every element of a large matrix, LoRA trains a much smaller parameter set. This can reduce:

- trainable parameter count;
- optimizer-state memory;
- storage per task;
- the cost of maintaining several adaptations of one base model.

It does not make training free. Activations, data preparation, evaluation, GPU memory, and serving design still matter.

### Adapters and base models

A LoRA adapter depends on the exact compatible base model and targeted architecture. The adapter alone is not a complete model.

Operational questions include:

- whether adapters are merged into model weights;
- whether they are loaded dynamically;
- how multiple adapters are versioned;
- whether batching works across adapters;
- what licensing applies to the base and training data;
- whether adapter switching affects latency or memory.

### LoRA is not automatically equal to full fine-tuning

LoRA can be highly effective, but results depend on:

- task complexity;
- data quality and quantity;
- selected layers;
- rank and scaling settings;
- optimization choices;
- base-model capability;
- evaluation distribution.

The correct comparison is empirical performance under the actual cost and deployment constraints.

---

## 12. Fine-tuning evaluation and lifecycle

### Establish a baseline first

Before training, record the best practical baseline using prompting, retrieval, tools, or a stronger base model. Otherwise, there is no evidence that fine-tuning caused an improvement.

### Split the data

Keep training, validation, and test examples separate. Near-duplicates and examples derived from the same source can leak across splits and exaggerate performance.

### Evaluate important slices

Measure performance across:

- common and rare inputs;
- difficult edge cases;
- each class or output type;
- languages and regions;
- short and long inputs;
- adversarial and safety cases;
- out-of-distribution requests;
- cases where the model should abstain.

### Watch for regressions

An adaptation can improve one target while damaging:

- general instruction following;
- safety behavior;
- factual accuracy;
- output diversity;
- multilingual performance;
- tool selection;
- behavior outside the training distribution.

### Version everything

Track:

- base-model identifier and revision;
- dataset version and provenance;
- preprocessing code;
- prompt format;
- hyperparameters and random seeds;
- adapter or checkpoint artifacts;
- evaluation results;
- deployment configuration;
- rollback target.

Fine-tuning is a lifecycle, not a one-time file creation.

---

## 13. Local models and self-hosting

### Terms that are often confused

**Local model** may mean a model running on a developer's laptop or workstation.

**Self-hosted model** usually means the organization operates the inference service on infrastructure it controls, which may be on-premises or in a cloud account.

**Open-weight model** means model weights are available under a license. Open weights do not automatically mean open source, unrestricted commercial use, or permission to use every training dataset.

### What self-hosting gives you

Potential benefits include:

- control over network and data paths;
- offline or edge operation;
- deployment in a specific region or environment;
- model and adapter selection;
- low network latency near the application;
- predictable capacity for stable workloads;
- access to lower-level inference settings;
- customization of quantization and serving.

### What self-hosting makes you responsible for

Responsibilities include:

- obtaining and scheduling accelerators;
- model downloads and artifact security;
- serving software and drivers;
- batching and memory management;
- autoscaling and capacity planning;
- monitoring and alerting;
- authentication and network security;
- rate limiting and abuse prevention;
- model upgrades and vulnerability response;
- safety controls;
- availability, backups, and disaster recovery;
- license compliance;
- measuring quality after quantization or conversion.

“No per-token API bill” does not mean “free.”

### Total cost of ownership

Compare total cost, including:

- hardware purchase or rental;
- idle capacity;
- energy and cooling;
- engineering and on-call time;
- storage and network transfer;
- observability;
- redundancy;
- training and adapter operations;
- opportunity cost;
- cost of degraded quality or reliability.

A hosted API converts much of this into a service price. Self-hosting internalizes it.

---

## 14. Ollama basics

### What Ollama is for

Ollama provides a convenient way to download, configure, and run supported models locally. It is useful for:

- learning and experimentation;
- local application prototypes;
- offline or private single-machine workflows;
- testing model sizes and quantizations;
- exposing a local HTTP API to applications.

### Core concepts

Ollama workflows commonly involve:

- pulling or creating a model definition;
- loading model weights into available local compute;
- sending generate or chat requests;
- passing a message history for conversational behavior;
- receiving streamed output;
- configuring model/runtime parameters;
- using tool calling or embeddings when supported by the chosen model and interface.

The REST chat interface streams by default; SDK defaults may differ. This is a good example of why transport behavior must be checked rather than assumed.

### Model configuration is not fine-tuning

A model configuration or template may set:

- a base model;
- system text;
- prompt templates;
- runtime parameters;
- an adapter reference.

Changing a template or runtime parameter does not itself train the base model.

### Local hardware constraints

Whether a model runs acceptably depends on:

- parameter count;
- weight precision or quantization;
- available RAM or VRAM;
- context length;
- prompt and batch size;
- CPU/GPU architecture;
- memory bandwidth;
- desired tokens per second.

A model that fits in memory may still be too slow for the intended experience.

---

## 15. vLLM basics

### What vLLM is for

vLLM is an inference and serving engine designed for efficient model execution, especially for server workloads. It can expose an OpenAI-compatible HTTP server for supported endpoints and models.

It is more naturally associated with service operation and throughput than with one-click desktop model management.

### Important serving concepts

vLLM deployments involve concepts such as:

- model loading across one or more accelerators;
- efficient attention-memory management;
- continuous or dynamic batching;
- request scheduling;
- tensor or pipeline parallelism where appropriate;
- quantization support;
- streaming output;
- chat templates;
- OpenAI-compatible endpoints;
- metrics and production deployment controls.

### Continuous batching

Users submit requests at different times and generate different numbers of tokens. Static batches waste capacity when short requests finish before long ones.

Continuous batching allows the scheduler to add and remove work as generation progresses, improving accelerator utilization and throughput.

### OpenAI-compatible does not mean identical

Compatibility can make client migration easier, but it does not guarantee identical:

- endpoint coverage;
- model behavior;
- tokenization;
- tool-call quality;
- structured-output behavior;
- parameter support;
- error semantics;
- safety systems;
- usage accounting.

Some server-specific parameters or features may require extra request fields.

### Chat templates

Instruction-tuned models expect conversations to be serialized into a particular token format. A wrong or missing chat template can severely reduce quality even though the HTTP request succeeds.

The serving layer must apply the template expected by the model.

### Security boundary

An inference server should not be exposed to untrusted networks without deliberate controls. Production security may require:

- a reverse proxy or API gateway;
- authentication and authorization;
- TLS;
- request-size and rate limits;
- network isolation;
- endpoint auditing;
- safe model and code-loading policies;
- logging and secret redaction.

An inference engine's built-in API-key option is not automatically a complete security architecture.

---

## 16. Ollama versus vLLM

| Dimension | Ollama | vLLM |
|---|---|---|
| Typical starting point | Local development and simple model operation | High-throughput inference service |
| User experience | Convenient local model lifecycle and API | Serving engine with production-oriented performance controls |
| Hardware scope | Commonly a workstation or single host | Often GPU servers and multi-accelerator deployments |
| Batching focus | Simpler local use | Strong emphasis on scheduling and throughput |
| API style | Native local API plus supported compatibility options | OpenAI-compatible server plus engine APIs |
| Best fit | Learning, prototypes, private local workflows | Shared services and performance-sensitive deployment |

These are typical orientations, not absolute rules. Evaluate the current feature set, hardware support, and operational requirements.

---

## 17. When self-hosting makes sense

Self-hosting may make sense when several of these are true:

- data must remain in a controlled network or device;
- the workload must operate without internet access;
- a suitable open-weight model meets measured quality requirements;
- request volume is high and predictable enough to utilize hardware efficiently;
- the organization already operates accelerator infrastructure;
- low network latency or edge deployment is essential;
- custom adapters or model internals are required;
- provider availability, geography, or feature constraints are unacceptable;
- the team can own security, reliability, and model operations.

Self-hosting may not make sense when:

- traffic is low, bursty, or unpredictable;
- the team lacks inference-operations expertise;
- top hosted-model quality is required;
- hardware would remain idle;
- rapid model improvements matter more than control;
- compliance can be satisfied by an appropriate managed service;
- engineering time is more expensive than the expected API usage.

The decision should follow a benchmark and total-cost analysis, not a preference for “local” or “cloud.”

---

## 18. Local-model evaluation

### Quality

Evaluate the exact served artifact, including:

- model revision;
- quantization;
- chat template;
- system prompt;
- sampling settings;
- context length;
- adapter;
- tool and structured-output configuration.

Do not rely only on the base model's published benchmark.

### Performance

Measure:

- time to first token;
- inter-token latency;
- total latency;
- tokens per second;
- throughput under concurrency;
- queue time;
- memory utilization;
- failure and out-of-memory rates;
- performance at realistic input and output lengths.

### Load behavior

A single fast demo does not establish production capacity. Test:

- concurrent users;
- long prompts;
- mixed short and long generations;
- cancellation;
- overload behavior;
- autoscaling or restart time;
- fairness between requests.

### Safety and operations

Hosted providers may supply safety tooling and abuse monitoring that a self-hosted deployment must recreate where required. Evaluate both model behavior and system controls.

---

## 19. Common misconceptions

### “All provider SDKs are basically the same”

They share high-level concepts, but instruction placement, content types, event schemas, tool protocols, errors, and state management differ.

### “Streaming makes the model generate faster”

Streaming usually improves perceived responsiveness by exposing partial output. It does not guarantee lower total completion time.

### “A streamed text fragment is a complete response”

False. It may be one delta among many, and tool arguments or structured data may still be incomplete.

### “Fine-tuning uploads facts into a reliable database”

False. Fine-tuning changes probabilistic behavior. Use retrieval or tools for updateable, exact, and source-backed facts.

### “Fine-tuning replaces prompt engineering”

False. Training examples encode an implicit prompt and output contract, while inference still needs clear input formatting and instructions.

### “LoRA is a different base model”

False. A LoRA adapter represents a learned update that depends on a compatible base model.

### “If weights are downloadable, the model is unrestricted”

False. Model, dataset, and commercial-use licenses must be checked separately.

### “Local means private”

Not automatically. Applications may still log prompts, call external tools, download remote artifacts, expose network ports, or leak data through insecure telemetry.

### “Self-hosting is cheaper because there is no API bill”

False. Hardware, idle capacity, engineering, reliability, and security are part of total cost.

### “OpenAI-compatible means behaviorally identical”

False. Protocol compatibility does not make models, features, errors, tokenization, or output quality identical.

---

## 20. A practical decision sequence

For a new AI requirement:

1. Define the task and a representative evaluation set.
2. Establish a prompt-only baseline using a suitable model.
3. Add tools if exact external state or actions are required.
4. Add RAG if the task depends on current, private, or citable knowledge.
5. Analyze remaining failures by category.
6. Consider fine-tuning only for stable, repeated behavior with sufficient high-quality examples.
7. Compare full fine-tuning and parameter-efficient methods such as LoRA if training is justified.
8. Benchmark hosted and self-hosted serving using the exact model artifact and expected load.
9. Compare total quality, latency, cost, privacy, reliability, and operational burden.
10. Version, monitor, evaluate, and retain a rollback path.

This sequence prevents fine-tuning or self-hosting from becoming a solution in search of a problem.

---

## 21. Knowledge check

You should now be able to answer these questions in your own words:

1. What does an SDK add on top of an HTTP API?
2. Which concepts are common to Anthropic, OpenAI, and Google GenAI requests?
3. Why can message-role translation between providers be unsafe?
4. Why should response content be inspected by type rather than assumed to be text?
5. What is a streaming delta, and why should partial JSON not be executed?
6. How do SSE streaming and a realtime bidirectional connection differ?
7. Which errors are reasonable to retry, and which require a request change?
8. When does a provider-neutral abstraction become harmful?
9. What changes during fine-tuning?
10. Why is fine-tuning usually a poor solution for current facts?
11. When should prompting be tried before fine-tuning?
12. When is RAG more appropriate than fine-tuning?
13. What does LoRA freeze, and what does it train?
14. Why is a LoRA adapter not a complete standalone model?
15. What is the difference between a local model, a self-hosted service, and an open-weight model?
16. What kinds of workflows suit Ollama?
17. What kinds of workloads suit vLLM?
18. Why does continuous batching improve serving throughput?
19. Why does OpenAI API compatibility not guarantee identical behavior?
20. Which factors belong in a self-hosting total-cost analysis?

# P4-06 — SDKs, Local Models, and When to Fine-Tune is completed with the provided readme notes
