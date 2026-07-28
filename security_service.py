import re
from sqlalchemy.orm import Session

from campaign_models import Campaign
from tracking_models import ClickLog


SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "password",
    "login",
    "signin",
    "credential",
    "account",
    "security",
    "click",
    "confirm",
    "bank",
    "payment",
    "invoice",
    "salary",
    "tax",
    "hr",
    "vpn",
    "otp",
    "pin",
    "gift card",
    "wire transfer",
    "reset",
    "immediately",
    "act now",
    "expires today",
    "limited time"
]


def detect_suspicious_words(subject: str, body: str):
    """
    Detect phishing-related keywords from subject and email body.
    """
    text = f"{subject} {body}".lower()

    detected = []

    for word in SUSPICIOUS_KEYWORDS:
        if word in text:
            detected.append(word)

    return detected


def get_risk_level(score):
    if score <= 25:
        return "Low"
    elif score <= 50:
        return "Medium"
    elif score <= 75:
        return "High"
    else:
        return "Critical"


def detect_threat_type(subject, body):
    text = f"{subject} {body}".lower()

    if any(word in text for word in ["password", "login", "credential", "verify"]):
        return "Credential Harvesting"

    if any(word in text for word in ["invoice", "payment", "bank"]):
        return "Financial Fraud"

    if any(word in text for word in ["salary", "hr", "tax"]):
        return "Business Email Compromise"

    if any(word in text for word in ["otp", "pin"]):
        return "OTP Theft"

    return "General Phishing"


def calculate_risk_score(
    difficulty: str,
    suspicious_words: list,
    has_attachment: bool,
    subject: str,
    body: str
):
    """
    Calculates phishing risk score.
    """

    score = 0
    reasons = []

    difficulty_scores = {
        "Low": 10,
        "Medium": 25,
        "High": 40,
        "Critical": 55
    }

    score += difficulty_scores.get(difficulty, 10)

    reasons.append(f"{difficulty} difficulty selected")

    keyword_score = min(len(suspicious_words) * 5, 25)

    if keyword_score > 0:
        score += keyword_score
        reasons.append(
            f"{len(suspicious_words)} suspicious keywords detected"
        )

    if has_attachment:
        score += 10
        reasons.append("Email contains attachment")

    # ALL CAPS subject
    if subject.isupper() and len(subject) > 8:
        score += 5
        reasons.append("Subject uses excessive uppercase")

    # Multiple exclamation marks
    if body.count("!") >= 3:
        score += 5
        reasons.append("Urgency punctuation detected")

    # URL Detection
    url_patterns = [
        "http://",
        "https://",
        "www.",
        "bit.ly",
        "tinyurl"
    ]

    if any(url in body.lower() for url in url_patterns):
        score += 10
        reasons.append("External link detected")

    score = min(score, 100)

    risk_level = get_risk_level(score)

    return score, risk_level, reasons


def analyze_trends(db: Session):
    """
    Analyze historical phishing campaign trends.
    """

    campaigns = db.query(Campaign).all()
    click_logs = db.query(ClickLog).all()

    total_campaigns = len(campaigns)
    total_clicks = len(click_logs)

    if total_campaigns == 0:
        return {
            "overall_trend": "No Data",
            "average_click_rate": 0,
            "high_risk_campaigns": 0,
            "total_campaigns": 0,
            "total_clicks": 0,
            "most_common_difficulty": "N/A"
        }

    average_click_rate = round(
        total_clicks / total_campaigns,
        2
    )

    difficulty_count = {}

    for campaign in campaigns:
        difficulty = campaign.difficulty

        difficulty_count[difficulty] = (
            difficulty_count.get(difficulty, 0) + 1
        )

    most_common_difficulty = max(
        difficulty_count,
        key=difficulty_count.get
    )

    high_risk_campaigns = len(
        [
            campaign
            for campaign in campaigns
            if campaign.difficulty in ["High", "Critical"]
        ]
    )

    if average_click_rate >= 3:
        trend = "Increasing"
    elif average_click_rate >= 1:
        trend = "Stable"
    else:
        trend = "Low"

    return {
        "overall_trend": trend,
        "average_click_rate": average_click_rate,
        "high_risk_campaigns": high_risk_campaigns,
        "total_campaigns": total_campaigns,
        "total_clicks": total_clicks,
        "most_common_difficulty": most_common_difficulty
    }