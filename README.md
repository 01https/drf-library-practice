# DRF Library Practice

## This is a practice that is not a pet project.

## Description
A web-based application for managing flights, airplanes, routes, crew assignments,
and providing users with the ability to book tickets.

## Features
- Implement the CRUD functionality for the Books Service
- Add permissions to the Books Service
- Implement CRUD for the Users Service
- Implement the Borrowing List & Detail endpoint
- Implement the Create Borrowing endpoint
- Add filtering for the Borrowings List endpoint

## Technologies Used
- **Backend:** Django Framework
- **Database:** Sqlite
- **API:** Django REST Framework

## Installation
### Python 3 must be installed
1. **Clone the repository:**
   ```bash
   git clone https://github.com/01https/api-airport.git
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
3. **Install dependencies:**
    ```bash
   pip install -r requirements.txt
6. **Apply database migrations:**
    ```bash
   python manage.py migrate
7. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
8. **Start the development server:**
    ```bash
   python manage.py runserver
