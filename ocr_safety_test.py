from ocr_engine import extract_text
from safety_analyzer import analyze_text


def run_ocr_safety_test():
    print("\n================================")
    print("       SURAKSHAAI OCR")
    print("================================\n")

    image_path = input("Enter image filename: ").strip()

    print("\n🔍 Reading image...")

    extracted_text = extract_text(image_path)

    if not extracted_text:
        print("\n❌ No text could be detected.")
        return

    print("\n===== EXTRACTED TEXT =====")
    print(extracted_text)

    print("\n🛡️ Analyzing message...")

    result = analyze_text(extracted_text)

    print("\n===== SURAKSHAAI RESULT =====")
    print("Risk Level:", result["risk_level"])
    print("Risk Score:", result["risk_score"])

    print("\nHigh Risk Indicators:")
    if result["high_risk_indicators"]:
        for item in result["high_risk_indicators"]:
            print(" -", item)
    else:
        print(" - None")

    print("\nMedium Risk Indicators:")
    if result["medium_risk_indicators"]:
        for item in result["medium_risk_indicators"]:
            print(" -", item)
    else:
        print(" - None")

    print("\nDetected URLs:")
    if result["detected_urls"]:
        for url in result["detected_urls"]:
            print(" -", url)
    else:
        print(" - None")

    print("\n💡 Safety Recommendation:")
    print(result["recommendation"])

    print("\n================================")
    print("       ANALYSIS COMPLETE")
    print("================================")


if __name__ == "__main__":
    run_ocr_safety_test()