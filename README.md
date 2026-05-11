# Smart Task Manager

A Flask-based Smart Task Manager with:

- User Authentication
- Task Management
- Analytics using Pandas & NumPy
- Real-time Notifications using WebSockets
- PostgreSQL Database
- Responsive UI

---

# Technologies Used

- Python
- Flask
- Flask-SocketIO
- PostgreSQL
- SQLAlchemy
- Pandas
- NumPy
- HTML
- CSS
- JavaScript

---

# Setup Instructions

## 1. Clone Repository

git clone <repo_link>

---

## 2. Create Virtual Environment

python -m venv venv

---

## 3. Activate Environment

### Windows

venv\Scripts\activate

---

## 4. Install Dependencies

pip install -r requirements.txt

---

## 5. Configure PostgreSQL

Create database:

taskmanager

Update database URI in app.py

Example:

app.config['SQLALCHEMY_DATABASE_URI'] = \
'postgresql://postgres:your_password@localhost/taskmanager'

---

## 6. Run Application

python app.py

---

## 7. Open Browser

Access the application:
The app runs on a local Flask server at http://localhost:5000 after startup.

---

# Features

- Register/Login
- Add Task
- Update Task
- Delete Task
- Analytics Dashboard
- WebSocket Notifications
- Responsive Design

---

# Project Structure

smart-task-manager/

│

├── app.py

├── db.py

├── extensions.py

├── requirements.txt

├── database_schema.sql

├── README.md

│

├── models/

├── routes/

├── templates/

---

# Database Schema

## User Table

| Column | Type |
|---|---|
| id | Integer |
| username | String |
| email | String |
| password | String |

---

## Task Table

| Column | Type |
|---|---|
| id | Integer |
| title | String |
| description | Text |
| priority | String |
| status | String |
| created_date | Timestamp |
| user_id | Integer |

---

# Author

Kallam Divyasri
