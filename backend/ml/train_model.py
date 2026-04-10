# ml/train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def main():
    # 1) Sample training data — now 3 CLASSES (scam, legit, course)
    data = [
        # ----------------------- SCAM MESSAGES -----------------------
        ("Work from home and earn ₹5000 per day. Pay ₹299 registration fee to start.", "scam"),
        ("Congratulations! You are selected for Amazon data entry. Send ₹499 for ID card.", "scam"),
        ("Part time job: Earn ₹2000 daily from mobile. Join our Telegram group and pay joining fee.", "scam"),
        ("Urgent hiring! No interview, no experience. Pay security deposit and start immediately.", "scam"),
        ("You have won a lottery job offer. Pay processing charge to receive appointment letter.", "scam"),
        ("Get instant income by doing simple tasks on Telegram. Pay ₹299 to activate your account.", "scam"),
        ("Dear candidate, pay ₹999 today and get guaranteed WFH job in MNC.", "scam"),

        # ----------------------- LEGIT JOB MESSAGES -----------------------
        ("We are pleased to invite you for an interview for the role of Software Engineer at our Bangalore office.", "legit"),
        ("Please find attached the job description. Share your updated resume if you are interested.", "legit"),
        ("Your profile is shortlisted for internship. There are no registration charges.", "legit"),
        ("HR from XYZ Pvt Ltd here, can we schedule a technical interview tomorrow at 3 PM?", "legit"),
        ("This is a reminder for your campus placement drive scheduled on Monday at 10 AM.", "legit"),
        ("Kindly fill this official company form before the interview. There is no fee involved.", "legit"),
        ("Your interview slot for the Software Developer role has been confirmed. Please carry your resume and ID proof.", "legit"),

        # ----------------------- PAID COURSE / TRAINING (new class) -----------------------
        ("Pay ₹999 and enroll in our Python full-stack development course.", "course"),
        ("Join our digital marketing workshop for ₹499. Limited seats!", "course"),
        ("Upskill yourself with our AI certification program. Course fee ₹1999.", "course"),
        ("Register for our premium job-oriented training program for ₹1499.", "course"),
        ("Pay ₹599 to join our resume-building masterclass.", "course"),
        ("Our company offers Java training with placement assistance. Course fee applicable.", "course"),
        ("Attend our cloud computing bootcamp. Registration charge: ₹799.", "course"),
    ]

    df = pd.DataFrame(data, columns=["text", "label"])

    # 2) Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )

    # 3) Pipeline: TF-IDF + Logistic Regression (multi-class)
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english"
        )),
        ("clf", LogisticRegression(max_iter=2000, multi_class="auto"))
    ])

    # 4) Train model
    pipeline.fit(X_train, y_train)

    # 5) Evaluate model
    y_pred = pipeline.predict(X_test)
    print("\n===== MODEL EVALUATION =====")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # 6) Save model
    os.makedirs("ml", exist_ok=True)
    model_path = os.path.join("backend", "ml", "scam_detector_model_3class.joblib")
    joblib.dump(pipeline, model_path)
    print(f"\nModel saved as {model_path}")

if __name__ == "__main__":
    main()
