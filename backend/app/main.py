from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import Base, engine, get_db
from . import crud, schemas
from ml.model_utils import (
    classify_message,
    extract_risk_reasons,
    generate_advice,
    generate_complaint_template,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="3-Class Job Scam Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_message", response_model=schemas.AnalyzeResponse)
def analyze_message(data: schemas.AnalyzeRequest, db: Session = Depends(get_db)):
    
    label, probabilities = classify_message(data.message)
    confidence = probabilities.get(label, 0.0)

    risk_reasons = extract_risk_reasons(data.message, label)
    advice = generate_advice(label, confidence)
    complaint = generate_complaint_template(data.message, data.phone, data.email)

    phone_count = crud.count_reports_by_phone(db, data.phone)
    email_count = crud.count_reports_by_email(db, data.email)

    return schemas.AnalyzeResponse(
        label=label,
        confidence=confidence,
        probabilities=probabilities,
        risk_reasons=risk_reasons,
        advice=advice,
        complaint_template=complaint,
        known_reports_count_for_phone=phone_count,
        known_reports_count_for_email=email_count,
    )


@app.post("/report_scam", response_model=schemas.ScamReportOut)
def report_scam(report: schemas.ScamReportCreate, db: Session = Depends(get_db)):
    return crud.create_scam_report(db, report)


@app.get("/reports/by_contact", response_model=List[schemas.ScamReportOut])
def get_reports_by_contact(phone: str | None = None, email: str | None = None,
                           db: Session = Depends(get_db)):
    return crud.get_reports_by_contact(db, phone, email)


@app.get("/reports/all", response_model=List[schemas.ScamReportOut])
def get_all_reports(db: Session = Depends(get_db)):
    return crud.get_all_reports(db)
