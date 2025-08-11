import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- File Paths ---
INPUT_PDF_DIR = "data"
OUTPUT_DATA_DIR = "output"

# --- OCR Settings ---
PDF_DPI = 300
TESSERACT_CONFIG = "--psm 6"
