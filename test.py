import joblib

model = joblib.load("ml/models/disease_model.pkl")

print("Model type:", type(model))
print("Number of trees:", model.n_estimators)
print("Number of features:", model.n_features_in_)

total_nodes = sum(tree.tree_.node_count for tree in model.estimators_)
print("Total tree nodes:", total_nodes)

print("Model loaded successfully")