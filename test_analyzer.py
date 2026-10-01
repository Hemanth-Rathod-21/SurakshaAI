from safety_analyzer import analyze_text


message = """
URGENT! Your bank account will be blocked.
Verify your account immediately.
Send your OTP and click https://example.com
"""


result = analyze_text(message)


print("\n===== SURAKSHAAI ANALYSIS =====")
print("Risk Level:", result["risk_level"])
print("Risk Score:", result["risk_score"])
print("High Risk Indicators:", result["high_risk_indicators"])
print("Medium Risk Indicators:", result["medium_risk_indicators"])
print("Detected URLs:", result["detected_urls"])
print("Recommendation:", result["recommendation"])