import os
from groq import Groq
from dotenv import load_dotenv
from routing.categories import CATEGORIES

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def classify_case(patient_case):

    prompt = f"""
You are a medical routing agent for Vellora Therapeutics.

Classify the patient case into exactly one category from this list:

{CATEGORIES}

Patient Case:
{patient_case}

Return only the category name.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip().replace('"', '').replace("'", "").strip()

    if result not in CATEGORIES:
     return "COMPLEX_CASE"

    return result