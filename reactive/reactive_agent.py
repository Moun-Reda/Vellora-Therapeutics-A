import random

class ReactiveAgent:
    def __init__(self, diseases, drugs):
        self.diseases = {d['id']: d for d in diseases}
        self.drugs = {d['drug_id']: d for d in drugs}
        self.patient = {}
        
    def start(self):
        print("MEDICAL AGENT (Reactive)")
        
        
        # Get patient info
        self.patient['age'] = int(input("\nAge: "))
        symptoms = input("Symptoms (comma separated): ").lower().split(',')
        self.patient['symptoms'] = [s.strip() for s in symptoms]
        allergies = input("Allergies (or 'none'): ").lower()
        self.patient['allergies'] = [] if allergies == 'none' else [a.strip() for a in allergies.split(',')]
        
        # Diagnose
        diagnosis = self._diagnose()
        if not diagnosis:
            print("\n No matching disease found")
            self._show_limitations()
            return
            
        # Recommend treatment
        drug, dosage, is_wrong = self._recommend(diagnosis)
        
        # Show results
        print(f"DIAGNOSIS: {diagnosis['disease_name']}")
        
        
        if drug:
            print(f"\n RECOMMENDED: {drug['brand_name']} ({drug['active_ingredient']})")
            print(f"   Dosage: {dosage}")
            print(f"   Side effects: {', '.join(drug['common_side_effects'][:2])}")
            
            if is_wrong:
                print(f"\n WRONG RECOMMENDATION!")
                print(f"   Reason: {is_wrong}")
                print(f"   Better alternative: {drug['alternative']}")
            else:
                print(f"\n RECOMMENDATION IS CORRECT")
        else:
            print("\n No suitable drug found")
            
        self._show_limitations()
        
    def _diagnose(self):
        """Simple diagnosis - matches symptoms"""
        for disease in self.diseases.values():
            matches = 0
            for symptom in self.patient['symptoms']:
                for d_symptom in disease['common_symptoms']:
                    if symptom in d_symptom.lower() or d_symptom.lower() in symptom:
                        matches += 1
                        break
            if matches >= 2:  # Needs at least 2 matching symptoms
                return disease
        return None
        
    def _recommend(self, diagnosis):
        """Recommend drug and check if recommendation is wrong"""
        drugs = [d for d in self.drugs.values() 
                if diagnosis['disease_name'] in d['used_for']]
        
        if not drugs:
            return None, None, "No drugs available"
            
        # Pick first available drug
        drug = drugs[0]
        
        # Check for allergies
        if drug['active_ingredient'].lower() in self.patient['allergies']:
            return drug, drug['dosage']['adult'], f"Patient is allergic to {drug['active_ingredient']}"
            
        # Check pregnancy (simulated)
        if self.patient.get('pregnant', False) and drug['active_ingredient'] == 'Lisinopril':
            return drug, drug['dosage']['adult'], "Lisinopril is contraindicated in pregnancy"
            
        # Check age
        if self.patient['age'] >= 65:
            dosage = drug['dosage']['elderly']
        else:
            dosage = drug['dosage']['adult']
            
        # Sometimes make random wrong recommendation
        if len(drugs) > 1 and random.random() < 0.3:
            wrong_drug = drugs[1]
            return wrong_drug, wrong_drug['dosage']['adult'], f"Should have recommended {drug['brand_name']} instead"
            
        return drug, dosage, None
    
    def _show_limitations(self):
        print(" REACTIVE AGENT LIMITATIONS:")
        print("• Can't ask follow-up questions")
        print("• Simple keyword matching only")
        print("• Doesn't consider drug interactions")
        print("• No reasoning, just if-then rules")
        print("• Makes random errors")
        print("• Can't handle complex cases")
        print("\nCONCLUSION: Reactive agents are NOT reliable for medical decisions")

# Data
diseases = [
    {"id": "D001", "disease_name": "Hypertension", "common_symptoms": ["headache", "dizziness", "blurred vision"]},
    {"id": "D002", "disease_name": "Type 2 Diabetes", "common_symptoms": ["frequent urination", "increased thirst", "fatigue"]},
    {"id": "D003", "disease_name": "Upper Respiratory Bacterial Infection", "common_symptoms": ["fever", "sore throat", "cough"]}
]

drugs = [
    {"drug_id": "DR001", "brand_name": "Norvasc", "active_ingredient": "Amlodipine", "used_for": ["Hypertension"], 
     "dosage": {"adult": "5mg once daily", "elderly": "2.5mg once daily"}, 
     "common_side_effects": ["Headache", "Dizziness", "Ankle swelling"], "alternative": "Lisinopril"},
     
    {"drug_id": "DR002", "brand_name": "Zestril", "active_ingredient": "Lisinopril", "used_for": ["Hypertension"], 
     "dosage": {"adult": "10mg once daily", "elderly": "5mg once daily"}, 
     "common_side_effects": ["Dry cough", "Dizziness"], "alternative": "Amlodipine"},
     
    {"drug_id": "DR003", "brand_name": "Glucophage", "active_ingredient": "Metformin", "used_for": ["Type 2 Diabetes"], 
     "dosage": {"adult": "500mg twice daily", "elderly": "500mg once daily"}, 
     "common_side_effects": ["Nausea", "Diarrhea"], "alternative": "Empagliflozin"},
     
    {"drug_id": "DR004", "brand_name": "Jardiance", "active_ingredient": "Empagliflozin", "used_for": ["Type 2 Diabetes"], 
     "dosage": {"adult": "10mg once daily", "elderly": "10mg once daily"}, 
     "common_side_effects": ["UTI", "Increased urination"], "alternative": "Metformin"},
     
    {"drug_id": "DR005", "brand_name": "Amoxil", "active_ingredient": "Amoxicillin", "used_for": ["Upper Respiratory Bacterial Infection"], 
     "dosage": {"adult": "500mg every 8 hours", "elderly": "500mg every 8 hours"}, 
     "common_side_effects": ["Skin rash", "Diarrhea"], "alternative": "Azithromycin"},
     
    {"drug_id": "DR006", "brand_name": "Zithromax", "active_ingredient": "Azithromycin", "used_for": ["Upper Respiratory Bacterial Infection"], 
     "dosage": {"adult": "500mg once daily for 3 days", "elderly": "500mg once daily for 3 days"}, 
     "common_side_effects": ["Nausea", "Abdominal pain"], "alternative": "Amoxicillin"}
]

# Run
agent = ReactiveAgent(diseases, drugs)
agent.start()