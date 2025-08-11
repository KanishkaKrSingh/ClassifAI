# ocr_extractor.py

import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import config  # Import our settings


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Applies advanced preprocessing to an image to improve OCR accuracy."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # Denoising
    denoised = cv2.fastNlMeansDenoising(img_cv, None, 30, 7, 21)

    # Adaptive thresholding using Otsu's method
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Morphological opening to remove small noise
    kernel = np.ones((1, 1), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return opened


import config

def clean_watermark(image):
    """Apply brightness, contrast, and threshold to reduce watermark effect."""
    bright = cv2.convertScaleAbs(image, alpha=1.3, beta=50)
    gray = cv2.cvtColor(bright, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    return binary

def extract_text_from_pdf(pdf_path):
    print(f"INFO: Starting OCR process for {pdf_path}...")
    images = convert_from_path(pdf_path, dpi=config.PDF_DPI)

    all_text = []
    for i, page in enumerate(images, start=1):
        print(f"  -> Processing page {i}/{len(images)}")

        # Convert PIL image to OpenCV format
        page_cv = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        # Clean watermark
        cleaned_page = clean_watermark(page_cv)

        # OCR
        text = pytesseract.image_to_string(cleaned_page, config=config.TESSERACT_CONFIG)
        all_text.append(text)

    print(f"INFO: OCR process completed for {pdf_path}.")
    return "\n".join(all_text)
