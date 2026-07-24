# Vellora Therapeutics Routing Agent

## Description
A Deterministic Routing Agent that receives patient information and classifies the case into a predefined category.

The LLM only decides the category, then normal Python code handles the next action.

## Categories
- STANDARD_CASE
- ALLERGY_RISK
- DRUG_INTERACTION
- COMPLEX_CASE

## Model
Provider: Groq API

Model: llama-3.1-8b-instant

## Run

Install requirements:

py -m pip install -r requirements.txt

Run:

py agent.py