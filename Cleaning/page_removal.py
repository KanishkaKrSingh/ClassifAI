import os
import fitz  # PyMuPDF

# Path to the 'data' folder (relative to this script)
cleaning_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

for filename in os.listdir(cleaning_dir):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(cleaning_dir, filename)
        temp_path = os.path.join(cleaning_dir, f"temp_{filename}")

        doc = fitz.open(pdf_path)

        if doc.page_count <= 1:
            print(f"Skipped (only 1 page): {filename}")
            doc.close()
            continue

        doc.delete_page(doc.page_count - 1)
        doc.save(temp_path, garbage=4)
        doc.close()

        os.replace(temp_path, pdf_path)
        print(f"✔ Last page removed: {filename}")
