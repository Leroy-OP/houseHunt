System Architecture
Vue Frontend  →  Django REST API  →  MySQL Database
                      ↓
                Media Storage (Images)
```

## 📁 Project Structure

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
│   ├── Dockerfile
│   └── .env
│
├── docker/
│   ├── nginx/
│   └── scripts/
│
├── docker-compose.yml
├── .gitignore
├── .env.example
└── README.md
```

## ⚙️ 1. Project Setup

```bash
git clone https://github.com/Leroy-OP/houseHunt.git
cd houseHunt
```

## 🔧 2. Source Control Management (Git & GitHub)

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

## 🖥️ 3. Frontend Setup (Vue)

```bash
cd frontend
npm install
npm run dev
```

Runs on: `http://localhost:5173`

## 🧠 4. Backend Setup (Django)

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

On macOS/Linux:
```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### MySQL Fix (if needed)

Add this to `backend/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 🗄️ 5. Database Setup (MySQL)

### Using XAMPP

1. Start Apache & MySQL
2. Open: `http://localhost/phpmyadmin`

### Create Database

```sql
CREATE DATABASE hunter_street;
```

### Create User

```sql
CREATE USER 'group_7'@'localhost' IDENTIFIED BY 'hunterstreet01';
GRANT ALL PRIVILEGES ON hunter_street.* TO 'group_7'@'localhost';
FLUSH PRIVILEGES;
```

### Connect Django to MySQL

Update `settings.py`:

```python
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
```

## 🔄 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 👤 7. Create Admin User

```bash
python manage.py createsuperuser
python manage.py runserver
```

Access admin at: `http://127.0.0.1:8000/admin`

## 🔌 8. API Usage

Example endpoints:

```bash
GET /api/properties/
POST /api/properties/
```

## 🔗 9. Connect Frontend to Backend

Update your Vue components to use:

```javascript
axios.get("http://127.0.0.1:8000/api/properties/")
```

## 🖼️ 10. Media Setup

Add to Django `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 🔐 11. CORS Setup

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

## 🐳 12. Docker Setup

### Backend Dockerfile

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "run", "dev"]
```

### docker-compose.yml

```yaml
version: '3.9'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: hunter_street
      MYSQL_USER: group_7
      MYSQL_PASSWORD: hunterstreet01
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "3307:3306"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
```

### Run Project with Docker

```bash
docker-compose up --build
```

## 📦 .env Example

```
DB_NAME=hunter_street
DB_USER=group_7
DB_PASSWORD=hunterstreet01
DB_HOST=db
DB_PORT=3306
```

## 🚫 .gitignore

```
venv/
__pycache__/
*.pyc
node_modules/
dist/
.env
```

## 🚀 Features

- ✅ Property listings
- ✅ Image uploads
- ✅ Search & filtering
- 🔄 Favorites (planned)
- 🔄 Maps integration (planned)

## ⚠️ Troubleshooting

### MySQL not starting
- Delete `aria_log.*` files
- Check for port conflicts

### Django DB connection error
- Verify database credentials in `settings.py`
- Ensure MySQL service is running

### Frontend not connecting to backend
- Check CORS settings
- Verify backend URL in axios calls
- Ensure both services are running

## 🧭 Future Improvements

- JWT Authentication
- Role-based access control
- Mapbox integration
- Cloud deployment (AWS/Heroku)
- Email notifications

## 👨‍💻 Contributors

**Group 7**
- Leroy-OP

## 📄 License

This project is licensed under the MIT License.