# 📟 Terminal Archives

**Terminal Archives** is a robust, secure, and highly efficient document management system designed with a hacker-aesthetic terminal interface. It allows students to search for exam papers instantly and administrators to upload metadata-rich documents via a secure, advanced dashboard.

![Homepage Screenshot](https://github.com/user-attachments/assets/a530f227-e8bd-4e9e-9a28-09d90d414d10)

---

## ✨ Features

### 🔍 Intelligent Search Engine
* **Smart Query Parsing:** The search engine understands human shortcuts and synonyms
  * *Input:* `3rd sem phy` → *System searches for:* `Semester III` + `Physics`
  * *Input:* `chem 2025` → *System searches for:* `Chemistry` + `2025`
* **Deep Database Search:** Scans 10+ metadata columns (Subject, Class, Uploader, University, etc.), not just filenames
* **Case Insensitive:** `bsc`, `BSc`, and `Bsc` yield identical results
* **Real-time Results:** Instant search results with no page reloads

### 🛡️ Enterprise-Grade Security
* **Secure Authentication:** Admin login uses **pbkdf2:sha256** password hashing - passwords are never stored in plain text
* **CSRF Protection:** All forms (Login, Upload) are protected against Cross-Site Request Forgery via `Flask-WTF` tokens
* **SQL Injection Proof:** Database queries utilize parameterization to prevent malicious inputs
* **Protected Routes:** Unauthorized access to `/admin` or `/upload` redirects immediately to the login page
* **Session Management:** Secure session handling with Flask's session management

### 📂 Advanced Admin Dashboard
* **Multi-File Drag & Drop:** Upload dozens of PDFs simultaneously with visual feedback
* **Parallel Form Cards:** Each file generates a dynamic form card for individual metadata entry
* **Smart Validation:** Prevents uploading if required fields (Class, Subject, Year) are missing
* **Duplicate Handling:** Automatically detects existing filenames and renames new uploads to prevent overwrites
* **Keyboard Navigation:** Scroll through upload cards using `Left` and `Right` arrow keys
* **Real-time Upload Status:** Visual indicators show pending, uploading, success, or error states

### 📱 Responsive Design
* **Desktop:** Clean, left-aligned terminal interface with a hidden `Ctrl + K` search modal
* **Mobile (Portrait):** Automatically detects mobile devices and moves the search bar to the bottom for thumb-friendly usage
* **Mobile (Landscape):** Optimized padding and layout for horizontal phone orientation
* **Tablet Support:** Adaptive layout for medium-sized screens
* **16:9 & 20:9 Displays:** Special optimizations for standard and ultra-wide aspect ratios
* **Cross-browser Compatible:** Works on Chrome, Firefox, Safari, and Edge

### 🎯 User Experience
* **Terminal Aesthetic:** Clean, modern terminal-style interface with smooth animations
* **Keyboard Shortcuts:** `Ctrl+K` to open search, `Esc` to close, arrow keys for navigation
* **Device Information:** Displays CPU cores, RAM, and storage quota on startup
* **Progress Indicators:** Animated progress bars for loading states
* **Error Handling:** Graceful error messages for network issues
* **Accessibility:** Proper HTML semantics and ARIA labels

---

## 📸 Screenshots

### Desktop Interface
![Desktop Homepage](https://github.com/user-attachments/assets/a530f227-e8bd-4e9e-9a28-09d90d414d10)
*Clean terminal interface with device information display*

### Search Modal
![Search Modal](https://github.com/user-attachments/assets/26120431-2ad6-4db9-ba01-145b0629fe86)
*Quick search with Ctrl+K keyboard shortcut*

### Mobile View
![Mobile Interface](https://github.com/user-attachments/assets/922e79ae-610c-4699-93f9-01e084aa4723)
*Bottom-aligned search bar for easy thumb access*

### Admin Login
![Login Page](https://github.com/user-attachments/assets/7a4274ca-8d41-4635-9679-09e0b69755be)
*Secure admin authentication page*

---

## 🎨 Design System

### Color Palette
| Color Name | Hex Code | Usage |
|:-----------|:---------|:------|
| **Void Black** | `#1a1a1a` | Main Background (Body) |
| **Terminal Green** | `#4CAF50` | Primary Accents, Success Messages, Prompts |
| **Off-White** | `#e0e0e0` | Primary Text, Input Text |
| **Dim Grey** | `#333333` | Input Backgrounds, Form Cards |
| **Comment Grey** | `#888888` | Instructional Text, Comments |
| **Error Red** | `#d9534f` | Error Messages, Failed Uploads |
| **Warning Orange** | `#f0ad4e` | Uploading Status |
| **Command Purple** | `#9C27B0` | Special prompts, Admin highlights |

### Typography
* **Font Family:** `'Fira Code'`, Monospace
* **Style:** Clean, legible, with coding ligatures for terminal aesthetic

### Animations
* **Marquee Progress Bar:** Smooth, back-and-forth scanning animation during loading states
* **Modal Fade:** Search modal fades in and out smoothly (0.3s transition)
* **Smooth Scroll:** Form cards scroll smoothly when using keyboard navigation
* **Hover Effects:** Interactive elements have subtle hover states

---

## 🛠️ Tech Stack

* **Backend:** Python 3.10+, Flask 3.1.2
* **Database:** SQLite (Native, Serverless)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
* **Security:** Werkzeug Security, Flask-WTF (CSRF Protection)
* **PDF Handling:** PyPDF2 (Metadata extraction/writing)
* **Server:** Gunicorn (Production), Flask dev server (Development)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/terminal-archives.git
cd terminal-archives
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure admin credentials:**
Edit `create_admin.py` and set your username and password:
```python
ADMIN_USERNAME = "your_username"
ADMIN_PASSWORD = "your_secure_password"
```

5. **Initialize database and create admin user:**
```bash
python3 create_admin.py
```

6. **Run the application:**
```bash
python3 app.py
```

7. **Access the application:**
Open your browser and navigate to `http://127.0.0.1:5000`

---

## 📁 Project Structure

```
terminal-archives/
├── app.py                  # Main Flask application with routes and logic
├── database.py             # Database initialization and user management
├── create_admin.py         # Script to create admin users
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── DEPLOYMENT.md          # Comprehensive deployment guide
├── README.md              # This file
├── static/
│   ├── style.css          # Global styles and responsive media queries
│   ├── script.js          # Search logic, device detection, animations
│   └── upload.js          # Admin drag-and-drop and validation logic
├── templates/
│   ├── index.html         # Main search interface
│   ├── login.html         # Admin login page
│   └── upload.html        # Admin upload dashboard
└── uploads/               # PDF storage directory (auto-created)
```

---

## 🧪 Testing

### Last Tested: November 23, 2025

### ✅ Features Tested & Working

#### Frontend (Desktop)
- [x] Homepage terminal interface loads correctly
- [x] Device information display (CPU, RAM, storage)
- [x] Search modal opens with Ctrl+K
- [x] Search modal closes with Esc
- [x] Click outside modal to close
- [x] Smooth animations and transitions
- [x] Terminal text formatting (prompts, commands, comments)
- [x] Progress bar animations

#### Frontend (Mobile)
- [x] Mobile search bar appears at bottom
- [x] Desktop-only elements hidden on mobile
- [x] Search modal hidden on mobile devices
- [x] Touch-friendly interface
- [x] Proper padding and spacing
- [x] Responsive typography

#### Search Functionality
- [x] Search with query returns results
- [x] Empty search returns all papers
- [x] Term translation (e.g., "3rd" → "III", "phy" → "physics")
- [x] Multi-column search across all fields
- [x] Case-insensitive search
- [x] Results display with proper formatting
- [x] PDF links open in new tab

#### Authentication
- [x] Login page renders correctly
- [x] CSRF token protection
- [x] Password hashing (pbkdf2:sha256)
- [x] Session management
- [x] Protected routes redirect to login
- [x] Flash messages for errors
- [x] Logout functionality

#### Admin Upload
- [x] Drag and drop zone
- [x] File selection button
- [x] PDF validation
- [x] Duplicate file detection
- [x] Dynamic form card generation
- [x] Required field validation
- [x] Upload status indicators
- [x] Keyboard navigation (arrow keys)
- [x] CSRF protection on uploads
- [x] Metadata storage in database

#### Database
- [x] Tables created successfully
- [x] Admin user creation
- [x] Password hashing on storage
- [x] Paper metadata insertion
- [x] File upload and storage
- [x] Query performance

#### Responsive Design
- [x] Desktop (1920x1080) - Perfect
- [x] Mobile Portrait (375x667) - Perfect
- [x] Mobile Landscape - Optimized
- [x] Tablet (768x1024) - Adaptive
- [x] Ultra-wide (21:9) - Supported
- [x] Standard (16:9) - Optimized

### 🧰 Testing Methods Used

1. **Manual Testing:** Tested all features in Chrome, Firefox, and Safari
2. **Responsive Testing:** Tested on various screen sizes and orientations
3. **Security Testing:** Verified CSRF protection, password hashing, SQL injection prevention
4. **User Flow Testing:** Tested complete user journeys (search, login, upload)
5. **Error Handling:** Tested edge cases and error scenarios
6. **Browser DevTools:** Inspected network requests, console logs, and DOM structure

### 📊 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 120+ | ✅ Fully Supported |
| Firefox | 120+ | ✅ Fully Supported |
| Safari | 17+ | ✅ Fully Supported |
| Edge | 120+ | ✅ Fully Supported |

### 🐛 Known Issues

- Font loading may fail if Google Fonts is blocked (fallback to system monospace)
- SQLite is not recommended for high-concurrency production use (migrate to PostgreSQL)
- Uploaded files are stored locally (consider cloud storage for production)

---

## 📚 Documentation

### For Users
- **Search Tips:** Use abbreviations like "3rd sem phy" or exact terms like "Physics 2025"
- **Admin Access:** Type "upload" in the search to navigate to admin login
- **Keyboard Shortcuts:** 
  - `Ctrl+K`: Open search modal
  - `Esc`: Close modal
  - `←/→`: Navigate upload forms

### For Developers
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- All code is thoroughly commented for easy understanding
- Follow existing patterns when adding features

### For Administrators
1. Login at `/login` with your credentials
2. Use drag-and-drop to upload PDFs
3. Fill in required metadata for each file
4. Click "Upload All Pending Files" to process

---

## 🌐 Deployment

This application can be deployed on various platforms. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides:

- ✅ [Heroku](DEPLOYMENT.md#heroku-deployment)
- ✅ [PythonAnywhere](DEPLOYMENT.md#pythonanywhere-deployment)
- ✅ [Railway](DEPLOYMENT.md#railway-deployment)
- ✅ [Render](DEPLOYMENT.md#render-deployment)

### Quick Deploy Commands

**Heroku:**
```bash
heroku create your-app-name
heroku config:set SECRET_KEY="your-secret-key"
git push heroku main
```

**Railway:**
```bash
railway login
railway init
railway up
```

---

## 🔒 Security Considerations

### Before Production:
1. Change default admin credentials in `create_admin.py`
2. Set a strong `SECRET_KEY` environment variable
3. Disable `debug=True` in `app.py`
4. Enable HTTPS/SSL on your hosting platform
5. Consider migrating from SQLite to PostgreSQL
6. Set up regular database backups
7. Configure rate limiting for API endpoints

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Alvido**
- GitHub: [@anacondy](https://github.com/anacondy)
- Project: Terminal Archives

---

## 🙏 Acknowledgments

- Flask framework and community
- Fira Code font by Nikita Prokopov
- All contributors and testers

---

## 📞 Support

If you encounter any issues or have questions:
1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
2. Review existing GitHub issues
3. Open a new issue with detailed description
4. Include error messages and screenshots

---

**Last Updated:** November 23, 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅
