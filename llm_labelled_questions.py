import pandas as pd
import json
import time
import os
import requests  # Using the standard 'requests' library for simplicity

# --- Configuration ---
# IMPORTANT: Replace with your actual API key from Google AI Studio
API_KEY = "AIzaSyADUiR2s-0G9blT8_zaCNQxwzzAORzoEcU"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-preview-0514:generateContent?key={API_KEY}"
HEADERS = {'Content-Type': 'application/json'}


def construct_prompt(question_text):
    """Creates a detailed prompt for the Gemini API for classification."""
    return f"""
    Analyze the following JEE examination question and classify it based on two criteria: difficulty and type.

    **Classification Criteria:**

    1.  **Difficulty:**
        * **Easy:** Requires direct application of a single, common formula or concept. Solvable in one or two steps.
        * **Medium:** Requires combining 2-3 concepts, involves multi-step calculations, or requires a trick or specific insight.
        * **Hard:** Involves complex calculations, requires synthesis of multiple disparate topics, or is based on an obscure or non-obvious concept.

    2.  **Type:**
        * **Numerical:** The question requires a calculation to arrive at a specific numerical answer. Look for numbers, units (like m/s, J, mol), and questions asking for a quantity.
        * **Theoretical:** The question tests conceptual understanding. Look for keywords like "which of the following is true/false," "explain why," "the reason for," or questions that can be answered without calculation.

    **Question to Analyze:**
    "{question_text}"

    **Instructions:**
    Return your response ONLY as a valid JSON object with two keys: "difficulty" and "type". Do not add any other text or markdown formatting.
    Example: {{"difficulty": "Medium", "type": "Numerical"}}
    """


def get_labels_from_api(session, question_text):
    """Sends a single question to the Gemini API and returns the parsed labels."""
    prompt = construct_prompt(question_text)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = session.post(API_URL, headers=HEADERS, data=json.dumps(payload), timeout=60)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)

        # Extract the JSON string from the response
        response_json = response.json()
        text_content = response_json['candidates'][0]['content']['parts'][0]['text']

        # Clean the text content to ensure it's a valid JSON string
        clean_text = text_content.strip().replace("```json", "").replace("```", "")
        labels = json.loads(clean_text)

        return labels.get('difficulty', 'error'), labels.get('type', 'error')

    except requests.exceptions.RequestException as e:
        print(f"Network/HTTP Error: {e}")
        return 'api_error', 'api_error'
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing API response: {e}. Response text: '{response.text if 'response' in locals() else 'N/A'}'")
        return 'parse_error', 'parse_error'


def auto_label_questions(input_csv_path, output_csv_path, sample_size=150, start_index=0):
    """
    Uses the Gemini API to automatically label questions for difficulty and type.
    """
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"Error: The file '{input_csv_path}' was not found.")
        return

    # Select the portion of the dataframe to process
    end_index = start_index + sample_size
    sample_df = df.iloc[start_index:end_index].copy()

    if sample_df.empty:
        print("No questions to process in the specified range.")
        return

    print(f"Starting auto-labeling for {len(sample_df)} questions (from index {start_index} to {end_index - 1})...")

    results = []

    # Use a session object for connection pooling
    with requests.Session() as session:
        for i, row in sample_df.iterrows():
            difficulty, q_type = get_labels_from_api(session, row['question_text'])
            results.append({
                'predicted_difficulty': difficulty,
                'predicted_type': q_type
            })
            print(f"Processed question {i}: Difficulty='{difficulty}', Type='{q_type}'")
            time.sleep(1)  # Add a small delay to respect API rate limits

    # Add the new labels to the DataFrame
    predictions_df = pd.DataFrame(results, index=sample_df.index)
    sample_df['predicted_difficulty'] = predictions_df['predicted_difficulty']
    sample_df['predicted_type'] = predictions_df['predicted_type']

    # Save the newly labeled data
    sample_df.to_csv(output_csv_path, index=False, mode='a' if start_index > 0 else 'w', header=(start_index == 0))

    print(f"\n✅ Auto-labeling complete for this batch!")
    print(f"Labeled data saved/appended to '{output_csv_path}'")


# --- USAGE ---
CLEAN_DATA_CSV = 'cleaned_jee_questions.csv'
LABELED_OUTPUT_CSV = 'llm_labeled_questions.csv'

# Run the function for the first 150 questions
# You can run this multiple times with different start_index values
# to process the file in chunks.
# For example:
# auto_label_questions(CLEAN_DATA_CSV, LABELED_OUTPUT_CSV, sample_size=150, start_index=0)
# auto_label_questions(CLEAN_DATA_CSV, LABELED_OUTPUT_CSV, sample_size=150, start_index=150)
# ...and so on.

auto_label_questions(CLEAN_DATA_CSV, LABELED_OUTPUT_CSV, sample_size=150, start_index=0)
