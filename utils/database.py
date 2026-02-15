import sqlite3 

DB_NAME = "hirecopilot.db"

def init_db():
    """Initializes the database and creates the jobs table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT NOT NULL UNIQUE,
        job_description TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def save_jd(job_title: str, job_description: str):
    """Saves or replaces a job description in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # INSERT OR REPLACE will update the description if the title already exists, or insert a new row if it doesn't.
    cursor.execute("INSERT OR REPLACE INTO jobs (job_title, job_description) VALUES (?, ?)", (job_title, job_description))
    conn.commit()
    conn.close()

def load_jd_titles():
    """Loads all unique job titles from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT job_title FROM jobs ORDER BY job_title ASC")
    titles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return titles

def get_jd_by_title(job_title: str):
    """Retrieves a specific job description by its title."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT job_description FROM jobs WHERE job_title = ?", (job_title,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None