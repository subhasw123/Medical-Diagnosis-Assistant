# ml/save_symptoms.py

import pandas as pd
import json

df = pd.read_csv("dataset/Final_Dataset.csv")

symptoms = list(
    df.drop("diseases", axis=1).columns
)

with open(
    "ml/models/symptoms.json",
    "w"
) as file:
    json.dump(symptoms, file)

print("Symptoms Saved")