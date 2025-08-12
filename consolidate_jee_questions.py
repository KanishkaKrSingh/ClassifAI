# import pandas as pd
# import json
# import glob
# import os
#
#
# def consolidate_questions(json_folder_path, output_csv_path):
#     """
#     Reads all JSON files from a folder, extracts question data,
#     and consolidates it into a single Pandas DataFrame, saving it as a CSV.
#     """
#     json_files = glob.glob(os.path.join(json_folder_path, '*.json'))
#
#     if not json_files:
#         print(f"No JSON files found in '{json_folder_path}'.")
#         return
#
#     all_questions_data = []
#     print(f"Found {len(json_files)} JSON files. Starting consolidation...")
#
#     for file_path in json_files:
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 # Assuming each JSON file contains a list of question objects
#                 # or a single question object. Let's handle both.
#                 data = json.load(f)
#
#                 # If the json file is a list of questions
#                 if isinstance(data, list):
#                     for question in data:
#                         all_questions_data.append(question)
#                 # If the json file is a single question object
#                 elif isinstance(data, dict):
#                     all_questions_data.append(data)
#
#         except Exception as e:
#             print(f"An error occurred while processing {file_path}: {e}")
#
#     df = pd.DataFrame(all_questions_data)
#
#     # Ensure all expected columns exist, fill with None if not
#     expected_cols = ['id', 'source_paper', 'question_text', 'options', 'subject', 'chapter', 'difficulty', 'type']
#     for col in expected_cols:
#         if col not in df.columns:
#             df[col] = None
#
#     df = df[expected_cols]  # Ensure consistent column order
#
#     df.to_csv(output_csv_path, index=False)
#     print(f"\n✅ Success! Consolidated {len(df)} questions into '{output_csv_path}'")
#     return df
#
#
# # --- USAGE ---
# # 1. Set the path to your folder of JSON files
# JSON_DIRECTORY = 'output'
#
# # 2. Set the desired name for the output file
# RAW_DATA_CSV = 'consolidated_jee_questions.csv'
#
# # 3. Run the function
# consolidate_questions(JSON_DIRECTORY, RAW_DATA_CSV)

import pandas as pd

import numpy as np



def clean_question_dataframe(input_csv_path):

  """

  Loads a CSV of consolidated questions and filters out low-quality

  or spoiled entries based on a set of heuristics.



  Args:

    input_csv_path (str): Path to the consolidated CSV file.



  Returns:

    pandas.DataFrame: A cleaned DataFrame with only high-quality questions.

  """

  try:

    df = pd.read_csv(input_csv_path)

  except FileNotFoundError:

    print(f"Error: The file '{input_csv_path}' was not found.")

    return pd.DataFrame()



  print(f"Initial dataset size: {len(df)} questions")



  # --- Rule 1: Filter out questions with very short or missing text ---

  # A real question needs a meaningful amount of text.

  initial_count = len(df)

  df.dropna(subset=['question_text'], inplace=True)

  df = df[df['question_text'].str.len() > 25] # A reasonable minimum length

  print(f"Removed {initial_count - len(df)} rows with short/missing question text.")

 

  # --- Rule 2: Filter out questions with no options (for MCQs) ---

  # This assumes 'options' is a string representation of a list, e.g., "['(a) 12m', ...]"

  # If not, you may need to adjust the logic.

  initial_count = len(df)

  # The line below handles both actual lists and string representations of empty lists '[]'

  df = df[df['options'].str.len() > 5]

  print(f"Removed {initial_count - len(df)} rows with missing options.")



  # --- Rule 3: Filter out gibberish based on character types ---

  # A high ratio of non-alphanumeric characters can indicate OCR failure.

  initial_count = len(df)

  def is_gibberish(text):

    if not isinstance(text, str) or len(text) == 0:

      return True

    # Calculate the proportion of alphabetic characters

    alpha_chars = sum(c.isalpha() for c in text)

    proportion = alpha_chars / len(text)

    # If less than 60% of characters are letters, flag as potential gibberish

    return proportion < 0.6



  df = df[~df['question_text'].apply(is_gibberish)]

  print(f"Removed {initial_count - len(df)} rows flagged as potential gibberish.")





  print(f"\nFinal cleaned dataset size: {len(df)} questions")

 

  return df



# --- USAGE ---

RAW_DATA_CSV = 'consolidated_jee_questions.csv'

cleaned_df = clean_question_dataframe(RAW_DATA_CSV)



# Save the cleaned data to a new file to keep the original safe

if not cleaned_df.empty:

  cleaned_df.to_csv('cleaned_jee_questions.csv', index=False)

  print(f"\n✅ Cleaned data saved to 'cleaned_jee_questions.csv'")

  print("\nHere's a sample of the clean data:")

  print(cleaned_df.head())