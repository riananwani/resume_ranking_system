import re
import PyPDF2
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {e}"

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.lower()

def calculate_scores(resumes_data, job_description):
    """
    resumes_data: list of dicts [{'name': 'filename', 'text': 'content'}]
    job_description: string
    
    Returns: DataFrame with scores
    """
    if not resumes_data or not job_description:
        return pd.DataFrame()

    jd_text = clean_text(job_description)
    resume_texts = [clean_text(r['text']) for r in resumes_data]
    filenames = [r['name'] for r in resumes_data]
    
    # Corpus: JD is index 0, followed by resumes
    corpus = [jd_text] + resume_texts
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Calculate cosine similarity between JD (index 0) and all resumes (indices 1 to N)
    # cosine_similarity returns a matrix. We want row 0, columns 1 onwards.
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    results = []
    for i, score in enumerate(cosine_sim):
        results.append({
            'Resume': filenames[i],
            'Score': round(score * 100, 2)
        })
        
    df = pd.DataFrame(results)
    df = df.sort_values(by='Score', ascending=False).reset_index(drop=True)
    return df
