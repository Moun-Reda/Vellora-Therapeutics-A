# Vellora Therapeutics – Medical Recommendation Agents

## About the Company

**Vellora Therapeutics** is a pharmaceutical company that develops and provides medications for common medical conditions. The company aims to support healthcare professionals by providing fast, safe, and evidence-based medication recommendations.

---

# Problem Statement

Healthcare professionals often need to choose the most appropriate medication while considering several patient-specific factors, such as:

* Disease diagnosis
* Drug allergies
* Contraindications
* Drug interactions
* Patient age
* Pregnancy status

Making these decisions manually can be time-consuming and may increase the risk of human error.

---

# Our Solution

We built an AI-powered medication recommendation system that assists healthcare professionals in selecting safer medications based on patient information.

The system uses a shared medical knowledge base containing:

* Diseases
* Drugs
* Clinical guidelines
* Test cases

The same medical problem is solved using **four different agent architectures**, allowing us to compare how each architecture approaches decision making.

---

# Agent Architectures

## 1. Reactive (Rule-Based) Agent

Uses predefined rules and conditions.

* Matches diseases using symptoms.
* Applies fixed medical rules.
* Recommends medication without LLM reasoning.

Best for predictable and straightforward cases.

---

## 2. Unconstrained ReAct Agent

Uses an LLM with tool calling.

The model freely decides:

* which tool to use,
* when to use it,
* and when enough information has been collected.

This provides flexible reasoning but the reasoning path may vary between runs.

---

## 3. Constrained ReAct Agent

Also uses an LLM, but follows a fixed workflow.

Required sequence:

1. Get disease
2. Get possible drugs
3. Check allergies
4. Check contraindications
5. Check drug interactions
6. Get dosage
7. Return final recommendation

This produces more predictable and reliable reasoning.

---

## 4. Routing Agent

Instead of solving every request directly, this agent first classifies the patient case into categories such as:

* Standard Case
* Allergy Risk
* Drug Interaction
* Complex Case

The request can then be routed to the most appropriate workflow.

---

# Why Use Agents Instead of a Simple Script?

A simple script can only execute predefined logic and cannot adapt its reasoning process.

Agent architectures provide additional capabilities such as:

* Multi-step reasoning
* Dynamic tool selection
* Decision making based on intermediate observations
* Better handling of complex medical scenarios
* Flexible workflows depending on patient information

This makes agent-based systems more suitable for real-world healthcare decision support.

---

# Project Structure

```text
data/
    diseases.json
    drugs.json
    guidelines.json
    clinical_cases.json

functions/
    dataloader.py
    tools.py

reactive/
    reactive_agent.py

unconstrained/
    unconstrainedAgent.py

constrained/
    constrainedAgent.py

routing/
    router.py

testCases/
    testCases.json

main.py
```

---

# Running the Project

Install the required packages:

```bash
pip install groq python-dotenv
```

Create a `.env` file:

```text
GROQ_API_KEY=your_api_key
```

Run:

```bash
python main.py
```

---

# Model & Provider

**Provider:** Groq

**Model:** `llama-3.1-8b-instant`

The Unconstrained and Constrained ReAct agents use the Groq API for reasoning and tool selection.

---

# Example Features

* Medication recommendation
* Dosage recommendation
* Allergy checking
* Contraindication checking
* Drug interaction checking
* Alternative medication suggestion
* Medical case routing

---

# Team Goal

The goal of this project is **not to find the "best" agent**, but to compare how different AI agent architectures solve the same healthcare problem and understand the strengths and limitations of each approach.
