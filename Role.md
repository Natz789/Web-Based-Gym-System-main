# 🔐 Role Hierarchy Configuration Guide

## Overview

Your gym management system now has a properly integrated role hierarchy that syncs with Django's built-in permissions system.

---

## 🎯 Role Hierarchy Structure

```
┌─────────────────────────────────────────────────┐
│              SUPERUSER (Django)                 │
│  ↓ Automatically becomes                        │
│              ADMIN (System Role)                │
│  • Full system access                           │
│  • Can manage all users, plans, payments        │
│  • Access to Django admin panel                 │
│  • View all analytics and reports               │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│              STAFF (System Role)                │
│  • Can process walk-in sales                    │
│  • Can view member list                         │
│  • Can view member details                      │
│  • Cannot delete users or modify system data    │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│              MEMBER (System Role)               │
│  • Can view own dashboard                       │
│  • Can subscribe to plans                       │
│  • Can view own payment history                 │
│  • Cannot access other members' data            │
└─────────────────────────────────────────────────┘
```

---

## 🔧 What Changed

### 1. User Model Updates
- **Auto-sync:** Superusers are automatically assigned `admin` role
- **Staff sync:** Staff users (is_staff=True) get `staff` role
- **Enhanced methods:** `is_admin()` now checks both role and superuser status

### 2. New Management Commands

#### a) `sync_roles` - Sync existing users
```bash
python manage.py sync_roles
```
This command:
- Updates all superusers to admin role
- Updates staff users to staff role
- Shows role distribution summary

#### b) `createadmin` - Create admin user
```bash
python manage.py createadmin
```
Interactive command that creates a superuser with admin role.

**Quick create (non-interactive):**
```bash
python manage.py createadmin --username admin --email admin@gym.com --noinput
# Default password: admin (change immediately!)
```

### 3. Admin Panel Integration
- Admin panel now shows role clearly
- Automatic role sync when changing permissions
- Better role management interface

---

## 📋 Step-by-Step Setup

### Step 1: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Sync Existing Users
If you already created a superuser:
```bash
python manage.py sync_roles
```

Output:
```
✓ Synced 1 superuser(s) to admin role
✓ Synced 0 staff user(s) to staff role

📊 Current Role Distribution:
   Admins: 1
   Staff: 0
   Members: 0

✅ Role synchronization complete!
```

### Step 3: Create Additional Admin (Optional)
```bash
python manage.py createadmin
```

Follow the prompts:
```
Creating admin user with superuser privileges...

Username: admin2
Email address: admin2@gym.com
First name (optional): John
Last name (optional): Admin
Mobile number (optional): 09123456789
Password: 
Password (again): 

✓ Admin user "admin2" created successfully!
   Role: admin
   Superuser: Yes
   Staff: Yes
```

---

## 🎭 How Roles Work Now

### Creating Users

#### Option 1: Django Admin Panel
1. Go to http://127.0.0.1:8000/admin/
2. Click "Users" → "Add User"
3. Fill in details
4. Check permissions:
   - **Admin:** Check "Superuser status" → Role automatically becomes "admin"
   - **Staff:** Check "Staff status" → Select role "staff"
   - **Member:** Leave unchecked → Role is "member"

#### Option 2: Registration Page
- Public registration → Always creates "member" role
- Cannot create admin/staff through public registration

#### Option 3: Management Command
```bash
# Create admin
python manage.py createadmin

# Create regular superuser (will auto-sync to admin)
python manage.py createsuperuser

# Then run sync if needed
python manage.py sync_roles
```

---

## 🔒 Permission Checks

### In Views
```python
# Check if user is admin
if request.user.is_admin():
    # Admin-only code

# Check if user is staff or admin
if request.user.is_staff_or_admin():
    # Staff or admin code

# Check role directly
if request.user.role == 'member':
    # Member code
```

### Using Decorators
```python
from gym_app.decorators import admin_required, staff_required

@admin_required
def admin_only_view(request):
    # Only admins can access

@staff_required
def staff_view(request):
    # Staff and admins can access
```

### In Templates
```html
{% if user.is_admin %}
    <!-- Admin content -->
{% endif %}

{% if user.is_staff_or_admin %}
    <!-- Staff/Admin content -->
{% endif %}

{% if user.role == 'member' %}
    <!-- Member content -->
{% endif %}
```

---

## 📊 Testing the Hierarchy

### Test 1: Superuser → Admin
```bash
# Create superuser
python manage.py createsuperuser
Username: testadmin
Email: test@admin.com
Password: ***

# Check role
python manage.py shell
```
```python
from gym_app.models import User
user = User.objects.get(username='testadmin')
print(user.role)  # Should output: admin
print(user.is_admin())  # Should output: True
```

### Test 2: Role Permissions
1. **Login as Admin**
   - Go to `/dashboard/` → Should see admin dashboard
   - Go to `/reports/` → Should have access
   - Go to `/admin/` → Should have access

2. **Login as Staff**
   - Create staff user in admin panel
   - Go to `/dashboard/` → Should see staff dashboard
   - Go to `/walkin/` → Should have access
   - Go to `/reports/` → Should be denied

3. **Login as Member**
   - Register through `/register/`
   - Go to `/dashboard/` → Should see member dashboard
   - Go to `/walkin/` → Should be denied
   - Go to `/members/` → Should be denied

---

## 🐛 Troubleshooting

### Issue: Superuser not showing as admin

**Solution:**
```bash
python manage.py sync_roles
```

### Issue: Can't access admin panel

**Check:**
1. User has `is_superuser=True`
2. User role is 'admin'
3. User `is_active=True`

```python
python manage.py shell
```
```python
from gym_app.models import User
user = User.objects.get(username='your_username')
print(f"Superuser: {user.is_superuser}")
print(f"Role: {user.role}")
print(f"Active: {user.is_active}")

# Fix if needed
user.is_superuser = True
user.role = 'admin'
user.save()
```

### Issue: Permission denied for admin user

**Check view decorators:**
```python
# Make sure views use updated methods
@login_required
def admin_view(request):
    if not request.user.is_admin():  # Uses updated method
        return redirect('dashboard')
```

---

## 📝 Quick Reference

### Commands
| Command | Purpose |
|---------|---------|
| `python manage.py createadmin` | Create admin user interactively |
| `python manage.py sync_roles` | Sync existing users' roles |
| `python manage.py createsuperuser` | Django's default (then run sync_roles) |

### Role Assignments
| Django Permission | System Role | Auto-Assigned |
|------------------|-------------|---------------|
| is_superuser=True | admin | ✅ Yes |
| is_staff=True (not super) | staff | ✅ Yes |
| Regular user | member | ✅ Yes (default) |

### Access Levels
| Feature | Admin | Staff | Member |
|---------|-------|-------|--------|
| Dashboard | Full analytics | Limited | Personal only |
| Members list | ✅ | ✅ | ❌ |
| Walk-in sales | ✅ | ✅ | ❌ |
| Reports | ✅ | ❌ | ❌ |
| Django Admin | ✅ | ❌ | ❌ |
| Subscribe plans | ✅ | ✅ | ✅ |
| View own data | ✅ | ✅ | ✅ |

---

## ✅ Verification Checklist

- [ ] Run `python manage.py sync_roles`
- [ ] Create test admin: `python manage.py createadmin`
- [ ] Verify admin can access all features
- [ ] Create staff user through admin panel
- [ ] Verify staff has limited access
- [ ] Register a member through `/register/`
- [ ] Verify member can only access own data
- [ ] Test permission denials work correctly

---

## 🎉 Summary

Your role hierarchy is now properly configured with:
✅ Automatic superuser → admin role sync
✅ Proper permission checks throughout the system
✅ Management commands for easy user creation
✅ Admin panel integration
✅ Clear access level separation

**Next Steps:**
1. Run `python manage.py sync_roles`
2. Test with different user roles
3. Create staff and member accounts
4. Verify access permissions

Your gym management system is now production-ready with proper role management! 🚀