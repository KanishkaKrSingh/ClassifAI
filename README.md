# 📄 ClassifAI

**An AI-powered system for automated classification and analysis of competitive exam questions.**  
Designed to work on **JEE Mains & Advanced** exam papers, **ClassifAI** leverages OCR and deep learning (Transformers) to extract, process, and classify questions by type, difficulty, and subject.

---

## 🚀 Features

- **PDF/Image Processing**
  - Removes irrelevant pages (e.g., answer keys)
  - Preprocesses scanned pages (brightness, binarization, denoising)
- **OCR Extraction**
  - Google Vision API / Tesseract-based text extraction
  - Handles faint watermarks and noisy backgrounds
- **Question Segmentation**
  - Regex-based detection of question boundaries
- **AI Classification**
  - Type detection: Numerical / Theoretical
  - Difficulty grading: Easy / Hard (binary for higher accuracy)
  - Subject & topic tagging (Physics, Chemistry, Mathematics)
- **Repetition Detection**
  - Uses transformer embeddings + cosine similarity to detect similar questions
- **Scalable Backend (Planned)**
  - Django REST API for uploading papers and retrieving predictions

---

## 🧠 Tech Stack

| Component            | Technology |
|----------------------|------------|
| **OCR**              | Google Vision API / Tesseract |
| **DL Models**        | HuggingFace Transformers (BERT / DistilBERT) |
| **Preprocessing**    | OpenCV, Pillow, pdf2image |
| **Backend (Planned)**| Django + DRF |
| **Deployment (Planned)** | Docker + Railway / Render |
| **Database (Optional)** | PostgreSQL / SQLite |

---

## 📂 Project Structure

ClassifAI/
│── data/ # PDF & Image datasets
│── notebooks/ # Experiments & prototyping
│── preprocessing/ # Image & text cleaning scripts
│── models/ # Model training & fine-tuning code
│── backend/ # Django API (planned)
│── utils/ # Helper functions
│── README.md # Project documentation


---

## 📊 Workflow

1. **Preprocessing**
   - Remove answer key pages
   - Convert PDF → images
   - Apply brightness boost + thresholding
2. **OCR Extraction**
   - Extract clean text from scanned papers
3. **Question Segmentation**
   - Use regex to split into individual questions
4. **Classification**
   - Apply fine-tuned BERT/DistilBERT model
5. **Similarity Check**
   - Detect repeated/near-duplicate questions

---

## 🔮 Future Improvements

- Add **symbolic math parsing** (Mathpix API)
- Enhance diagram detection and interpretation
- Expand difficulty grading to Easy / Medium / Hard
- Deploy as a **public web app** with an interactive dashboard

---

## 🏗 Current Status

- ✅ PDF preprocessing pipeline under development
- ✅ OCR accuracy testing on watermarked papers
- 🔄 Dataset labeling in progress (Easy/Hard classification)
- 🔜 Transformer fine-tuning

---

## 📜 License

MIT License – feel free to use, modify, and distribute with attribution.

---

## 👤 Author

**Kanishka Kumar Singh**  
**Varun Kant**
**Krrish Sagar**
B.Tech, Computer Science @ BIT Mesra  
Core Member – Google Developers Students’ Club 
