"""
Terminal Archives - Database Module
====================================
Handles database initialization and user management.
Creates and manages SQLite database tables for papers and users.

Author: Alvido
Last Updated: 2025
"""

import sqlite3
from werkzeug.security import generate_password_hash


def init_db():
    """
    Initialize the database and create required tables if they don't exist.
    
    Tables created:
        1. papers: Stores exam paper metadata and file references
        2. users: Stores admin user credentials with hashed passwords
    
    Called on application startup.
    """
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    
    # Create papers table with comprehensive metadata fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class TEXT NOT NULL,                -- e.g., BA, BSc, BCA
            subject TEXT NOT NULL,              -- e.g., Physics, Chemistry
            semester TEXT NOT NULL,             -- e.g., I, II, III
            exam_year TEXT NOT NULL,            -- e.g., 2025, 2024
            exam_type TEXT NOT NULL,            -- e.g., Main Semester, CIA
            paper_code TEXT,                    -- Optional paper code
            exam_number TEXT,                   -- Optional exam number
            medium TEXT NOT NULL,               -- e.g., English Medium, Hindi Medium
            university TEXT,                    -- Optional university name
            time TEXT,                          -- Optional exam duration
            max_marks TEXT,                     -- Optional maximum marks
            uploader_name TEXT NOT NULL,        -- Admin who uploaded the file
            filename TEXT NOT NULL UNIQUE,      -- Unique filename for the PDF
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create users table for secure authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,      -- Unique username
            password_hash TEXT NOT NULL         -- Password stored as hash (never plain text)
        )
    ''')
    
    conn.commit()
    conn.close()


def add_user(username, password):
    """
    Add a new admin user to the database.
    Passwords are automatically hashed using pbkdf2:sha256.
    
    Args:
        username (str): The username for the new user
        password (str): The plain text password (will be hashed before storage)
    
    Returns:
        None
        
    Prints:
        Success or error message
    """
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    
    try:
        # Hash the password before storing (never store plain text passwords)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, generate_password_hash(password)))
        conn.commit()
        print(f"User '{username}' created successfully.")
    except sqlite3.IntegrityError:
        # Username already exists
        print(f"User '{username}' already exists.")
    finally:
        conn.close()
