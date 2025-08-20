# train_models.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("diabetes_dataset.csv")

X = df[['Glucose']]
y = df['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Diabetes Model Accuracy: {acc * 100:.2f}%")

joblib.dump(model, "diabetes_model.pkl")
print("Model saved to ml_model/diabetes_model.pkl")