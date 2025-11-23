# 🚀 Deployment Guide - Terminal Archives

This guide provides detailed instructions for deploying Terminal Archives on various platforms.

---

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Heroku Deployment](#heroku-deployment)
3. [PythonAnywhere Deployment](#pythonanywhere-deployment)
4. [Railway Deployment](#railway-deployment)
5. [Render Deployment](#render-deployment)
6. [Environment Variables](#environment-variables)
7. [Production Checklist](#production-checklist)

---

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/terminal-archives.git
cd terminal-archives
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize the database:**
```bash
python3 create_admin.py
```

5. **Run the development server:**
```bash
python3 app.py
```

6. **Access the application:**
Open your browser and navigate to `http://127.0.0.1:5000`

---

## Heroku Deployment

### Prerequisites
- Heroku account ([Sign up here](https://signup.heroku.com/))
- Heroku CLI installed ([Installation guide](https://devcenter.heroku.com/articles/heroku-cli))

### Steps

1. **Create required files:**

Create `Procfile` in the root directory:
```
web: gunicorn app:app
```

Create `runtime.txt` (optional, to specify Python version):
```
python-3.12.3
```

2. **Update requirements.txt:**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

3. **Login to Heroku:**
```bash
heroku login
```

4. **Create a new Heroku app:**
```bash
heroku create your-app-name
```

5. **Set environment variables:**
```bash
heroku config:set SECRET_KEY="your-super-secret-key-here"
```

6. **Deploy to Heroku:**
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

7. **Initialize the database on Heroku:**
```bash
heroku run python create_admin.py
```

8. **Open your application:**
```bash
heroku open
```

### Important Notes for Heroku:
- SQLite is ephemeral on Heroku (files are lost on dyno restart)
- For production, consider upgrading to PostgreSQL:
  ```bash
  heroku addons:create heroku-postgresql:mini
  ```

---

## PythonAnywhere Deployment

### Prerequisites
- PythonAnywhere account ([Sign up here](https://www.pythonanywhere.com/registration/register/beginner/))

### Steps

1. **Upload your code:**
   - Go to "Files" tab
   - Click "Upload a file" or clone from Git
   - Navigate to your home directory

2. **Clone from GitHub:**
```bash
git clone https://github.com/yourusername/terminal-archives.git
cd terminal-archives
```

3. **Create a virtual environment:**
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
workon myenv
pip install -r requirements.txt
```

4. **Configure Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10

5. **Configure WSGI file:**
   - Click on WSGI configuration file link
   - Replace contents with:
```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/terminal-archives'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variable
os.environ['SECRET_KEY'] = 'your-super-secret-key-here'

# Import and run the Flask app
from app import app as application
```

6. **Set up static files:**
   - In "Web" tab, add static file mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/terminal-archives/static`

7. **Initialize database:**
   - Go to "Consoles" tab
   - Start a Bash console:
```bash
cd ~/terminal-archives
workon myenv
python create_admin.py
```

8. **Reload web app:**
   - Go to "Web" tab
   - Click "Reload" button

---

## Railway Deployment

### Prerequisites
- Railway account ([Sign up here](https://railway.app/))
- GitHub account

### Steps

1. **Create `railway.json` (optional):**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. **Add gunicorn to requirements.txt:**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

3. **Deploy on Railway:**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect and deploy your Flask app

4. **Set environment variables:**
   - Go to your project settings
   - Click "Variables" tab
   - Add: `SECRET_KEY = your-super-secret-key-here`

5. **Generate domain:**
   - Go to "Settings" tab
   - Click "Generate Domain"

6. **Initialize database:**
   - Use Railway CLI or console to run:
```bash
python create_admin.py
```

---

## Render Deployment

### Prerequisites
- Render account ([Sign up here](https://dashboard.render.com/register))

### Steps

1. **Create `render.yaml` (Blueprint):**
```yaml
services:
  - type: web
    name: terminal-archives
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.12.3
```

2. **Add gunicorn to requirements.txt:**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

3. **Deploy on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render auto-detects Flask and configures build

4. **Configure environment:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

5. **Add environment variables:**
   - In dashboard, go to "Environment"
   - Add `SECRET_KEY` with a strong random value

6. **Initialize database:**
   - Use Render Shell to run:
```bash
python create_admin.py
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for session management | `a-very-long-random-string-here` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment mode | `production` |
| `UPLOAD_FOLDER` | Directory for uploaded files | `uploads` |

### Generating a Secure SECRET_KEY

**Python method:**
```python
import secrets
print(secrets.token_hex(32))
```

**Command line:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## Production Checklist

Before deploying to production, ensure you've completed these steps:

### Security
- [ ] Set a strong, unique `SECRET_KEY` environment variable
- [ ] Change default admin credentials in `create_admin.py`
- [ ] Remove or disable `debug=True` in `app.py`
- [ ] Enable HTTPS/SSL on your hosting platform
- [ ] Review and update CORS settings if needed

### Database
- [ ] Run `create_admin.py` to create initial admin user
- [ ] Consider migrating from SQLite to PostgreSQL for better performance
- [ ] Set up automated database backups

### Files & Storage
- [ ] Configure persistent storage for uploads (SQLite is ephemeral on some platforms)
- [ ] Add `.gitignore` for database and uploads
- [ ] Consider using cloud storage (AWS S3, Cloudinary) for PDFs

### Performance
- [ ] Use a production WSGI server (gunicorn, uWSGI)
- [ ] Enable caching if needed
- [ ] Configure CDN for static files (optional)

### Monitoring
- [ ] Set up error logging
- [ ] Configure application monitoring (e.g., Sentry)
- [ ] Set up uptime monitoring

### Documentation
- [ ] Update README with production URL
- [ ] Document admin credentials storage
- [ ] Create user guide for administrators

---

## Troubleshooting

### Database Issues
**Problem:** "No such table: papers"
**Solution:** Run `python create_admin.py` to initialize the database

### Upload Issues
**Problem:** Uploads fail or disappear after deployment
**Solution:** Configure persistent storage or use cloud storage service

### Import Errors
**Problem:** "ModuleNotFoundError"
**Solution:** Ensure all dependencies are in `requirements.txt` and installed

### Permission Errors
**Problem:** Can't write to uploads directory
**Solution:** Ensure the uploads directory has write permissions

---

## Support & Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Heroku Python Guide:** https://devcenter.heroku.com/articles/getting-started-with-python
- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **Railway Docs:** https://docs.railway.app/
- **Render Docs:** https://render.com/docs

---

## Next Steps

After successful deployment:
1. Test all features (search, upload, login)
2. Upload some sample papers
3. Share the URL with users
4. Monitor for errors and performance issues
5. Set up regular backups

---

**Last Updated:** 2025
**Maintained by:** Alvido
