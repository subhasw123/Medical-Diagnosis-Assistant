import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.predictor import predict_disease

sample = [0] * 377

sample[154] = 1  # fever
sample[50] = 1   # headache

disease, confidence = predict_disease(sample)

print(disease)
print(confidence)