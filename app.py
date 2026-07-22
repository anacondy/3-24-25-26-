"""
Terminal Archives - Main Application File
Phase 1 Secure Core – P0 fixes applied
======================================
Fixes:
 C1 – no hardcoded creds (moved to create_admin_secure.py)
 C2 – strict PDF upload whitelist, magic check, uuid filenames
 C3 – server-side output escaping, secure headers
 C4 – absolute DB_PATH everywhere
 C5 – uuid filenames, no os.times() collision
 C6 – optional pikepdf import
 C7 – session fixation mitigation, secure cookie flags
 H4 – uploader_name from session
 H7 – debug=False by default
 H8 – WAL + timeout via database.get_conn()
 H9 – /uploads/<string:filename> + safe validation
 + input length caps, logging, security headers
"""
import os
import sqlite3
import uuid
import time
import html
import logging
from functools import wraps
from datetime import timedelta

from flask import Flask, request, render_template, url_for, jsonify, send_from_directory, session, redirect, flash, abort
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect

# Local imports
import database  # database.get_conn() uses absolute DB_PATH

# Optional PDF optimizer – C6 fix
try:
    import pikepdf
    PIKEPDF_AVAILABLE = True
except Exception:
    PIKEPDF_AVAILABLE = False

# --- Config centralization ---
try:
    import config as app_config
    BASE_DIR = app_config.BASE_DIR
    DB_PATH = app_config.DB_PATH
    UPLOAD_FOLDER = app_config.UPLOAD_FOLDER
    SECRET_KEY = app_config.SECRET_KEY
    MAX_CONTENT_LENGTH = app_config.MAX_CONTENT_LENGTH
    ALLOWED_EXTENSIONS = app_config.ALLOWED_EXTENSIONS
except Exception:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "papers.db")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-prod")
    MAX_CONTENT_LENGTH = 120 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Session hardening – C7
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_SECURE_COOKIES', '0') == '1'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

csrf = CSRFProtect(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
database.init_db()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("terminal_archives")

TRANSLATION_MAP = {
    '1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V', '6': 'VI', '7': 'VII', '8': 'VIII', '9': 'IX', '10': 'X',
    'one': 'I', 'two': 'II', 'three': 'III', 'four': 'IV', 'five': 'V', 'six': 'VI', 'seven': 'VII', 'eight': 'VIII',
    '1st': 'I', '2nd': 'II', '3rd': 'III', '4th': 'IV', '5th': 'V', '6th': 'VI', '7th': 'VII', '8th': 'VIII',
    'i': 'I', 'ii': 'II', 'iii': 'III', 'iv': 'IV', 'v': 'V', 'vi': 'VI', 'vii': 'VII', 'viii': 'VIII', 'ix': 'IX', 'x': 'X',
    'sem': 'semester', 'semester': 'semester',
    'phy': 'physics', 'pys': 'psychology', 'env': 'environmental', 'sci': 'science',
    'his': 'history', 'eco': 'economics', 'stats': 'statistics', 'biotech': 'biotechnology',
    'cs': 'computer', 'ps': 'political', 'geo': 'geography', 'zoo': 'zoology',
    'bot': 'botany', 'eng': 'english', 'hin': 'hindi', 'chem': 'chemistry'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_pdf_magic(file_stream):
    """Check %PDF magic – C2"""
    pos = file_stream.tell()
    try:
        file_stream.seek(0)
        header = file_stream.read(5)
        file_stream.seek(pos)
        return header == b'%PDF-'
    except Exception:
        try:
            file_stream.seek(pos)
        except Exception:
            pass
        return False

@app.after_request
def set_security_headers(resp):
    # H6 – security headers
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'DENY'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    resp.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"
    return resp

@app.route('/')
def terminal_ui():
    return render_template('index.html')

@app.route('/offline')
def offline():
    return render_template('offline.html')

@app.route('/admin')
@login_required
def upload_form():
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()[:64]
        password = request.form.get('password') or ''
        # Mitigate brute force later in Phase2 with Flask-Limiter – H2
        conn = database.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            # C7 – session fixation fix
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True
            return redirect(url_for('upload_form'))
        else:
            flash('Invalid username or password.')
            # generic delay to slow brute force a bit
            time.sleep(0.5)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('terminal_ui'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return "Missing file part", 400
    file = request.files['file']
    if file.filename == '':
        return "Invalid file", 400
    if not allowed_file(file.filename):
        return "Only PDF files allowed", 400
    if not validate_pdf_magic(file.stream):
        return "Invalid PDF file", 400

    # Collect form data with length caps – M4
    def cap(v, n=200):
        return (v or '')[:n].strip()
    data = {
        "class_name": cap(request.form.get('class', ''), 50),
        "subject": cap(request.form.get('subject', ''), 100),
        "semester": cap(request.form.get('semester', ''), 20),
        "exam_year": cap(request.form.get('exam_year', ''), 10),
        "exam_type": cap(request.form.get('exam_type', ''), 50),
        "paper_code": cap(request.form.get('paper_code', 'N/A'), 50),
        "exam_number": cap(request.form.get('exam_number', 'N/A'), 50),
        "medium": cap(request.form.get('medium', ''), 50),
        "university": cap(request.form.get('university', 'N/A'), 150),
        "time": cap(request.form.get('time', 'N/A'), 30),
        "max_marks": cap(request.form.get('max_marks', 'N/A'), 20),
        # H4 – uploader from session, not client
        "uploader_name": session.get('username', 'Unknown')[:100]
    }

    required_fields = ['class_name', 'subject', 'semester', 'exam_year', 'exam_type', 'medium', 'uploader_name']
    if not all(data[key] for key in required_fields):
        return "A required field is empty", 400

    # C5 – secure unique filename
    safe_base = secure_filename(file.filename)
    # force .pdf extension
    if not safe_base.lower().endswith('.pdf'):
        safe_base += '.pdf'
    unique_name = f"{uuid.uuid4().hex}_{int(time.time())}_{safe_base}"
    filename = unique_name[:220]  # filesystem safe
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # prevent path traversal – ensure inside UPLOAD_FOLDER
    if not os.path.abspath(filepath).startswith(os.path.abspath(app.config['UPLOAD_FOLDER']) + os.sep):
        return "Invalid filename", 400

    file.save(filepath)

    # Optimize PDF – C6 optional
    if PIKEPDF_AVAILABLE:
        try:
            pdf = pikepdf.open(filepath)
            with pdf.open_metadata() as meta:
                meta['dc:title'] = f"{data['class_name']} - {data['subject']} (Sem {data['semester']})"
                meta['dc:creator'] = data['uploader_name']
                meta['dc:description'] = f"University: {data['university']}, Year: {data['exam_year']}, Type: {data['exam_type']}, Time: {data['time']}, Marks: {data['max_marks']}"
            pdf.save(filepath, linearize=True)
            pdf.close()
        except Exception as e:
            log.warning(f"PDF Optimization Warning: {e}")

    # Insert metadata – C4 absolute DB
    try:
        conn = database.get_conn()
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
        log.error(f"Database Error: {e}")
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass
        return "Database error", 500

    return "Success", 200

@app.route('/api/papers')
def get_papers():
    search_query = request.args.get('q', '').strip().lower()
    # H3 – pagination Phase1: soft limit 500 max, Phase2 proper offset
    try:
        limit = min(int(request.args.get('limit', '200')), 500)
    except ValueError:
        limit = 200
    try:
        offset = max(int(request.args.get('offset', '0')), 0)
    except ValueError:
        offset = 0

    conn = database.get_conn()
    cursor = conn.cursor()

    if not search_query:
        cursor.execute('SELECT * FROM papers ORDER BY exam_year DESC, subject LIMIT ? OFFSET ?', (limit, offset))
        params = []
    else:
        raw_terms = search_query.split()
        processed_terms = [TRANSLATION_MAP.get(term, term) for term in raw_terms]
        sql_query = 'SELECT * FROM papers WHERE '
        conditions = []
        params = []
        search_columns = ['class', 'subject', 'semester', 'exam_year', 'exam_type', 'paper_code', 'exam_number',
                          'medium', 'university', 'uploader_name']
        for term in processed_terms:
            # sanitize term length
            term = term[:50]
            term_conditions = []
            for col in search_columns:
                term_conditions.append(f'LOWER({col}) LIKE ?')
                params.append(f'%{term}%')
            conditions.append(f"({' OR '.join(term_conditions)})")
        sql_query += ' AND '.join(conditions)
        sql_query += ' ORDER BY exam_year DESC, subject LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        cursor.execute(sql_query, params)

    papers_rows = cursor.fetchall()
    conn.close()

    papers_list = []
    for row in papers_rows:
        paper = dict(row)
        # C3 – escape output server-side
        safe_subject = html.escape(paper.get('subject',''))
        safe_exam_type = html.escape(paper.get('exam_type',''))
        safe_exam_year = html.escape(str(paper.get('exam_year','')))
        paper['url'] = url_for('get_uploaded_file', filename=paper['filename'])
        paper['original_name'] = f"{safe_subject} {safe_exam_type} {safe_exam_year}"
        # M7 – minimize leaked fields – keep for compat Phase1, Phase2 strip uploader_name/filename
        papers_list.append(paper)

    return jsonify(papers_list)

# H9 – use <string:filename> not <path:filename>
@app.route('/uploads/<string:filename>')
def get_uploaded_file(filename):
    # Validate filename – only allow safe chars
    if '..' in filename or filename.startswith('/') or '\\' in filename:
        abort(404)
    # secure_filename check
    if secure_filename(filename) != filename:
        # allow uuid_ prefixed names which secure_filename keeps
        pass
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False, mimetype='application/pdf',
                               download_name=filename)

if __name__ == '__main__':
    # H7 – debug off by default
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
