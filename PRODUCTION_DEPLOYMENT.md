# Production Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Rhose Gym Management System to a production environment.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher (recommended) or MySQL 8.0+
- Nginx or Apache web server
- Ubuntu 20.04+ or similar Linux distribution
- SSL/TLS certificate (Let's Encrypt recommended)
- Ollama (for AI chatbot functionality)

## 1. Server Setup

### Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Install Dependencies
```bash
# Python and pip
sudo apt install python3.10 python3.10-venv python3-pip -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Nginx
sudo apt install nginx -y

# Ollama (for chatbot)
curl -fsSL https://ollama.com/install.sh | sh
```

## 2. Database Configuration

### Create PostgreSQL Database
```bash
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE gym_system_db;
CREATE USER gym_user WITH PASSWORD 'your_secure_password';
ALTER ROLE gym_user SET client_encoding TO 'utf8';
ALTER ROLE gym_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gym_user SET timezone TO 'Asia/Manila';
GRANT ALL PRIVILEGES ON DATABASE gym_system_db TO gym_user;
\q
```

## 3. Application Setup

### Create Application Directory
```bash
sudo mkdir -p /var/www/gym-system
sudo chown $USER:$USER /var/www/gym-system
cd /var/www/gym-system
```

### Clone Repository
```bash
git clone <your-repository-url> .
```

### Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Environment Configuration

### Create .env File
```bash
cp .env.example .env
nano .env
```

### Configure Environment Variables
Edit `.env` with your production values:

```bash
# Generate a new SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Update `.env`:
```
SECRET_KEY=<generated-secret-key>
ENVIRONMENT=production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=gym_system_db
DB_USER=gym_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Static/Media Files
STATIC_ROOT=/var/www/gym-system/staticfiles
MEDIA_ROOT=/var/www/gym-system/media
```

## 5. Database Migration

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## 6. Create Required Directories

```bash
mkdir -p logs media staticfiles
chmod 755 logs media staticfiles
```

## 7. Gunicorn Configuration

### Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/gym-system.service
```

Add the following content:
```ini
[Unit]
Description=Gym Management System Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/gym-system
Environment="PATH=/var/www/gym-system/venv/bin"
ExecStart=/var/www/gym-system/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/gym-system/gym-system.sock \
          --timeout 120 \
          gym_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Set Permissions
```bash
sudo chown -R www-data:www-data /var/www/gym-system
```

### Start Gunicorn
```bash
sudo systemctl start gym-system
sudo systemctl enable gym-system
sudo systemctl status gym-system
```

## 8. Nginx Configuration

### Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/gym-system
```

Add the following:
```nginx
upstream gym_system {
    server unix:/var/www/gym-system/gym-system.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 10M;

    # Static files
    location /static/ {
        alias /var/www/gym-system/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/gym-system/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Application
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://gym_system;
    }
}
```

### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/gym-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 9. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 10. Ollama Setup (For Chatbot)

```bash
# Pull required models
ollama pull llama2
ollama pull mistral

# Ensure Ollama runs on startup
sudo systemctl enable ollama
sudo systemctl start ollama
```

## 11. Security Hardening

### Firewall Configuration
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Fail2Ban (Optional but recommended)
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## 12. Maintenance & Monitoring

### View Application Logs
```bash
# Application logs
tail -f /var/www/gym-system/logs/django.log

# Error logs
tail -f /var/www/gym-system/logs/errors.log

# Gunicorn logs
sudo journalctl -u gym-system -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Restart Services
```bash
# Restart application
sudo systemctl restart gym-system

# Restart Nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status gym-system
sudo systemctl status nginx
```

### Database Backups
```bash
# Create backup script
sudo nano /usr/local/bin/backup-gym-db.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/gym-system"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U gym_user gym_system_db > $BACKUP_DIR/gym_db_$DATE.sql
# Keep only last 7 days of backups
find $BACKUP_DIR -name "gym_db_*.sql" -mtime +7 -delete
```

Make executable:
```bash
sudo chmod +x /usr/local/bin/backup-gym-db.sh
```

Add to crontab (daily at 2 AM):
```bash
sudo crontab -e
# Add:
0 2 * * * /usr/local/bin/backup-gym-db.sh
```

## 13. Updates and Deployment

### Deploy New Changes
```bash
cd /var/www/gym-system
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gym-system
```

## 14. Troubleshooting

### Application won't start
```bash
# Check service status
sudo systemctl status gym-system

# Check logs
sudo journalctl -u gym-system -n 50

# Check permissions
ls -la /var/www/gym-system
```

### Static files not loading
```bash
# Recollect static files
python manage.py collectstatic --noinput

# Check Nginx configuration
sudo nginx -t
```

### Database connection issues
```bash
# Test PostgreSQL connection
psql -U gym_user -d gym_system_db -h localhost

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

## 15. Performance Optimization

### Redis Cache (Optional)
```bash
# Install Redis
sudo apt install redis-server -y

# Update .env
# Add: CACHE_BACKEND=redis://localhost:6379/1

# Update settings.py to use Redis cache
```

### Database Connection Pooling
Consider using `pgbouncer` for PostgreSQL connection pooling.

## 16. Security Checklist

- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY set in .env
- [ ] Database credentials secured
- [ ] HTTPS/SSL enabled
- [ ] HSTS headers configured
- [ ] Firewall configured
- [ ] Regular database backups
- [ ] Log rotation configured
- [ ] Fail2Ban installed
- [ ] Strong passwords for all accounts
- [ ] Database not in version control
- [ ] .env file not in version control
- [ ] Regular security updates

## Support

For issues or questions, refer to the main README.md or contact the development team.

---

**Last Updated:** 2025-11-21
