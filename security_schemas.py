from pydantic import BaseModel
from typing import List


class AnalyzeRequest(BaseModel):
    subject: str
    body: str
    difficulty: str
    has_attachment: bool = False


class TrendAnalysis(BaseModel):
    overall_trend: str
    average_click_rate: float
    high_risk_campaigns: int
    total_campaigns: int
    total_clicks: int
    most_common_difficulty: str


class AnalyzeResponse(BaseModel):
    risk_score: int
    risk_level: str
    threat_type: str
    suspicious_words: List[str]
    reasons: List[str]
    trend_analysis: TrendAnalysis