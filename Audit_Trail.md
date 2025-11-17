# 🔍 Audit Trail System - Complete Guide

## Overview

The Audit Trail system provides comprehensive logging of all activities and transactions in your Gym Management System. This ensures accountability, security, and easy troubleshooting.

---

## 📊 What Gets Logged

### 1. Authentication Events
- ✅ **User Login** - Successful logins
- ⚠️ **Login Failed** - Failed login attempts (security monitoring)
- ✅ **User Logout** - When users log out
- ✅ **User Registration** - New member registrations

### 2. Membership Activities
- ✅ **Membership Created** - New subscriptions
- ✅ **Membership Updated** - Subscription changes
- ❌ **Membership Cancelled** - Cancelled subscriptions
- ⏰ **Membership Expired** - Auto-expired memberships

### 3. Financial Transactions
- 💰 **Payment Received** - Member payments
- 🚶 **Walk-in Sale** - Walk-in pass purchases
- 💳 **Payment Refunded** - Refund transactions

### 4. User Management
- 👤 **User Created** - New user accounts
- ✏️ **User Updated** - User profile changes
- 🔐 **Role Changed** - Permission changes
- ❌ **User Deleted** - Account deletions

### 5. Security Events
- 🚫 **Unauthorized Access** - Access denial attempts
- ⚠️ **Permission Denied** - Insufficient permissions
- 🔑 **Password Changed** - Password updates

### 6. System Operations
- 📊 **Report Generated** - Analytics reports
- 📤 **Data Export** - Data exports
- ⚙️ **Settings Changed** - System configuration changes

---

## 🗄️ Database Schema

```sql
Table: audit_logs
├── id (Primary Key)
├── user (Foreign Key → users)
├── action (VARCHAR: login, payment_received, etc.)
├── severity (VARCHAR: info, warning, error, critical)
├── description (TEXT)
├── ip_address (IP Address)
├── user_agent (TEXT: Browser info)
├── model_name (VARCHAR: Related model)
├── object_id (VARCHAR: Related object ID)
├── object_repr (VARCHAR: String representation)
├── extra_data (JSON: Additional data)
└── timestamp (DATETIME with index)
```

---

## 🚀 Setup Instructions

### Step 1: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Verify the Table

```bash
python manage.py shell
```

```python
from gym_app.models import AuditLog
print(AuditLog.objects.count())  # Should work without errors
```

### Step 3: Test Logging

Perform any action (login, logout, subscribe, etc.) and check:

```python
from gym_app.models import AuditLog
logs = AuditLog.objects.all()[:5]
for log in logs:
    print(f"{log.timestamp} - {log.user} - {log.action}")
```

---

## 💻 How to Use

### Accessing the Audit Trail

**For Admins Only:**
1. Login as admin
2. Click "Audit Trail" in the navigation menu
3. URL: http://127.0.0.1:8000/audit-trail/

### Filtering Logs

**By Action:**
- Select action type from dropdown (Login, Payment, etc.)

**By Severity:**
- Info, Warning, Error, Critical

**By User:**
- Search by username

**By Time Period:**
- Last 24 hours
- Last 7 days
- Last 30 days
- Last 90 days
- All time

**Example Filters:**
- Failed logins in last 24 hours → Action: "Login Failed", Days: "1"
- All payments → Action: "Payment Received", Days: "All time"
- Security events → Severity: "Warning" or "Critical"

---

## 🔧 Programmatic Usage

### Creating Audit Logs

```python
from gym_app.models import AuditLog

# Basic log
AuditLog.log(
    action='login',
    user=request.user,
    description='User logged in successfully',
    request=request
)

# Log with extra data
AuditLog.log(
    action='payment_received',
    user=request.user,
    description=f'Payment received: ₱{amount}',
    severity='info',
    request=request,
    model_name='Payment',
    object_id=payment.id,
    object_repr=str(payment),
    amount=float(amount),
    payment_method=method
)

# Security log
AuditLog.log(
    action='unauthorized_access',
    user=request.user,
    description='Attempted to access admin panel',
    severity='warning',
    request=request
)
```

### Querying Logs

```python
from gym_app.models import AuditLog
from datetime import timedelta
from django.utils import timezone

# Get user's recent activity
user_logs = AuditLog.get_user_activity(user, days=30)

# Get security events
security_logs = AuditLog.get_security_events(days=7)

# Get financial transactions
financial_logs = AuditLog.get_financial_transactions(
    start_date=start,
    end_date=end
)

# Custom query
failed_logins = AuditLog.objects.filter(
    action='login_failed',
    timestamp__gte=timezone.now() - timedelta(hours=24)
).count()
```

---

## 📈 Analytics & Reports

### Security Dashboard

```python
# Failed login attempts (potential brute force)
failed_logins = AuditLog.objects.filter(
    action='login_failed'
).values('ip_address').annotate(
    count=Count('id')
).order_by('-count')

# Unauthorized access attempts
unauthorized = AuditLog.objects.filter(
    action='unauthorized_access',
    timestamp__gte=timezone.now() - timedelta(days=7)
)
```

### Financial Reports

```python
# Daily revenue tracking
from django.db.models import Sum

daily_revenue = AuditLog.objects.filter(
    action__in=['payment_received', 'walkin_sale'],
    timestamp__date=date.today()
).aggregate(
    total=Sum('extra_data__amount')
)
```

### User Activity

```python
# Most active users
active_users = AuditLog.objects.filter(
    timestamp__gte=timezone.now() - timedelta(days=30)
).values('user__username').annotate(
    count=Count('id')
).order_by('-count')[:10]
```

---

## 🔒 Security Features

### IP Address Tracking
- Every log captures the user's IP address
- Useful for detecting suspicious activity
- Can track access patterns

### User Agent Logging
- Records browser and device information
- Helps identify automated attacks
- Device fingerprinting

### Automatic Threat Detection
- Failed login attempts are logged as warnings
- Unauthorized access attempts are flagged
- Permission denials are tracked

---

## 📋 Best Practices

### 1. Regular Review
- Check audit logs daily for security events
- Review failed login attempts
- Monitor unauthorized access

### 2. Retention Policy
```python
# Auto-delete logs older than 1 year
from datetime import timedelta
from django.utils import timezone

old_logs = AuditLog.objects.filter(
    timestamp__lt=timezone.now() - timedelta(days=365)
)
old_logs.delete()
```

### 3. Alert System
```python
# Email admin on critical events
critical_logs = AuditLog.objects.filter(
    severity='critical',
    timestamp__gte=timezone.now() - timedelta(hours=1)
)

if critical_logs.exists():
    send_admin_email('Critical Security Alert', critical_logs)
```

### 4. Export Logs
```python
# Export to CSV for external analysis
import csv

logs = AuditLog.objects.all()
with open('audit_logs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'User', 'Action', 'Description', 'IP'])
    
    for log in logs:
        writer.writerow([
            log.timestamp,
            log.user.username if log.user else 'Anonymous',
            log.action,
            log.description,
            log.ip_address
        ])
```

---

## 🐛 Troubleshooting

### Issue: No logs appearing

**Check:**
1. Migrations applied: `python manage.py migrate`
2. Table exists: Check in Django admin
3. Logging is working:
```python
from gym_app.models import AuditLog
AuditLog.log('login', description='Test log')
print(AuditLog.objects.count())
```

### Issue: Can't access audit trail page

**Solution:**
- Only admins can access
- Verify: `user.is_admin()` returns True
- Check user role in database

### Issue: Performance problems

**Solution:**
- Add database indexes (already included)
- Implement pagination (already included)
- Archive old logs periodically

---

## 📊 Example Queries

### Find Suspicious Activity
```python
# Multiple failed logins from same IP
suspicious_ips = AuditLog.objects.filter(
    action='login_failed',
    timestamp__gte=timezone.now() - timedelta(hours=1)
).values('ip_address').annotate(
    attempts=Count('id')
).filter(attempts__gte=5)
```

### Track User Journey
```python
# All actions by a specific user today
user_journey = AuditLog.objects.filter(
    user=user,
    timestamp__date=date.today()
).order_by('timestamp')
```

### Revenue Audit
```python
# All payments with details
payments = AuditLog.objects.filter(
    action='payment_received'
).values(
    'timestamp',
    'user__username',
    'extra_data__amount',
    'extra_data__payment_method'
)
```

---

## ✅ Checklist

- [ ] Migrations applied
- [ ] AuditLog model created
- [ ] Admin can access audit trail page
- [ ] Logs are being created automatically
- [ ] Filters work correctly
- [ ] Pagination works
- [ ] IP addresses are captured
- [ ] Security events are flagged

---

## 🎯 Summary

Your Gym Management System now has:
- ✅ Comprehensive activity logging
- ✅ Security event tracking
- ✅ Financial transaction audit
- ✅ User activity monitoring
- ✅ Advanced filtering and search
- ✅ IP address tracking
- ✅ Automatic threat detection

**Benefits:**
- 🔒 Enhanced security
- 📊 Better compliance
- 🐛 Easier troubleshooting
- 📈 Activity insights
- ⚖️ Legal protection

---

*Last Updated: October 2024*
*Version: 1.0.0*