import pandas as pd

df = pd.read_csv("dataset/Final_Dataset.csv")

print("Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())