# 🎓 BCA Admission System

A full-stack web-based admission portal built with **Django**, **MySQL**, and **Bootstrap 5** that digitizes the entire BCA college admission process — from student registration to admin approval.

---

## 📌 Project Overview

The BCA Admission System allows students to apply for Bachelor of Computer Applications (BCA) admission online without visiting the college physically. It features a **role-based access system** where students and admins have completely separate login pages, dashboards, and permissions.

---

## ✨ Features

### 👩‍🎓 Student Side
- Register and login securely
- Fill a **4-step multi-page admission form** (Personal → Address → Academic → Review)
- Upload a **profile picture** (JPG, PNG, WEBP, GIF — error-free handling)
- View application status in real time from the dashboard
- See detailed application info with a visual **status timeline**
- Receive admin remarks (approval/rejection reasons) directly on dashboard

### 🛡️ Admin Side
- Separate **Admin Login Page** (restricted access only)
- View **all student applications** in a searchable, filterable table
- **Approve** applications with one click
- **Reject** applications with a mandatory reason (shown to student)
- Mark applications as **Under Review**
- Stats dashboard: Total / Pending / Approved / Rejected counts
- Search by name, application number, email, or phone
- Filter by status and sort by date or percentage

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10, Django 5.2 |
| Database | MySQL (via XAMPP) |
| Frontend | Bootstrap 5, HTML5, CSS3, JavaScript |
| Image Handling | Pillow |
| Forms | Django Crispy Forms + crispy-bootstrap5 |
| Icons | Font Awesome 6 |


---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- XAMPP (for MySQL)
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/NaziyaAkbari/bca-admission-system.git
cd bca-admission-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start XAMPP MySQL
- Open XAMPP Control Panel
- Start **MySQL**
- Go to `http://localhost/phpmyadmin`
- Create a new database: **`bca_admission_db`**

### 5. Configure Database in `settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bca_admission_db',
        'USER': 'root',
        'PASSWORD': '',        # XAMPP default — no password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Admin (Superuser)
```bash
python manage.py createsuperuser
```

### 8. Run the Server
```bash
python manage.py runserver
```

### AUTHOR: NAZIYA AKBARI
