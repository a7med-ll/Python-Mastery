# P4-03 — Structured Output and Tool Calling

## Purpose

This study task builds a conceptual model of how language-model output can be constrained, validated, and connected to external tools. It is deliberately **not a build project**: the evidence is an explanation, in your own words, of the ideas below.

## Learning outcomes

By the end, you should be able to explain:

- why free-form text is difficult for software to consume reliably;
- the difference between plain text, valid JSON, and schema-conforming structured output;
- what JSON mode guarantees and what it does not guarantee;
- how JSON Schema describes an output contract;
- how function calling and tool calling work conceptually;
- why the model requests a tool but does not execute application code itself;
- how an application completes the tool-calling loop;
- how tool choice differs from tool execution;
- how Pydantic parses and validates LLM-generated data;
- why validation failures must be handled explicitly;
- why structured output does not guarantee factual correctness or safe behavior.

---

## 1. Why structured output matters

### Free-form text versus machine-readable data

Language models naturally generate text. Text is convenient for people, but software usually needs predictable fields, types, and allowed values.

Suppose an application asks a model to extract an event. A free-form response might be:

```text
The meeting is with Ahmed next Tuesday at 10 in the morning.
```

A program now has to guess where the name, date, and time are. The model might change the sentence structure in the next response.

A structured representation is easier to consume:

```json
{
  "title": "Meeting with Ahmed",
  "date": "2026-09-22",
  "time": "10:00"
}
```

Structured output creates a clearer contract between a probabilistic model and deterministic application code.

### Three levels of output control

| Output style | Main guarantee | What can still go wrong |
| --- | --- | --- |
| Prompted text | The prompt asks for a format | The model may ignore or vary the format |
| JSON mode | The response is valid JSON | Fields, types, and allowed values may be wrong |
| Schema-constrained output | The response conforms to a supported schema | Values may still be false, unsafe, or unsuitable |

These levels should not be treated as equivalent. A response can be valid JSON while violating the application's intended structure.

Example of valid JSON that may still be structurally wrong:

```json
{
  "meeting": "Ahmed",
  "when": 10
}
```

The JSON parser accepts it, but an application expecting `title`, `date`, and `time` cannot use it safely without additional handling.

### Syntax, structure, and meaning

Structured LLM output has three separate correctness layers:

1. **Syntax validity:** Can a JSON parser read the response?
2. **Schema validity:** Does it contain the required fields, types, and allowed values?
3. **Semantic validity:** Are the values true, sensible, authorized, and appropriate for the real task?

JSON mode mainly addresses the first layer. Schema-constrained generation addresses the first two. Application logic, trusted data, authorization, and verification are still needed for the third.

> Memory hook: parseable does not mean usable, and usable does not mean true.

---

## 2. JSON fundamentals for LLM output

### What JSON is

JSON is a text format for representing values with a small set of data types:

- object;
- array;
- string;
- number;
- boolean;
- `null`.

Objects contain key–value pairs, while arrays contain ordered values.

```json
{
  "customer": "Aisha",
  "priority": "high",
  "tags": ["billing", "refund"],
  "requires_follow_up": true,
  "amount": 125.50,
  "reference": null
}
```

JSON does not have native date, datetime, decimal, UUID, or enum types. These are normally represented using strings or numbers and then interpreted and validated by application code.

### Common JSON mistakes

- using single quotes instead of double quotes;
- leaving a trailing comma;
- returning explanatory text before or after the JSON;
- using an unquoted key;
- producing a number where a string is required;
- confusing missing fields with fields whose value is `null`;
- returning `NaN` or another value not supported by standard JSON;
- embedding comments, which standard JSON does not support.

### Missing, null, and empty are different

These states have different meanings:

```json
{}
```

The field is missing.

```json
{"email": null}
```

The field is present but has no value.

```json
{"email": ""}
```

The field is present and contains an empty string.

A schema and a validator must define which states are acceptable. Treating all three as identical can create subtle application bugs.

---

## 3. JSON mode

### What JSON mode does

JSON mode instructs a supported model to return a syntactically valid JSON object. This is stronger than merely writing “return JSON” in the prompt because the API participates in constraining the generated format.

JSON mode is useful when:

- the application only requires a generic JSON object;
- the schema changes dynamically and is validated elsewhere;
- the selected model or API does not support schema-constrained output;
- compatibility with an older integration matters.

### What JSON mode does not do

JSON mode does not by itself guarantee:

- the required keys are present;
- values have the expected types;
- strings follow a date or identifier format;
- enum values belong to an allowed set;
- arrays contain the correct item type;
- additional unwanted fields are absent;
- a value is factually correct;
- the requested operation is safe or authorized.

Therefore, JSON-mode output must still be parsed and validated.

### JSON mode versus schema-constrained output

If the API and model support a JSON Schema contract, schema-constrained output is normally preferable when the application knows the required structure in advance. It reduces formatting retries and moves more structural guarantees into generation.

JSON mode remains a valid compatibility tool, but it should not be described as “guaranteed structured data” without stating that its main guarantee is valid JSON syntax.

---

## 4. JSON Schema and structured output

### What a schema describes

JSON Schema can describe the shape of a JSON value, including:

- object properties;
- required fields;
- data types;
- arrays and their item types;
- enumerated values;
- nested objects;
- whether unknown properties are allowed;
- some string and numeric constraints.

Conceptual event schema:

```json
{
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "date": {"type": "string"},
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"]
    }
  },
  "required": ["title", "date", "priority"],
  "additionalProperties": false
}
```

This contract says which fields must exist, which types they use, which priority values are accepted, and whether extra fields are permitted.

### Strictness

A strict schema reduces ambiguity. Requiring fields and rejecting undeclared properties makes downstream behavior easier to reason about.

Strictness must still match the real domain. Making every field mandatory can force the model to invent a value when the input does not contain it. A better schema may allow `null`, include an explicit `unknown` state, or return a separate list of missing fields.

### Schema design principles

A useful schema should:

- represent the application's actual data model;
- use descriptive property names;
- make required and optional fields intentional;
- use enums for genuinely closed sets;
- distinguish unknown values from empty values;
- reject unneeded additional properties;
- avoid deeply nested structures unless the domain requires them;
- include descriptions that clarify ambiguous fields;
- stay within the subset supported by the selected API and model.

### Structured output is not factual verification

A model can return this perfectly schema-valid object:

```json
{
  "capital": "Sydney",
  "country": "Australia",
  "confidence": 0.99
}
```

The structure is correct, but the claim is false. Schema adherence prevents a class of integration errors; it does not turn generation into a trusted database query.

---

## 5. Function calling and tool calling

### What a tool is

A tool is a capability that the application makes available to the model. It may:

- call application code;
- query a database;
- retrieve a file;
- search the web;
- calculate a value;
- send a message;
- update an external service.

The application describes each tool using a name, purpose, and input schema. The model can then decide that the task requires that tool and generate a structured call.

### Function calling versus tool calling

**Function calling** traditionally refers to the model producing structured arguments for a developer-defined function. **Tool calling** is the broader concept: function tools, platform-provided tools, remote services, search, file access, computer interaction, or other capabilities may all be exposed as tools.

The terms are often used interchangeably when the only available tools are functions. The durable idea is that the model selects a capability and proposes structured inputs; the surrounding application performs the real operation.

### A tool definition is an interface contract

A conceptual weather tool might be described as:

```json
{
  "name": "get_weather",
  "description": "Return the current weather for a city.",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {"type": "string"},
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"]
      }
    },
    "required": ["city", "unit"],
    "additionalProperties": false
  }
}
```

The description helps the model decide **when** to use the tool. The schema constrains **what arguments** it should supply. Neither one implements the function or authorizes its effects.

### The model does not execute the function

When the model emits a tool call, it has produced a structured request such as:

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Dubai",
    "unit": "celsius"
  }
}
```

The application must decide whether the call is allowed, validate the arguments, execute the function, capture the result, and return that result to the model. The model itself did not access a weather service merely by generating the JSON.

> Memory hook: the model proposes; the application validates and executes.

---

## 6. The tool-calling loop

### Complete lifecycle

A normal tool interaction contains the following steps:

1. The application sends the user's request and available tool definitions to the model.
2. The model decides whether to answer directly or request one or more tools.
3. The model returns a tool name, structured arguments, and a call identifier.
4. The application parses and validates the request.
5. The application checks authentication, authorization, policy, and current state.
6. The application executes the permitted tool.
7. The application sends the tool result back with the matching call identifier.
8. The model uses the result to produce an answer or request another tool.
9. The application enforces stopping conditions such as call limits, timeouts, or completion rules.

Skipping steps creates common failures. For example, if a result is returned without its call identifier, the model may not know which request it answers. If authorization happens only in the prompt, a generated call can receive more power than the user actually has.

### Tool choice

Applications can commonly configure tool selection in modes such as:

- **none:** the model must not call a tool;
- **auto:** the model may answer directly or select a tool;
- **required:** the model must call at least one allowed tool;
- **specific tool:** the application forces one named tool;
- **allowed subset:** the application exposes only a restricted group for the current step.

Exact option names differ by API. Tool choice controls what the model may propose; server-side authorization still controls what the application may execute.

### Multiple and parallel calls

A model may request more than one tool. Independent calls can sometimes run in parallel, while dependent calls must run in sequence.

For example, looking up weather for three unrelated cities can be parallel. Looking up a customer, then using the returned customer ID to fetch invoices, is sequential.

Applications should not assume that every response contains exactly one text message or one tool call. They must inspect response item types and handle all supported cases.

### Tool errors

Tools can fail because of invalid arguments, network problems, missing records, expired credentials, rate limits, timeouts, or denied authorization.

A safe error result should be structured and should distinguish:

- retryable failures;
- invalid user input;
- unavailable data;
- authorization failure;
- permanent tool failure.

Do not convert every error into invented data. The model should receive enough information to explain the failure, correct a safe argument, choose another permitted method, or ask the user for missing input.

---

## 7. Pydantic-validated LLM output

### What Pydantic contributes

Pydantic is a Python data-validation library. A Pydantic model declares fields, Python types, defaults, constraints, and validation rules. It can also generate JSON Schema from that model.

Conceptual model:

```python
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CalendarEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1)
    event_date: date
    priority: Literal["low", "medium", "high"]
```

This model says:

- `title` must be a non-empty string;
- `event_date` must parse as a date;
- `priority` must be one of three values;
- undeclared fields are rejected.

### Generation and validation are separate steps

Even when a provider constrains model output using a schema, the application should understand the separate responsibilities:

1. The schema guides or constrains generation.
2. The SDK receives the model response.
3. Pydantic parses the data into Python types.
4. Pydantic applies field and model validators.
5. Application rules decide whether the validated object is acceptable for use.

Pydantic may convert a date string into a Python `date`, reject an invalid enum, forbid an unexpected field, or enforce relationships between fields. It cannot independently determine whether an extracted date was actually present in the source or whether a requested action is authorized.

### Parsing versus validation

Parsing converts serialized data into application types. Validation checks whether the data satisfies declared rules. These often happen together, but the concepts are different.

For example, Pydantic may parse `"2026-09-15"` into a `date`. It should reject `"not-a-date"`. Both values were valid JSON strings, which shows why JSON validity alone is insufficient.

### Validation errors are normal control flow

Model output, user input, schemas, and external data can disagree. Applications must expect validation errors rather than treating them as impossible.

Possible responses include:

- return a clear error to the caller;
- ask the user for missing information;
- retry with the validation errors as corrective feedback;
- use a safe default when the domain explicitly permits it;
- route the case for human review.

Retries must be bounded. Repeating indefinitely increases cost and latency and may never repair a schema or input that is fundamentally inconsistent.

### Validators should enforce domain rules

Types are only the beginning. Domain validation may need to check that:

- an end date is not before a start date;
- a percentage is between 0 and 100;
- exactly one of two alternative fields is present;
- an identifier exists in the application's database;
- a requested transition is allowed from the current state.

The first three can often be checked by Pydantic. Database existence, permissions, and current workflow state normally require application services outside the model.

---

## 8. Structured responses versus tool arguments

### Two different goals

Structured output and tool calling both use schemas, but they solve different problems.

| Mechanism | Primary purpose | Consumer |
| --- | --- | --- |
| Structured response | Return predictable data as the model's answer | Application or user interface |
| Tool call | Request that an external capability be invoked | Tool executor or orchestration layer |

Use a structured response when the desired result is data: an extracted record, classification, plan, or UI object.

Use a tool call when the task requires an external operation or information the model does not possess: querying a live system, performing a calculation, retrieving a record, or causing an authorized change.

### They can be combined

An application may let the model call a search tool, receive results, and then return a schema-conforming summary. In that flow:

- the tool schema validates the search request;
- the tool result supplies external evidence;
- the response schema validates the final answer structure.

Each boundary has its own validation and error handling. A valid tool call does not imply a successful tool result, and a valid final structure does not prove the summary is grounded in the result.

---

## 9. Reliability and security boundaries

### Never execute unvalidated arguments

Tool arguments are model-generated input. They must be treated as untrusted even when they conform to a schema.

Before execution, the application should verify:

- the tool is allowed for this request;
- the authenticated user has permission;
- identifiers belong to resources the user may access;
- paths, URLs, queries, and commands are safe;
- numerical limits and business constraints are respected;
- consequential or irreversible actions have the required confirmation;
- duplicate requests will not repeat an unsafe side effect.

### Schema validation is not authorization

This object may be perfectly schema-valid:

```json
{
  "account_id": "another-user-account",
  "amount": 1000000
}
```

Validation can confirm that `account_id` is a string and `amount` is a number. Only the application can decide whether the current user owns that account and is permitted to perform that operation.

### Tool descriptions are not security controls

A description such as “use this tool only for administrators” may guide model behavior, but it does not authenticate an administrator. Access control must be enforced in deterministic code at execution time.

### Prompt injection and tool calling

Untrusted webpages, emails, files, or tool results may contain instructions attempting to trigger another tool or reveal data. Their text does not grant authority.

A safe tool system combines:

- trusted instruction hierarchy;
- least-privilege tool exposure;
- narrow schemas;
- server-side authentication and authorization;
- validation and sanitization;
- user confirmation for consequential actions;
- timeouts and call limits;
- audit logs and monitoring;
- safe error handling;
- adversarial evaluation.

---

## 10. Common misconceptions

### “Valid JSON means the output is correct”

False. It only means the syntax is parseable. The structure may be wrong, and the content may be false.

### “Structured output eliminates hallucinations”

False. A model can place a hallucinated value inside the correct field and type.

### “The model called my function”

Usually incomplete. The model generated a request to call the function. The application decided whether and how to execute it.

### “Pydantic makes LLM output trustworthy”

False. Pydantic enforces declared structural and domain rules. Trust also requires evidence, authorization, business logic, and verification.

### “If the schema is strict, every field should be required”

Not always. If information may genuinely be unavailable, requiring a fabricated value is worse than representing `null`, `unknown`, or a missing-information state intentionally.

### “A tool schema prevents dangerous actions”

False. It limits argument shape. The executor must enforce permissions, safe ranges, allowed resources, confirmation, and idempotency.

### “A retry always fixes invalid output”

False. The source may lack the value, the schema may be contradictory, or the model may not support the requested constraint. Retries need limits and a fallback path.

---

## 11. Evaluating structured-output and tool systems

### Structured-output evaluation

Test more than whether one response looks correct. A representative evaluation set should include:

- complete inputs;
- missing fields;
- ambiguous dates and numbers;
- invalid enum values;
- unexpected extra information;
- nested records and empty arrays;
- multilingual or unusually formatted text;
- refusals and incomplete model responses;
- values that are schema-valid but factually wrong.

Useful metrics include JSON parse rate, schema-validation rate, field accuracy, extraction accuracy, missing-value behavior, retry rate, latency, and cost.

### Tool-calling evaluation

Test whether the system:

- selects the correct tool;
- avoids a tool when none is needed;
- supplies correct arguments;
- handles multiple and dependent calls;
- matches tool results to call identifiers;
- responds safely to failures and timeouts;
- respects authentication and authorization;
- refuses or confirms consequential actions correctly;
- stops within the allowed call budget;
- remains safe when tool results contain prompt injection.

### End-to-end correctness

The complete system is correct only when all relevant layers succeed:

1. the model interprets the task correctly;
2. the selected output or tool schema matches the task;
3. generated data validates;
4. external facts are grounded;
5. authorization and policy checks pass;
6. the tool executes successfully;
7. the final response accurately reflects the result.

A green check at one layer does not prove that the other layers succeeded.

# P4-03 — Structured Output and Tool Calling is completed with the provided readme notes
