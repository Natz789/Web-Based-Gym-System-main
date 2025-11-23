# Gym System - Render Deployment Guide

Complete guide to deploying the Web-Based Gym Management System on Render.

**Table of Contents:**
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Deployment](#step-by-step-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Post-Deployment](#post-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Overview

This guide covers deploying the Gym System Django application on Render with a PostgreSQL database. The deployment includes:

- **Web Application**: Django 5.2.7 with Gunicorn
- **Database**: PostgreSQL 15 (using provided Render credentials)
- **Static Files**: WhiteNoise with Render Disk storage
- **Media Storage**: Persistent disk for user uploads
- **SSL/TLS**: Automatic HTTPS with Render

### System Requirements

- Render account (free or paid)
- GitHub repository access
- PostgreSQL database credentials (provided)
- 10GB+ storage for media files

---

## Prerequisites

### 1. Render Account Setup

1. Create a Render account at https://render.com
2. Connect your GitHub repository to Render
3. Authorize Render to access your GitHub account

### 2. PostgreSQL Database Credentials

You have been provided with the following PostgreSQL credentials:

```
Name: Gym
Hostname: dpg-d4hgpcruibrs73djpc7g-a
Port: 5432
Database: gym_4iym
Username: gym_4iym_user
Password: kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6
Internal URL: postgresql://gym_4iym_user:kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6@dpg-d4hgpcruibrs73djpc7g-a/gym_4iym
External URL: postgresql://gym_4iym_user:kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6@dpg-d4hgpcruibrs73djpc7g-a.singapore-postgres.render.com/gym_4iym
```

**⚠️ IMPORTANT**: These credentials are sensitive. Never commit them to version control.

### 3. GitHub Repository

Ensure your repository has:
- `render.yaml` (Infrastructure as Code configuration)
- `build.sh` (Build script for Render)
- `requirements.txt` (Python dependencies)
- `.env.example` (Environment variables template)

---

## Step-by-Step Deployment

### Step 1: Set Up PostgreSQL Connection

You have **TWO options** for using the provided PostgreSQL database:

#### Option A: Manual Setup with Render Dashboard (Recommended)

1. Go to Render Dashboard → New → Web Service
2. Choose your GitHub repository
3. Configure service settings:
   - **Name**: `gym-system-web`
   - **Runtime**: Python
   - **Python Version**: 3.11
   - **Build Command**: `bash ./build.sh`
   - **Start Command**: `gunicorn gym_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class sync --worker-timeout 60`

#### Option B: Using Infrastructure as Code (render.yaml)

Render now supports `render.yaml` for infrastructure definition. The repository includes a pre-configured `render.yaml` file.

To use it:
1. Go to Render Dashboard
2. Click **New** → **Web Service**
3. Select your GitHub repository
4. Render will auto-detect `render.yaml` and load the configuration
5. Review settings and click **Deploy**

### Step 2: Configure Environment Variables

The `render.yaml` file automatically configures most environment variables. However, you MUST manually set the database password:

1. **In Render Dashboard** → Your web service
2. **Go to Environment**
3. **Add/Update the following critical variable**:

#### Database Password (MUST BE SET MANUALLY)

```
DB_PASSWORD=kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6
```

⚠️ **IMPORTANT**: The `DB_PASSWORD` is intentionally marked as `sync: false` in `render.yaml` to prevent it from being stored in version control. You must:
1. Set this value manually in Render Dashboard
2. Never commit this to GitHub
3. Use Render's environment variable settings for secrets

#### Other Database Configuration (Auto-configured in render.yaml)

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=gym_4iym
DB_USER=gym_4iym_user
DB_HOST=dpg-d4hgpcruibrs73djpc7g-a.singapore-postgres.render.com
DB_PORT=5432
```

#### Django Security Settings

```
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<Render will auto-generate this>
ALLOWED_HOSTS=your-domain.onrender.com,yourdomain.com,www.yourdomain.com
```

#### HTTPS/SSL Settings

```
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

#### Optional: AI Chatbot Configuration

If using the Ollama AI chatbot feature:

```
OLLAMA_HOST=http://your-ollama-instance:11434
```

### Step 3: Persistent Disk (Auto-configured)

The `render.yaml` automatically configures a 10GB persistent disk for:
- Static files (CSS, JavaScript, images)
- User-uploaded media files

**Auto-configured in render.yaml**:
- **Mount Path**: `/var/data`
- **Size**: 10GB
- **Environment Variables**:
  ```
  STATIC_ROOT=/var/data/staticfiles
  MEDIA_ROOT=/var/data/media
  ```

If you need to adjust the disk size, edit `render.yaml` and redeploy.

### Step 4: Configure Custom Domain (Optional)

To use your own domain instead of `*.onrender.com`:

1. **In Render Dashboard** → Your web service
2. **Go to Settings** → **Custom Domain**
3. **Add your domain** (e.g., `gym.yourdomain.com`)
4. **Update your domain registrar**:
   - Add a CNAME record pointing to your Render app URL
   - Or use the nameservers provided by Render
5. **Render will auto-provision SSL certificate** (via Let's Encrypt)

### Step 5: Deploy Application

1. **Push to GitHub** (your changes should already be pushed)
2. **Go to Render Dashboard** → **New** → **Web Service**
3. **Connect your GitHub repository**
4. **Render auto-detects `render.yaml`** and loads configuration
5. **Before deploying, set `DB_PASSWORD` environment variable**:
   - Click **Environment** tab
   - Click **Add Environment Variable**
   - Key: `DB_PASSWORD`
   - Value: `kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6`
   - Click **Save**
6. **Click Deploy**
7. **Watch the build logs**:
   - Dependencies installation
   - Static file collection
   - Database migrations
   - Gunicorn startup
   - Build completion

**Initial deployment may take 5-15 minutes.**

---

## Environment Configuration

### Understanding the Environment Variables

#### Development vs Production

**Development (Local):**
```bash
ENVIRONMENT=development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**Production (Render):**
```bash
ENVIRONMENT=production
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com
DB_ENGINE=django.db.backends.postgresql
# PostgreSQL credentials from Render
```

### Setting Up Local .env File

For local development, create `.env` file (not in git):

```bash
# Copy from .env.example and modify
cp .env.example .env

# Edit .env with your values
# For local development:
SECRET_KEY=your-generated-secret-key
ENVIRONMENT=development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# SQLite for development
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# For testing with Render's PostgreSQL:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=gym_4iym
# DB_USER=gym_4iym_user
# DB_PASSWORD=kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6
# DB_HOST=dpg-d4hgpcruibrs73djpc7g-a.singapore-postgres.render.com
# DB_PORT=5432
```

---

## Database Setup

### PostgreSQL Connection Details

The provided PostgreSQL instance is hosted on Render's Singapore region.

**Connection String (Internal - from within Render services):**
```
postgresql://gym_4iym_user:kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6@dpg-d4hgpcruibrs73djpc7g-a/gym_4iym
```

**Connection String (External - from outside Render):**
```
postgresql://gym_4iym_user:kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6@dpg-d4hgpcruibrs73djpc7g-a.singapore-postgres.render.com/gym_4iym
```

### Initial Database Setup

When you deploy to Render:

1. **Build script automatically runs** (`build.sh`):
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

2. **Database migrations are applied** to the PostgreSQL instance

3. **Static files are collected** to the persistent disk

### Seeding Initial Data (Optional)

To populate the database with initial data:

1. **Via Django Admin** (Recommended):
   - Create a superuser
   - Use the Django admin interface

2. **Via Management Commands**:
   ```bash
   python manage.py createadmin
   python manage.py seed_database
   python manage.py comprehensive_seeder
   ```

   To run management commands on Render:
   - Use Render Shell (available in dashboard)
   - Or create a one-off job

3. **Example: Create Admin User via Render Shell**:
   ```bash
   python manage.py createadmin
   ```

---

## Post-Deployment

### 1. Verify Application

1. **Access your application**: `https://your-domain.onrender.com`
2. **Check the homepage** loads correctly
3. **Test login functionality**
4. **Verify static files** (CSS/images) load properly

### 2. Create Admin User

Access Render Shell for your web service:

```bash
# Connect to the running service
python manage.py createsuperuser

# Or use the custom command
python manage.py createadmin
```

### 3. Access Django Admin

Visit: `https://your-domain.onrender.com/admin`
- Username: admin
- Password: (the one you created)

### 4. Test Database Connection

```bash
# Connect via Render Shell
python manage.py dbshell

# Or check in Django Shell
python manage.py shell
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute("SELECT version();")
>>> print(cursor.fetchone())
```

### 5. View Logs

**In Render Dashboard**:
- **Logs** tab shows real-time application logs
- **Metrics** tab shows resource usage

**Common Log Files**:
- Gunicorn access logs
- Django error logs
- Database connection logs

### 6. Monitor Performance

Use Render's built-in monitoring:
- CPU usage
- Memory consumption
- Requests per second
- Error rates

---

## Troubleshooting

### Deployment Issues

#### 1. Build Fails

**Error**: `pip install` fails during build

**Solution**:
- Check `requirements.txt` for syntax errors
- Ensure all packages are compatible with Python 3.11
- Review build logs in Render dashboard

**Command to test locally**:
```bash
pip install -r requirements.txt
```

#### 2. Database Connection Error

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
- Verify PostgreSQL credentials are correct
- Check `DB_HOST` includes full domain (for external access)
- Ensure IP whitelist if using restricted access

**Test connection**:
```bash
PGPASSWORD=kSZlA71WuWG7R9srM0yk3hzs1GbO8Ts6 psql \
  -h dpg-d4hgpcruibrs73djpc7g-a.singapore-postgres.render.com \
  -U gym_4iym_user \
  gym_4iym
```

#### 3. Static Files Not Loading

**Error**: CSS/images return 404

**Solution**:
- Check disk is mounted and has space
- Verify `STATIC_ROOT` in environment variables
- Run `collectstatic` command:
  ```bash
  python manage.py collectstatic --noinput
  ```

#### 4. Application Crashes After Deploy

**Error**: Service keeps restarting

**Solution**:
- Check logs in Render dashboard
- Common causes:
  - Missing environment variables
  - Database migration errors
  - Memory limit exceeded (upgrade instance)
- Review recent commits for breaking changes

#### 5. Secret Key Not Generated

**Error**: `SECRET_KEY` is empty

**Solution**:
- Render auto-generates this, but if it fails:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Manually set in Render environment variables

### Runtime Issues

#### Memory Issues

If seeing out-of-memory errors:
1. Reduce Gunicorn workers in `build.sh`:
   ```bash
   gunicorn gym_project.wsgi:application \
     --bind 0.0.0.0:$PORT \
     --workers 2  # Reduce from 3
   ```
2. Upgrade Render instance to Standard plan

#### Slow Performance

1. **Check database**:
   - Run slow query analysis
   - Add database indexes

2. **Optimize views**:
   - Use `select_related()` and `prefetch_related()`
   - Implement caching

3. **Scale application**:
   - Increase `numInstances` in `render.yaml`
   - Use a larger Render plan

### Database Issues

#### Disk Space

Check disk usage:
```bash
# In Render Shell
du -sh /var/www/gym-system/
du -sh /var/www/gym-system/media/
```

Clean up if needed:
```bash
python manage.py cleanup_database
```

#### Database Backup

Render automatically backs up PostgreSQL. To restore:
1. Go to Render dashboard → Database instance
2. **Backups** tab
3. Click **Restore** on desired backup

---

## Monitoring and Maintenance

### Daily Monitoring

- **Check Render dashboard** for errors and crashes
- **Monitor resource usage** (CPU, memory, storage)
- **Review application logs** for warnings

### Weekly Maintenance

- **Update dependencies**:
  ```bash
  pip list --outdated
  ```
- **Check database size** and storage
- **Review audit logs** for suspicious activity

### Monthly Tasks

- **Security updates**:
  ```bash
  pip install --upgrade django psycopg2-binary
  ```
- **Database optimization**:
  ```bash
  python manage.py cleanup_database
  ```
- **Backup verification** (test restore)

### Automated Monitoring Setup

Use Render's built-in alerts:
1. **Render Dashboard** → Settings
2. **Notifications** → Set up email alerts for:
   - Deployment failures
   - High CPU usage
   - High memory usage
   - Database connection errors

### Debugging Commands (via Render Shell)

```bash
# Check application status
ps aux | grep gunicorn

# View recent logs
tail -100 /var/log/render/*.log

# Test database
python manage.py dbshell

# Check environment variables
env | grep DB_

# Run management command
python manage.py showmigrations
python manage.py migrate --dry-run
```

---

## Advanced Configuration

### Custom Gunicorn Settings

Edit `build.sh` to customize Gunicorn:

```bash
gunicorn gym_project.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 4 \
  --worker-class sync \
  --worker-timeout 60 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### Background Jobs

For long-running tasks, consider:
- **Render Background Workers** (separate service)
- **Celery** with Redis (for task queue)
- **Scheduled jobs** via management commands

### Caching Strategy

Implement caching for better performance:

```python
# In Django settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

For distributed caching, use Redis.

---

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Set up Render account | 5 min |
| 2 | Configure environment variables | 5 min |
| 3 | Set up persistent disk | 5 min |
| 4 | Deploy application | 10-15 min |
| 5 | Create admin user | 2 min |
| 6 | Verify application | 5 min |

**Total estimated time: 30-40 minutes**

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **GitHub Issues**: Report issues in the repository

---

## Frequently Asked Questions

### Q: Can I use SQLite in production?
**A**: No, SQLite is not suitable for production. Use PostgreSQL (provided).

### Q: How do I update the application?
**A**: Push changes to GitHub. Render auto-detects and redeploys.

### Q: Can I have multiple instances?
**A**: Yes, set `numInstances` in `render.yaml` or Render dashboard.

### Q: How do I scale the database?
**A**: Upgrade your Render PostgreSQL plan from Starter to Standard/Premium.

### Q: Is SSL/HTTPS automatic?
**A**: Yes, Render provides free SSL via Let's Encrypt automatically.

### Q: How do I reset the database?
**A**: Use Render Shell to run: `python manage.py migrate zero gym_app`

---

**Last Updated**: 2025-11-23
**Django Version**: 5.2.7
**Python Version**: 3.11
**Render Region**: Singapore
