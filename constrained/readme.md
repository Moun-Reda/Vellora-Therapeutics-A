# Constrained ReAct Agent

## Overview

This agent implements a **Constrained ReAct** workflow for the Vellora Therapeutics project. The language model can only use a predefined set of approved tools and must return structured JSON responses that match the validation schema.

## Model / Provider

* **Provider:** Groq
* **Model:** `llama-3.1-8b-instant`

Make sure a valid `GROQ_API_KEY` is available in your `.env` file before running the agent.

Example:

```text
GROQ_API_KEY=your_api_key_here
```

## How to Run

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Add your Groq API key to the `.env` file.

3. Run the agent:

   ```bash
   python constrained_react/agent.py
   ```

## Project Constraints

The following components are intentionally easy to locate in the code:

* **Validation Schema:** `schema.py`
* **Tool Allow-list:** `ALLOWED_TOOLS`
* **Maximum Reasoning Steps:** `MAX_STEPS`

These constraints ensure that the agent:

* uses only approved tools,
* produces validated JSON responses,
* and stops after a fixed number of reasoning steps.
