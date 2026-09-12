# Product Review API — Python Client

A lightweight Python client for the **Product Review API**, generated from the Postman collection, integration tests, and OpenAPI spec in this workspace.

---

## Project structure

```
python_app/
├── __init__.py
├── config.py       # Base URL (reads PRODUCT_REVIEW_BASE_URL env var)
├── client.py       # Base HTTP client (session, auth token, helpers)
├── users.py        # /users endpoints
├── products.py     # /products endpoints
├── reviews.py      # /products/:id/reviews endpoints
├── suppliers.py    # /products/:id/suppliers endpoints
├── api.py          # Unified facade — single import point
└── main.py         # Demo script (full lifecycle)
```

---

## Requirements

```bash
pip install requests
```

Python 3.10+ is required (uses `X | None` union syntax).

---

## Quick start

```python
from python_app.api import ProductReviewAPI

api = ProductReviewAPI()  # defaults to https://api.productreview.com/v1

# Override with a local dev server or mock server:
# api = ProductReviewAPI(base_url="http://localhost:3000/v1")
```

### 1 — Register & login

```python
api.users.register(username="johndoe", email="john@example.com", password="SecurePass123!")

login = api.users.login(email="john@example.com", password="SecurePass123!")
# The token is automatically stored — all subsequent calls are authenticated.
user_id = login["id"]
```

### 2 — Products

```python
# Create
product = api.products.create(
    name="Wireless Headphones",
    description="Premium noise-cancelling headphones",
    category="Electronics",
    price=199.99,
    image_url="https://example.com/headphones.jpg",
)
product_id = product["id"]

# List with filters (mirrors Postman query params: minPrice, maxPrice, minRating, sortBy, sortOrder, search)
api.products.list(min_rating=4, sort_by="createdAt", sort_order="desc")

# Get / Update / Delete
api.products.get(product_id)
api.products.update(product_id, price=179.99)
api.products.delete(product_id)
```

### 3 — Reviews

```python
review = api.reviews.create(
    product_id=product_id,
    rating=5,
    title="Excellent product!",
    body="I've been using this for 3 months and it's fantastic.",
    user_id=user_id,
)
review_id = review["id"]

api.reviews.list(product_id)
api.reviews.get(product_id, review_id)
api.reviews.update(product_id, review_id, title="Still great after 6 months!")
api.reviews.delete(product_id, review_id)
```

### 4 — Suppliers

```python
supplier = api.suppliers.add(
    product_id=product_id,
    name="TechDistributors Inc.",
    email="contact@techdistributors.com",
    phone="+1-800-555-0199",
    address="123 Supply Chain Ave, San Francisco, CA 94105",
    country="US",
    website="https://techdistributors.com",
)
supplier_id = supplier["id"]

api.suppliers.list(product_id)
api.suppliers.get(product_id, supplier_id)
api.suppliers.update(product_id, supplier_id, phone="+1-800-555-9999")
api.suppliers.remove(product_id, supplier_id)
```

---

## Configuration

| Environment variable          | Default                              | Description                  |
|-------------------------------|--------------------------------------|------------------------------|
| `PRODUCT_REVIEW_BASE_URL`     | `https://api.productreview.com/v1`   | API base URL (mirrors `{{baseUrl}}` in Postman) |

---

## Run the demo

The `main.py` script walks through the full lifecycle in the same order as the **Integration Test** collection (User Auth → Product → Review → Supplier):

```bash
# Against the live API
python -m python_app.main

# Against a local server or Postman mock
PRODUCT_REVIEW_BASE_URL=http://localhost:3000/v1 python -m python_app.main
```

---

## Mapping to Postman collection

| Python method | HTTP | Postman request |
|---|---|---|
| `users.register()` | `POST /users/register` | POST Register User |
| `users.login()` | `POST /users/login` | POST Login |
| `users.get_profile()` | `GET /users/:userId` | GET Get User Profile |
| `users.update_profile()` | `PUT /users/:userId` | PUT Update User Profile |
| `products.list()` | `GET /products` | GET List Products |
| `products.create()` | `POST /products` | POST Create Product |
| `products.get()` | `GET /products/:productId` | GET Get Product |
| `products.update()` | `PUT /products/:productId` | PUT Update Product |
| `products.delete()` | `DELETE /products/:productId` | DELETE Delete Product |
| `reviews.list()` | `GET /products/:id/reviews` | GET List Reviews for Product |
| `reviews.create()` | `POST /products/:id/reviews` | POST Create Review |
| `reviews.get()` | `GET /products/:id/reviews/:reviewId` | GET Get Review |
| `reviews.update()` | `PUT /products/:id/reviews/:reviewId` | PUT Update Review |
| `reviews.delete()` | `DELETE /products/:id/reviews/:reviewId` | DELETE Delete Review |
| `suppliers.list()` | `GET /products/:id/suppliers` | GET List Suppliers for Product |
| `suppliers.add()` | `POST /products/:id/suppliers` | POST Add Supplier to Product |
| `suppliers.get()` | `GET /products/:id/suppliers/:supplierId` | GET Get Supplier |
| `suppliers.update()` | `PUT /products/:id/suppliers/:supplierId` | PUT Update Supplier |
| `suppliers.remove()` | `DELETE /products/:id/suppliers/:supplierId` | DELETE Remove Supplier from Product |
