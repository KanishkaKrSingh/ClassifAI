# text_parser.py

import os
import re
import json
import google.generativeai as genai
import config

# Configure the Gemini client securely using the key from config
if not config.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
genai.configure(api_key="AIzaSyDaVXe8MSt-0GHDJy0QLNSwjCgtDn3NzUs")


def clean_text_with_gemini(raw_text: str) -> str:
    """Uses Gemini to clean and format raw OCR text."""
    print("INFO: Sending text to Gemini for cleaning...")

    # Initialize the Gemini model. 'gemini-1.5-flash-latest' is fast and cost-effective.
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = f"""
    You are an expert assistant that extracts and formats exam questions from raw OCR text. Preserve the original text, including all mathematical symbols and equations, exactly as they are.
    Please extract all valid questions and their options from the OCR text below. Also, avoid any extra text that u extract 
    Format each question strictly like this, ensuring all original text and symbols are kept:

    You must output ONLY in this exact format with no extra text:
    Q1. Question text
    (a) Option A
    (b) Option B
    (c) Option C
    (d) Option D
    
    - Always start questions with Q<number>.
    - Always label options exactly as (a), (b), (c), (d) each on its own line.
    - Do NOT add explanations, headings, or any text before Q1.
    
    OCR TEXT:
    {raw_text}
    """

    try:
        response = model.generate_content(prompt)
        cleaned_text = response.text
        print("INFO: Gemini cleaning successful.")
        return cleaned_text
    except Exception as e:
        print(f"ERROR: Failed to call Gemini API. {e}")
        return ""


def structure_cleaned_text(cleaned_text: str, source_paper: str) -> list[dict]:
    """Parses the cleaned text from the LLM into a structured list of dictionaries."""
    print("INFO: Structuring cleaned text into JSON format...")
    pattern = re.compile(r'(Q\d+)\.\s(.*?)\n((?:\([a-d]\).*?(?:\n|$))+)', re.DOTALL)

    matches = pattern.findall(cleaned_text)
    structured_data = []

    for i, match in enumerate(matches):
        q_num_raw, q_text, options_raw = match

        question_text = q_text.strip().replace('\n', ' ')
        options_list = [opt.strip() for opt in options_raw.strip().split('\n') if opt.strip()]

        structured_data.append({
            "id": f"{os.path.basename(source_paper).replace('.pdf', '')}_{i + 1}",
            "source_paper": source_paper,
            "question_text": question_text,
            "options": options_list,
            "subject": None,
            "chapter": None,
            "difficulty": None,
            "type": None
        })
    print(f"INFO: Successfully structured {len(structured_data)} questions.")
    return structured_data