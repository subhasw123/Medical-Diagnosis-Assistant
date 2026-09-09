#!/bin/bash

mkdir -p ml/models

echo "Downloading disease model..."
curl -L --fail \
  "https://media.githubusercontent.com/media/subhasw123/Medical-Diagnosis-Assistant/main/ml/models/disease_model.pkl" \
  -o ml/models/disease_model.pkl

echo "Downloading label encoder..."
curl -L --fail \
  "https://media.githubusercontent.com/media/subhasw123/Medical-Diagnosis-Assistant/main/ml/models/label_encoder.pkl" \
  -o ml/models/label_encoder.pkl

echo "Model files downloaded:"
ls -lh ml/models/