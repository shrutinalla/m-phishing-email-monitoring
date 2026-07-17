# Risk score for each suspicious keyword

KEYWORD_SCORES = {
    "urgent": 5,
    "verify": 8,
    "password": 10,
    "login": 8,
    "account": 6,
    "bank": 8,
    "payment": 7,
    "invoice": 6,
    "click here": 5,
    "confirm": 4,
    "update": 3,
    "security alert": 6,
    "reset password": 10,
    "otp": 10,
    "immediately": 3
}
def calculate_risk_score(found_words, patterns):
    """
    Calculates phishing risk score using weighted keywords
    and phishing patterns.
    """

    score = 0
    reasons = []

    # Score based on suspicious words
    for word in found_words:
        if word in KEYWORD_SCORES:
            score += KEYWORD_SCORES[word]
            reasons.append(
                f"Detected suspicious keyword: '{word}' (+{KEYWORD_SCORES[word]})"
            )

    # Pattern scores
    if patterns["shortened_url"]:
        score += 20
        reasons.append("Shortened URL detected (+20)")

    if patterns["multiple_exclamation"]:
        score += 10
        reasons.append("Multiple exclamation marks detected (+10)")

    capital_count = len(patterns["capital_words"])

    if capital_count > 0:
        capital_score = capital_count * 2
        score += capital_score
        reasons.append(
            f"{capital_count} ALL CAPS words detected (+{capital_score})"
        )

    score = min(score, 100)

    return score, reasons
def get_risk_level(score):

    if score >= 60:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    return "LOW"
if __name__ == "__main__":

    from suspicious_words import (
        find_suspicious_words,
        detect_patterns
    )

    sample_text = """
    URGENT!!!

    Your ACCOUNT has been suspended.

    Click here immediately to VERIFY your PASSWORD.

    Visit:
    https://bit.ly/security-check
    """

    words = find_suspicious_words(sample_text)

    patterns = detect_patterns(sample_text)

    score, reasons = calculate_risk_score(words, patterns)

    level = get_risk_level(score)

    print("\n===== RISK ANALYSIS =====")

    print("\nWords Found:")
    print(words)

    print("\nPatterns:")
    print(patterns)

    print("\nRisk Score:", score)

    print("Risk Level:", level)

    print("\nReasons:")

    for reason in reasons:
        print("-", reason)