# Quick Production Deployment Guide - Railway.app

This is the EASIEST way to deploy your Gym Management System to production.

## Why Railway?

- ✅ Free tier available ($5 credit/month)
- ✅ Automatic deployments from GitHub
- ✅ PostgreSQL database included
- ✅ HTTPS/SSL automatic
- ✅ No server management needed
- ✅ Takes ~15 minutes

## Prerequisites

1. GitHub account
2. Your code pushed to GitHub
3. Railway account (free)

---

## Step 1: Prepare Your Code

### 1.1 Create Procfile
Create a file named `Procfile` (no extension) in your project root:

```
web: gunicorn gym_project.wsgi --log-file -
```

### 1.2 Create runtime.txt
Create `runtime.txt` in your project root:

```
python-3.11.0
```

### 1.3 Update requirements.txt
Make sure `requirements.txt` includes:
```
Django==5.2.7
gunicorn==23.0.0
psycopg2-binary==2.9.10
python-decouple==3.8
whitenoise==6.8.2
Pillow==11.0.0
```

### 1.4 Commit and Push
```bash
git add Procfile runtime.txt requirements.txt
git commit -m "Prepare for Railway deployment"
git push origin main
```

---

## Step 2: Sign Up for Railway

1. Go to https://railway.app/
2. Click "Start a New Project"
3. Sign up with GitHub (free)
4. Authorize Railway to access your repositories

---

## Step 3: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your gym system repository
4. Railway will detect it's a Django app

---

## Step 4: Add PostgreSQL Database

1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway creates and connects it automatically
4. Database credentials are auto-configured

---

## Step 5: Configure Environment Variables

Click on your web service → "Variables" tab

Add these variables:

```
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}

# Database (auto-filled by Railway)
DATABASE_URL=${{DATABASE_URL}}

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

**Generate SECRET_KEY:**
```python
# Run locally
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## Step 6: Update settings.py for Railway

Railway provides `DATABASE_URL`, so we need to parse it.

Add this to the top of `settings.py` (after imports):

```python
import dj_database_url

# ... existing code ...

# Database configuration
if 'DATABASE_URL' in os.environ:
    # Production (Railway)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    # Development
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
            'NAME': config('DB_NAME', default=str(BASE_DIR / 'db.sqlite3')),
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default=''),
            'PORT': config('DB_PORT', default=''),
        }
    }
```

Also update `ALLOWED_HOSTS`:
```python
# Add Railway domain
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
if 'RAILWAY_PUBLIC_DOMAIN' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RAILWAY_PUBLIC_DOMAIN'])
```

---

## Step 7: Add dj-database-url to requirements.txt

```
dj-database-url==2.1.0
```

Commit and push:
```bash
git add requirements.txt gym_project/settings.py
git commit -m "Configure for Railway deployment"
git push origin main
```

---

## Step 8: Deploy!

Railway automatically:
1. Detects your push
2. Installs dependencies
3. Runs migrations (if configured)
4. Starts your app

Watch the deployment logs in Railway dashboard.

---

## Step 9: Run Initial Setup Commands

In Railway dashboard → your service → "Settings":

1. Find the "Deploy" section
2. Add these commands to run after deploy:

**One-time setup commands:**
```bash
python manage.py migrate
python manage.py createsuperuser --noinput --username admin --email admin@example.com
python manage.py collectstatic --noinput
```

**Or run manually in Railway CLI:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Run commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic --noinput
```

---

## Step 10: Access Your Live Site

1. In Railway dashboard, find your service
2. Click "Settings" → "Generate Domain"
3. You'll get a URL like: `your-app.up.railway.app`
4. Visit it in your browser!

---

## Troubleshooting

### Build fails
- Check deployment logs in Railway
- Verify all dependencies in requirements.txt
- Ensure Procfile is correct

### Static files not loading
- Make sure WhiteNoise is in requirements.txt
- Check STATIC_ROOT in settings.py
- Run collectstatic command

### Database errors
- Verify PostgreSQL is added to project
- Check DATABASE_URL is set
- Run migrations: `railway run python manage.py migrate`

### 500 errors
- Check logs: Railway dashboard → Deployments → View logs
- Verify DEBUG=False
- Check ALLOWED_HOSTS includes Railway domain

---

## Cost

**Free Tier:**
- $5 credit per month
- Enough for small apps
- PostgreSQL included

**When you outgrow free:**
- Pay-as-you-go
- ~$5-10/month for small app
- Scales automatically

---

## Alternative: Render.com

Very similar to Railway:

1. Go to https://render.com/
2. Connect GitHub
3. Create "Web Service"
4. Add PostgreSQL database
5. Configure environment variables
6. Deploy!

Both are excellent for Django apps.

---

## Production Checklist

Before going live:
- [ ] DEBUG=False
- [ ] Strong SECRET_KEY
- [ ] PostgreSQL database connected
- [ ] ALLOWED_HOSTS configured
- [ ] Static files collecting
- [ ] Admin account created
- [ ] SSL/HTTPS enabled (automatic on Railway)
- [ ] Database backups enabled
- [ ] Monitor logs regularly

---

## Updating Your App

Just push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Railway automatically redeploys!

---

**You're now in production! 🚀**

Your app is live and accessible to anyone on the internet.

---

**Last Updated:** 2025-11-22
