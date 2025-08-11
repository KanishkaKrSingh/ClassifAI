# main.py

import os
import json
import config
from ocr_extractor import extract_text_from_pdf
# Updated import to use the new function names
from text_parser import clean_text_with_gemini, structure_cleaned_text


def process_single_paper(pdf_path: str):
    """
    Runs the full pipeline for a single PDF paper.
    """
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found at {pdf_path}")
        return

    print(f"\n{'=' * 20} PROCESSING: {os.path.basename(pdf_path)} {'=' * 20}")

    # --- Step 1: Extract Raw Text using OCR ---
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text:
        print("ERROR: OCR extraction failed, aborting.")
        return

    # --- Step 2: Clean Raw Text using Gemini ---
    cleaned_text = clean_text_with_gemini(raw_text)  # Updated function call
    if not cleaned_text:
        print("ERROR: LLM cleaning failed, aborting.")
        return

    # --- Step 3: Structure Cleaned Text ---
    paper_name = os.path.basename(pdf_path)
    final_data = structure_cleaned_text(cleaned_text, paper_name)  # Updated function call

    # --- Step 4: Save the Final JSON Output ---
    if final_data:
        os.makedirs(config.OUTPUT_DATA_DIR, exist_ok=True)
        output_filename = paper_name.replace('.pdf', '.json')
        output_path = os.path.join(config.OUTPUT_DATA_DIR, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4)

        print(f"\n✅ SUCCESS: Pipeline complete. Structured data saved to {output_path}")
    else:
        print("\n❌ FAILURE: No questions could be structured from the paper.")


if __name__ == "__main__":
    # Define the single paper you want to process for testing
    target_paper_name = r"JEE_Main_2002.pdf"  # Make sure this matches your test file name
    pdf_file_path = os.path.join(config.INPUT_PDF_DIR, target_paper_name)

    process_single_paper(pdf_file_path)