## Key Features

* **Case Validation**: Verifies that patient data contains essential fields and valid age input.
* **Allergy Detection**: Flags drugs that match the patient's recorded allergies.
* **Contraindication Checking**: Filters out drugs that conflict with existing medical conditions or pregnancy.
* **Drug Interaction Analysis**: Identifies potential interactions between newly prescribed drugs and the patient's current medications.
* **Automatic Alternatives**: Suggests alternative drugs when the primary drug choice is contraindicated.
* **Age-Based Dosage**: Calculates correct dosages for pediatric, adult, and elderly patients.

---

## Code Functions Reference

### Data Retrieval Functions
* `get_disease(disease_name)`: Searches for a disease in the database by name (case-insensitive).
* `get_drug(active_ingredient)`: Retrieves drug information using its active ingredient name.
* `get_possible_drugs(disease_name)`: Returns a list of all drugs containing active ingredients capable of treating the specified disease.

### Safety & Logic Functions
* `check_allergy(patient, drug)`: Checks if the patient has a recorded allergy to the drug class.
* `check_contraindications(patient, drug)`: Checks if the drug is unsafe due to current medical conditions or pregnancy.
* `check_interactions(patient, drug)`: Checks for interactions between the proposed drug and the patient's current medications.
* `get_dosage(patient, drug)`: Determines the dosage based on age thresholds (under 18, 18-64, 65 and older).
* `get_alternative(drug)`: Fetches an alternative drug record if the initial drug cannot be safely prescribed.

### Core Workflow Functions
* `validate_case(patient)`: Validates that all required patient fields exist and that the diagnosis is registered in the database.
* `recommend_drug(patient)`: Runs the entire pipeline and returns a list of safe drug recommendations along with dosage and warnings.

---

## File Structure Dependency

The script relies on JSON files located in the `data/` directory:

```text
data/
├── diseases.json
├── drugs.json
├── guidelines.json
└── clinical_cases.json