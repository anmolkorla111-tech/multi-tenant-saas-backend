\# SaaS Attendance Backend (FastAPI + PostgreSQL)



A clean backend API for managing users and attendance records using FastAPI, PostgreSQL, and SQLAlchemy.



This repository's \*\*main branch\*\* is a stable, recruiter-ready version.



---



\## 🚀 Features



\- Create User API

\- Duplicate Email Validation

\- Mark Attendance (present / absent)

\- Get Attendance List

\- PostgreSQL Integration

\- Swagger UI Testing

\- Postman Testing



---



\## 🛠 Tech Stack



\- FastAPI

\- PostgreSQL

\- SQLAlchemy

\- Uvicorn

\- Pydantic



---



\## 📂 Project Structure



\- main.py → API routes

\- database.py → DB connection

\- models.py → SQLAlchemy models

\- create\_tables.py → Create DB tables

\- test\_db.py → Test DB connection

\- screenshots/ → Working proof screenshots



---



\## ⚙️ Setup Instructions (Windows)



\### 1️⃣ Clone Repository



git clone https://github.com/anmolkorla111-tech/multi-tenant-saas-backend.git

cd multi-tenant-saas-backend



\### 2️⃣ Create Virtual Environment



python -m venv venv

venv\\Scripts\\activate



\### 3️⃣ Install Dependencies



pip install -r requirements.txt



\### 4️⃣ Create Database



Create PostgreSQL database:

saas\_app\_db



\### 5️⃣ Create Tables



python create\_tables.py



\### 6️⃣ Run Server



python -m uvicorn main:app --reload



---



\## 🌐 Swagger UI



http://127.0.0.1:8000/docs



---



\## 📸 Proof of Working Backend



\### Swagger Overview

!\[Swagger Overview](./screenshots/swagger\_overview.png)



\### Create User Success

!\[Create User Success](./screenshots/swagger\_success\_user.png)



\### Duplicate Email Validation

!\[Duplicate Validation](./screenshots/swagger\_duplicate\_validation.png)



\### Mark Attendance

!\[Mark Attendance](./screenshots/swagger\_attendance\_mark.png)



\### Attendance List

!\[Attendance List](./screenshots/swagger\_attendance\_list.png)



\### Database Tables (pgAdmin)

!\[User Table](./screenshots/db\_user.png)



!\[Attendance Table](./screenshots/db\_attendance.png)

---



\## 🔮 Roadmap



Multi-tenant support (Tenant isolation, RBAC, advanced SaaS features) is being developed in a separate feature branch.

