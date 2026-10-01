from ocr_engine import extract_text

image_path = "test_image.png"

text = extract_text(image_path)

print("\n===== OCR RESULT =====\n")
print(text)