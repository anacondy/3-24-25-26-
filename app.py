"""
Terminal Archives - Main Application File
==========================================
A Flask-based document management system for previous year exam papers.
Features intelligent search, secure authentication, and admin upload capabilities.

Author: Alvido
Last Updated: 2025
"""

# Standard library imports
import os
import re
import sqlite3

# Local imports
import database

# Flask and related imports
from flask import Flask, request, render_template, url_for, jsonify, send_from_directory, session, redirect, flash
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from flask_wtf.csrf import CSRFProtect

# Initialize Flask application
app = Flask(__name__)

# Configuration
# IMPORTANT: For production, set SECRET_KEY as an environment variable for security
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-default-secret-key-for-local-development')
app.config['UPLOAD_FOLDER'] = 'uploads'

# Enable CSRF protection for all forms
csrf = CSRFProtect(app)

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database tables
database.init_db()

# Translation map for intelligent search
# Converts common abbreviations and number formats to standard formats
TRANSLATION_MAP = {
    # Numeric to Roman numerals
    '1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V', '6': 'VI', '7': 'VII', '8': 'VIII', '9': 'IX', '10': 'X',
    # Word numbers to Roman numerals
    'one': 'I', 'two': 'II', 'three': 'III', 'four': 'IV', 'five': 'V', 'six': 'VI', 'seven': 'VII', 'eight': 'VIII',
    # Ordinal numbers to Roman numerals
    '1st': 'I', '2nd': 'II', '3rd': 'III', '4th': 'IV', '5th': 'V', '6th': 'VI', '7th': 'VII', '8th': 'VIII',
    # Lowercase Roman to uppercase Roman
    'i': 'I', 'ii': 'II', 'iii': 'III', 'iv': 'IV', 'v': 'V', 'vi': 'VI', 'vii': 'VII', 'viii': 'VIII', 'ix': 'IX',
    'x': 'X',
    # Common abbreviations
    'sem': 'semester', 'semester': 'semester',
    # Subject abbreviations
    'phy': 'physics', 'pys': 'psychology', 'env': 'environmental', 'sci': 'science',
    'his': 'history', 'eco': 'economics', 'stats': 'statistics', 'biotech': 'biotechnology',
    'cs': 'computer', 'ps': 'political', 'geo': 'geography', 'zoo': 'zoology',
    'bot': 'botany', 'eng': 'english', 'hin': 'hindi', 'chem': 'chemistry'
}

# Authentication decorator
def login_required(f):
    """
    Decorator to protect routes that require authentication.
    Redirects to login page if user is not authenticated.
    
    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return "This is protected"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Route: Homepage / Terminal UI
@app.route('/')
def terminal_ui():
    """
    Renders the main terminal interface for searching papers.
    Displays a terminal-style UI with search capabilities.
    """
    return render_template('index.html')


# Route: Admin Upload Dashboard
@app.route('/admin')
@login_required
def upload_form():
    """
    Renders the admin upload dashboard.
    Protected route - requires authentication.
    Allows administrators to upload multiple PDF files with metadata.
    """
    return render_template('upload.html')


# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user authentication.
    GET: Displays login form
    POST: Processes login credentials and creates session
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Query database for user
        conn = sqlite3.connect('papers.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        # Verify credentials using secure password hashing
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('upload_form'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')


# Route: Logout
@app.route('/logout')
def logout():
    """
    Clears user session and logs out.
    Redirects to homepage after logout.
    """
    session.clear()
    return redirect(url_for('terminal_ui'))


# Route: Upload File
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """
    Handles file upload from admin dashboard.
    Processes PDF files with metadata and stores them in database.
    
    Expected form data:
        - file: PDF file
        - class, subject, semester, exam_year, exam_type, medium: Required fields
        - paper_code, exam_number, university, time, max_marks: Optional fields
        - admin_name: Uploader name
    
    Returns:
        200: Success
        400: Missing required fields or invalid file
        500: Database error
    """
    # Validate file presence
    if 'file' not in request.files: 
        return "Missing file part", 400
    
    file = request.files['file']
    if file.filename == '': 
        return "Invalid file", 400

    # Collect all form data
    data = {
        "class_name": request.form.get('class', ''),
        "subject": request.form.get('subject', ''),
        "semester": request.form.get('semester', ''),
        "exam_year": request.form.get('exam_year', ''),
        "exam_type": request.form.get('exam_type', ''),
        "paper_code": request.form.get('paper_code', 'N/A'),
        "exam_number": request.form.get('exam_number', 'N/A'),
        "medium": request.form.get('medium', ''),
        "university": request.form.get('university', 'N/A'),
        "time": request.form.get('time', 'N/A'),
        "max_marks": request.form.get('max_marks', 'N/A'),
        "uploader_name": request.form.get('admin_name', 'Unknown')
    }

    # Validate required fields
    required_fields = ['class_name', 'subject', 'semester', 'exam_year', 'exam_type', 'medium', 'uploader_name']
    if not all(data[key] for key in required_fields): 
        return "A required field is empty", 400

    # Secure filename and handle duplicates with unique timestamp prefix
    unique_prefix = str(int(os.times().system * 1000))
    filename = secure_filename(f"{unique_prefix}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Insert metadata into database
    try:
        conn = sqlite3.connect('papers.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO papers (class, subject, semester, exam_year, exam_type, paper_code, exam_number, medium, university, time, max_marks, uploader_name, filename) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['class_name'], data['subject'], data['semester'], data['exam_year'], data['exam_type'],
              data['paper_code'], data['exam_number'], data['medium'], data['university'], data['time'],
              data['max_marks'], data['uploader_name'], filename))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")
        os.remove(filepath)  # Clean up file if DB operation fails
        return "Database error", 500
    
    return "Success", 200


# API Route: Get Papers
@app.route('/api/papers')
def get_papers():
    """
    API endpoint for searching papers.
    Supports intelligent search with abbreviation expansion.
    
    Query parameters:
        q (optional): Search query string
    
    Returns:
        JSON array of paper objects with metadata
        
    Search behavior:
        - No query: Returns all papers ordered by year (desc) and subject
        - With query: Performs intelligent multi-column search with term translation
    """
    search_query = request.args.get('q', '').strip().lower()
    conn = sqlite3.connect('papers.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if not search_query:
        # Return all papers if no search query provided
        cursor.execute('SELECT * FROM papers ORDER BY exam_year DESC, subject')
    else:
        # Intelligent Search Logic
        # Step 1: Split query into individual terms
        raw_terms = search_query.split()
        
        # Step 2: Translate terms using TRANSLATION_MAP (e.g., "3rd" -> "III", "phy" -> "physics")
        processed_terms = [TRANSLATION_MAP.get(term, term) for term in raw_terms]

        # Step 3: Build dynamic SQL query
        sql_query = 'SELECT * FROM papers WHERE '
        conditions = []
        params = []
        
        # Search across all text columns
        search_columns = ['class', 'subject', 'semester', 'exam_year', 'exam_type', 'paper_code', 'exam_number',
                          'medium', 'university', 'uploader_name']

        # Each term must match at least one column (AND logic between terms)
        for term in processed_terms:
            term_conditions = []
            for col in search_columns:
                term_conditions.append(f'LOWER({col}) LIKE ?')
                params.append(f'%{term}%')
            conditions.append(f"({' OR '.join(term_conditions)})")

        sql_query += ' AND '.join(conditions)
        sql_query += ' ORDER BY exam_year DESC, subject'
        cursor.execute(sql_query, params)

    papers_rows = cursor.fetchall()
    conn.close()

    # Convert database rows to JSON-serializable format
    papers_list = []
    for row in papers_rows:
        paper = dict(row)
        paper['url'] = url_for('get_uploaded_file', filename=paper['filename'])
        # Construct user-friendly display title
        paper['original_name'] = f"{paper['subject']} {paper['exam_type']} {paper['exam_year']}"
        papers_list.append(paper)

    return jsonify(papers_list)


# Route: Serve Uploaded Files
@app.route('/uploads/<path:filename>')
def get_uploaded_file(filename):
    """
    Serves uploaded PDF files from the uploads directory.
    
    Args:
        filename: The name of the file to serve
        
    Returns:
        The requested PDF file
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Application entry point
if __name__ == '__main__':
    # Run development server
    # WARNING: debug=True should NEVER be used in production
    app.run(debug=True)
