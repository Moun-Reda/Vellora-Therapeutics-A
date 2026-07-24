from schema import AgentResponse
from groq import Groq
from dotenv import load_dotenv
import os
import re
import sys
from pathlib import Path
load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

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

    get_alternative,


)



ALLOWED_TOOLS = {

    "get_disease": get_disease,

    "get_drug": get_drug,

    "get_possible_drugs": get_possible_drugs,

    "check_allergy": check_allergy,

    "check_contraindications": check_contraindications,

    "check_interactions": check_interactions,

    "get_dosage": get_dosage,

    "get_alternative": get_alternative,


}

Max_steps=6


system_prompt = """
You are Vellora Therapeutics Healthcare Agent.

Your task is to recommend the safest medication for a patient by using ONLY the available tools.

Available tools:

1. get_disease
Arguments:
{
    "disease_name": "<diagnosis>"
}

2. get_drug
Arguments:
{
    "name": "<drug name or active ingredient>"
}

3. get_possible_drugs
Arguments:
{
    "disease_name": "<diagnosis>"
}

4. check_allergy
Arguments:
{
    "patient": {...},
    "drug": {...}
}
5. check_contraindications
Arguments:
{
    "patient": {...},
    "drug": {...}
}
6. check_interactions
Arguments:
{
    "patient": {...},
    "drug": {...}
}
7. get_dosage
Arguments:
{
    "patient": {...},
    "drug": {...}
}
8. get_alternative
Arguments:
{
    "drug": {...}
}
Workflow:

1. Call get_disease.
2. Call get_possible_drugs.
3. For each candidate drug:
   - check_allergy
   - check_contraindications
   - check_interactions
4. Choose the safest drug.
5. Call get_dosage.
6. Return FinalAnswer.

Rules:

- Use ONLY one tool per response.
- Never invent medical information.
- Never skip safety checks.
- Never call the same successful tool twice.
- Wait for the observation before choosing the next tool.
- Return ONLY valid JSON.
- When enough information is available, return FinalAnswer.

Tool Call JSON:

{
  "response": {
    "type": "tool_call",
    "action": "tool_name",
    "arguments": {}
  }
}

FinalAnswer JSON:

{
  "response": {
    "type": "final_answer",
    "drug": "",
    "active_ingredient": "",
    "dosage": "",
    "warnings": []
  }
}
"""

def ask_llm(messages):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages, temperature=0

    )
    return response.choices[0].message.content

import json
def parse_response(response):

    try:
        data = json.loads(response)

        validated = AgentResponse(**data)

        return validated

    except Exception as e:
        print("Invalid response:", e)
        return None


def validate_tool(tool_name):

    if tool_name not in ALLOWED_TOOLS:
        return False

    return True


def execute_tool(action):

    if action.action not in ALLOWED_TOOLS:
        return "Invalid tool"

    tool =ALLOWED_TOOLS[action.action]

    try:
        result = tool(**action.arguments)
        return result

    except Exception as e:
        return f"Tool error: {str(e)}"



def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(Max_steps):

        print(f"\n========== STEP {step+1} ==========\n")

        response = ask_llm(messages)
        print(response)

        parsed = parse_response(response)

        if parsed is None:
            messages.append({
                "role": "user",
                "content": "Return ONLY valid JSON matching the required schema."
            })
            continue
        messages.append({
    "role": "assistant",
    "content": response
})

        from schema import FinalAnswer

        if isinstance(parsed.response, FinalAnswer):
            print("\nFINAL ANSWER:")
            print(parsed.response.model_dump())
            return parsed.response

        observation = execute_tool(parsed.response)

        print("\nOBSERVATION:")
        print(observation)


        messages.append({
    "role": "user",
    "content": f"""
Previous tool:
{parsed.response.action}

Observation:
{observation}

Rules:
- Do NOT call the same successful tool again.
- Use the observation to decide the next tool.
- Return ONLY one JSON object.
- If you already have enough information, return FinalAnswer.
"""
})
    print("\nGenerating final recommendation...\n")

    messages.append({
        "role": "user",
        "content": """
    Based on all previous observations, return ONLY a FinalAnswer JSON.

    Do not call any more tools.
    """
    })

    response = ask_llm(messages)
    print(response)
    print("Maximum steps reached.")
        


# if __name__ == "__main__":
#     test_case = """
# Patient Information:
# - diagnosis: Hypertension
# - age: 45
# - allergies: []
# - medical_conditions: []
# - current_medications: []

# Question:
# Recommend a suitable medication and dosage for this patient.
# Return the safest recommendation.
# """

#     run_agent(test_case)