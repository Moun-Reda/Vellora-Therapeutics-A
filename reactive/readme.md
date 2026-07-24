This folder contains the Reactive Agent.

#  Medical Diagnosis Reactive Agent

## Project Overview

This project implements a **Reactive AI Agent** that performs a simple medical diagnosis based on a patient's symptoms and recommends a medication.

The agent follows a **rule-based (if-then)** approach and does not perform reasoning or learning. It simply reacts to the current input and returns a predefined response.

This project is intended for educational purposes to demonstrate the strengths and limitations of reactive agents in Artificial Intelligence.


##  Features

- Accepts patient information
  - Age
  - Symptoms
  - Allergies

- Diagnoses diseases using symptom matching.

- Recommends a medication based on the diagnosed disease.

- Adjusts dosage according to age.

- Detects drug allergies.

- Simulates incorrect recommendations to demonstrate the weaknesses of reactive agents.

- Displays the limitations of reactive AI.



## AI Agent Type

This project represents a **Reactive Agent** because it:

- Uses predefined if-then rules.
- Does not store previous experiences.
- Makes decisions based only on the current input.
- Does not learn from mistakes.
- Cannot plan or reason.





##  Example

### Input

Age: 45
Symptoms: headache, dizziness
Allergies: none

### Output

Diagnosis:
Hypertension

Recommended Drug:
Norvasc (Amlodipine)

Dosage:
5 mg once daily

Recommendation accepted.


##  Example Failure

### Input

Age: 22
Symptoms: chest pain, shortness of breath
Allergies: none

### Output

No matching disease found.

This demonstrates that the reactive agent cannot diagnose diseases outside its predefined knowledge base.


##  Limitations

This reactive agent has several limitations:

- Cannot ask follow-up questions.
- Uses simple keyword matching.
- Cannot understand misspelled symptoms.
- Cannot learn from previous cases.
- Does not consider drug interactions.
- Cannot diagnose multiple diseases simultaneously.
- Cannot explain its reasoning.
- Cannot adapt to new medical knowledge.
- May intentionally produce an incorrect recommendation (for demonstration).

---

##  Future Improvements

This project could be improved by implementing a more advanced AI agent that:

- Learns from previous patients.
- Uses machine learning models.
- Supports natural language processing.
- Understands symptom similarity.
- Performs probabilistic diagnosis.
- Considers medical history and drug interactions.
- Ranks multiple possible diseases.

---

##  Educational Purpose

This project was developed as part of an Artificial Intelligence course to demonstrate how **Reactive Agents** work and why they are insufficient for complex medical decision-making.
