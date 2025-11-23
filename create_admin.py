"""
Terminal Archives - Admin User Creation Script
==============================================
Creates an admin user for accessing the upload dashboard.
Run this script once to create your first admin account.

Usage:
    python3 create_admin.py

Author: Alvido
Last Updated: 2025
"""

import database

# --- CONFIGURATION: SET YOUR ADMIN USERNAME AND PASSWORD HERE ---
# Change these values before running the script
ADMIN_USERNAME = "Alvido"
ADMIN_PASSWORD = "890890"  # IMPORTANT: Choose a strong password for production!
# ----------------------------------------------------------------

# Initialize database tables (if not already created)
database.init_db()

# Create the admin user
database.add_user(ADMIN_USERNAME, ADMIN_PASSWORD)
