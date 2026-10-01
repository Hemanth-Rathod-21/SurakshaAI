import re
from urllib.parse import urlparse


# Suspicious words commonly found in scam links
SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "account",
    "secure",
    "update",
    "kyc",
    "bank",
    "wallet",
    "payment",
    "claim",
    "reward",
    "prize",
    "free",
]


def check_link(url):
    """
    Perform a basic safety check on a URL.
    This is an awareness-oriented heuristic,
    not a definitive malware/phishing detector.
    """

    url = url.strip()

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

    except Exception:
        return {
            "risk_level": "UNKNOWN",
            "risk_score": 0,
            "reasons": ["Invalid URL format."]
        }

    score = 0
    reasons = []

    # HTTP instead of HTTPS
    if parsed.scheme == "http":
        score += 25
        reasons.append(
            "The link does not use HTTPS."
        )

    # Suspicious words
    combined_text = domain + path

    found_words = []

    for word in SUSPICIOUS_WORDS:
        if word in combined_text:
            found_words.append(word)

    if found_words:
        score += min(len(found_words) * 10, 40)

        reasons.append(
            "Contains potentially suspicious keywords: "
            + ", ".join(found_words)
        )

    # IP address instead of normal domain
    ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    if re.match(ip_pattern, domain):
        score += 30
        reasons.append(
            "The link uses an IP address instead of a normal domain."
        )

    # Very long URL
    if len(url) > 100:
        score += 15
        reasons.append(
            "The URL is unusually long."
        )

    score = min(score, 100)

    if score >= 50:
        risk_level = "HIGH RISK"

    elif score >= 20:
        risk_level = "MEDIUM RISK"

    else:
        risk_level = "LOW RISK"

    if not reasons:
        reasons.append(
            "No major warning signs were detected by the basic checks."
        )

    return {
        "risk_level": risk_level,
        "risk_score": score,
        "reasons": reasons,
    }