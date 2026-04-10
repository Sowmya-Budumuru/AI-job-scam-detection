from pydantic import BaseModel
from datetime import datetime

class AnalyzeRequest(BaseModel):
    message: str
    phone: str | None = None
    email: str | None = None
    source: str | None = None

class AnalyzeResponse(BaseModel):
    label: str                 # scam, legit, or course
    confidence: float
    probabilities: dict
    risk_reasons: list
    advice: str
    complaint_template: str
    known_reports_count_for_phone: int
    known_reports_count_for_email: int

class ScamReportCreate(BaseModel):
    message_text: str
    label: str
    confidence: float
    phone: str | None = None
    email: str | None = None
    source: str | None = None

class ScamReportOut(BaseModel):
    id: int
    message_text: str
    label: str
    confidence: float
    phone: str | None
    email: str | None
    source: str | None
    created_at: datetime

    class Config:
        orm_mode = True
