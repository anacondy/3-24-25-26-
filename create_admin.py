import database

# --- SET YOUR ADMIN USERNAME AND PASSWORD HERE ---
ADMIN_USERNAME = "Alvido"
ADMIN_PASSWORD = "890890" # Choose a strong password!
# ---------------------------------------------

database.init_db() # Make sure tables exist
database.add_user(ADMIN_USERNAME, ADMIN_PASSWORD)
