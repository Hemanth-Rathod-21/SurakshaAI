import re


# Common suspicious words/phrases
HIGH_RISK_KEYWORDS = [
    "otp",
    "one time password",
    "password",
    "pin",
    "cvv",
    "bank account",
    "account blocked",
    "account will be blocked",
    "verify your account",
    "click immediately",
    "urgent",
    "send money",
    "transfer money",
    "upi",
    "payment failed",
    "kyc expired",
    "kyc update",
]

MEDIUM_RISK_KEYWORDS = [
    "click here",
    "claim now",
    "limited time",
    "congratulations",
    "winner",
    "prize",
    "offer",
    "free",
    "refund",
    "cashback",
]


def analyze_text(text):
    """
    Analyze extracted message text and return
    a simple SurakshaAI risk assessment.
    """

    text_lower = text.lower()

    high_matches = [
        keyword for keyword in HIGH_RISK_KEYWORDS
        if keyword in text_lower
    ]

    medium_matches = [
        keyword for keyword in MEDIUM_RISK_KEYWORDS
        if keyword in text_lower
    ]

    # Detect URLs
    urls = re.findall(
        r"https?://\S+|www\.\S+",
        text_lower
    )

    # Calculate a simple risk score
    score = 0

    score += len(high_matches) * 25
    score += len(medium_matches) * 10

    if urls:
        score += 20

    score = min(score, 100)

    # Determine risk level
    if score >= 50:
        risk_level = "HIGH RISK"
    elif score >= 20:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"

    # Recommendation
    if risk_level == "HIGH RISK":
        recommendation = (
            "Do not click links, share OTP/passwords, "
            "or transfer money. Verify the message "
            "through an official source."
        )

    elif risk_level == "MEDIUM RISK":
        recommendation = (
            "Be cautious. Do not click unknown links "
            "and verify the sender before taking action."
        )

    else:
        recommendation = (
            "No major warning signs were detected. "
            "Still verify unexpected requests."
        )

    return {
        "risk_level": risk_level,
        "risk_score": score,
        "high_risk_indicators": high_matches,
        "medium_risk_indicators": medium_matches,
        "detected_urls": urls,
        "recommendation": recommendation,
    }