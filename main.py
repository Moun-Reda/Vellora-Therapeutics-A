import json

from reactive.reactive_agent0 import ReactiveAgent, diseases, drugs
from unconstrained.unconstrainedAgent import run_agent as run_unconstrained
from constrained.constrainedAgent import run_agent as run_constrained
from routing.router import classify_case
from routing.agent import handle_route


# -----------------------------
# Load Test Cases
# -----------------------------

with open("testCases/testCases.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)


# -----------------------------
# Reactive Agent
# -----------------------------

reactive = ReactiveAgent(diseases, drugs)


# -----------------------------
# Run All Agents
# -----------------------------

for i, case in enumerate(test_cases):

    print("\n" + "=" * 70)
    print(case["description"])
    print("=" * 70)

    data = case["input"]

    patient = {
        "age": data["age"],
        "pregnant": data.get("pregnant", False),
        "diagnosis": data["diagnosis"],
        "symptoms": data.get("symptoms", []),
        "medical_conditions": data.get("medical_conditions", []),
        "allergies": data.get("allergies", []),
        "current_medications": data.get("current_medications", [])
    }

    question = f"""
Disease: {patient['diagnosis']}
Age: {patient['age']}
Pregnant: {patient['pregnant']}
Allergies: {patient['allergies']}
Medical Conditions: {patient['medical_conditions']}
Current Medications: {patient['current_medications']}

Recommend the safest medication with dosage.
"""

    # ================= Reactive =================
    print("\n########## REACTIVE ##########")

    reactive.patient = patient
    diagnosis = reactive.diagnose()

    if diagnosis:
        drug, dosage, warning = reactive.recommend_treatment(diagnosis)
        reactive.display_results(diagnosis, drug, dosage, warning)
    else:
        print("No diagnosis found.")

    # ================= Unconstrained =================
    print("\n########## UNCONSTRAINED ##########")
    run_unconstrained(question, patient)

    # ================= Constrained =================
    print("\n########## CONSTRAINED ##########")

    test_case = f"""
Patient Information:
- diagnosis: {patient["diagnosis"]}
- age: {patient["age"]}
- allergies: {patient.get("allergies", [])}
- medical_conditions: {patient.get("medical_conditions", [])}
- current_medications: {patient.get("current_medications", [])}

Question:
Recommend a suitable medication and dosage for this patient.
Return the safest recommendation.
"""

    run_constrained(test_case)

    # ================= Routing =================
    print("\n########## ROUTING ##########")

    category = classify_case(question)
    action = handle_route(category)

    print("Category :", category)
    print("Action   :", action)

    break