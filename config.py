"""
Terminal Archives - Central Config
Phase 1 Secure Core
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# When config.py is copied into project root, __file__ resolves correctly.
# If you keep config.py separate, adjust BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database absolute path – fixes Ghost DB bug C4
DB_PATH = os.path.join(BASE_DIR, "papers.db")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Security
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    # Fail closed in production – set env. For local dev you can set a temporary key.
    # os.environ['SECRET_KEY'] = 'dev-only-change-me'
    SECRET_KEY = "change-me-in-prod-use-env-SECRET_KEY"

MAX_CONTENT_LENGTH = 120 * 1024 * 1024  # 120 MB

ALLOWED_EXTENSIONS = {"pdf"}

# Session hardening
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = os.environ.get("FLASK_SECURE_COOKIES", "0") == "1"
PERMANENT_SESSION_LIFETIME = 3600 * 8  # 8 hours, in seconds – Flask expects timedelta, set in app

# Upload hardening
UPLOAD_STRICT_PDF_MAGIC = True
