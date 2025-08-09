# train_anemia_model.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset from CSV
df = pd.read_csv("anemia_dataset.csv")  # Make sure this file is in the same folder

# Features and target
X = df[['Hemoglobin']]
y = df['Outcome']

# Split data (optional, for accuracy check)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Anemia Model Accuracy: {acc * 100:.2f}%")

# Save model
joblib.dump(model, "anemia_model.pkl")
print("Model saved as anemia_model.pkl")
