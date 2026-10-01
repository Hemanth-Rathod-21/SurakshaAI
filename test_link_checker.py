from link_checker import check_link


url = input("Enter a URL to check: ")

result = check_link(url)

print("\n===== SURAKSHAAI LINK CHECK =====")

print("Risk Level:", result["risk_level"])
print("Risk Score:", result["risk_score"])

print("\nReasons:")

for reason in result["reasons"]:
    print("-", reason)