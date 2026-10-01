import os
import shutil
import pytesseract
from PIL import Image


def configure_tesseract():
    # Windows
    windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(windows_path):
        pytesseract.pytesseract.tesseract_cmd = windows_path
        return

    # Cloud/Linux
    linux_path = shutil.which("tesseract")

    if linux_path:
        pytesseract.pytesseract.tesseract_cmd = linux_path


configure_tesseract()


def extract_text(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()

    except Exception as e:
        return f"OCR Error: {e}"