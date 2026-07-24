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

system_prompt = """
You are Vellora Therapeutics Healthcare Agent.

Your role is to assist users with medical information about diseases and medications
available in the Vellora Therapeutics knowledge base.

You must always reason step by step before answering.

=========================
AVAILABLE TOOLS
=========================

1. get_disease(name)
   Returns information about a disease.

2. get_drug(name)
   Returns information about a drug.

3. get_possible_drugs(disease_name)
   Returns medications that may treat the disease.

4. check_allergy(patient_allergies, drug_name)
   Checks whether the patient is allergic to the medication.

5. check_contraindications(patient_conditions, drug_name)
   Checks whether the medication is contraindicated.

6. check_interactions(current_medications, drug_name)
   Checks for drug interactions.

7. get_dosage(drug_name, age)
   Returns the recommended dosage.

8. get_alternative(drug_name)
   Returns an alternative medication.

=========================
RULES
=========================

- Think step by step.
- Use ONLY the tools listed above.
- Never invent tool names.
- Use only ONE tool at a time.
- Never guess medical information.
- Always verify information using the available tools.
- If a tool returns no result, explain that to the user.
- If enough information is available, provide the Final Answer.
- Do NOT provide a Final Answer before receiving an Observation after using a tool.

When recommending medication, always consider:
- Allergies
- Contraindications
- Drug interactions
- Dosage

=========================
OUTPUT FORMAT
=========================

Thought:
<your reasoning>

Action:
tool_name(arguments)
(The system will execute the tool.)

After receiving an Observation:


Thought:
<continue reasoning if needed>

Final Answer:
<your final response>

=========================
EXAMPLE
=========================

User:
Patient has Hypertension.

Assistant:

Thought:
I need information about the disease before recommending any medication.

Action:
get_disease("Hypertension")

Observation:
<Provided by the system>

Thought:
Now I have the disease information. I can continue checking possible medications before giving a recommendation.

"""
def ask_llm(messages):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages, temperature=0

    )
    return response.choices[0].message.content

def extract_action(response):
    pattern = r"Action:\s*(\w+)\((.*?)\)"
    match = re.search(pattern, response)

    if not match:
        return None, []

    tool = match.group(1)
    args_str = match.group(2).strip()

    if not args_str:
        return tool, []
    raw_args = [arg.strip().strip("'\"") for arg in args_str.split(",")]
    return tool, raw_args
   
def execute_tool(tool_name, args, patient=None):

    if tool_name == "get_disease":
        return get_disease(args[0])


    elif tool_name == "get_drug":
        return get_drug(args[0])


    elif tool_name == "get_possible_drugs":
        return get_possible_drugs(args[0])


    elif tool_name == "get_dosage":
        drug = get_drug(args[0])

        if drug is None:
            return "Drug not found"

        return get_dosage(patient, drug)


    elif tool_name == "check_allergy":
        drug = get_drug(args[0])

        if drug is None:
            return "Drug not found"

        return check_allergy(patient, drug)


    elif tool_name == "check_contraindications":
        drug = get_drug(args[0])

        if drug is None:
            return "Drug not found"

        return check_contraindications(patient, drug)


    elif tool_name == "check_interactions":
        drug = get_drug(args[0])

        if drug is None:
            return "Drug not found"

        return check_interactions(patient, drug)


    elif tool_name == "get_alternative":
        drug = get_drug(args[0])

        if drug is None:
            return "Drug not found"

        return get_alternative(drug)
def run_agent(question, patient):

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    max_steps = 10

    for step in range(1, max_steps + 1):

        print("\n" + "=" * 50)
        print(f"STEP {step}")
        print("=" * 50)

        # Ask LLM
        response = ask_llm(messages)

        # Prevent LLM from generating fake observations
        if "Observation:" in response:
            response = response.split("Observation:")[0].strip()

        print("\nLLM Response:")
        print(response)

        messages.append({
            "role": "assistant",
            "content": response
        })


        # Check if final answer exists
        if "Final Answer:" in response:

            answer = response.split("Final Answer:")[-1].strip()

            print("\n" + "=" * 50)
            print("FINAL ANSWER")
            print("=" * 50)

            print(answer)

            return answer


        # Extract action
        tool_name, args = extract_action(response)


        if tool_name is None:

            print("\nNo valid Action found.")

            messages.append({
                "role": "user",
                "content": (
                    "Observation: "
                    "No valid action detected. "
                    "Use format Action: tool_name(arguments) "
                    "or provide Final Answer."
                )
            })

            continue


        print("\nTool Selected:", tool_name)
        print("Arguments:", args)


        # Execute tool with patient information
        observation = execute_tool(
            tool_name,
            args,
            patient
        )


        if observation is None:
            observation = "No information found."


        print("\nObservation:")
        print(observation)


        # Send observation back to LLM
        messages.append({
            "role": "user",
            "content": f"Observation:\n{observation}"
        })


    print("\nMaximum reasoning steps reached.")

    return None

# if __name__ == "__main__":

#     # Fixed Test Case

#     patient = {
#         "age": 45,
#         "allergies": [],
#         "medical_conditions": [],
#         "current_medications": []
#     }

#     question = """
# Patient Information:

# Disease: Hypertension
# Age: 45
# Allergies: None
# Medical Conditions: None
# Current Medications: None

# Question:
# Recommend the safest medication with dosage.
# """

#     run_agent(question, patient)