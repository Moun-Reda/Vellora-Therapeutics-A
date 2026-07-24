
import sys

from groq import Groq
from dotenv import load_dotenv
import os

from functions.tools import get_disease
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
    
from functions.tools import (
    get_disease,
    get_drug,
    get_possible_drugs,
    check_allergy,
    check_contraindications,
    check_interactions,
    get_dosage,
    get_alternative    
)
TOOLS = {
    "get_disease": get_disease,
    "get_drug": get_drug,
    "get_possible_drugs": get_possible_drugs,
    "check_allergy": check_allergy,
    "check_contraindications": check_contraindications,
    "check_interactions": check_interactions,
    "get_dosage": get_dosage,
    "get_alternative": get_alternative
}
def chat_with_agent(question):
    system_prompt = """
you are Vellora Therapeutics healthcare agent. You are a helpful and knowledgeable assistant that can answer questions about Vellora Therapeutics products,Always reason step by step before answering.

You have access to several medical tools.

Use tools whenever needed.

Never guess medical information.
Always check:
- allergies
- contraindications
- drug interactions
- dosage

Use this format:

Thought,

Action:
Available Tools:

get_disease(name)
Returns disease information.

get_possible_drugs(disease_name)
Returns candidate drugs.

check_allergy(patient_allergies, drug_name)
Checks whether the patient is allergic.

check_contraindications(patient_conditions, drug_name)
Checks contraindications.

check_interactions(current_medications, drug_name)
Checks for drug interactions.

get_dosage(drug_name, age)
Returns the recommended dosage.

get_alternative(drug_name)
Returns an alternative medication.
,
Observation,

Thought,

Final Answer:
Do not write Final Answer until you receive an Observation.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"system",
                "content":system_prompt
            },
            {
                "role":"user",
                "content":question
            }
]
    )
    return response.choices[0].message.content
question = "Patient has Hypertension"

print(chat_with_agent(question))