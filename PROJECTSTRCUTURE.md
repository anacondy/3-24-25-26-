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
