# app/crud.py

from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

def create_scam_report(db: Session, report: schemas.ScamReportCreate) -> models.ScamReport:
    db_obj = models.ScamReport(
        message_text=report.message_text,
        label=report.label,
        confidence=report.confidence,
        phone=report.phone,
        email=report.email,
        source=report.source,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def count_reports_by_phone(db: Session, phone: Optional[str]) -> int:
    if not phone:
        return 0
    return db.query(models.ScamReport).filter(models.ScamReport.phone == phone).count()

def count_reports_by_email(db: Session, email: Optional[str]) -> int:
    if not email:
        return 0
    return db.query(models.ScamReport).filter(models.ScamReport.email == email).count()

def get_reports_by_contact(db: Session, phone: Optional[str] = None, email: Optional[str] = None) -> List[models.ScamReport]:
    query = db.query(models.ScamReport)
    if phone:
        query = query.filter(models.ScamReport.phone == phone)
    if email:
        query = query.filter(models.ScamReport.email == email)
    return query.order_by(models.ScamReport.created_at.desc()).all()

def get_all_reports(db: Session) -> List[models.ScamReport]:
    """
    Returns all scam reports ordered by newest first.
    """
    return db.query(models.ScamReport).order_by(models.ScamReport.created_at.desc()).all()
