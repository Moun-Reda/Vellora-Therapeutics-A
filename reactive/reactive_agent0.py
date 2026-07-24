import random

MIN_SYMPTOM_MATCHES = 2
WRONG_RECOMMENDATION_CHANCE = 0.30


class ReactiveAgent:
    def __init__(self, diseases: list, drugs: list):
        self.diseases = {d["id"]: d for d in diseases}
        self.drugs = {d["drug_id"]: d for d in drugs}
        self.patient = {}

    def start(self): 
        print("        MEDICAL REACTIVE AGENT")
        
        self.collect_patient_information()

        diagnosis = self.diagnose()

        if diagnosis is None:
            print("\nNo matching disease was found.")
            self.show_limitations()
            return

        drug, dosage, warning = self.recommend_treatment(diagnosis)

        self.display_results(diagnosis, drug, dosage, warning)

        self.show_limitations()

    # -------------------------------------------------
    # Patient Information
    # -------------------------------------------------

    def collect_patient_information(self):
        self.patient["age"] = int(input("\nAge: "))

        symptoms = input("Symptoms (comma separated): ").lower().split(",")
        self.patient["symptoms"] = [s.strip() for s in symptoms]

        allergies = input("Allergies (or 'none'): ").lower()

        if allergies == "none":
            self.patient["allergies"] = []
        else:
            self.patient["allergies"] = [
                allergy.strip() for allergy in allergies.split(",")
            ]

    # -------------------------------------------------
    # Diagnosis
    # -------------------------------------------------

    def diagnose(self):
        best_match = None
        highest_score = 0
        if "diagnosis" in self.patient:
                    for disease in self.diseases.values():
                        if disease["disease_name"] == self.patient["diagnosis"]:
                            return disease
        for disease in self.diseases.values():

            score = sum(
                any(
                    symptom in disease_symptom.lower()
                    or disease_symptom.lower() in symptom
                    for disease_symptom in disease["common_symptoms"]
                )
                for symptom in self.patient["symptoms"]
            )

            if score >= MIN_SYMPTOM_MATCHES and score > highest_score:
                highest_score = score
                best_match = disease

        return best_match

    # -------------------------------------------------
    # Drug Recommendation
    # -------------------------------------------------

    def recommend_treatment(self, diagnosis):

        available_drugs = [
            drug
            for drug in self.drugs.values()
            if diagnosis["disease_name"] in drug["used_for"]
        ]

        if not available_drugs:
            return None, None, "No suitable medication found."

        recommended = available_drugs[0]

        dosage = (
            recommended["dosage"]["elderly"]
            if self.patient["age"] >= 65
            else recommended["dosage"]["adult"]
        )

        # Allergy check
        if (
            recommended["active_ingredient"].lower()
            in self.patient["allergies"]
        ):
            return (
                recommended,
                dosage,
                f"Patient is allergic to {recommended['active_ingredient']}.",
            )

        # Pregnancy check
        if (
            self.patient.get("pregnant", False)
            and recommended["active_ingredient"] == "Lisinopril"
        ):
            return (
                recommended,
                dosage,
                "Lisinopril should not be used during pregnancy.",
            )

        # Simulate a wrong recommendation
        if (
            len(available_drugs) > 1
            and random.random() < WRONG_RECOMMENDATION_CHANCE
        ):
            wrong = available_drugs[1]
            return (
                wrong,
                wrong["dosage"]["adult"],
                f"Correct drug should be {recommended['brand_name']}.",
            )

        return recommended, dosage, None

    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    def display_results(self, diagnosis, drug, dosage, warning):

        print(f"Diagnosis : {diagnosis['disease_name']}")
        

        if drug is None:
            print("No suitable medication found.")
            return

        print(f"Drug        : {drug['brand_name']}")
        print(f"Ingredient  : {drug['active_ingredient']}")
        print(f"Dosage      : {dosage}")
        print(
            f"Side Effects: {', '.join(drug['common_side_effects'][:2])}"
        )

        if warning:
            print("\n⚠ Warning")
            print(warning)
            print(f"Alternative: {drug['alternative']}")
        else:
            print("\nRecommendation accepted.")


# -------------------------------------------------
# Data
# -------------------------------------------------

diseases = [
    {
        "id": "D001",
        "disease_name": "Hypertension",
        "common_symptoms": ["headache", "dizziness", "blurred vision"],
    },
    {
        "id": "D002",
        "disease_name": "Type 2 Diabetes",
        "common_symptoms": [
            "frequent urination",
            "increased thirst",
            "fatigue",
        ],
    },
    {
        "id": "D003",
        "disease_name": "Upper Respiratory Bacterial Infection",
        "common_symptoms": ["fever", "sore throat", "cough"],
    },
]

drugs = [
    {
        "drug_id": "DR001",
        "brand_name": "Norvasc",
        "active_ingredient": "Amlodipine",
        "used_for": ["Hypertension"],
        "dosage": {
            "adult": "5mg once daily",
            "elderly": "2.5mg once daily",
        },
        "common_side_effects": [
            "Headache",
            "Dizziness",
            "Ankle swelling",
        ],
        "alternative": "Lisinopril",
    },
    {
        "drug_id": "DR002",
        "brand_name": "Zestril",
        "active_ingredient": "Lisinopril",
        "used_for": ["Hypertension"],
        "dosage": {
            "adult": "10mg once daily",
            "elderly": "5mg once daily",
        },
        "common_side_effects": ["Dry cough", "Dizziness"],
        "alternative": "Amlodipine",
    },
    {
        "drug_id": "DR003",
        "brand_name": "Glucophage",
        "active_ingredient": "Metformin",
        "used_for": ["Type 2 Diabetes"],
        "dosage": {
            "adult": "500mg twice daily",
            "elderly": "500mg once daily",
        },
        "common_side_effects": ["Nausea", "Diarrhea"],
        "alternative": "Empagliflozin",
    },
    {
        "drug_id": "DR004",
        "brand_name": "Jardiance",
        "active_ingredient": "Empagliflozin",
        "used_for": ["Type 2 Diabetes"],
        "dosage": {
            "adult": "10mg once daily",
            "elderly": "10mg once daily",
        },
        "common_side_effects": [
            "UTI",
            "Increased urination",
        ],
        "alternative": "Metformin",
    },
    {
        "drug_id": "DR005",
        "brand_name": "Amoxil",
        "active_ingredient": "Amoxicillin",
        "used_for": ["Upper Respiratory Bacterial Infection"],
        "dosage": {
            "adult": "500mg every 8 hours",
            "elderly": "500mg every 8 hours",
        },
        "common_side_effects": ["Skin rash", "Diarrhea"],
        "alternative": "Azithromycin",
    },
    {
        "drug_id": "DR006",
        "brand_name": "Zithromax",
        "active_ingredient": "Azithromycin",
        "used_for": ["Upper Respiratory Bacterial Infection"],
        "dosage": {
            "adult": "500mg once daily for 3 days",
            "elderly": "500mg once daily for 3 days",
        },
        "common_side_effects": ["Nausea", "Abdominal pain"],
        "alternative": "Amoxicillin",
    },
]


if __name__ == "__main__":
    agent = ReactiveAgent(diseases, drugs)
    agent.start()