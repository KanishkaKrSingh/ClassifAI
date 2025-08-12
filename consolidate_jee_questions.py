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