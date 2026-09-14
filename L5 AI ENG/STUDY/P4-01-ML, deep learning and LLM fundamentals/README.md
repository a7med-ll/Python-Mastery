# P4-01 — ML, Deep Learning, and LLM Fundamentals

## Purpose

This study task builds a conceptual model of how modern language models learn and generate text. It is deliberately **not a build project**: the evidence is an explanation, in your own words, of the ideas below.

## Learning outcomes

By the end, you should be able to explain:

- supervised and unsupervised learning;
- training versus inference;
- underfitting, overfitting, and generalization;
- what a neural network learns;
- why transformers use attention;
- tokens and context windows;
- autoregressive generation;
- temperature and top-p sampling;
- why hallucination is a structural risk, not just a random software bug.

---

## 1. Machine-learning fundamentals

### What machine learning is

Traditional programming gives a computer explicit rules. Machine learning instead gives an algorithm examples and an objective. Training adjusts model parameters so that its predictions reduce an error measure called a **loss**. The resulting model is a learned statistical mapping from inputs to outputs.

### Supervised versus unsupervised learning

| Type | Training signal | Goal | Examples |
| --- | --- | --- | --- |
| Supervised learning | Each example has a target label or value | Learn a mapping from input to known target | spam classification, price prediction |
| Unsupervised learning | No target label is supplied | Discover structure or useful representations | clustering, dimensionality reduction |

Self-supervised learning is especially important for LLMs. The labels are created from the data itself: given earlier tokens, predict a token that actually occurred next. It resembles supervised learning because there is a target, but humans did not manually label every example.

### Training versus inference

**Training** is the learning phase. The model processes many examples, computes loss, and updates its parameters. It is expensive and changes the model.

**Inference** is the use phase. The parameters are normally frozen; the model applies what it learned to a new input. For an autoregressive LLM, inference repeatedly predicts and selects one new token at a time.

> Memory hook: training changes the model; inference uses the model.

### Underfitting, overfitting, and generalization

- **Underfitting:** the model has not learned enough of the useful pattern, so it performs poorly even on training data.
- **Good fit/generalization:** it captures patterns that transfer to unseen data.
- **Overfitting:** it learns training-specific detail or noise, so training performance is strong while validation or real-world performance is weak.

Low training loss alone does not prove that a model is useful. Compare performance on data that was not used for parameter updates. A widening gap between training and validation loss is a classic warning sign.

---

## 2. Deep-learning fundamentals

### Neural networks at a conceptual level

A neural network is a stack of parameterized transformations. A neuron combines inputs using weights and a bias, then applies a nonlinear activation. Layers build increasingly useful internal representations. During training:

1. a **forward pass** produces a prediction;
2. a loss function measures the error;
3. **backpropagation** assigns responsibility for that error through the network;
4. an optimizer updates parameters to reduce future loss.

Depth matters because several simple transformations can compose into complex ones. Nonlinear activations matter because a stack of purely linear layers would still behave like one linear transformation.

### Transformers

A transformer processes token representations through repeated blocks. A typical block contains:

- **self-attention**, which lets each token combine relevant information from other allowed token positions;
- a **feed-forward network**, which transforms each position's representation;
- residual connections and normalization, which help information and gradients flow through a deep network.

An LLM that generates left to right uses **causal masking**: a position can attend to earlier positions but not future tokens. Positional information is also needed because attention alone does not know token order.

### Attention in plain language

For each token, the model forms a query, key, and value representation. Query–key compatibility produces attention scores. After normalization, those scores become weights used to mix the value vectors.

Attention is therefore a learned, context-dependent information-routing mechanism. It does **not** by itself prove that the model understands text as a person does, and an attention weight should not automatically be treated as a complete explanation of a model decision.

---

## 3. LLM fundamentals

### Tokens

LLMs operate on **tokens**, not directly on words. A tokenizer converts text into IDs from a finite vocabulary. A token may be a word, part of a word, punctuation, whitespace, or another byte-derived unit. Therefore:

- token count is not the same as word count;
- uncommon text may require more tokens;
- spelling and formatting can change tokenization;
- cost and context limits are usually measured in tokens.

### Autoregressive generation

Given tokens \(x_1, \ldots, x_t\), an autoregressive language model estimates a probability distribution for \(x_{t+1}\). One token is selected, appended to the sequence, and fed back into the model. The cycle continues until a stop condition.

This explains both fluency and a major limitation: generation is a sequence of locally conditioned predictions. The model is not retrieving a guaranteed true sentence from a database.

### Temperature and top-p

The model produces scores, or logits, for candidate next tokens.

- **Temperature** rescales the logits before probabilities are calculated. Lower values sharpen the distribution and favor high-probability tokens; higher values flatten it and increase variation. Temperature does not add knowledge or verify truth.
- **Top-p (nucleus sampling)** keeps the smallest candidate set whose cumulative probability reaches \(p\), then samples from that set. The size of the set changes at every step.
- **Greedy decoding** always chooses the highest-probability token. It is more repeatable but not automatically more factual or globally optimal.

Temperature and top-p both affect selection, but in different ways: temperature reshapes the whole distribution; top-p truncates it dynamically.

### Context windows

The **context window** is the maximum token sequence the model can consider for a request and its generation, subject to the model/API definition. It can include system instructions, conversation history, retrieved material, tool results, the current prompt, and generated output.

A longer context window provides more capacity, not perfect memory or guaranteed use of every detail. Information outside the window is unavailable; information inside it can still be overlooked, weakly weighted, ambiguous, or contradicted. A context window is also different from the model's learned parameters and from external retrieval.

### Hallucination as a structural property

A hallucination is a fluent output containing unsupported or false claims. It is a structural risk because the core objective is to predict plausible next tokens—not to consult an internal truth table and certify every claim.

Several mechanisms contribute:

- pretraining supplies examples of text rather than a truth label for every statement;
- rare or arbitrary facts may not be statistically recoverable from patterns;
- the model must still produce a probability distribution even when the prompt is ambiguous, outside its knowledge, or missing evidence;
- sampling can select a plausible but wrong continuation;
- generated mistakes become part of the context and can steer later tokens;
- training and evaluation can reward attempting an answer more than admitting uncertainty.

Hallucination is **not** unavoidable in every response, and retrieval, tools, grounding, calibration, verification, and better incentives can reduce it. But fluent generation alone cannot guarantee factual correctness. Larger context and lower temperature may help in some cases; neither is a truth mechanism.

# P4-01 — ML, Deep Learning, and LLM Fundamentals is completed with the provided readme notes 