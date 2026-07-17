import re

# Common phishing keywords
SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "password",
    "login",
    "account",
    "bank",
    "payment",
    "invoice",
    "click here",
    "confirm",
    "update",
    "security alert",
    "reset password",
    "otp",
    "immediately"
]
def find_suspicious_words(text):
    """
    Finds phishing-related keywords in the given text.
    Returns a list of matched words.
    """

    text = text.lower()

    found_words = []

    for word in SUSPICIOUS_KEYWORDS:
        if word in text:
            found_words.append(word)

    return found_words
def detect_patterns(text):
    """
    Detects common phishing patterns in the email.
    Returns a dictionary of detected patterns.
    """

    patterns = {
        "shortened_url": False,
        "multiple_exclamation": False,
        "capital_words": []
    }

    # Detect shortened URLs
    short_urls = ["bit.ly", "tinyurl.com", "goo.gl", "t.co"]

    for url in short_urls:
        if url.lower() in text.lower():
            patterns["shortened_url"] = True
            break

    # Detect multiple exclamation marks
    if "!!!" in text:
        patterns["multiple_exclamation"] = True

    # Detect words written in ALL CAPS
    capital_words = re.findall(r"\b[A-Z]{3,}\b", text)
    patterns["capital_words"] = capital_words

    return patterns






if __name__ == "__main__":

    sample_text = """
    URGENT!!!

    Your ACCOUNT has been suspended.

    Click here immediately to VERIFY your PASSWORD.

    Visit: https://bit.ly/security-check
    """

    words = find_suspicious_words(sample_text)
    patterns = detect_patterns(sample_text)

    print("Suspicious Words:")
    print(words)

    print("\nDetected Patterns:")
    print(patterns)





# if __name__ == "__main__":

#     sample_text = """
#     URGENT!

#     Your account has been suspended.

#     Click here immediately to verify your password.
#     """

#     result = find_suspicious_words(sample_text)

#     print("Suspicious Words Found:")
#     print(result)