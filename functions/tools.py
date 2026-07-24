from functions.dataloader import diseases, drugs


def get_disease(disease_name):
    for disease in diseases:
        if disease["disease_name"].lower() == disease_name.lower():
            return disease
    return None

def get_drug(name):
    for drug in drugs:
        if drug["brand_name"].lower() == name.lower():
            return drug

        if drug["active_ingredient"].lower() == name.lower():
            return drug

    return None


def get_possible_drugs(disease_name):
    """
    Return all drugs names that can treat the given disease.
    """
    disease = get_disease(disease_name)

    if disease is None:
        return []

    result = []

    for ingredient in disease["possible_active_ingredients"]:
        drug = get_drug(ingredient)

        if drug:
            result.append(drug)

    return result


def check_allergy(patient, drug):
    """
    Check if patient is allergic to the drug.
    """

    allergies = patient.get("allergies", [])

    active = drug["active_ingredient"].lower()
    brand = drug["brand_name"].lower()

    for allergy in allergies:
        if allergy.lower() == active or allergy.lower() == brand:
            return True

    return False

def check_contraindications(patient, drug):
    """
    Check contraindications.
    """

    conditions = patient.get("medical_conditions", [])

    for condition in conditions:
        if condition in drug["contraindications"]:
            return True

    if patient.get("pregnant", False):

        if drug["active_ingredient"] == "Lisinopril":
            return True

    return False

def check_interactions(patient, drug):
    """
    Return drug interaction warnings.
    """

    warnings = []

    current_medications = patient.get("current_medications", [])

    for medication in current_medications:

        if medication in drug["drug_interactions"]:
            warnings.append(medication)

    return warnings

def get_dosage(patient, drug):
    """
    Return suitable dosage according to patient's age.
    """

    age = patient["age"]

    if age >= 65:
        return drug["dosage"]["elderly"]

    elif age < 18:
        return drug["dosage"]["child"]

    else:
        return drug["dosage"]["adult"]


def get_alternative(drug):

    alternative_name = drug["alternative"]

    return get_drug(alternative_name)



def validate_case(patient):

    required_fields = [
        "age",
        "diagnosis",
        "allergies",
        "current_medications"
    ]

    for field in required_fields:

        if field not in patient:
            return False, f"{field} is required."

    if patient["age"] <= 0:
        return False, "Invalid age."

    disease = get_disease(patient["diagnosis"])

    if disease is None:
        return False, "Diagnosis not found."

    return True, "Valid case."

def recommend_drug(patient):

    valid, message = validate_case(patient)

    if not valid:
        return {"error": message}

    possible_drugs = get_possible_drugs(patient["diagnosis"])

    recommendations = []

    for drug in possible_drugs:

        if check_allergy(patient, drug):
            continue

        if check_contraindications(patient, drug):
            alternative = get_alternative(drug)

            if alternative:
                drug = alternative
            else:
                continue

        dosage = get_dosage(patient, drug)

        interactions = check_interactions(patient, drug)

        recommendations.append({

            "brand_name": drug["brand_name"],

            "active_ingredient": drug["active_ingredient"],

            "dosage": dosage,

            "warnings": interactions

        })

    return recommendations