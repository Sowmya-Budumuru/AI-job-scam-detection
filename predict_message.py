# predict_message.py

import joblib

# 1) Load the trained model
model = joblib.load("scam_detector_model.joblib")

def classify_message(text: str):
    """
    Takes a message string and returns:
    - predicted label ("scam" or "legit")
    - prediction probability
    """
    # 2) Get prediction
    pred = model.predict([text])[0]

    # 3) Get probabilities for each class
    proba = model.predict_proba([text])[0]

    # 4) Map class -> probability
    classes = model.classes_
    proba_dict = {cls: float(p) for cls, p in zip(classes, proba)}

    return pred, proba_dict

if __name__ == "__main__":
    # 5) Test some messages
    test_msg = input("Enter a job message to check: ")
    label, probs = classify_message(test_msg)

    print("\nPrediction:", label.upper())
    print("Probabilities:", probs)
