import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import shap
import joblib

print("Loading data...")
dataset = pd.read_csv("training_data.csv")

X = dataset.drop('Target', axis=1)
y = dataset['Target']

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

print("Training XGBoost Classifier...")
# We use multi:softmax for 3 classes
# To get probabilities, we could use multi:softprob, but XGBClassifier handles it nicely

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    objective='multi:softprob',
    num_class=3,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

print("Predicting and Evaluating...")
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Cannot Run", "Playable", "Optimal"]))

# Calculate SHAP values for a sample (takes a while for full dataset)
print("\nCalculating SHAP explainer baseline...")
# Use tree explainer
explainer = shap.TreeExplainer(model)
# Just calculate on the first few rows to verify it works
shap_values = explainer.shap_values(X_test.iloc[:10])
print(f"SHAP values generated successfully. Shape depends on number of classes.")

# Save model
print("\nSaving model and explainer components...")
model.save_model("xgb_model.json")
joblib.dump(explainer, "shap_explainer.pkl")
joblib.dump(list(X.columns), "feature_names.pkl")

print("Training script finished successfully!")
