# Title

E-Commerce Backend API

## Objective

To build a secure and scalable **E-Commerce Backend REST API** using Django and Django REST Framework (DRF), covering user authentication, products, cart, checkout, orders, and payments.

## Project Description

This project is a backend API for an e-commerce application. It provides REST APIs for customers and sellers and uses **JWT authentication** to protect authenticated operations.

The application manages the complete basic shopping flow:

**User → Products → Cart → Checkout → Order → Payment**

## Features

* User registration and login
* JWT-based authentication
* Customer and seller user types
* Product listing and creation
* Product filtering, sorting, and pagination
* Prime product access for authenticated users
* User-specific shopping cart
* Add, update, and remove cart items
* Checkout selected cart items
* Order and order-item management
* Order status management
* Payment management
* Validation for cancelled and already-processed payments

## Tech Stack

* **Language:** Python
* **Framework:** Django
* **API:** Django REST Framework
* **Authentication:** Simple JWT
* **Database:** SQLite
* **Filtering:** django-filter
* **CORS:** django-cors-headers
* **Version Control:** Git & GitHub

## Project Architecture

```text
ecommerce/
│
├── User/
├── products/
├── cart/
├── orders/
├── payments/
├── ecommerce/
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Applications

| App       | Responsibility                      |
| --------- | ----------------------------------- |
| User      | Registration, login, authentication |
| Products  | Product management and filtering    |
| Cart      | Shopping cart management            |
| Orders    | Checkout and order management       |
| Payments  | Payment processing and validation   |
| Ecommerce | Project configuration and URLs      |

## Database Design

Main models and relationships:

```text
User
 │
 ├── Cart
 │     └── CartItem ─── Product
 │
 └── Order
       └── OrderItem ─── Product
              │
              └── Payment
```

### Main Models

* **User** – Stores customer/seller information.
* **Product** – Stores product details and seller information.
* **Cart** – One-to-one relationship with User.
* **CartItem** – Connects products with a user's cart.
* **Order** – Stores order information and status.
* **OrderItem** – Stores products, quantities, and prices for an order.
* **Payment** – Stores payment method, status, amount, and order.

## Authentication & Authorization

The project uses **JWT authentication** with Django REST Framework.

### Authentication Flow

```text
Register
   ↓
Login
   ↓
Access + Refresh Token
   ↓
Send Access Token
   ↓
Access Protected APIs
```

Protected APIs require:

```http
Authorization: Bearer <access_token>
```

The project also uses permission classes such as:

```python
IsAuthenticated
```

to restrict authenticated operations.

## API Endpoints

### Users

| Method | Endpoint               | Description   |
| ------ | ---------------------- | ------------- |
| POST   | `/api/users/register/` | Register user |
| POST   | `/api/users/login/`    | Login user    |

### Products

| Method | Endpoint                              | Description           |
| ------ | ------------------------------------- | --------------------- |
| GET    | `/api/products/`                      | List products         |
| POST   | `/api/products/`                      | Create product        |
| GET    | `/api/products/?category=Electronics` | Filter products       |
| GET    | `/api/products/?ordering=price`       | Sort by price         |
| GET    | `/api/products/?ordering=-price`      | Sort high to low      |
| GET    | `/api/products/?is_prime=true`        | Access Prime products |

### Cart

| Method | Endpoint     | Description      |
| ------ | ------------ | ---------------- |
| GET    | `/api/cart/` | View cart        |
| POST   | `/api/cart/` | Add item to cart |
| PATCH  | `/api/cart/` | Update cart item |
| DELETE | `/api/cart/` | Remove cart item |

### Orders

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| GET    | `/api/orders/`          | View user orders        |
| POST   | `/api/orders/checkout/` | Checkout selected items |

### Payments

Payment APIs are used to create and manage payments associated with orders.

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd ecommerce
```

### 2. Create Virtual Environment

```bash
python -m venv env
```

### 3. Activate Virtual Environment

Windows:

```powershell
.\env\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

## How to Run the Project

Start the Django development server:

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

APIs can be tested using **Postman** or any API client.

## Testing

The APIs can be tested using:

* Postman
* Django REST Framework browsable API
* Django test framework

Testing includes:

* User registration and login
* JWT authentication
* Product APIs
* Cart operations
* Checkout
* Order creation
* Payment validation
* Protected API access

## Future Enhancements

* Razorpay payment gateway integration
* PostgreSQL database
* Product reviews and ratings
* Wishlist
* Coupons and discounts
* Seller dashboard
* Email notifications
* Swagger/OpenAPI documentation
* Production deployment

## Learning Outcomes

Through this project, I gained practical experience in:

* Python and Django
* Django REST Framework
* REST API development
* JWT authentication
* Permissions and authorization
* Django ORM and relationships
* Serializers and validation
* Filtering, sorting, and pagination
* Cart and checkout business logic
* Order and payment management
* Git and GitHub
