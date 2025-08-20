# train_anemia_model.py

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("anemia_dataset.csv")  # Make sure this file is in the same folder

X = df[['Hemoglobin']]
y = df['Outcome']

model = DecisionTreeClassifier(max_depth=2, random_state=42)  # max_depth=2 enough for threshold rules
model.fit(X, y)

y_pred = model.predict(X)
acc = accuracy_score(y, y_pred)
print(f"Anemia Model Accuracy: {acc * 100:.2f}%")

joblib.dump(model, "anemia_model.pkl")
print("Model saved as anemia_model.pkl")
