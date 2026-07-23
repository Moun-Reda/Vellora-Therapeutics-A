# tools.py

# │

# ├── get_disease()

# ├── get_drug()

# ├── get_possible_drugs()

# ├── check_allergy()

# ├── check_contraindications()

# ├── check_interactions()

# ├── get_dosage()

# ├── get_alternative()

# ├── validate_case()

# └── recommend_drug()
 
from functions.dataloader import diseases, drugs, guidelines, clinical_cases

def get_disease(disease_name):
    
    # Retrieve disease information by name.
    
    return diseases.get(disease_name, None)

def get_drug(drug_name):
  
    # Retrieve drug information by name.
   
    return drugs.get(drug_name, None)

def get_possible_drugs(disease_name):
    
    # Retrieve possible drugs for a given disease.
   
    disease = get_disease(disease_name)
    if disease:
        return disease.get("possible_drugs", [])
    return []

def check_allergy(patient_allergies, drug_name):
    
    # Check if the patient is allergic to the given drug.
    
    drug = get_drug(drug_name)
    if drug:
        return any(allergy in patient_allergies for allergy in drug.get("allergens", []))
    return False

def check_contraindications(patient_conditions, drug_name):
    
    # Check if the patient has any contraindications for the given drug.
    
    drug = get_drug(drug_name)
    if drug:
        return any(condition in patient_conditions for condition in drug.get("contraindications", []))
    return False
def check_interactions(drug_name1, drug_name2):
    
    # Check if there are any interactions between two drugs.
    
    drug1 = get_drug(drug_name1)
    drug2 = get_drug(drug_name2)
    if drug1 and drug2:
        return any(interaction in drug2.get("interactions", []) for interaction in drug1.get("interactions", []))
    return False

def get_dosage(drug_name, patient_weight):
    
    # Retrieve the recommended dosage for a given drug based on patient weight.
    
    drug = get_drug(drug_name)
    if drug:
        dosage_info = drug.get("dosage", {})
        if "per_kg" in dosage_info:
            return dosage_info["per_kg"] * patient_weight
        return dosage_info.get("standard", None)
    return None

def get_alternative(drug_name):
    
    # Retrieve alternative drugs for a given drug.
    
    drug = get_drug(drug_name)
    if drug:
        return drug.get("alternatives", [])
    return []

