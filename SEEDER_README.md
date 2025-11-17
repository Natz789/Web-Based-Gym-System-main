# Database Seeder Documentation

## Overview

The gym management system includes a comprehensive database seeder for generating realistic test data. This is useful for development, testing, and demonstration purposes.

## What Gets Created

The seeder populates the database with:

### Users
- **3 Admins** (including 1 superuser)
- **15 Staff Members**
- **100+ Members** (configurable)

### Membership Plans & Passes
- **5 Membership Plans**:
  - Weekly Pass (7 days) - ₱500
  - Monthly Membership (30 days) - ₱1,500
  - Quarterly Membership (90 days) - ₱4,000
  - Semi-Annual Premium (180 days) - ₱7,500
  - Annual VIP Membership (365 days) - ₱14,000

- **3 Walk-in Passes**:
  - Single Day Pass - ₱100
  - 3-Day Trial Pass - ₱250
  - 5-Day Flex Pass - ₱400

### Transactional Data
- **User Memberships** - Active, expired, and cancelled subscriptions
- **Payments** - With realistic statuses:
  - 70% Confirmed
  - 20% Pending (for testing approval workflow)
  - 10% Rejected
- **Walk-in Payments** - 2-8 per day across historical period
- **Attendance Records** - Check-in/check-out history
- **Analytics** - Daily aggregated statistics
- **Audit Logs** - System activity logs

## Usage

### Basic Usage

Generate 100 members with 90 days of historical data:

```bash
python manage.py seed_database
```

### Custom Configuration

#### Specify Number of Members

```bash
python manage.py seed_database --users 150
```

#### Specify Historical Data Period

```bash
python manage.py seed_database --days 120
```

#### Combined Options

```bash
python manage.py seed_database --users 200 --days 180
```

### Reset and Reseed Database

**⚠️ WARNING: This will delete all existing data!**

```bash
python manage.py seed_database --flush
```

This will:
1. Delete all existing users (except superusers)
2. Delete all memberships, payments, and transactions
3. Delete all analytics and audit logs
4. Create fresh test data

## Default Credentials

After seeding, you can log in with these accounts:

### Admin Accounts
| Username | Password | Email | Role |
|----------|----------|-------|------|
| admin | admin123 | admin@gym.com | Superuser Admin |
| manager | admin123 | manager@gym.com | Admin |
| director | admin123 | director@gym.com | Admin |

### Staff Accounts
| Username | Password | Email |
|----------|----------|-------|
| staff1 | staff123 | sarah.johnson@gym.com |
| staff2 | staff123 | mike.williams@gym.com |
| staff3 | staff123 | lisa.martinez@gym.com |
| ... | staff123 | (15 total staff members) |

### Member Accounts
- **Username**: Various (e.g., juan.santos123, maria.reyes456)
- **Password**: member123
- **Count**: 100+ members (configurable)

## Features

### Realistic Data Generation

1. **Filipino-Inspired Names** - First and last names common in the Philippines
2. **Age Diversity** - Members aged 18-65 with appropriate birthdates
3. **Mobile Numbers** - Philippine format (09XXXXXXXXX)
4. **Addresses** - Realistic Metro Manila addresses
5. **Kiosk PINs** - Auto-generated 6-digit PINs for all members

### Payment Statuses

The seeder creates payments with varied statuses to test the approval workflow:

- **Confirmed Payments** (70%)
  - Have approval metadata (approved_by, approved_at)
  - Associated memberships are activated

- **Pending Payments** (20%)
  - Awaiting staff/admin approval
  - Visible on dashboard for action

- **Rejected Payments** (10%)
  - Include rejection reasons
  - Associated memberships are cancelled

### Membership Distribution

- **80%** of members have at least one membership
- **60%** have one membership
- **30%** have two memberships
- **10%** have three memberships

### Attendance Patterns

- **40-70%** of active members check in each day
- **Realistic times** - 6 AM to 9 PM
- **Workout duration** - 30 minutes to 3 hours
- **90%** complete check-out, 10% still in progress

## Example Output

```
======================================================================
🏋️  GYM MANAGEMENT SYSTEM - COMPREHENSIVE DATABASE SEEDER
======================================================================

👥 Creating Admin & Staff Users...
   ✓ Created admin: admin (admin@gym.com)
   ✓ Created admin: manager (manager@gym.com)
   ✓ Created admin: director (director@gym.com)
   ✓ Created staff: staff1 (sarah.johnson@gym.com)
   ...

💳 Creating Membership Plans...
   ✓ Created plan: Weekly Pass (₱500.00)
   ✓ Created plan: Monthly Membership (₱1500.00)
   ...

👤 Creating 100 Member Users...
   ✓ Created 100 new members

📋 Creating User Memberships...
   ✓ Created 143 memberships
   ℹ Active: 65
   ℹ Expired: 72
   ℹ Cancelled: 6

💰 Creating Payment Records...
   ✓ Created 137 payment records
   ℹ Confirmed: 96
   ℹ Pending: 27
   ℹ Rejected: 14

======================================================================
✅ DATABASE SEEDING COMPLETE!
======================================================================

👥 Total Users                 118
   ├─ Admins                  3
   ├─ Staff                   15
   └─ Members                 100

💳 Membership Plans            5
🎫 Walk-in Passes             3

📋 User Memberships            143
   ├─ Active                  65
   ├─ Expired                 72
   └─ Cancelled               6

💰 Member Payments             137
   ├─ Confirmed               96
   ├─ Pending                 27
   └─ Rejected                14

🚶 Walk-in Payments           450
📊 Attendance Records          3,245
📈 Analytics Records           90
📝 Audit Logs                  200

💵 Total Revenue Generated: ₱256,750.00
   ├─ Member Payments: ₱211,500.00
   └─ Walk-in Payments: ₱45,250.00

----------------------------------------------------------------------
💡 DEFAULT CREDENTIALS:
----------------------------------------------------------------------
Admin:  username=admin, password=admin123
Staff:  username=staff1, password=staff123
Member: username=<any member>, password=member123
----------------------------------------------------------------------
```

## Testing Scenarios

### Test Pending Payment Approvals

1. Log in as admin/staff
2. Navigate to dashboard
3. See "Pending Payment Approvals" section
4. Approve or reject payments
5. Verify membership activation/cancellation

### Test Member Flow

1. Log in as any member (password: member123)
2. View active membership
3. Check attendance history
4. Use kiosk check-in with 6-digit PIN

### Test Reports & Analytics

1. Log in as admin
2. View Reports page
3. Analyze revenue trends
4. Check member attendance patterns
5. Review audit trail

## Maintenance

### Re-running the Seeder

The seeder uses `get_or_create` for most objects, so:
- **Running multiple times** will NOT create duplicates
- **New members** will be added each time
- **Existing users** (admin, staff) will be skipped

### Complete Reset

For a fresh start:

```bash
python manage.py seed_database --flush --users 100 --days 90
```

## Troubleshooting

### Issue: "No membership plans found"

**Solution**: Ensure you run the seeder completely, it creates plans before memberships

### Issue: "Duplicate username"

**Solution**: Use `--flush` to clear existing data or change usernames in seeder

### Issue: Performance is slow

**Solution**: Reduce --users or --days parameters for faster seeding:

```bash
python manage.py seed_database --users 50 --days 30
```

## Advanced Usage

### Seeding for Production Demo

```bash
# Create a realistic 6-month demo with 200 active members
python manage.py seed_database --flush --users 200 --days 180
```

### Seeding for Quick Testing

```bash
# Minimal data for rapid testing
python manage.py seed_database --flush --users 20 --days 14
```

### Seeding with Maximum Data

```bash
# Heavy load testing with 1 year of data
python manage.py seed_database --flush --users 500 --days 365
```

## Notes

- All payments use Philippine Peso (₱) currency
- Payment methods are limited to Cash and GCash (realistic for PH market)
- Walk-in payments automatically get reference numbers
- All datetimes are timezone-aware (Asia/Manila)
- Audit logs include realistic IP addresses (192.168.1.x range)

## Support

For issues or questions about the seeder, check:
1. Django migrations are up to date (`python manage.py migrate`)
2. Database connection is working
3. All model dependencies are satisfied

---

**Last Updated**: November 2024
**Version**: 2.0
**Supports**: Gym Management System v2.0+
