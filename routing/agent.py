from routing.router import classify_case


def handle_route(category):
    routes = {
        "STANDARD_CASE": "Proceed with standard treatment recommendation",
        "ALLERGY_RISK": "Check allergy before recommending medication",
        "DRUG_INTERACTION": "Review current medications for interactions",
        "COMPLEX_CASE": "Refer case to medical specialist"
    }

    return routes.get(category, "Need additional review")


test_cases = [
    """
    Patient age: 45
    Weight: 80 kg
    Diagnosis: Hypertension
    Allergy: Penicillin
    Current medications: None
    """,

    """
    Patient age: 70
    Weight: 75 kg
    Diagnosis: Diabetes
    Current medications: Multiple diabetes medications
    Possible drug interaction detected
    """,

    """
    Patient age: 30
    Weight: 60 kg
    Diagnosis: Common cold
    No allergies
    No other medications
    """
]


# for i, case in enumerate(test_cases, 1):

#     category = classify_case(case)
#     action = handle_route(category)

#     print(f"\nTest Case {i}")
#     print("Category:", category)
#     print("Action:", action)