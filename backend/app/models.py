# app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class ScamReport(Base):
    __tablename__ = "scam_reports"

    id = Column(Integer, primary_key=True, index=True)
    message_text = Column(String, nullable=False)
    label = Column(String, nullable=False)            # "scam" / "legit" / "doubtful"
    confidence = Column(Float, nullable=False)        # probability of the predicted label
    phone = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    source = Column(String, nullable=True)            # "whatsapp", "telegram", "email", etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
