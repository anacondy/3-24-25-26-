"""
Terminal Archives - Database Module
Phase 1 Secure Core
Fixes: C4 Ghost DB – absolute DB_PATH, WAL, timeout, indexes
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

# Centralized DB path – import from config if available, fallback to absolute
try:
    from config import DB_PATH
except ImportError:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "papers.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable WAL for concurrency H8
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
    except Exception:
        pass
    return conn

def init_db():
    """
    Initialize the database and create required tables if they don't exist.
    Phase1: adds indexes, keeps 'class' column for compat – Phase2 renames to class_name.
    """
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class TEXT NOT NULL,
            subject TEXT NOT NULL,
            semester TEXT NOT NULL,
            exam_year TEXT NOT NULL,
            exam_type TEXT NOT NULL,
            paper_code TEXT,
            exam_number TEXT,
            medium TEXT NOT NULL,
            university TEXT,
            time TEXT,
            max_marks TEXT,
            uploader_name TEXT NOT NULL,
            filename TEXT NOT NULL UNIQUE,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    # Phase1 indexes – mitigate M8 full scan
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_papers_subject ON papers(subject);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_papers_exam_year ON papers(exam_year DESC);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_papers_semester ON papers(semester);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_papers_class ON papers(class);')

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, generate_password_hash(password)))
        conn.commit()
        print(f"User '{username}' created successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")
        return False
    finally:
        conn.close()
