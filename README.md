# AI Resume Ranking System 🚀

A Streamlit-based application that ranks resumes against a job description using NLP techniques.

---

## 📌 Overview

This project allows users to:

- Upload multiple resumes (PDF or DOCX)
- Paste a job description
- Automatically calculate similarity scores
- Rank candidates based on relevance
- Store ranking results in a MySQL database

The system uses **TF-IDF vectorization** and **Cosine Similarity** to compare resumes with the job description.

---

## 🧠 How It Works

1. Resume text is extracted using `PyPDF2` (PDF) and `python-docx` (DOCX).
2. Text is cleaned and preprocessed.
3. The job description and resumes are vectorized using **TF-IDF**.
4. **Cosine similarity** calculates relevance scores.
5. Resumes are ranked from highest to lowest score.
6. Results are stored in a MySQL database for persistence.

---

## 🛠 Tech Stack

- Python
- Streamlit
- MySQL
- scikit-learn
- Pandas
- NumPy
- PyPDF2
- python-docx
- python-dotenv

---

## 📂 Project Structure
resume-ranking-system/
│
├── app.py # Streamlit UI
├── db_utils.py # Database connection & queries
├── utils.py # NLP & file parsing logic
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
