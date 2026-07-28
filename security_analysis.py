from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from security_schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
)

from security_service import (
    detect_suspicious_words,
    calculate_risk_score,
    analyze_trends,
    detect_threat_type,
)

router = APIRouter(
    prefix="/security",
    tags=["Security Analysis"]
)


@router.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze_email(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    suspicious_words = detect_suspicious_words(
        request.subject,
        request.body
    )

    risk_score, risk_level, reasons = calculate_risk_score(
        request.difficulty,
        suspicious_words,
        request.has_attachment,
        request.subject,
        request.body
    )

    threat_type = detect_threat_type(
        request.subject,
        request.body
    )

    trend_analysis = analyze_trends(db)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "threat_type": threat_type,
        "suspicious_words": suspicious_words,
        "reasons": reasons,
        "trend_analysis": trend_analysis,
    }