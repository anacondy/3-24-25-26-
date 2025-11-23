# ⚠️ Deployment Caveats & Troubleshooting Log

**Project:** Terminal Archives (Flask/SQLite)
**Platform:** PythonAnywhere

This document tracks specific errors encountered during deployment and their proven solutions.

---

### 1. The "Ghost Database" Problem
**Symptoms:**
* Admin user created via console does not exist on the web login.
* Uploaded files appear in the file manager but not on the website.
* Data seems to "disappear" after web reload.

**Cause:**
Using relative paths (e.g., `sqlite3.connect('papers.db')`) causes the Console and the Web Server to create two separate database files in different working directories.

**Solution:**
Always use **Absolute Paths** derived from the file location.
* **Code Fix:**
    ```python
    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'papers.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ```

---

### 2. Dependency Failures (pikepdf)
**Symptoms:**
* Deployment crashes with `ImportError` or installation fails in console.

**Cause:**
Libraries like `pikepdf` (used for PDF linearization) rely on system-level C++ libraries (`libqpdf`) that are often not available or restricted on free-tier hosting environments like PythonAnywhere.

**Solution:**
* **Fix:** Remove the dependency for the production environment or wrap the import in a try/except block to fail gracefully without crashing the app.
* **Action:** Feature was disabled for the live deployment to ensure stability.

---

### 3. 400 Bad Request (CSRF Token Missing)
**Symptoms:**
* Submitting a form (Login or Upload) returns a standard 400 Error.
* Logs show "The CSRF token is missing."

**Cause:**
We implemented `Flask-WTF` for security but forgot to include the token in the HTML forms or AJAX headers.

**Solution:**
* **HTML Forms:** Add `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>`.
* **AJAX/Fetch:** Add a `<meta>` tag with the token and read it into the request header:
    ```javascript
    headers: { 'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content }
    ```

---

### 4. NameError: name 'secure_filename' is not defined
**Symptoms:**
* 500 Internal Server Error upon file upload.

**Cause:**
Using a function without importing it.

**Solution:**
* **Fix:** Ensure all utilities are imported at the top of `app.py`:
    ```python
    from werkzeug.utils import secure_filename
    ```

---

### 5. "Method Not Allowed" on Login
**Symptoms:**
* Accessing `/login` returns a 405 Method Not Allowed error.

**Cause:**
The `app.py` file on the server was outdated or out-of-sync with the local version, missing the route definition entirely.

**Solution:**
* **Fix:** Perform a full code replacement of `app.py` to ensure local and remote versions match exactly.
