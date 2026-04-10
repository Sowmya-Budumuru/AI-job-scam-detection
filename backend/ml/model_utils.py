import joblib

MODEL = joblib.load("ml/scam_detector_model_3class.joblib")

def classify_message(text: str):
    label = MODEL.predict([text])[0]
    probabilities = MODEL.predict_proba([text])[0]
    
    class_labels = MODEL.classes_  # ['course', 'legit', 'scam']
    prob_dict = {cls: float(probabilities[i]) for i, cls in enumerate(class_labels)}
    
    return label, prob_dict


def extract_risk_reasons(text, label):
    text_lower = text.lower()
    reasons = []

    if label == "scam":
        if "fee" in text_lower or "pay" in text_lower or "deposit" in text_lower:
            reasons.append("Requests money payment")

        if "earn" in text_lower and "/day" in text_lower:
            reasons.append("Unrealistic earning promise")

        if "urgent" in text_lower or "immediately" in text_lower:
            reasons.append("Creates urgency pressure")

    elif label == "course":
        if "course" in text_lower or "training" in text_lower:
            reasons.append("Promotes paid course or training")

    else:
        reasons.append("No major risk indicators detected")

    return reasons


def generate_advice(label, confidence):
    if label == "scam":
        return "Do NOT pay any money. This appears to be a scam job offer."
    elif label == "course":
        return "This appears to be a paid training/course. Verify the company before paying."
    else:
        return "This message appears legitimate. Proceed carefully and verify details."


def generate_complaint_template(text, phone=None, email=None):
    return (
        f"Subject: Complaint Regarding Suspicious Job/Online Message\n\n"
        f"Message Content:\n{text}\n\n"
        f"Phone: {phone}\n"
        f"Email: {email}\n\n"
        f"I request the cyber department to investigate this matter."
    )
