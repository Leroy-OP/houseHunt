Backend Django project for houseHunt

Quick start (local dev):

1. Create a Python virtualenv and activate it.

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Configure MySQL credentials via environment variables (see `.env.example`).

3. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Run the dev server:

```bash
python manage.py runserver
```

The API is available under `/api/` (e.g. `/api/properties/`).
