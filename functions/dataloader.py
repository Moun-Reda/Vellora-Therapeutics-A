import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

with open(DATA_DIR / "diseases.json", "r") as f:
    diseases = json.load(f)

with open(DATA_DIR / "drugs.json", "r") as f:
    drugs = json.load(f)

with open(DATA_DIR / "guidelines.json", "r") as f:
    guidelines = json.load(f)

