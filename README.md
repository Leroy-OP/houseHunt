System Architecture
Vue Frontend  →  Django REST API  →  Postgres Database
                      ↓
                Media Storage (Images)
```

##  Project Structure

```
house-hunting-system/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── backend/
│   ├── api/
│   ├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
└── README.md
```

## 1. Project Setup

```bash
git clone https://github.com/Leroy-OP/houseHunt.git
cd houseHunt
```

## 2. Source Control Management (Git & GitHub)

### Initialize Git

```bash
git init
git add .
git commit -m "Initial commit"
```

### Connect Remote Repository

```bash
git remote add origin https://github.com/Leroy-OP/houseHunt.git
git branch -M main
git push -u origin main
```

### Branching Strategy

| Branch | Purpose |
|--------|---------|
| main | Production-ready |
| develop | Integration |
| feature/* | New features |
| bugfix/* | Fixes |

### Create Develop Branch

```bash
git checkout -b develop
git push -u origin develop
```

### Contributor Workflow

```bash
git checkout develop
git pull origin develop

git checkout -b feature/property-cards

git add .
git commit -m "feat: add property cards"

git push -u origin feature/property-cards
```

Then create a Pull Request → merge into develop

### Keep Branch Updated

```bash
git checkout develop
git pull origin develop

git checkout feature/your-branch
git merge develop
```

### Delete Branch After Merge

```bash
git branch -d feature/property-cards
git push origin --delete feature/property-cards
```

## 3. Frontend Setup (Vue)

```bash
cd frontend
npm install
npm run dev
```

Runs on: `http://localhost:5173`

## 4. Backend Setup (Django)

### Virtual Environment

```bash
cd backend
python -m venv venv
```

**Activate:**

On Windows:
```bash
venv\Scripts\activate
```
### Install Dependencies

```bash
pip install -r requirements.txt
```
## 🗄️ 5. Database Setup (Postgres)

### Connect Django to Postgres

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'House',
        'USER': 'group_7',
        'PASSWORD': 'house001',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
## 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Create Admin User

```bash
python manage.py createsuperuser
python manage.py runserver
```

Access admin at: `http://127.0.0.1:8000/admin`

## 8. API Usage

Example endpoints:

```bash
GET /api/properties/
POST /api/properties/
```

## 9. Connect Frontend to Backend

Update your Vue components to use:

```javascript
axios.get("http://127.0.0.1:8000/api/properties/")
```

## 10. Media Setup

Add to Django `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 11. CORS Setup

Add to Django `settings.py`:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

Or use specific origins in production:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```
## .env Example

```
DB_NAME=House
DB_USER=postgres
DB_PASSWORD=house001
DB_HOST=db
DB_PORT=3306
```

## .gitignore

```
venv/
__pycache__/
*.pyc
node_modules/
dist/
.env
```

## Features

-  Property listings
-  Image uploads
-  Search & filtering
-  Favorites (planned)
-  Maps integration (planned)

##  Troubleshooting

### Django DB connection error
- Verify database credentials in `settings.py`
- Ensure MySQL service is running

### Frontend not connecting to backend
- Check CORS settings
- Verify backend URL in axios calls
- Ensure both services are running

## Future Improvements

- JWT Authentication
- Role-based access control
- Mapbox integration
- Cloud deployment (AWS/Heroku)
- Email notifications

## Contributors

**Group 7**
- Leroy Keretts
- Deborah Rotich
- Victoria Chebet
- Frank Obare
- Mercy Mbingu
- Anthony Ojwang
- Ignatius Wango
- Walter Ojwang

