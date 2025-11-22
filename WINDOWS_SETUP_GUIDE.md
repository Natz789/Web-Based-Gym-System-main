# Windows Setup Guide - Rhose Gym Management System

This guide will help you set up and run the Gym Management System on Windows for development and testing.

## Prerequisites

Before starting, ensure you have:
- Windows 10/11
- Administrator access
- Internet connection

---

## Step 1: Install Python

### 1.1 Download Python
1. Go to https://www.python.org/downloads/
2. Download **Python 3.10 or higher** (recommended: Python 3.11)
3. Run the installer

### 1.2 Install Python (IMPORTANT)
1. ✅ **CHECK** "Add Python to PATH" (very important!)
2. Click "Install Now"
3. Wait for installation to complete
4. Click "Close"

### 1.3 Verify Installation
Open PowerShell and run:
```powershell
python --version
```
You should see something like: `Python 3.11.x`

---

## Step 2: Install Git (if not already installed)

### 2.1 Download Git
1. Go to https://git-scm.com/download/win
2. Download the installer
3. Run the installer with default settings

### 2.2 Verify Installation
```powershell
git --version
```

---

## Step 3: Clone or Navigate to Project

### Option A: If you already have the project
```powershell
# Navigate to your project folder
cd D:\Web-Based-Gym-System-main-main
```

### Option B: If you need to clone it
```powershell
# Navigate to where you want the project
cd D:\

# Clone the repository
git clone <your-repository-url>
cd Web-Based-Gym-System-main
```

---

## Step 4: Create Virtual Environment

### 4.1 Create Virtual Environment
```powershell
# Make sure you're in the project directory
cd D:\Web-Based-Gym-System-main-main

# Create virtual environment
python -m venv venv
```

### 4.2 Activate Virtual Environment
```powershell
# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```

**If you get an error about execution policy:**
```powershell
# Run this command first (one-time setup)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1
```

**You'll know it worked when you see `(venv)` at the start of your prompt:**
```
(venv) PS D:\Web-Based-Gym-System-main-main>
```

---

## Step 5: Install Python Dependencies

### 5.1 Upgrade pip
```powershell
python -m pip install --upgrade pip
```

### 5.2 Install Requirements
```powershell
pip install -r requirements.txt
```

This will install:
- Django 5.2.7
- python-decouple (for environment variables)
- Pillow (for image handling)
- gunicorn, psycopg2-binary, whitenoise (for production, won't be used in development)
- ollama (for AI chatbot)

**Wait for all packages to install (may take 2-5 minutes)**

---

## Step 6: Configure Environment Variables

### 6.1 Create .env File
```powershell
# Copy the example file
Copy-Item .env.example .env
```

### 6.2 Edit .env File
```powershell
# Open in Notepad
notepad .env
```

### 6.3 Update .env for Development
Replace the contents with this (for local development):

```env
# Django Configuration
SECRET_KEY=django-insecure-4yj)609$72ppy!&e527=wsgm9+_sasg^3^)r263)ykovwj_c(r

# Environment: development
ENVIRONMENT=development

# Debug Mode (enabled for development)
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration - SQLite for development
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Security Settings (disabled for local development)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
```

**Save and close Notepad**

---

## Step 7: Set Up Database

### 7.1 Run Migrations
```powershell
# Create database tables
python manage.py migrate
```

You should see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, gym_app, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### 7.2 Create Admin User
```powershell
# Create superuser account
python manage.py createsuperuser
```

Enter details when prompted:
- **Username:** (e.g., admin)
- **Email:** (can leave blank, just press Enter)
- **Password:** (type password - it won't show on screen)
- **Password (again):** (retype same password)

---

## Step 8: Load Sample Data (Optional)

### 8.1 Load Demo Data
If you want sample members, plans, etc.:

```powershell
# Run the seeder
python manage.py seed_database
```

This creates:
- Admin account (if you didn't create one)
- Sample membership plans
- Sample members
- Sample attendance records

---

## Step 9: Run the Development Server

### 9.1 Start Server
```powershell
python manage.py runserver
```

You should see:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 22, 2025 - 10:30:00
Django version 5.2.7, using settings 'gym_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 9.2 Open in Browser
1. Open your web browser
2. Go to: **http://127.0.0.1:8000/** or **http://localhost:8000/**

---

## Step 10: Access the Application

### Main Pages:
- **Homepage:** http://localhost:8000/
- **Login:** http://localhost:8000/login/
- **Admin Dashboard:** http://localhost:8000/dashboard/
- **Django Admin:** http://localhost:8000/admin/

### Login Credentials:
Use the superuser credentials you created in Step 7.2

---

## Step 11: Install Ollama for AI Chatbot (Optional)

The chatbot feature requires Ollama running locally.

### 11.1 Download Ollama
1. Go to https://ollama.com/download/windows
2. Download "Ollama for Windows"
3. Run the installer

### 11.2 Install AI Models
Open a new PowerShell window:

```powershell
# Install Llama 2 (recommended)
ollama pull llama2

# OR install Mistral (faster)
ollama pull mistral
```

### 11.3 Verify Ollama is Running
```powershell
ollama list
```

You should see your installed models.

---

## Common Issues & Solutions

### Issue 1: "python is not recognized"
**Solution:** Python not in PATH
1. Reinstall Python
2. Make sure to check "Add Python to PATH"
3. Restart PowerShell

### Issue 2: "Cannot activate virtual environment"
**Solution:** Execution policy issue
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 3: "No module named 'decouple'"
**Solution:** Virtual environment not activated or requirements not installed
```powershell
# Make sure (venv) appears in your prompt
.\venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt
```

### Issue 4: Port 8000 already in use
**Solution:** Kill the process or use different port
```powershell
# Use different port
python manage.py runserver 8080

# Then access: http://localhost:8080/
```

### Issue 5: Static files not loading
**Solution:** Run collectstatic
```powershell
python manage.py collectstatic --noinput
```

### Issue 6: "OperationalError: no such table"
**Solution:** Run migrations
```powershell
python manage.py migrate
```

---

## Daily Development Workflow

### Starting Work:
```powershell
# 1. Navigate to project
cd D:\Web-Based-Gym-System-main-main

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Start server
python manage.py runserver
```

### Stopping Work:
```powershell
# 1. Stop server (in the terminal where server is running)
Ctrl + C

# 2. Deactivate virtual environment
deactivate
```

---

## Project Structure

```
Web-Based-Gym-System-main/
├── gym_project/              # Main project settings
│   ├── settings.py          # Configuration file
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config
├── gym_app/                 # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── venv/                    # Virtual environment (created)
├── db.sqlite3              # Database file (created)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (created)
└── .env.example            # Environment template
```

---

## Updating the Application

### Pull Latest Changes:
```powershell
# 1. Stop the server (Ctrl + C)

# 2. Pull changes
git pull origin main

# 3. Install any new dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Restart server
python manage.py runserver
```

---

## Testing the Application

### Access Different User Roles:

**1. Admin Dashboard:**
- Login with your superuser account
- Access all features

**2. Staff Dashboard:**
- Create staff user in Django admin
- Test staff-specific features

**3. Member Dashboard:**
- Create member account
- Test member-specific features

---

## Development Tools (Optional but Recommended)

### 1. VS Code (Code Editor)
1. Download: https://code.visualstudio.com/
2. Install Python extension
3. Open project folder in VS Code

### 2. DB Browser for SQLite (Database Viewer)
1. Download: https://sqlitebrowser.org/dl/
2. Open `db.sqlite3` to view database

### 3. Postman (API Testing)
1. Download: https://www.postman.com/downloads/
2. Test API endpoints

---

## Quick Reference Commands

### Virtual Environment:
```powershell
# Activate
.\venv\Scripts\Activate.ps1

# Deactivate
deactivate
```

### Django Commands:
```powershell
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Open Django shell
python manage.py shell
```

### Database:
```powershell
# Reset database (WARNING: Deletes all data!)
Remove-Item db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## Getting Help

### If you encounter issues:

1. **Check the error message** - Read carefully
2. **Check this guide** - Solution might be in "Common Issues"
3. **Check Django documentation** - https://docs.djangoproject.com/
4. **Check project logs** - Look in `logs/` folder (if exists)

### Useful Django Debug Commands:
```powershell
# Check for issues
python manage.py check

# View migrations status
python manage.py showmigrations

# Test database connection
python manage.py dbshell
```

---

## Production Deployment

⚠️ **DO NOT use `python manage.py runserver` for production!**

For production deployment:
- See `PRODUCTION_DEPLOYMENT.md` for Linux/Cloud deployment
- Consider platforms like:
  - **Heroku** (easiest)
  - **Railway** (modern)
  - **PythonAnywhere** (beginner-friendly)
  - **DigitalOcean** (full control)

---

## Security Reminders

### For Development (Local):
✅ DEBUG=True is OK
✅ SQLite is OK
✅ Simple SECRET_KEY is OK

### For Production (Public):
❌ NEVER set DEBUG=True
❌ NEVER use SQLite
❌ NEVER use the default SECRET_KEY
❌ NEVER commit .env file to git
✅ Use PostgreSQL/MySQL
✅ Use strong SECRET_KEY
✅ Enable HTTPS/SSL
✅ Follow `PRODUCTION_DEPLOYMENT.md`

---

## Next Steps

1. ✅ Complete setup (Steps 1-9)
2. ✅ Create admin account
3. ✅ Explore the application
4. ✅ Test all features
5. 📚 Read Django documentation
6. 💻 Start customizing!

---

**Congratulations! You now have the Gym Management System running on Windows!** 🎉

For questions or issues, refer to the main README.md or open an issue on GitHub.

---

**Last Updated:** 2025-11-22
**Version:** 1.0
**Platform:** Windows 10/11
