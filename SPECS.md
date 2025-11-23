# 📟 Terminal Archives

**Terminal Archives** is a robust, secure, and highly efficient document management system designed with a hacker-aesthetic terminal interface. It allows students to search for exam papers instantly and administrators to upload metadata-rich documents via a secure, advanced dashboard.

---



### Project Structure 

paper-archive-project/
├── app.py                 # Main Flask server & Logic
├── database.py            # Database initialization & helper functions
├── papers.db              # SQLite Database (Auto-generated)
├── static/
│   ├── style.css          # Global styles & responsive media queries
│   ├── script.js          # Search logic, device detection, animations
│   └── upload.js          # Admin drag-and-drop & validation logic
├── templates/
│   ├── index.html         # Main search interface
│   └── upload.html        # Admin upload dashboard
└── uploads/               # PDF storage directory



## ✨ Key Features

### 🔍 Intelligent Search Engine
* **Smart Query Parsing:** The search engine understands human shortcuts and synonyms.
    * *Input:* `3rd sem phy` → *System searches for:* `Semester III` + `Physics`.
    * *Input:* `chem 2025` → *System searches for:* `Chemistry` + `2025`.
* **Deep Database Search:** Scans 10+ metadata columns (Subject, Class, Uploader, University, etc.), not just filenames.
* **Case Insensitive:** `bsc`, `BSc`, and `Bsc` yield identical results.

### 🛡️ Enterprise-Grade Security
* **Secure Authentication:** Admin login uses **pbkdf2:sha256** password hashing. Passwords are never stored in plain text.
* **CSRF Protection:** All forms (Login, Upload) are protected against Cross-Site Request Forgery via `Flask-WTF` tokens.
* **SQL Injection Proof:** Database queries utilize parameterization to prevent malicious inputs.
* **Protected Routes:** Unauthorized access to `/admin` or `/upload` redirects immediately to the login page.

### 📂 Advanced Admin Dashboard
* **Multi-File Drag & Drop:** Upload dozens of PDFs simultaneously.
* **Parallel Form Cards:** Each file generates a dynamic form card for individual metadata entry.
* **Smart Validation:** Prevents uploading if required fields (Class, Subject, Year) are missing.
* **Duplicate Handling:** Automatically detects existing filenames and renames new uploads to prevent overwrites.
* **Keyboard Navigation:** Scroll through upload cards using `Left` and `Right` arrow keys.

### 📱 Responsive Design
* **Desktop:** Clean, left-aligned terminal interface with a hidden `Ctrl + K` search modal.
* **Mobile:** Automatically detects mobile devices and moves the search bar to the bottom of the screen for thumb-friendly usage.

---

## 🎨 Theming & Design System

The UI is built to mimic a modern, high-contrast code editor or terminal.

### Color Palette
| Color Name | Hex Code | Usage |
| :--- | :--- | :--- |
| **Void Black** | `#1a1a1a` | Main Background (Body) |
| **Terminal Green** | `#4CAF50` | Primary Accents, Success Messages, Prompts |
| **Off-White** | `#e0e0e0` | Primary Text, Input Text |
| **Dim Grey** | `#333333` | Input Backgrounds, Form Cards |
| **Comment Grey** | `#888888` | Instructional Text, Comments |
| **Error Red** | `#d9534f` | Error Messages, Failed Uploads |
| **Warning Orange** | `#f0ad4e` | Uploading Status |
| **Command Purple** | `#9C27B0` | Special prompts, Admin highlights |

### Typography
* **Font Family:** `'Fira Code'`, Monospace.
* **Style:** Clean, legible, with coding ligatures.

### Animations
* **Marquee Progress Bar:** A smooth, back-and-forth scanning animation during loading states.
* **Modal Fade:** Search modal fades in and out smoothly (0.3s transition).
* **Smooth Scroll:** Form cards scroll smoothly when using keyboard navigation.

### For security, set your secret key. On Linux/Mac
export SECRET_KEY='your-super-secret-random-key'


### Setting password 
python
>>> import database
>>> database.init_db()
>>> database.add_user("Alvido", "YourStrongPassword")
>>> exit()

---

## 🛠️ Tech Stack

* **Backend:** Python 3.10+, Flask.
* **Database:** SQLite (Native, Serverless).
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+).
* **Security:** Werkzeug Security, Flask-WTF.
* **PDF Handling:** PyPDF2 (Metadata extraction/writing).

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/terminal-archives.git](https://github.com/yourusername/terminal-archives.git)
cd terminal-archives


