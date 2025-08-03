
# 📦 SmartMart Backend Documentation

> **A secure, modular, and scalable e-commerce API built with Django and Django REST Framework.**  
> Focused on JWT authentication, blacklisting, and production-ready deployment.

![Python](https://img.shields.io/badge/python-3.10-blue)
![Django](https://img.shields.io/badge/django-5.2.1-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ Key Features

- JWT authentication with blacklisting
- Role-based permission system
- ePayco payment integration
- Slug-based product & category URLs
- Modular apps, production-ready
- RESTful APIs using DRF

---

## 📋 Table of Contents

- [Purpose and Scope](#purpose-and-scope)
- [Technology Stack](#technology-stack)
- [Key System Components](#key-system-components)
- [Authentication Architecture](#authentication-architecture)
- [JWT Authentication System](#jwt-authentication-system)
- [User Registration & Login Flow](#user-registration--login-flow)
- [Permission System](#permission-system)
- [Security Highlights](#security-highlights)
- [API Endpoints](#api-endpoints)
- [Business Logic Overview](#business-logic-overview)
- [File Structure & Models](#file-structure--models)
- [Product & Category Models](#product--category-models)
- [Order Models](#order-models)
- [Data Serialization](#data-serialization)
- [Model Relationships & Rules](#model-relationships--rules)
- [Database Table Mappings](#database-table-mappings)
- [Environment Setup](#environment-setup)
- [API Testing](#api-testing)

---

## Purpose and Scope 

The **SmartMart backend** is a Django-based e-commerce API that handles:

- 🛍 Product catalog CRUD & inventory
- 👥 User registration, verification, login/logout
- 🛒 Order management & ePayco payment confirmation
- 🔐 JWT authentication & token blacklisting
- ⚙ Modular architecture, ready for production
- 🔗 RESTful APIs using Django REST Framework

---

## Technology Stack

| Layer          | Technology            | Version | Purpose                              |
|----------------|----------------------|--------|-------------------------------------|
| Web Framework  | Django                | 5.2.1  | Core application & admin panel     |
|                | djangorestframework   | 3.16.0 | API serialization & toolkit        |
| Authentication | drf-simplejwt         | 5.5.0  | JWT authentication & blacklisting  |
| Data Layer     | Django ORM (built-in) | —      | Abstraction over SQL                |
|                | PyMySQL               | 1.1.1  | MySQL driver                        |
| Database       | MySQL                 | 8.4.4  | Production database                |
| Caching        | Django Cache          | —      | Temporary checkout data storage    |

**Note**:

This table shows the principal technologies.

To run the system, you must install all required Python packages listed in `requirements.txt`.

---

## Key System Components

### Authentication & Security

- Custom `JWTWithAccessBlacklistAuthentication`
- Email verification before activation
- Access & refresh token rotation
- Role-based permissions
- Token blacklisting on logout

![Authentication Diagram](Authentication_Diagram.png)

---

### Product Catalog System

- CRUD for products & categories
- Slug-based hierarchical categories
- Inventory tracking
- External image URLs
- Optimized RESTful endpoints

![Product Catalog](Product_Catalog.png)

---

### Order Management

- ePayco checkout & payment confirmation
- Caches checkout data temporarily
- Generates invoice IDs
- Tracks subtotal, tax, payment status

![Order Management](order_management.png)

---



## Authentication Architecture

- Blacklist check for access tokens
- Email verification before activation
- Secure logout (blacklists tokens)
- Refresh token rotation
- Role-based permissions (User, Staff, Superuser)

---

## JWT Authentication System

> Extends DRF SimpleJWT to add blacklisting.

- Custom: `JWTWithAccessBlacklistAuthentication`
- Validates against `BlacklistedAccessToken`
- Auto-cleans expired tokens

<details>
<summary>📂 BlacklistedAccessToken Model</summary>

| Field           | Type      | Purpose                |
|----------------|-----------|-----------------------|
| token           | TextField | Access token string   |
| blacklisted_at  | DateTime  | Blacklist timestamp   |
| expires_at      | DateTime  | Token expiry          |

Includes helper: `is_expired()`
</details>

---

## User Registration & Login Flow

### Registration

- `RegisterView`: validate, cache, send email
- `VerifyEmailView`: finalize user creation

![Registration Flow](registration_flow.png)

---

### Login Process

| Step | Component                | Purpose                          |
|-----|-------------------------|---------------------------------|
| 1   | LoginSerializer         | Validate credentials           |
| 2   | authenticate()         | Authenticate user              |
| 3   | Check active status    | Ensure email verified          |
| 4   | RefreshToken.for_user()| Generate tokens                |
| 5   | Response               | Return tokens                  |

---

### Logout Process

- Blacklists access token
- Invalidates refresh token

![Logout Flow](logout_flow.png)

---

## Permission System

| Group          | Purpose                                |
|---------------|----------------------------------------|
| User          | Read-only on products/orders           |
| Staff         | CRUD on products/categories            |
| Superuser     | Full access incl. user management     |
| Checkout Group| Access to checkout endpoint            |

- `IsAuthenticated`, `IsSuperUser`, `IsInGroup`, `IsOwner`, `AllowAny`

---

## Security Highlights

- Blacklisting & token rotation
- Auto-remove expired tokens
- Email verification TTL: 5 min
- Rejects malformed/inactive tokens
- Unique UUID tokens & invoice IDs
- Password hashing: `pbkdf2_sha256`
- ePayco signature validated via SHA256

---

## API Endpoints

### Product Management

| Endpoint                | Method | Auth | Purpose          |
|------------------------|------|----|-----------------|
| `/products/`           | POST | JWT | Create product  |
| `/products/`           | GET  | —   | List products   |
| `/products/{slug}/`    | GET  | —   | Retrieve        |

![Product Diagram](product_diagram.png)

---

## Category Management Endpoints

| Endpoint                            | Method | Auth | Permissions                           | Purpose                     |
|-------------------------------------|--------|------|---------------------------------------|-----------------------------|
| `/categories/`                      | POST   | JWT  | IsAuthenticated, DjangoModelPermissions | Create category             |
| `/categories/`                      | GET    | —    | —                                     | List categories             |
| `/categories/{slug}/`               | GET    | —    | —                                     | Retrieve category           |
| `/categories/{pk}/{slug}/`          | PATCH  | JWT  | Same                                  | Update category             |
| `/categories/{pk}/{slug}/`          | DELETE | JWT  | Same                                  | Delete category             |
| `/categories/{pk}/{slug}/activate/` | PATCH  | JWT  | Same                                  | Activate category + products |
| `/categories/{pk}/{slug}/deactivate/` | PATCH | JWT  | Same                                  | Deactivate category + products |

![Category Diagram](category_diagram.png)

---

## User Management Endpoints

| Endpoint             | Method | Auth | Permissions               | Purpose                   |
|----------------------|--------|------|---------------------------|---------------------------|
| `/users/profile/`    | GET    | JWT  | IsAuthenticated, IsOwner  | View profile              |
| `/users/profile/`    | PATCH  | JWT  | Same                      | Update profile            |
| `/users/deactivate/` | PATCH  | JWT  | Same                      | Deactivate account        |
| `/users/`            | GET    | JWT  | IsSuperUser               | List all users            |
| `/users/{pk}/`       | DELETE | JWT  | IsSuperUser               | Delete user               |

![User Management](user_management.png)

---

## Order Management Endpoints

| Endpoint                        | Method | Auth | Permissions                     | Purpose                                  |
|---------------------------------|--------|------|---------------------------------|------------------------------------------|
| `/epayco/checkout/`             | POST   | JWT  | IsAuthenticated, IsInGroup      | Generate ePayco payment data for checkout |
| `/epayco/response/`             | GET    | —    | AllowAny                        | Handle ePayco payment response (redirect) |
| `/checkoutconfirmation/`        | POST   | —    | AllowAny                        | Process ePayco payment confirmation      |

#### Details

- **`/epayco/checkout/`**  
  - Input: JSON with `items` (array of `{product_id, quantity, price}`)
  - Validates items, calculates subtotal and tax (19%), caches order data for 5 minutes, returns ePayco payment data
  - Requires: authenticated and in checkout group

- **`/epayco/response/`**  
  - Handles redirect after payment attempt
  - Public (no auth required)

- **`/checkoutconfirmation/`**  
  - Input: payment data (`x_ref_payco`, `x_signature`, etc.)
  - Validates SHA256 signature, creates `Order` and `OrderItem` records if payment approved (`x_cod_transaction_state == "1"`)
  - Public (no auth required)

> Signature validated using `P_CUST_ID_CLIENTE` and `P_KEY`



---

## Business Logic Overview

- User flow: register → verify → login
- Product & category CRUD
- Orders: checkout → cache → confirm
- Role-based permissions
- Token security & ePayco signature validation

![Logic Diagram](logic_diagram.png)
![Order Diagram](order_diagram.png)

---

## File Structure & Models

| File                | Purpose                                    |
|--------------------|---------------------------------------------|
| `models`        | AppUser, Product, Category, Order, etc.    |
| `views`         | API logic                                  |
| `serializers`   | Data serialization                         |
| `permissions`   | Custom permissions                          |
| `integrations/`    | ePayco checkout & confirmation logic       |
| `business_logic/`    | business logic       |


---

## Product & Category Models

<details>
<summary>Category</summary>

Fields: `name`, `slug`, `is_active`, timestamps  
Unique name & slug; auto-generate slug.
</details>

<details>
<summary>Product</summary>

Fields: `name`, `slug`, `description`, `price`, `stock_quantity`, `category_id`  
Auto-generate slug; FK to category.
</details>

---

## Order Models

<details>
<summary>Order</summary>

Tracks invoice ID, user FK, totals, timestamps.
</details>

<details>
<summary>OrderItem</summary>

Links product → order; tracks qty & price.
</details>

---

## Data Serialization

- DRF `ModelSerializer` & `Serializer`
- User, Product, Category, Checkout, Order serializers

![Serialization Flow](serialization_flow.png)

---

## Model Relationships & Rules

- AppUser ↔ Orders
- Category ↔ Products
- Product ↔ OrderItems, ProductImage
- Auto slugs, soft deletes, timestamps
- Unique invoice IDs & names

![Relationships](model_relationships.png)

---

## Database Table Mappings

| Model                   | Table                   |
|------------------------|------------------------|
| AppUser                | app_users              |
| Category               | category               |
| Product                | product                |
| ProductImage           | productimage           |
| Order                  | order                   |
| OrderItem              | orderitem               |
| BlacklistedAccessToken | BlacklistedAccessToken |

---

## Environment Setup

```bash
cd backend/smartmart
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
````

* Adjust `.env` with secrets, DB URL, ePayco keys

---

## API Testing

Use Postman collection (Deployed on  PythonAnywhere):
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/45628109-ffd10932-54ee-48b5-9dff-18215e2c444d?action=collection%2Ffork)

