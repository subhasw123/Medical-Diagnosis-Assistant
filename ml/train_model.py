import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("dataset/Final_Dataset.csv")

# Features
X = df.drop("diseases", axis=1)

# Target
y = df["diseases"]

# Encode diseases
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42
)

# Train
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=1
)

model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)

# Save model
joblib.dump(
    model,
    "ml/models/disease_model.pkl"
)

joblib.dump(
    encoder,
    "ml/models/label_encoder.pkl"
)

print("Model Saved Successfully")