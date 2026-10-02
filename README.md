# AI Resume Ranking System

A Streamlit web app that ranks resumes against a job description. Upload a set of PDF or DOCX resumes, paste a job description, and the app scores each resume by how closely its wording matches the job, then shows the results as a sorted table and bar chart and saves them to MySQL.

## How it works

1. **Text extraction:** each uploaded resume is converted to plain text, using PyPDF2 for PDFs and python-docx for Word files.
2. **Cleaning:** the text is lowercased, punctuation is removed, and extra whitespace is collapsed.
3. **TF-IDF vectorization:** the job description and all resumes are turned into TF-IDF vectors with scikit-learn's `TfidfVectorizer` (English stop words removed). TF-IDF gives each word a weight that is high when the word appears often in one document but rarely across the others, so distinctive skills count for more than common words.
4. **Cosine similarity:** each resume vector is compared with the job description vector. The similarity (0 to 1) is converted into a score from 0 to 100.
5. **Ranking:** resumes are sorted from highest to lowest score and displayed.
6. **Persistence:** the job description and each resume's score are saved to MySQL.

## Features

- Upload multiple resumes at once (PDF and DOCX)
- Relevance score (0–100) for every resume against the job description
- Ranked results table with the top match highlighted, plus a bar chart for comparison
- Job descriptions and results stored in MySQL for later reference
- Database credentials loaded from environment variables, never hardcoded

## Tech stack

- **Language:** Python
- **UI:** Streamlit
- **ML:** scikit-learn (TF-IDF, cosine similarity), pandas
- **Parsing:** PyPDF2, python-docx
- **Database:** MySQL (mysql-connector-python)
- **Config:** python-dotenv

## Project structure

```
resume_ranking_system/
├── app.py            # Streamlit UI: inputs, ranking flow, results display
├── utils.py          # Text extraction, cleaning, TF-IDF scoring
├── db_utils.py       # MySQL connection, schema setup, saving results
├── requirements.txt  # Python dependencies
├── .env.example      # Template for database settings
└── .gitignore
```

## Database schema

The app creates a database named `resume_ranking` with two tables:

| Table | Columns | Purpose |
| --- | --- | --- |
| `jobs` | `id`, `job_description`, `created_at` | One row per ranking run |
| `results` | `id`, `job_id` (foreign key → `jobs.id`), `resume_name`, `score` | One row per resume scored in that run |

## Setup

**Prerequisites:** Python 3 and a running MySQL server.

1. Clone the repository:
   ```bash
   git clone https://github.com/riananwani/resume_ranking_system.git
   cd resume_ranking_system
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create your environment file by copying the template, then fill in your MySQL username and password:
   ```bash
   cp .env.example .env
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```
5. In the app's sidebar, click **Initialize Database** once to create the database and tables.

## Usage

1. Paste a job description into the left panel.
2. Upload one or more resumes (PDF or DOCX) in the right panel.
3. Click **Rank Resumes**.
4. Review the ranked table and bar chart. Results are saved to MySQL automatically.

## Limitations

- **Keyword-based, not semantic.** TF-IDF matches exact words, so "Spring Boot developer" and "built Java microservices" may score low against each other even though they are related. Synonyms and context are not understood.
- **Scanned PDFs are not supported.** PDFs that are images of text contain no extractable text and will score poorly.
- **Scores are relative.** Because TF-IDF weights depend on the set of documents uploaded together, the same resume can score differently against a different batch.
- **No section awareness.** Skills, experience, and education are treated as one block of text.

## Possible improvements

- Use sentence embeddings for semantic matching instead of exact keywords
- Extract skills explicitly and show which job requirements each resume matches or misses
- Add OCR for scanned PDFs
- Add a page to browse past ranking runs stored in the database
