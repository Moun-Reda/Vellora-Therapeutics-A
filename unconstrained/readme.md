# Unconstrained ReAct Agent

## Description

This agent implements an **Unconstrained ReAct** architecture for the Vellora Therapeutics project.

The LLM is free to decide:
- which tool to use,
- how many reasoning steps to take,
- when to stop and provide the final answer.

It follows the **Thought → Action → Observation → Final Answer** pattern.

---

## Model / Provider

- **Provider:** Groq
- **Model:** llama-3.1-8b-instant

---

## Requirements

Install the required packages:

```bash
pip install groq python-dotenv
```

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_api_key
```

---

## How to Run

From the project root, run:

```bash
python unconstrained/unconstrainedAgent.py
```

The agent will execute a sample patient case and use the available medical tools to generate a recommendation.