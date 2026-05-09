# HouseHunt Backend

A robust backend API for the **HouseHunt** real estate platform, built with Django and Django REST Framework. This service powers property listings, agency management, user authentication, and property booking workflows.

---

## Features

- User registration and authentication using JWT
- Agency profile management
- Property listing creation and management
- Property image uploads
- Amenities support
- Property booking system
- PostgreSQL database integration
- Django admin interface

---

## Technology Stack

- Python 3.10+
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT for authentication

---

## Project Structure

```text
houseHunt/
├── backend/
│   ├── backend/          # Django project settings
│   ├── listings/         # Main application (models, serializers, views, URLs)
│   ├── manage.py
│   └── requirements.txt
├── .env.example
└── README.md