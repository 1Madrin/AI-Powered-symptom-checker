from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Define diseases and their common symptoms
DISEASE_SYMPTOMS = {
    "Common Cold": [
        "fever",
        "runny nose",
        "sore throat",
        "cough",
        "congestion",
        "body aches",
    ],
    "Influenza": ["high fever", "fatigue", "body aches", "cough", "headache"],
    "COVID-19": ["fever", "dry cough", "tiredness", "loss of taste", "loss of smell"],
    "Gastroenteritis": [
        "nausea",
        "vomiting",
        "diarrhea",
        "abdominal pain",
        "fever",
        "headache",
    ],
    "Migraine": [
        "severe headache",
        "nausea",
        "sensitivity to light",
        "sensitivity to sound",
    ],
    "Allergies": ["sneezing", "itchy eyes", "runny nose", "congestion"],
    "Asthma": ["shortness of breath", "wheezing", "chest tightness", "coughing"],
    "Pneumonia": [
        "high fever",
        "cough with phlegm",
        "difficulty breathing",
        "chest pain",
    ],
    "Strep Throat": [
        "severe sore throat",
        "fever",
        "swollen lymph nodes",
        "difficulty swallowing",
    ],
    "Bronchitis": ["persistent cough", "chest discomfort", "fatigue", "mild fever"],
    "Sinusitis": [
        "facial pain",
        "nasal congestion",
        "headache",
        "postnasal drip",
        "cough",
    ],
    "Diabetes": [
        "frequent urination",
        "excessive thirst",
        "extreme fatigue",
        "blurry vision",
    ],
    "Hypertension": ["headache", "shortness of breath", "nosebleeds", "dizziness"],
    "Heart Disease": ["chest pain", "shortness of breath", "nausea", "fatigue"],
    "Peptic Ulcer": ["abdominal pain", "nausea", "vomiting", "loss of appetite"],
    "Kidney Infection": [
        "flank pain",
        "fever",
        "frequent urination",
        "painful urination",
    ],
    "Urinary Tract Infection": [
        "painful urination",
        "frequent urination",
        "cloudy urine",
        "lower abdominal pain",
    ],
    "Herpes Simplex Virus": [
        "blisters around the mouth or genital area",
        "painful urination",
        "itching",
    ],
    "Chickenpox": ["itchy rash", "fever", "fatigue", "headache"],
    "Shingles": ["painful rash", "itching", "fever", "headache"],
    "Lung Cancer": [
        "persistent cough",
        "coughing up blood",
        "shortness of breath",
        "chest pain",
    ],
    "Tuberculosis": ["persistent cough", "night sweats", "weight loss", "fever"],
    "Whooping Cough": [
        "severe coughing fits",
        "vomiting after coughing",
        "runny nose",
        "fatigue",
    ],
    "HIV/AIDS": [
        "rapid weight loss",
        "recurrent fever",
        "night sweats",
        "persistent cough",
    ],
    "Hepatitis": ["jaundice", "abdominal pain", "dark urine", "fatigue"],
    "Anemia": ["fatigue", "paleness", "shortness of breath", "dizziness"],
    "Rheumatoid Arthritis": ["joint pain", "swelling", "morning stiffness", "fatigue"],
    "Systemic Lupus Erythematosus": ["fatigue", "joint pain", "rash", "fever"],
    "Multiple Sclerosis": [
        "numbness",
        "difficulty walking",
        "vision problems",
        "muscle spasms",
    ],
    "Parkinson's Disease": [
        "tremors",
        "muscle rigidity",
        "bradykinesia",
        "postural instability",
    ],
    "Epilepsy": ["seizures", "aura", "loss of consciousness", "muscle contractions"],
    "Dengue Fever": [
        "high fever",
        "severe headache",
        "pain behind the eyes",
        "joint and muscle pain",
        "nausea",
        "vomiting",
        "rash",
        "mild bleeding",
        "fatigue",
    ],
}


def calculate_disease_probabilities(symptoms):
    symptom_words = set(symptoms.lower().split())
    scores = defaultdict(float)

    for disease, disease_symptoms in DISEASE_SYMPTOMS.items():
        for symptom in disease_symptoms:
            if any(word in symptom for word in symptom_words):
                scores[disease] += 1

    total_score = sum(scores.values())
    if total_score == 0:
        return []

    probabilities = [
        (disease, score / total_score) for disease, score in scores.items()
    ]
    return sorted(probabilities, key=lambda x: x[1], reverse=True)


@app.route("/api/check-symptoms", methods=["POST"])
def check_symptoms():
    data = request.get_json()
    symptoms_input = data.get("symptoms", "")

    predictions = calculate_disease_probabilities(symptoms_input)

    if not predictions:
        return jsonify({
            "top_prediction": "Unable to determine",
            "top_5_predictions": [
                {"disease": "Unable to determine", "probability": "100.00%"}
            ],
        })

    top_prediction = predictions[0][0]
    top_5_predictions = [
        {"disease": disease, "probability": f"{prob:.2%}"}
        for disease, prob in predictions[:5]
    ]

    return jsonify({
        "top_prediction": top_prediction,
        "top_5_predictions": top_5_predictions,
    })


if __name__ == "__main__":
    app.run(debug=True)
