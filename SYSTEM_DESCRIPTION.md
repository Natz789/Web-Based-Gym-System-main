# 🏋️ Web-Based Gym Management System
## Comprehensive System Documentation

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Database Schema](#database-schema)
5. [User Roles & Permissions](#user-roles--permissions)
6. [Core Features](#core-features)
7. [Security Features](#security-features)
8. [API Endpoints](#api-endpoints)
9. [AI Chatbot Integration](#ai-chatbot-integration)
10. [Setup & Deployment](#setup--deployment)

---

## 🎯 Project Overview

The Web-Based Gym Management System is a comprehensive solution designed to manage gym operations, including membership subscriptions, walk-in payments, user management, attendance tracking, and financial analytics. Built with Django and modern web technologies, the system supports three distinct user roles (Admin, Staff, Member) with role-based access control.

### Project Goals
- Streamline gym membership management
- Track walk-in customers and revenue
- Provide comprehensive analytics and reporting
- Enable self-service member portal
- Integrate AI-powered customer support
- Maintain complete audit trail for all operations

### Target Users
- **Gym Administrators**: Full system control and analytics
- **Gym Staff**: Daily operations and customer service
- **Gym Members**: Self-service portal for subscriptions and payments
- **Walk-in Customers**: Quick access purchase without registration

---

## 💻 Technology Stack

### Backend Framework
- **Django 5.2.7** - Python web framework
- **Python 3.x** - Programming language
- **SQLite3** - Database (development)
- **Django ORM** - Object-Relational Mapping

### Frontend Technologies
- **HTML5** - Markup language
- **CSS3** - Styling (with custom stylesheets)
- **JavaScript** - Client-side interactivity
- **Django Template Engine** - Server-side rendering

### AI & Machine Learning
- **Ollama** - Local LLM server
- **Llama 3.2** - Default AI model (1B/3B variants)
- **Alternative models**: Gemma2, Phi3, Mistral

### Authentication & Security
- **Django Authentication System** - Built-in user authentication
- **CSRF Protection** - Cross-Site Request Forgery protection
- **Session Management** - Secure session handling
- **Password Hashing** - PBKDF2 algorithm with SHA256

### Additional Libraries & Tools
- **Django Admin** - Administrative interface
- **JSON** - Data interchange format
- **Pillow** - Image processing (profile pictures)
- **Requests** - HTTP library for Ollama integration

### Development Tools
- **Git** - Version control
- **Django Management Commands** - Custom commands for seeding, role sync
- **Django Migrations** - Database version control

---

## 🏗️ System Architecture

### Application Structure
```
Web-Based-Gym-System/
├── gym_project/              # Django project configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
│
├── gym_app/                  # Main application
│   ├── models.py            # Database models (11 models)
│   ├── views.py             # View functions (30+ views)
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin panel configuration
│   ├── decorators.py        # Custom decorators
│   ├── chatbot.py           # AI chatbot logic
│   ├── seeder.py            # Database seeding
│   │
│   ├── templates/           # HTML templates
│   │   └── gym_app/         # App-specific templates
│   │
│   ├── static/              # Static files
│   │   └── gym_app/         # CSS, JS, images
│   │
│   ├── migrations/          # Database migrations
│   └── management/          # Custom management commands
│       └── commands/
│           ├── seed_data.py
│           ├── sync_roles.py
│           └── createadmin.py
│
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
└── README.md                # Documentation
```

### Request Flow
```
User Request → URL Router → View Function → Model (Database) → Template → Response
                  ↓
           Authentication Middleware
                  ↓
            CSRF Middleware
                  ↓
          Session Middleware
```

### Design Patterns
- **MVT (Model-View-Template)** - Django's architectural pattern
- **Singleton Pattern** - Chatbot configuration (only one config instance)
- **Decorator Pattern** - Access control decorators
- **Repository Pattern** - Django ORM as data access layer

---

## 🗄️ Database Schema

### Entity Relationship Diagram (ERD)
```
┌─────────────┐        ┌──────────────────┐        ┌──────────────┐
│    User     │───────>│ UserMembership   │───────>│   Payment    │
│  (Custom)   │   1:N  │                  │   1:N  │              │
└─────────────┘        └──────────────────┘        └──────────────┘
      │                        │
      │                        │
      │                        ↓
      │                ┌──────────────────┐
      │                │ MembershipPlan   │
      │                │                  │
      │                └──────────────────┘
      │
      │                ┌──────────────────┐        ┌──────────────────┐
      │                │ FlexibleAccess   │───────>│ WalkInPayment    │
      │                │                  │   1:N  │                  │
      │                └──────────────────┘        └──────────────────┘
      │
      ├───────────────>┌──────────────────┐
      │           1:N  │   AuditLog       │
      │                └──────────────────┘
      │
      ├───────────────>┌──────────────────┐
      │           1:N  │  Attendance      │
      │                └──────────────────┘
      │
      ├───────────────>┌──────────────────┐
      │           1:N  │ LoginActivity    │
      │                └──────────────────┘
      │
      └───────────────>┌──────────────────┐
                  1:N  │  Conversation    │
                       └──────────────────┘
                               │
                               │ 1:N
                               ↓
                       ┌──────────────────────┐
                       │ ConversationMessage  │
                       └──────────────────────┘
```

### Database Models (11 Tables)

#### 1. **User** (Custom User Model)
Extends Django's AbstractUser with additional fields.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| username | VARCHAR(150) | Unique username |
| email | VARCHAR(254) | Email address |
| password | VARCHAR(128) | Hashed password |
| first_name | VARCHAR(150) | First name |
| last_name | VARCHAR(150) | Last name |
| role | VARCHAR(10) | admin, staff, member |
| mobile_no | VARCHAR(20) | Contact number |
| address | TEXT | Full address |
| birthdate | DATE | Date of birth |
| age | INT | Auto-calculated from birthdate |
| profile_image | ImageField | Profile picture |
| kiosk_pin | VARCHAR(6) | 6-digit PIN for kiosk |
| is_active | BOOLEAN | Account status |
| is_staff | BOOLEAN | Django staff flag |
| is_superuser | BOOLEAN | Superuser flag |
| created_at | DATETIME | Account creation |
| updated_at | DATETIME | Last update |

**Relationships:**
- 1:N with UserMembership
- 1:N with Payment
- 1:N with AuditLog
- 1:N with Attendance
- 1:N with LoginActivity
- 1:N with Conversation

#### 2. **MembershipPlan**
Permanent membership plans (monthly, yearly).

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| name | VARCHAR(100) | Plan name |
| duration_days | INT | Duration in days |
| price | DECIMAL(10,2) | Plan cost |
| description | TEXT | Plan details |
| is_active | BOOLEAN | Active status |
| is_archived | BOOLEAN | Archive status |
| archived_at | DATETIME | Archive timestamp |
| archived_by_id | BigInt (FK) | Admin who archived |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Update timestamp |

**Relationships:**
- 1:N with UserMembership

#### 3. **FlexibleAccess**
Walk-in passes (1-day, 3-day, weekly).

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| name | VARCHAR(100) | Pass name |
| duration_days | INT | Validity in days |
| price | DECIMAL(10,2) | Pass cost |
| description | TEXT | Pass details |
| is_active | BOOLEAN | Active status |
| is_archived | BOOLEAN | Archive status |
| archived_at | DATETIME | Archive timestamp |
| archived_by_id | BigInt (FK) | Admin who archived |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Update timestamp |

**Relationships:**
- 1:N with WalkInPayment

#### 4. **UserMembership**
Tracks member subscriptions to plans.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| user_id | BigInt (FK) | Reference to User |
| plan_id | BigInt (FK) | Reference to MembershipPlan |
| start_date | DATE | Membership start |
| end_date | DATE | Membership end |
| status | VARCHAR(20) | pending, active, expired, cancelled |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Update timestamp |

**Relationships:**
- N:1 with User
- N:1 with MembershipPlan
- 1:N with Payment

#### 5. **Payment**
Payment records for registered members.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| user_id | BigInt (FK) | Reference to User |
| membership_id | BigInt (FK) | Reference to UserMembership |
| amount | DECIMAL(10,2) | Payment amount |
| method | VARCHAR(10) | cash, gcash |
| payment_date | DATETIME | Payment timestamp |
| reference_no | VARCHAR(50) | Unique reference (PAY-YYYYMMDD-XXXXXX) |
| notes | TEXT | Additional notes |
| status | VARCHAR(20) | pending, confirmed, rejected |
| approved_by_id | BigInt (FK) | Admin/staff who approved |
| approved_at | DATETIME | Approval timestamp |
| rejection_reason | TEXT | Rejection reason |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Update timestamp |

**Relationships:**
- N:1 with User
- N:1 with UserMembership

#### 6. **WalkInPayment**
Payment records for walk-in customers.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| pass_type_id | BigInt (FK) | Reference to FlexibleAccess |
| customer_name | VARCHAR(100) | Customer name (optional) |
| mobile_no | VARCHAR(20) | Contact (optional) |
| amount | DECIMAL(10,2) | Payment amount |
| method | VARCHAR(10) | cash, gcash |
| payment_date | DATETIME | Payment timestamp |
| reference_no | VARCHAR(50) | Unique reference (WLK-YYYYMMDD-XXXXXX) |
| notes | TEXT | Additional notes |
| processed_by_id | BigInt (FK) | Staff/admin who processed |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Update timestamp |

**Relationships:**
- N:1 with FlexibleAccess
- N:1 with User (processed_by)

#### 7. **Analytics**
Daily aggregated data for reporting.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| date | DATE | Report date (unique) |
| total_members | INT | Active member count |
| total_passes | INT | Walk-in passes sold |
| total_sales | DECIMAL(10,2) | Total revenue |
| age_group | VARCHAR(20) | Demographics |
| created_at | DATETIME | Creation timestamp |

#### 8. **AuditLog**
Comprehensive audit trail for all system activities.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| user_id | BigInt (FK) | User who performed action |
| action | VARCHAR(50) | Action type (40+ types) |
| severity | VARCHAR(10) | info, warning, error, critical |
| description | TEXT | Action description |
| ip_address | GenericIPAddress | User's IP address |
| user_agent | TEXT | Browser info |
| model_name | VARCHAR(100) | Related model |
| object_id | VARCHAR(100) | Related object ID |
| object_repr | VARCHAR(200) | Object string representation |
| extra_data | JSON | Additional metadata |
| timestamp | DATETIME | Action timestamp (indexed) |

**Logged Actions:**
- Authentication: login, logout, login_failed, register
- User Management: user_created, user_updated, user_deleted, role_changed
- Memberships: membership_created, membership_updated, membership_cancelled
- Payments: payment_received, walkin_sale, payment_refunded
- Security: unauthorized_access, permission_denied, password_changed
- System: report_generated, data_export, settings_changed

#### 9. **Attendance**
Track member check-ins and check-outs.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| user_id | BigInt (FK) | Reference to User |
| check_in | DATETIME | Check-in timestamp |
| check_out | DATETIME | Check-out timestamp (nullable) |
| duration_minutes | INT | Auto-calculated duration |
| notes | TEXT | Additional notes |

**Relationships:**
- N:1 with User

#### 10. **LoginActivity**
Track user login activity for security.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| user_id | BigInt (FK) | Reference to User |
| login_time | DATETIME | Login timestamp |
| ip_address | GenericIPAddress | User's IP address |
| user_agent | TEXT | Browser info |
| success | BOOLEAN | Login success status |
| failure_reason | VARCHAR(200) | Failure reason |

**Relationships:**
- N:1 with User

#### 11. **ChatbotConfig** (Singleton)
Configuration for AI chatbot.

| Field | Type | Description |
|-------|------|-------------|
| id | INT (PK) | Primary key (always 1) |
| active_model | VARCHAR(50) | Current Ollama model |
| temperature | FLOAT | Creativity (0.0-1.0) |
| top_p | FLOAT | Nucleus sampling |
| max_tokens | INT | Max response length |
| context_window | INT | Chat history size |
| enable_streaming | BOOLEAN | Streaming responses |
| enable_persistence | BOOLEAN | Save conversations |
| ollama_host | VARCHAR(200) | Ollama server URL |
| timeout_seconds | INT | Request timeout |
| updated_at | DATETIME | Last update |
| updated_by_id | BigInt (FK) | Admin who updated |

#### 12. **Conversation**
Persistent conversation storage.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| user_id | BigInt (FK) | User (nullable for anonymous) |
| conversation_id | VARCHAR(100) | Unique UUID |
| title | VARCHAR(200) | Auto-generated title |
| model_used | VARCHAR(50) | Ollama model |
| session_key | VARCHAR(100) | Session for anonymous users |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Update timestamp |

**Relationships:**
- N:1 with User
- 1:N with ConversationMessage

#### 13. **ConversationMessage**
Individual messages in conversations.

| Field | Type | Description |
|-------|------|-------------|
| id | BigInt (PK) | Primary key |
| conversation_id | BigInt (FK) | Reference to Conversation |
| role | VARCHAR(20) | user, assistant, system |
| content | TEXT | Message content |
| tokens_used | INT | Token count |
| response_time_ms | INT | Response time |
| created_at | DATETIME | Creation timestamp |

**Relationships:**
- N:1 with Conversation

### Database Indexes
Optimized indexes for performance:
- `audit_logs.timestamp` (DESC)
- `audit_logs.user_id, timestamp` (DESC)
- `audit_logs.action, timestamp` (DESC)
- `attendance.check_in` (DESC)
- `attendance.user_id, check_in` (DESC)
- `login_activities.user_id, login_time` (DESC)
- `conversations.user_id, updated_at` (DESC)
- `conversations.conversation_id`
- `conversation_messages.conversation_id, created_at`

---

## 👥 User Roles & Permissions

### Role Hierarchy
```
┌─────────────────────────────────────────────────┐
│              ADMIN (Superuser)                  │
│  ✓ Full system access                           │
│  ✓ User management (create/edit/delete)         │
│  ✓ Plan management (create/archive/restore)     │
│  ✓ Payment approval/rejection                   │
│  ✓ Reports & analytics                          │
│  ✓ Audit trail access                           │
│  ✓ Chatbot configuration                        │
│  ✓ Django admin panel                           │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│                   STAFF                         │
│  ✓ Process walk-in sales                        │
│  ✓ View member list                             │
│  ✓ View member details                          │
│  ✓ Process check-in/check-out                   │
│  ✓ Limited dashboard                            │
│  ✗ Cannot modify plans                          │
│  ✗ Cannot access reports                        │
│  ✗ Cannot approve payments                      │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│                  MEMBER                         │
│  ✓ View own dashboard                           │
│  ✓ Subscribe to plans                           │
│  ✓ Make payments                                │
│  ✓ View payment history                         │
│  ✓ Update profile                               │
│  ✓ Kiosk check-in/check-out (with PIN)          │
│  ✗ Cannot access other members' data            │
│  ✗ Cannot process walk-ins                      │
└─────────────────────────────────────────────────┘
```

### Access Control Matrix

| Feature | Admin | Staff | Member | Public |
|---------|-------|-------|--------|--------|
| **Authentication** |
| Login | ✅ | ✅ | ✅ | ✅ |
| Register | ✅ | ✅ | ✅ | ✅ |
| **Dashboard** |
| Full Analytics | ✅ | ❌ | ❌ | ❌ |
| Limited Dashboard | ❌ | ✅ | ❌ | ❌ |
| Personal Dashboard | ✅ | ✅ | ✅ | ❌ |
| **Memberships** |
| View Plans | ✅ | ✅ | ✅ | ✅ |
| Subscribe to Plans | ✅ | ✅ | ✅ | ❌ |
| Manage Plans | ✅ | ❌ | ❌ | ❌ |
| Archive/Restore Plans | ✅ | ❌ | ❌ | ❌ |
| **Payments** |
| Make Payment | ✅ | ✅ | ✅ | ❌ |
| Approve Payment | ✅ | ✅ | ❌ | ❌ |
| Reject Payment | ✅ | ✅ | ❌ | ❌ |
| View All Payments | ✅ | ✅ | ❌ | ❌ |
| View Own Payments | ✅ | ✅ | ✅ | ❌ |
| **Walk-in** |
| Process Walk-in Sale | ✅ | ✅ | ❌ | ❌ |
| View Walk-in History | ✅ | ✅ | ❌ | ❌ |
| **Members** |
| View All Members | ✅ | ✅ | ❌ | ❌ |
| View Member Details | ✅ | ✅ | ❌ | ❌ |
| Create Staff Account | ✅ | ❌ | ❌ | ❌ |
| Edit User | ✅ | ❌ | Self | ❌ |
| **Reports** |
| Analytics Dashboard | ✅ | ❌ | ❌ | ❌ |
| Audit Trail | ✅ | ❌ | ❌ | ❌ |
| Attendance Report | ✅ | ✅ | ❌ | ❌ |
| **Attendance** |
| Kiosk Check-in/out | ✅ | ✅ | ✅ | ❌ |
| View All Attendance | ✅ | ✅ | ❌ | ❌ |
| View Own Attendance | ✅ | ✅ | ✅ | ❌ |
| **Chatbot** |
| Use Chatbot | ✅ | ✅ | ✅ | ✅ |
| Configure Chatbot | ✅ | ❌ | ❌ | ❌ |
| **System** |
| Django Admin | ✅ | ❌ | ❌ | ❌ |
| Change Settings | ✅ | ❌ | ❌ | ❌ |

### Role Auto-Assignment Logic
```python
# User save method (models.py)
if user.is_superuser:
    role = 'admin'
elif user.is_staff and not user.is_superuser:
    role = 'staff'
else:
    role = 'member'  # Default
```

---

## ⚙️ Core Features

### 1. Authentication & Authorization

#### Multi-Step Registration
- **Step 1**: Account credentials (username, email, password)
- **Step 2**: Personal information (name, birthdate, contact)
- **Step 3**: Address details
- **Review**: Confirm all information before submission

#### Login System
- Username/password authentication
- Session-based security
- Login activity tracking
- Failed login attempt logging
- Auto-redirect based on role

#### Access Control
- Custom decorators: `@admin_required`, `@staff_required`
- View-level permission checks
- Template-level permission checks
- Role-based redirects

### 2. Membership Management

#### Plan Types
- **Monthly Plans** - 30-day duration
- **Quarterly Plans** - 90-day duration
- **Annual Plans** - 365-day duration
- **Custom Plans** - Configurable duration

#### Subscription Flow
1. Member browses available plans
2. Selects plan and subscription period
3. Reviews payment details
4. Makes payment (Cash/GCash)
5. Payment pending approval
6. Admin/Staff approves payment
7. Membership activated automatically

#### Membership Status
- **Pending** - Payment not confirmed
- **Active** - Currently valid membership
- **Expired** - End date passed
- **Cancelled** - Manually cancelled

#### Plan Management (Admin)
- Create new plans
- Edit existing plans
- Archive plans (preserve records)
- Restore archived plans
- Set active/inactive status

### 3. Walk-in System

#### Flexible Access Passes
- **1-Day Pass** - Single day access
- **3-Day Pass** - 3-day validity
- **Weekly Pass** - 7-day access
- **Custom Duration** - Configurable

#### Walk-in Purchase Flow
1. Staff/Admin access walk-in page
2. Select pass type
3. Enter customer details (optional)
4. Process payment
5. Generate unique reference number
6. Print/display confirmation

#### Walk-in Features
- No registration required
- Optional customer info capture
- Quick payment processing
- Instant confirmation
- Sales tracking per staff

### 4. Payment System

#### Payment Methods
- **Cash** - Physical payment
- **GCash** - QR code payment

#### Payment Workflow
##### Member Payments
1. Member subscribes to plan
2. Payment record created (status: pending)
3. Admin/Staff reviews payment
4. Approve → Membership activated
5. Reject → Membership cancelled

##### Walk-in Payments
1. Staff processes sale
2. Payment recorded immediately
3. No approval needed
4. Reference number generated

#### Payment Features
- Auto-generated reference numbers
  - Member: `PAY-YYYYMMDD-XXXXXX`
  - Walk-in: `WLK-YYYYMMDD-XXXXXX`
- Payment history tracking
- Approval/rejection workflow
- Notes and rejection reasons
- Revenue tracking

### 5. Dashboard System

#### Admin Dashboard
- **Key Metrics**
  - Total active members
  - Today's revenue
  - Pending payments count
  - New registrations (this month)
- **Charts & Graphs**
  - Revenue trends (7 days)
  - Membership growth
  - Walk-in sales
  - Age demographics
- **Quick Actions**
  - Approve pending payments
  - View recent transactions
  - Access reports

#### Staff Dashboard
- Walk-in sales summary
- Recent transactions
- Member lookup
- Quick access to common tasks

#### Member Dashboard
- Current membership status
- Days remaining
- Payment history
- Profile information
- Subscription options

### 6. Reports & Analytics

#### Admin Reports
- **Financial Reports**
  - Daily/Weekly/Monthly revenue
  - Payment breakdown (Cash vs GCash)
  - Member vs Walk-in revenue
  - Revenue trends

- **Membership Reports**
  - Active memberships count
  - Expiring soon (next 7/30 days)
  - New subscriptions
  - Cancellations

- **Demographics**
  - Age distribution
  - Gender breakdown
  - Member locations

- **Attendance Analytics**
  - Daily check-ins
  - Peak hours
  - Average session duration
  - Member frequency

#### Audit Trail
- Complete activity log
- Filterable by:
  - Action type
  - User
  - Date range
  - Severity level
- IP address tracking
- User agent logging
- Security event monitoring

### 7. Attendance & Kiosk System

#### Kiosk Check-in/Check-out
- **PIN-based Access**
  - 6-digit unique PIN per member
  - No username/password needed
  - Quick check-in/check-out

- **Workflow**
  1. Member enters PIN
  2. System validates PIN and membership
  3. Check-in recorded with timestamp
  4. Member uses gym
  5. Member enters PIN to check-out
  6. Duration calculated automatically

- **Features**
  - Active membership validation
  - Duplicate check-in prevention
  - Session duration tracking
  - Attendance history

#### Attendance Reports
- View all check-ins
- Filter by date range
- Member attendance history
- Duration statistics
- Peak hour analysis

### 8. AI Chatbot Integration

#### Chatbot Capabilities
- **Natural Language Processing**
  - Powered by Ollama
  - Local LLM (no internet required)
  - Context-aware responses

- **Gym-Specific Knowledge**
  - Membership plans information
  - Operating hours
  - Facilities and equipment
  - Class schedules
  - Pricing information

- **Role-Based Assistance**
  - **Members**: Membership status, workout tips
  - **Staff**: Operational guidance
  - **Admin**: System help, analytics
  - **Public**: General information

#### Chatbot Features
- Conversation persistence
- Chat history
- Quick suggestions
- Model switching (llama, gemma, mistral)
- Performance tracking
- Streaming responses (optional)

#### Admin Configuration
- Switch AI models
- Adjust creativity (temperature)
- Set response length
- Configure context window
- Enable/disable features

### 9. Profile Management

#### Member Profile
- Personal information
- Profile picture upload
- Contact details
- Address
- Birthdate/Age (auto-calculated)

#### Password Management
- Change password
- Password strength validation
- Secure password hashing

#### Kiosk PIN
- Generate unique 6-digit PIN
- Regenerate if compromised
- PIN uniqueness guaranteed

### 10. Admin Features

#### User Management
- View all users
- Create staff accounts
- Edit user details
- Assign roles
- Activate/deactivate accounts

#### Plan Management
- Create membership plans
- Create walk-in passes
- Edit plans
- Archive/restore plans
- Set pricing

#### Payment Management
- Approve pending payments
- Reject payments with reason
- View all transactions
- Generate financial reports

#### System Configuration
- Chatbot settings
- System settings
- Email configuration (future)
- General preferences

---

## 🔒 Security Features

### 1. Authentication Security
- **Password Hashing**: PBKDF2 with SHA256
- **Session Management**: Secure session cookies
- **CSRF Protection**: Token-based protection
- **Login Throttling**: Failed attempt tracking

### 2. Authorization
- **Role-Based Access Control (RBAC)**
  - 3 distinct roles
  - Granular permissions
  - Decorator-based enforcement
- **View-Level Protection**
  - `@login_required` for authenticated access
  - `@admin_required` for admin-only views
  - `@staff_required` for staff/admin views

### 3. Audit & Monitoring
- **Complete Audit Trail**
  - All user actions logged
  - IP address tracking
  - User agent logging
  - Timestamp indexing
- **Security Event Tracking**
  - Failed login attempts
  - Unauthorized access attempts
  - Permission denials
  - Password changes

### 4. Data Protection
- **Database Security**
  - Prepared statements (SQL injection protection)
  - Django ORM (parameterized queries)
- **XSS Protection**
  - Template auto-escaping
  - Input sanitization
- **File Upload Security**
  - Restricted file types (images only)
  - Size limitations
  - Secure file storage

### 5. Session Security
- **Session Configuration**
  - Secure session cookies
  - HttpOnly flag
  - Session timeout
  - Session invalidation on logout

### 6. Input Validation
- **Form Validation**
  - Server-side validation
  - Data type checking
  - Length restrictions
- **Model Validation**
  - Field constraints
  - Unique constraints
  - Foreign key integrity

---

## 🌐 API Endpoints

### Public Endpoints
```
GET  /                          # Homepage
GET  /about/                    # About page
GET  /login/                    # Login page
POST /login/                    # Login submission
GET  /register/step1/           # Registration step 1
POST /register/step1/           # Submit step 1
GET  /register/step2/           # Registration step 2
POST /register/step2/           # Submit step 2
GET  /register/step3/           # Registration step 3
POST /register/step3/           # Submit step 3
GET  /register/review/          # Review registration
POST /register/review/          # Submit registration
GET  /logout/                   # Logout
```

### Member Endpoints (Authentication Required)
```
GET  /dashboard/                # Role-based dashboard
GET  /plans/                    # View membership plans
POST /plans/subscribe/<id>/     # Subscribe to plan
GET  /profile/                  # Profile settings
POST /profile/                  # Update profile
GET  /change-password/          # Change password page
POST /change-password/          # Submit password change
```

### Staff Endpoints (Staff/Admin Only)
```
GET  /walkin/                   # Walk-in purchase page
POST /walkin/                   # Process walk-in sale
GET  /walkin/confirm/           # Walk-in confirmation
GET  /members/                  # Member list
GET  /members/<id>/             # Member details
GET  /pending-payments/         # Pending payments list
POST /pending-payments/confirm/<id>/  # Confirm payment
POST /pending-payments/reject/<id>/   # Reject payment
GET  /attendance/               # Attendance report
```

### Admin Endpoints (Admin Only)
```
GET  /reports/                  # Analytics & reports
GET  /audit-trail/              # Audit log viewer
GET  /manage-plans/             # Plan management
POST /manage-plans/             # Create/edit plans
GET  /archived-plans/           # Archived plans
POST /archive-membership/<id>/  # Archive membership plan
POST /archive-walkin/<id>/      # Archive walk-in pass
POST /restore-membership/<id>/  # Restore membership plan
POST /restore-walkin/<id>/      # Restore walk-in pass
GET  /create-staff/             # Create staff account
POST /create-staff/             # Submit staff creation
```

### Kiosk Endpoints (No Authentication)
```
GET  /kiosk/                    # Kiosk login
POST /kiosk/                    # Kiosk check-in/out
GET  /kiosk/success/<action>/<duration>/<user_id>/  # Success page
```

### Chatbot API Endpoints
```
GET  /chatbot/                  # Chatbot interface
POST /api/chatbot/              # Send message
GET  /api/chatbot/suggestions/  # Get quick suggestions
```

### Chatbot Admin Endpoints
```
GET  /chatbot/config/           # Configuration page
POST /api/chatbot/config/update/  # Update config
GET  /api/chatbot/models/       # List available models
POST /api/chatbot/models/switch/  # Switch model
GET  /api/chatbot/conversations/  # List conversations
```

### Django Admin
```
GET  /admin/                    # Admin panel login
GET  /admin/gym_app/            # App model list
GET  /admin/gym_app/user/       # User management
GET  /admin/gym_app/payment/    # Payment records
# ... all other models
```

---

## 🤖 AI Chatbot Integration

### Overview
The system includes an advanced AI chatbot powered by **Ollama**, a local LLM server that runs AI models directly on the server without requiring internet connectivity or external API calls.

### Supported AI Models

| Model | RAM Required | Speed | Quality | Use Case |
|-------|-------------|-------|---------|----------|
| **llama3.2:1b** | 8GB | ⚡⚡⚡ | ⭐⭐ | Quick responses, low resources |
| **llama3.2:3b** | 12GB | ⚡⚡ | ⭐⭐⭐⭐ | Balanced performance |
| **gemma2:2b** | 8GB | ⚡⚡⚡ | ⭐⭐⭐ | Fast and efficient |
| **phi3:3.8b** | 12GB | ⚡⚡ | ⭐⭐⭐⭐ | High quality |
| **mistral:7b** | 16GB | ⚡ | ⭐⭐⭐⭐⭐ | Best quality, slower |

### Architecture
```
User → Django View → GymChatbot Class → Ollama Server → AI Model
                          ↓
                    Conversation DB
                          ↓
                  ConversationMessage DB
```

### Chatbot Features

#### 1. Context-Aware Responses
- Maintains conversation history
- Configurable context window (4-12 messages)
- Role-based system prompts
- Gym-specific knowledge base

#### 2. Conversation Persistence
- All chats saved to database
- User/anonymous tracking
- Conversation titles auto-generated
- Full message history

#### 3. Dynamic Configuration
- Switch models on-the-fly
- Adjust temperature (creativity)
- Set max response length
- Configure sampling parameters

#### 4. Performance Tracking
- Response time monitoring
- Token usage tracking
- Model performance metrics

#### 5. Streaming Support
- Word-by-word response (optional)
- Better user experience
- Real-time feedback

### Chatbot Configuration Options

```python
ChatbotConfig:
    active_model: str           # Current AI model
    temperature: float          # 0.0-1.0 (creativity)
    top_p: float                # 0.0-1.0 (nucleus sampling)
    max_tokens: int             # Max response length
    context_window: int         # Chat history size
    enable_streaming: bool      # Streaming responses
    enable_persistence: bool    # Save conversations
    ollama_host: str            # Ollama server URL
    timeout_seconds: int        # Request timeout
```

### Role-Based System Prompts

#### Admin Prompt
```
You are a helpful gym management assistant for gym administrators.
Help with system operations, analytics, staff management, and business insights.
```

#### Staff Prompt
```
You are a helpful gym assistant for gym staff members.
Help with daily operations, member check-ins, walk-in sales, and customer service.
```

#### Member Prompt
```
You are a helpful gym assistant for gym members.
Provide information about memberships, workouts, facilities, and personal fitness goals.
```

#### Public Prompt
```
You are a helpful gym assistant. Provide information about gym plans,
facilities, operating hours, and general gym information.
```

### Quick Suggestions
Context-aware suggestion chips provided based on user role:

- **Admin**: "Show today's revenue", "How many active members?", "Pending payments"
- **Staff**: "How to process walk-in?", "Check member status", "Recent sales"
- **Member**: "My membership status", "Workout tips", "Class schedule"
- **Public**: "Available plans", "Pricing", "Operating hours", "Location"

### Chatbot API Usage

#### Send Message
```javascript
POST /api/chatbot/
{
    "message": "What are the membership plans?",
    "conversation_id": "uuid-or-null"
}

Response:
{
    "response": "We offer three membership plans...",
    "conversation_id": "uuid",
    "suggestions": ["Tell me more", "Pricing details"]
}
```

#### Get Suggestions
```javascript
GET /api/chatbot/suggestions/

Response:
{
    "suggestions": [
        "What are your membership plans?",
        "Tell me about facilities",
        "Operating hours"
    ]
}
```

### Model Management

#### Switch Model
```javascript
POST /api/chatbot/models/switch/
{
    "model": "llama3.2:3b"
}

Response:
{
    "status": "success",
    "model": "llama3.2:3b",
    "message": "Model switched successfully"
}
```

#### List Models
```javascript
GET /api/chatbot/models/

Response:
{
    "models": [
        {"name": "llama3.2:1b", "size": "1.3 GB", "status": "available"},
        {"name": "llama3.2:3b", "size": "2.0 GB", "status": "available"}
    ],
    "active": "llama3.2:1b"
}
```

### Database Schema for Chatbot

#### Conversation Table
- Stores chat sessions
- Links to users (nullable for anonymous)
- Auto-generated titles
- Session tracking

#### ConversationMessage Table
- Individual messages
- Role (user/assistant/system)
- Token usage
- Response time
- Timestamps

#### ChatbotConfig Table (Singleton)
- Single configuration record
- All chatbot settings
- Admin-manageable
- Version tracking

---

## 🚀 Setup & Deployment

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- SQLite3 (included with Python)
- Git (for version control)
- Ollama (for AI chatbot)

### Installation Steps

#### 1. Clone Repository
```bash
git clone <repository-url>
cd Web-Based-Gym-System-main
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install django==5.2.7
pip install pillow  # For image handling
pip install requests  # For Ollama integration
```

#### 4. Database Setup
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

#### 5. Create Admin User
```bash
# Option 1: Custom command
python manage.py createadmin

# Option 2: Django's createsuperuser
python manage.py createsuperuser
python manage.py sync_roles  # Sync role to admin
```

#### 6. Seed Database (Optional)
```bash
# Populate with sample data
python manage.py seed_data
```

#### 7. Install Ollama (For Chatbot)
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows/Mac
# Download from https://ollama.com

# Start Ollama
ollama serve

# Pull AI model
ollama pull llama3.2:1b
```

#### 8. Run Development Server
```bash
python manage.py runserver

# Access at: http://127.0.0.1:8000/
```

### Configuration

#### settings.py Key Settings
```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Custom User Model
AUTH_USER_MODEL = 'gym_app.User'

# Timezone
TIME_ZONE = 'Asia/Manila'

# Static Files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security
SECRET_KEY = 'your-secret-key-here'  # Change in production
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

### Management Commands

#### Create Admin User
```bash
python manage.py createadmin [--username USERNAME] [--email EMAIL] [--noinput]
```

#### Sync User Roles
```bash
python manage.py sync_roles
```
Syncs Django permissions (is_superuser, is_staff) with system roles.

#### Seed Database
```bash
python manage.py seed_data
```
Creates:
- 3 membership plans (Monthly, Quarterly, Annual)
- 3 walk-in passes (1-Day, 3-Day, Weekly)
- 10 demo members
- 2 staff users
- Sample payments and memberships
- Analytics data

### Production Deployment

#### 1. Security Settings
```python
# settings.py
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### 2. Database Migration
```bash
# Switch to PostgreSQL or MySQL
pip install psycopg2-binary  # PostgreSQL
# OR
pip install mysqlclient  # MySQL

# Update DATABASES in settings.py
```

#### 3. Collect Static Files
```bash
python manage.py collectstatic
```

#### 4. Use Production Server
```bash
# Install gunicorn
pip install gunicorn

# Run
gunicorn gym_project.wsgi:application
```

#### 5. Setup Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Testing

#### Run Tests
```bash
python manage.py test
```

#### Test User Accounts (After Seeding)
- **Admin**: username: `admin`, password: `admin123`
- **Staff**: username: `staff1`, password: `staff123`
- **Member**: username: `member1`, password: `member123`

### Backup & Maintenance

#### Backup Database
```bash
# SQLite
cp db.sqlite3 backups/db_$(date +%Y%m%d).sqlite3

# PostgreSQL
pg_dump dbname > backup.sql
```

#### Clean Old Audit Logs
```python
# In Django shell
from gym_app.models import AuditLog
from datetime import timedelta
from django.utils import timezone

old_logs = AuditLog.objects.filter(
    timestamp__lt=timezone.now() - timedelta(days=365)
)
old_logs.delete()
```

---

## 📊 System Statistics

### Code Metrics
- **Total Models**: 13 database models
- **Total Views**: 30+ view functions
- **Total URL Routes**: 40+ endpoints
- **Total Templates**: 25+ HTML templates
- **Lines of Code**: ~5,000+ lines (Python + HTML + CSS + JS)

### Database Tables
- **User Tables**: 1 (User)
- **Membership Tables**: 4 (MembershipPlan, FlexibleAccess, UserMembership, Analytics)
- **Payment Tables**: 2 (Payment, WalkInPayment)
- **Activity Tables**: 3 (AuditLog, Attendance, LoginActivity)
- **Chatbot Tables**: 3 (ChatbotConfig, Conversation, ConversationMessage)

### Features Count
- **Authentication**: 3 (Login, Register, Logout)
- **Dashboards**: 3 (Admin, Staff, Member)
- **Payment Methods**: 2 (Cash, GCash)
- **User Roles**: 3 (Admin, Staff, Member)
- **Report Types**: 4+ (Financial, Membership, Demographics, Attendance)
- **Audit Actions**: 40+ logged actions

---

## 🎓 Capstone Project Documentation

### Project Title
**Web-Based Gym Management System with AI-Powered Customer Support**

### Project Type
Full-Stack Web Application

### Technologies Demonstrated
1. **Backend Development**: Django Framework, Python, ORM
2. **Frontend Development**: HTML5, CSS3, JavaScript, Responsive Design
3. **Database Design**: Relational Database (SQLite/PostgreSQL), Normalization, Indexing
4. **Security**: Authentication, Authorization, RBAC, Audit Logging
5. **AI Integration**: Local LLM Integration, Natural Language Processing
6. **Software Engineering**: MVC Pattern, REST API, Version Control (Git)

### Key Learning Outcomes
- Web application architecture
- Database design and optimization
- User authentication and authorization
- Role-based access control
- Payment processing workflows
- Analytics and reporting
- AI/ML integration
- Security best practices
- Code organization and documentation

### Project Complexity Indicators
- **Multi-user System**: 3 distinct roles with different permissions
- **Complex Business Logic**: Membership lifecycle, payment workflows, attendance tracking
- **Real-time Features**: Kiosk check-in/out, chatbot interactions
- **Data Analytics**: Dashboard metrics, reports, trend analysis
- **Advanced Security**: Audit trails, IP tracking, session management
- **AI Integration**: Local LLM, context management, model switching
- **Scalable Architecture**: Modular design, reusable components

### Potential Extensions
1. **Mobile App**: React Native or Flutter mobile application
2. **Payment Gateway**: Stripe, PayPal integration
3. **Email Notifications**: Automated emails for expiring memberships
4. **SMS Notifications**: Twilio integration for alerts
5. **Biometric Check-in**: Fingerprint or face recognition
6. **Class Scheduling**: Workout class management
7. **Trainer Management**: Personal trainer scheduling
8. **Equipment Tracking**: Gym equipment inventory
9. **Nutrition Module**: Meal planning and tracking
10. **Workout Logs**: Exercise tracking and progress monitoring

---

## 📞 Support & Documentation

### Additional Documentation Files
- `README.md` - Project overview and quick start
- `Role.md` - Detailed role hierarchy guide
- `Audit_Trail.md` - Audit logging documentation
- `CHATBOT_SETUP.md` - AI chatbot setup guide
- `SEEDER_README.md` - Database seeding instructions
- `schema.md` - Database schema reference
- `Addons.md` - Feature additions and improvements
- `STAFF.md` - Staff functionality guide
- `Phases.md` - Development phases
- `Filepath.md` - Project structure reference

### Common Issues & Solutions

#### Issue: Migrations Not Applied
```bash
python manage.py migrate --run-syncdb
```

#### Issue: Admin Can't Access Admin Panel
```bash
python manage.py sync_roles
```

#### Issue: Chatbot Not Responding
```bash
# Check Ollama is running
ollama list

# Restart Ollama
ollama serve
```

#### Issue: Static Files Not Loading
```bash
python manage.py collectstatic
```

---

## 🏆 Project Highlights

### Innovation
- **Local AI Integration**: No external API dependency for chatbot
- **Role-Based Intelligence**: Chatbot adapts to user role
- **Comprehensive Audit**: Complete activity tracking with IP logging
- **Kiosk System**: PIN-based self-service check-in

### Best Practices
- **Security First**: CSRF, XSS protection, password hashing
- **Code Organization**: Modular design, reusable components
- **Documentation**: Extensive inline and external docs
- **Database Optimization**: Proper indexing, query optimization
- **User Experience**: Intuitive UI, responsive design

### Production-Ready Features
- **Error Handling**: Graceful error management
- **Data Validation**: Server-side and client-side validation
- **Scalability**: Modular architecture for easy scaling
- **Maintainability**: Clean code, proper separation of concerns
- **Extensibility**: Easy to add new features

---

## 📈 Future Roadmap

### Phase 1 (Current)
✅ User management
✅ Membership management
✅ Payment processing
✅ Walk-in system
✅ Dashboard & analytics
✅ Audit trail
✅ AI Chatbot

### Phase 2 (Planned)
- Email notifications
- SMS alerts
- Advanced reporting (PDF export)
- Multi-gym support
- Equipment tracking
- Trainer management

### Phase 3 (Future)
- Mobile application
- Biometric integration
- Class scheduling
- Nutrition tracking
- Workout logging
- Social features

---

## 📝 License & Credits

### Project Information
- **Project Name**: Web-Based Gym Management System
- **Version**: 1.0.0
- **Development Status**: Production-Ready
- **Framework**: Django 5.2.7
- **Python Version**: 3.8+
- **AI Model**: Ollama (Llama 3.2)

### Credits
- **Django**: High-level Python web framework
- **Ollama**: Local LLM server
- **Meta AI**: Llama models
- **Google**: Gemma models
- **Mistral AI**: Mistral models

---

## 📧 Contact Information

For support, questions, or contributions, please refer to the project repository or contact the development team.

---

**Last Updated**: November 2024
**Document Version**: 1.0
**System Version**: 1.0.0

---

*This documentation is part of the Web-Based Gym Management System capstone project.*
