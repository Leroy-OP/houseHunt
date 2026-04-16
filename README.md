Tech Stack
Frontend
Vue.js
Vuetify / MDB UI
Axios (API communication)
Backend
Django
Django REST Framework (DRF)
Database
MySQL (via XAMPP or standalone)
DevOps
Docker & Docker Compose
🧭 System Architecture
Vue Frontend  →  Django REST API  →  MySQL Database
                      ↓
                Media Storage (Images)

1. Project Setup
Clone the Repository
git clone <https://github.com/Leroy-OP/houseHunt>
cd houseHunt

2. Frontend Setup (Vue)
cd frontend
npm install
npm run dev


Frontend runs on:

http://localhost:5173

3. Backend Setup (Django)
Create Virtual Environment
cd backend
python -m venv venv

Activate:
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

Install Dependencies
pip install -r requirements.txt


If no requirements file:

pip install django djangorestframework mysqlclient pillow pymysql django-cors-headers

Configure PyMySQL (if mysqlclient fails)
# backend/__init__.py
import pymysql
pymysql.install_as_MySQLdb()

🗄️ 4. Database Setup (MySQL via XAMPP)
Start Services
Open XAMPP
Start:
Apache
MySQL
Create Database

Go to:

http://localhost/phpmyadmin


Create database:

hunter_street

Create User (optional)
CREATE USER 'group_7'@'localhost' IDENTIFIED BY 'hunterstreet01';
GRANT ALL PRIVILEGES ON hunter_street.* TO 'group_7'@'localhost';
FLUSH PRIVILEGES;

Connect Django to MySQL
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hunter_street',
        'USER': 'group_7',
        'PASSWORD': 'hunterstreet01',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

5. Run Migrations (Creates Tables)
python manage.py makemigrations
python manage.py migrate


Tables will appear automatically in phpMyAdmin.

6. Create Admin User
python manage.py createsuperuser


Run server:

python manage.py runserver


Access:

http://127.0.0.1:8000/admin/

7. API Endpoints

Example:

GET     /api/properties/
POST    /api/properties/
GET     /api/properties/{id}/
PUT     /api/properties/{id}/
DELETE  /api/properties/{id}/

🔌 8. Connect Vue to Django

Example Axios call:

axios.get("http://127.0.0.1:8000/api/properties/")
  .then(response => {
    console.log(response.data);
  });

9. Media Configuration (Images)
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

10. CORS Configuration
INSTALLED_APPS = [
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

11. Docker Setup (Production Ready)
Create Dockerfile (Backend)
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

Create docker-compose.yml
version: '3.9'

services:
  db:
    image: mysql:8.0
    container_name: mysql_db
    restart: always
    environment:
      MYSQL_DATABASE: hunter_street
      MYSQL_USER: group_7
      MYSQL_PASSWORD: hunterstreet01
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "3307:3306"
    volumes:
      - db_data:/var/lib/mysql

  backend:
    build: ./backend
    container_name: django_backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    container_name: vue_frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
    command: npm run dev

volumes:
  db_data:

Run with Docker
docker-compose up --build

12. Features
Property listing system
Image uploads
Search & filtering
Favorites system (planned)
Map integration (planned)
Agent/user authentication (planned)
Troubleshooting
MySQL not starting (XAMPP)
Delete aria_log.* files
Check port conflicts
Run XAMPP as administrator
Django not connecting to DB
Check credentials in settings.py
Ensure MySQL is running
Images not loading
Check MEDIA_URL and MEDIA_ROOT
Future Improvements
JWT Authentication
Role-based access (Agent/User)
Mapbox integration
Booking/view scheduling
Deployment (AWS / Render)
Contributors
13. Source Control Management (Git & GitHub)

This project uses Git for version control and GitHub for collaboration.

📥 13.1 Initialize Git (First Time Setup)

Inside your project root:

git init
git add .
git commit -m "Initial commit"

🔗 13.2 Connect to GitHub Repository

Create a repository on GitHub, then link it:

git remote add origin https://github.com/<username>/house-hunting-system.git


Verify:

git remote -v


Push your code:

git branch -M main
git push -u origin main

🌿 13.3 Branching Strategy

We use a feature-based workflow:

Main Branches
main → Production-ready code
develop → Integration branch for all features
Create Develop Branch
git checkout -b develop
git push -u origin develop

Feature Branch Naming Convention

Each contributor works on their own branch:

feature/<feature-name>
bugfix/<issue-name>


Examples:

feature/property-listing
feature/authentication
bugfix/navbar-routing

👥 13.4 Contributor Workflow
1. Pull latest changes
git checkout develop
git pull origin develop

2. Create a feature branch
git checkout -b feature/property-cards

3. Work and commit changes
git add .
git commit -m "Add property card UI"

4. Push branch to GitHub
git push -u origin feature/property-cards

5. Create Pull Request (PR)
Go to GitHub repository
Click “Compare & pull request”
Merge into develop (NOT main)
🔄 13.5 Merging Strategy
All features → merged into develop
Stable develop → merged into main
🚫 13.6 Rules for Contributors
❌ Do NOT push directly to main
❌ Do NOT push untested code
✅ Always create a feature branch
✅ Always pull latest changes before starting work
✅ Write meaningful commit messages
🧾 13.7 Commit Message Convention

Use clear, structured commits:

feat: add property listing API
fix: resolve navbar routing issue
docs: update README instructions
style: improve card layout UI

🔄 13.8 Keeping Your Branch Updated
git checkout develop
git pull origin develop

git checkout feature/your-branch
git merge develop

🧹 13.9 Delete Branch After Merge
git branch -d feature/property-cards
git push origin --delete feature/property-cards

📦 13.10 .gitignore Setup

Create a .gitignore file:

# Python
venv/
__pycache__/
*.pyc

# Django
db.sqlite3
media/

# Node
node_modules/
dist/

# Environment variables
.env

# OS files
.DS_Store
Thumbs.db

🔐 13.11 Environment Variables (Recommended)

Do NOT commit sensitive data like passwords.

Use .env:

DB_NAME=hunter_street
DB_USER=group_7
DB_PASSWORD=hunterstreet01

🚀 13.12 Cloning the Project (For New Contributors)
git clone https://github.com/<username>/house-hunting-system.git
cd house-hunting-system
git checkout develop
Group 7