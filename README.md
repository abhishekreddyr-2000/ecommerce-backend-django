# Title

E-Commerce Backend API

## Objective

To build a RESTful E-Commerce Backend API using Django and Django REST Framework (DRF), implementing user authentication, product management, cart operations, checkout, orders, and payments.

## Project Description

This project is a backend API for an e-commerce application. It provides REST APIs for customers and sellers and uses **JWT authentication** to protect authenticated operations.

The application manages the complete basic shopping flow:

**User → Products → Cart → Checkout → Order → Payment**

## Live API

Base URL:

https://ecommerce-backend-django-lw1t.onrender.com

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
* Order status and cancellation management
* Payment management and validation
* Validation for cancelled and already-processed payments

## Tech Stack

* **Language:** Python
* **Framework:** Django
* **API:** Django REST Framework
* **Authentication:** Simple JWT
* **Database:** PostgreSQL (Production), SQLite (Local Development)
* **Deployment:** Render
* **Static Files:** WhiteNoise
* **WSGI Server:** Gunicorn
* **Filtering:** django-filter
* **CORS:** django-cors-headers
* **Version Control:** Git & GitHub
* **API Testing:** Postman
* **Configuration:** python-dotenv

## Project Architecture

```text
ecommerce/
|
|-- User/
|-- products/
|-- cart/
|-- orders/
|-- payments/
|-- ecommerce/
|
|-- manage.py
|-- .gitignore
|-- .env.example
|-- requirements.txt
|-- README.md
```

### Applications

| App       | Responsibility                                            |
| --------- | --------------------------------------------------------- |
| User      | User registration, authentication, profile, and logout    |
| products  | Product management, filtering, sorting, and pagination    |
| cart      | User shopping cart and cart item management               |
| orders    | Checkout, order creation, order details, and cancellation |
| payments  | Payment creation, status management, and validation       |
| ecommerce | Project configuration, settings, and main URL routing     |


## Database Design

Main models and relationships:

```text
User
|
|-- Cart
|   |
|   |-- CartItem ---> Product
|
|-- Order
    |
    |-- OrderItem ---> Product
    |
    |-- Payment
```

### Main Models

* **User** - Stores user information, including customer and seller user types.
* **Product** - Stores product details and seller information.
* **Cart** - Stores the shopping cart associated with a user.
* **CartItem** - Connects products with a user's cart and stores quantity.
* **Order** - Stores order information, total amount, and order status.
* **OrderItem** - Stores products, quantities, and product prices for an order.
* **Payment** - Stores payment method, payment status, amount, and the associated order.


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

### User Authentication

| Method | Endpoint                   | Description                 |
| ------ | -------------------------- | --------------------------- |
| POST   | `/api/user/register/`      | Register a new user         |
| POST   | `/api/user/login/`         | Login and obtain JWT tokens |
| POST   | `/api/user/login/refresh/` | Refresh access token        |
| GET    | `/api/user/profile/`       | View user profile           |
| POST   | `/api/user/logout/`        | Logout user                 |

### Products

| Method | Endpoint              | Description                |
| ------ | --------------------- | -------------------------- |
| GET    | `/api/products/`      | List products              |
| POST   | `/api/products/`      | Create a product           |
| GET    | `/api/products/<id>/` | View product details       |
| PUT    | `/api/products/<id>/` | Update a product           |
| PATCH  | `/api/products/<id>/` | Partially update a product |
| DELETE | `/api/products/<id>/` | Delete a product           |

### Cart

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/api/cart/`       | View user's cart    |
| POST   | `/api/add/`        | Add product to cart |
| PATCH  | `/api/items/<id>/` | Update cart item    |
| DELETE | `/api/items/<id>/` | Remove cart item    |

### Orders

| Method | Endpoint                         | Description                     |
| ------ | -------------------------------- | ------------------------------- |
| GET    | `/api/orders/`                   | View all orders of the logged-in user |
| POST   | `/api/orders/`                   | Create an order from cart items |
| GET    | `/api/orders/<order_id>/`        | View order details              |
| POST   | `/api/orders/<order_id>/cancel/` | Cancel an order                 |

### Payments

| Method | Endpoint                             | Description           |
| ------ | ------------------------------------ | --------------------- |
| POST   | `/api/payments/`                     | Create a payment      |
| GET    | `/api/payments/<payment_id>/`        | View payment details  |
| POST   | `/api/payments/<payment_id>/status/` | Update payment status |

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/abhishekreddyr-2000/ecommerce-backend-django.git
cd ecommerce-backend-django
```

### 2. Create a Virtual Environment

```bash
python -m venv env
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as a template and replace the placeholder values with your local values.

Generate a Django secret key using:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

### 6. Run Database Migrations

```bash
python manage.py migrate
```

### 7. Create a Superuser

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

## Deployment

The application is deployed on Render.

Production setup includes:

* Django application served using Gunicorn
* PostgreSQL database for persistent production data
* WhiteNoise for static file handling
* Environment variables for sensitive configuration
* `DEBUG=False` in production

## Testing

API functionality was tested using:

* Postman
* Django REST Framework browsable API

The following scenarios were tested:

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
* Product reviews and ratings
* Wishlist
* Coupons and discounts
* Seller dashboard
* Email notifications
* Swagger/OpenAPI documentation

## Learning Outcomes

This project provided practical experience in:

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
