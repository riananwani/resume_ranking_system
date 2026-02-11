import mysql.connector
from mysql.connector import Error
import streamlit as st

import os
from dotenv import load_dotenv

load_dotenv()

# Default Configuration - loaded from .env
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    # 'database': 'resume_ranking' # We connect without DB first to create it
}

def create_connection():
    """Create a database connection to the MySQL server"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
    return connection

def init_db():
    """Initialize the database and tables"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Create Database
            cursor.execute("CREATE DATABASE IF NOT EXISTS resume_ranking")
            cursor.execute("USE resume_ranking")
            
            # Create Jobs Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create Resumes Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_id INT,
                resume_name VARCHAR(255),
                score FLOAT,
                resume_text TEXT, 
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
            """)
            
            conn.commit()
            return True, "Database initialized successfully!"
        except Error as e:
            return False, f"Database initialization failed: {e}"
        finally:
            cursor.close()
            conn.close()
    else:
        return False, "Could not connect to MySQL server."

def save_job(job_description):
    conn = mysql.connector.connect(**DB_CONFIG, database='resume_ranking')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (job_description) VALUES (%s)", (job_description,))
    conn.commit()
    job_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return job_id

def save_results(job_id, results_df):
    conn = mysql.connector.connect(**DB_CONFIG, database='resume_ranking')
    cursor = conn.cursor()
    
    # results_df has columns: 'Resume', 'Score'
    # We might want to pass resume_text too, but for now let's skip saving text to keep it simple or modify logic
    
    for _, row in results_df.iterrows():
        cursor.execute("""
        INSERT INTO results (job_id, resume_name, score)
        VALUES (%s, %s, %s)
        """, (job_id, row['Resume'], row['Score']))
        
    conn.commit()
    cursor.close()
    conn.close()

def fetch_all_results():
    conn = mysql.connector.connect(**DB_CONFIG, database='resume_ranking')
    query = """
    SELECT j.id as JobID, r.resume_name, r.score, j.job_description 
    FROM results r 
    JOIN jobs j ON r.job_id = j.id 
    ORDER BY j.id DESC, r.score DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
