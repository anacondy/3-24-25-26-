"""
Terminal Archives - Admin User Creation Script
Phase 1 Secure – no hardcoded creds
Usage:
  python create_admin_secure.py --username Alvido --password "Strong!Pass123"
Or env:
  ADMIN_USER=Alvido ADMIN_PASS=Strong!Pass123 python create_admin_secure.py
"""
import argparse
import os
import sys
import getpass

# ensure local import
sys.path.insert(0, os.path.dirname(__file__))
import database

def main():
    parser = argparse.ArgumentParser(description='Create admin user securely')
    parser.add_argument('--username', '-u', default=os.environ.get('ADMIN_USER'))
    parser.add_argument('--password', '-p', default=os.environ.get('ADMIN_PASS'))
    args = parser.parse_args()

    username = args.username or input('Admin username: ').strip()
    password = args.password
    if not password:
        password = getpass.getpass('Admin password: ')
        confirm = getpass.getpass('Confirm password: ')
        if password != confirm:
            print('Passwords do not match', file=sys.stderr)
            sys.exit(1)

    if len(password) < 12:
        print('WARNING: password < 12 chars – use strong password in production!', file=sys.stderr)

    database.init_db()
    ok = database.add_user(username, password)
    if ok:
        print(f'✅ Admin {username} created.')
    else:
        print(f'User exists – to reset: delete from users table then rerun.')

if __name__ == '__main__':
    main()
