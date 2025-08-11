import os
import re

# Path to your data folder
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# List all files in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith('.pdf'):
        # Match year and optional date info
        match = re.search(r'JEE Main (\d{4})(?: \((.*?)\))?', filename)

        if match:
            year = match.group(1)
            details = match.group(2)  # this could be "07 Apr Online", etc.

            new_name = f"JEE_Main_{year}"
            if details:
                # Clean details to format like 07_Apr_Online
                cleaned_details = '_'.join(details.split())
                new_name += f"_{cleaned_details}"

            new_name += '.pdf'

            # Old and new full paths
            old_path = os.path.join(data_dir, filename)
            new_path = os.path.join(data_dir, new_name)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")
        else:
            print(f"Skipped: {filename}")
