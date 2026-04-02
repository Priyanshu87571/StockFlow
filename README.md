# StockFlow – B2B Inventory Management System

StockFlow is a B2B SaaS backend application designed to help small and medium businesses manage inventory across multiple warehouses, track low-stock alerts, manage suppliers, and handle reorder workflows securely.

## Features

* JWT-based Authentication

* Multi-company & multi-warehouse support

* Product & Inventory Management

* Low-stock alerts based on sales velocity

🏷️ Supplier management & reorder requests

🧾 Inventory history & sales tracking

🐳 Dockerized setup

🗄️ Database migrations using Flask-Migrate

🧪 Unit test structure with Pytest

🛠️ Tech Stack

Backend: Python, Flask

Database: SQLite (can be replaced with PostgreSQL/MySQL)

ORM: SQLAlchemy

Authentication: Flask-JWT-Extended

Migrations: Flask-Migrate (Alembic)

Containerization: Docker & Docker Compose

Testing: Pytest

📂 Project Structure

stockflow/
│
├── app/
│   ├── __init__.py        # App factory
│   ├── config.py          # Configuration
│   ├── models.py          # Database models
│   ├── routes.py          # API routes
│   └── utils.py           # Helper functions
│
├── migrations/            # Database migrations
├── tests/                 # Unit tests
│
├── run.py                 # Application entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

⚙️ Setup Instructions

1️⃣ Clone Repository
git clone https://github.com/Priyanshu87571/StockFlow.git
cd StockFlow

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Environment Variables (Windows PowerShell)
$env:FLASK_APP="run.py"
$env:FLASK_ENV="development"

5️⃣ Run Database Migrations
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade

6️⃣ Start the Server
python run.py


Server runs at:

http://127.0.0.1:5000

🔐 Authentication
Login API

POST /api/auth/login

{
  "email": "admin@demo.com"
}


Response:

{
  "access_token": "JWT_TOKEN"
}


Use token in headers:

Authorization: Bearer JWT_TOKEN

📦 Create Product API

POST /api/products

{
  "name": "Widget A",
  "sku": "WID-001",
  "price": "99.99",
  "warehouse_id": 1,
  "initial_quantity": 10,
  "product_type": "standard"
}

🚨 Low Stock Alerts API

GET /api/companies/{company_id}/alerts/low-stock

Sample Response
{
  "alerts": [
    {
      "product_id": 1,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_name": "Main Warehouse",
      "current_stock": 5,
      "threshold": 20,
      "days_until_stockout": 7,
      "supplier": {
        "id": 1,
        "name": "ABC Supplier",
        "email": "orders@abc.com"
      }
    }
  ],
  "total_alerts": 1
}

📦 Reorder Request API

POST /api/reorders

{
  "product_id": 1,
  "supplier_id": 1,
  "warehouse_id": 1,
  "quantity": 50
}

🐳 Docker Setup
docker-compose up --build

🧪 Run Tests
pytest

🧠 Design Decisions & Assumptions

Inventory is modeled as a relationship between Product and Warehouse

SKU is globally unique

Low-stock alerts are triggered only for products with recent sales

Threshold varies by product type

Sales velocity determines days until stockout

One primary supplier per product (extendable)

📈 Future Improvements

Role-based access control (Admin, Manager)

Background jobs for alerts & notifications

Pagination & filtering for APIs

Cloud deployment (AWS / GCP)

Frontend dashboard (React)

👤 Author

Priyanshu Raj
Backend Developer | Python | Flask | SQL

GitHub: https://github.com/Priyanshu87571


⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!
