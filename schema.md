# 🗄️ Database Schema (Updated with Walk-in Support)

---

## 1. `users`  
Stores all system users (admins, staff, members) with demographic details.

| Field         | Type         | Description                                |
|---------------|--------------|--------------------------------------------|
| id (PK)       | BIGINT       | Unique ID for each user                    |
| name          | VARCHAR(100) | Full name of the user                      |
| email         | VARCHAR(100) | Unique email for login                     |
| password      | VARCHAR(255) | Hashed password                            |
| role          | ENUM         | `admin`, `staff`, `member`                 |
| mobile_no     | VARCHAR(20)  | User’s contact number                      |
| address       | TEXT         | Full address of the user                   |
| birthdate     | DATE         | User’s date of birth                       |
| age           | INT          | User’s age (calculated from birthdate)     |
| created_at    | TIMESTAMP    | Auto timestamp                             |
| updated_at    | TIMESTAMP    | Auto timestamp                             |

---

## 2. `membership_plans`  
Stores permanent gym plans (e.g., monthly, yearly).

| Field         | Type          | Description                                |
|---------------|---------------|--------------------------------------------|
| id (PK)       | BIGINT        | Unique ID for plan                         |
| name          | VARCHAR(100)  | Plan name (e.g., Monthly Plan, Yearly Plan)|
| duration_days | INT           | Length of the plan in days                 |
| price         | DECIMAL(10,2) | Cost of the plan                           |
| created_at    | TIMESTAMP     | Auto timestamp                             |
| updated_at    | TIMESTAMP     | Auto timestamp                             |

---

## 3. `flexible_access`  
Defines short-term access passes available for walk-ins (1-day, 3-day, weekly).

| Field         | Type          | Description                                |
|---------------|---------------|--------------------------------------------|
| id (PK)       | BIGINT        | Unique ID for pass                         |
| name          | VARCHAR(100)  | Access name (e.g., 1-Day Pass, 3-Day Pass) |
| duration_days | INT           | Validity in days                           |
| price         | DECIMAL(10,2) | Cost of the pass                           |
| created_at    | TIMESTAMP     | Auto timestamp                             |
| updated_at    | TIMESTAMP     | Auto timestamp                             |

---

## 4. `user_memberships`  
Tracks which registered member purchased which permanent plan.

| Field              | Type        | Description                                |
|--------------------|-------------|--------------------------------------------|
| id (PK)            | BIGINT      | Unique ID                                  |
| user_id (FK)       | BIGINT      | Linked to `users.id`                       |
| plan_id (FK)       | BIGINT      | Linked to `membership_plans.id`            |
| start_date         | DATE        | When membership starts                     |
| end_date           | DATE        | When membership ends                       |
| status             | ENUM        | `active`, `expired`, `cancelled`           |
| created_at         | TIMESTAMP   | Auto timestamp                             |
| updated_at         | TIMESTAMP   | Auto timestamp                             |

---

## 5. `payments`  
Records all financial transactions for registered members.

| Field              | Type          | Description                                |
|--------------------|---------------|--------------------------------------------|
| id (PK)            | BIGINT        | Unique ID for payment                      |
| user_id (FK)       | BIGINT        | Linked to `users.id`                       |
| membership_id (FK) | BIGINT        | Linked to `user_memberships.id`            |
| amount             | DECIMAL(10,2) | Amount paid                                |
| method             | ENUM          | `cash`, `gcash`, `card`                    |
| payment_date       | TIMESTAMP     | When payment was made                      |
| created_at         | TIMESTAMP     | Auto timestamp                             |
| updated_at         | TIMESTAMP     | Auto timestamp                             |

---

## 6. `walk_in_payments`  
Handles payments from walk-in clients (no registered account).

| Field         | Type          | Description                                |
|---------------|---------------|--------------------------------------------|
| id (PK)       | BIGINT        | Unique ID for walk-in payment              |
| pass_id (FK)  | BIGINT        | Linked to `flexible_access.id`             |
| customer_name | VARCHAR(100)  | Optional: name of walk-in client           |
| mobile_no     | VARCHAR(20)   | Optional: contact number (if provided)     |
| amount        | DECIMAL(10,2) | Amount paid                                |
| method        | ENUM          | `cash`, `gcash`, `card`                    |
| payment_date  | TIMESTAMP     | When payment was made                      |
| created_at    | TIMESTAMP     | Auto timestamp                             |
| updated_at    | TIMESTAMP     | Auto timestamp                             |

---

## 7. `analytics` (Optional)  
Stores summarized data for reporting and demographics.

| Field         | Type          | Description                                |
|---------------|---------------|--------------------------------------------|
| id (PK)       | BIGINT        | Unique ID                                  |
| date          | DATE          | Report date                                |
| total_members | INT           | Count of active members                    |
| total_passes  | INT           | Count of walk-in passes sold               |
| total_sales   | DECIMAL(10,2) | Revenue for the day                        |
| age_group     | VARCHAR(20)   | Age group (e.g., 18-25, 26-35)             |
| created_at    | TIMESTAMP     | Auto timestamp                             |

---

# 🔗 Relationships (ERD Overview)

- `users` → `user_memberships` (One-to-Many)  
- `user_memberships` → `payments` (One-to-Many)  
- `membership_plans` → `user_memberships`  
- `flexible_access` → `walk_in_payments`  
- `analytics` aggregates from `users`, `user_memberships`, `payments`, and `walk_in_payments`  