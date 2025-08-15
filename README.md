# 📦 Orders & Inventory Service — FastAPI

A simple yet powerful **Orders & Inventory Management API** built with **FastAPI**, **SQLite**, and **SQLAlchemy**.  
This project demonstrates practical FastAPI usage including **CRUD operations**, **API key authentication**, and **rate limiting**.

🌐 **Live Demo**: [orders-inventory-service-fastapi.onrender.com](https://orders-inventory-service-fastapi.onrender.com/)

---

## ✨ Features

- 🛍 **Product Management** — Create, read, update, and delete products.
- 📦 **Order Management** — Manage orders linked to products.
- 🔑 **API Key Authentication** — Secure endpoints with generated API keys.
- 🚦 **Rate Limiting** — Prevent abuse with request limits.
- ⚡ **FastAPI Benefits** — Async support, automatic OpenAPI docs, and blazing-fast performance.
- 🗄 **SQLite Database** — Lightweight, file-based relational database.

---

## 🛠 Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Authentication**: API Key
- **Deployment**: Render

---

## 📂 Project Structure

```
orders-inventory-service-fastapi/
│
├── app/
│   ├── main.py               # Application entry point
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── crud.py                # CRUD operations
│   ├── dependencies.py       # Auth, rate limit logic
│   ├── database.py           # DB connection
│   ├── routers/              # API routes
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/RD191295/orders-Inventory-service-FastAPI.git
cd orders-Inventory-service-FastAPI
```

### 2️⃣ Create & Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📖 API Documentation

FastAPI automatically generates interactive docs:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## 🔑 API Key Usage

1. Create an API key using the `/apikeys/` endpoint.
2. Pass the API key in the `X-API-Key` header for protected routes:
```bash
curl -H "X-API-Key: YOUR_API_KEY" http://127.0.0.1:8000/products/
```

---

## 📌 Example Endpoints

| Method | Endpoint              | Description                | Auth Required |
|--------|-----------------------|----------------------------|-------------- |
| POST   | `/products/`           | Create a new product       | ✅           |
| GET    | `/products/`           | List all products          | ✅           |
| POST   | `/orders/`             | Create a new order         | ✅           |
| GET    | `/orders/`             | List all orders            | ✅           |
| POST   | `/apikeys/`            | Generate an API key        | ❌           |

---

## ⚡ Rate Limiting

- Default: `100` requests/minute per API key  
- Configurable in the `rate_limiter.py` file.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`feature/your-feature`)
3. Commit your changes
4. Push and open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent framework
- [Render](https://render.com/) for free hosting
- [SQLAlchemy](https://www.sqlalchemy.org/) for ORM support
