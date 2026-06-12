import json

with open(
    "ml/models/symptoms.json",
    "r"
) as file:
    SYMPTOMS = json.load(file)