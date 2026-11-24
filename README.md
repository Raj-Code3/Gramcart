# GramKart - Fashion e-commerce (Django)

## Run (Windows / macOS / Linux)
1. Install Python 3.10+ from python.org (tick "Add Python to PATH" on Windows).
2. Open a terminal in this folder and run:

    python -m venv venv
    # Windows:  venv\Scripts\activate        macOS/Linux:  source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python seed_data.py
    python manage.py runserver

3. Open http://127.0.0.1:8000/

Logins: admin / admin123 (admin panel at /admin/)  |  priya_sharma / password123 (customer)

Needs internet for Tailwind CSS, icons, fonts and product photos (loaded from CDNs).
