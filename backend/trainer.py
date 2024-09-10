import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

data = {
    "symptoms": ["fever cough", "headache fatigue", "nausea", "fever fatigue"],
    "disease": ["Flu", "Migraine", "Gastroenteritis", "COVID-19"],
}
df = pd.DataFrame(data)

SYMPTOMS_LIST = ["fever", "cough", "fatigue", "headache", "nausea"]
X = (
    df["symptoms"]
    .apply(lambda x: [1 if symptom in x.split() else 0 for symptom in SYMPTOMS_LIST])
    .tolist()
)
y = df["disease"]

model = RandomForestClassifier()
model.fit(X, y)

# Save the model
with open("symptom_checker_model.pkl", "wb") as f:
    pickle.dump(model, f)
