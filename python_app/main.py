"""
Demo script — walks through the full lifecycle mirroring the
Integration Test collection order:

  01 User Auth Flow      → register → login → get profile → update profile
  02 Product Lifecycle   → create → get → update → list → delete
  03 Review Lifecycle    → create → get → update → list → delete
  04 Supplier Lifecycle  → add → get → update → list → remove

Run:
    python -m python_app.main
    # or override the base URL:
    PRODUCT_REVIEW_BASE_URL=http://localhost:3000/v1 python -m python_app.main
"""

import json
from python_app.api import ProductReviewAPI


def pp(label: str, data: dict) -> None:
    """Pretty-print a labelled API response."""
    print(f"\n{'─' * 60}")
    print(f"  {label}")
    print('─' * 60)
    print(json.dumps(data, indent=2))


def main() -> None:
    api = ProductReviewAPI()

    # ── 01 User Auth Flow ────────────────────────────────────────────
    print("\n╔══════════════════════════════╗")
    print("║   01  User Auth Flow         ║")
    print("╚══════════════════════════════╝")

    reg = api.users.register(
        username="johndoe",
        email="john.doe@example.com",
        password="SecurePass123!",
    )
    pp("POST /users/register", reg)
    user_id = reg.get("id", "<user_id>")

    login = api.users.login(
        email="john.doe@example.com",
        password="SecurePass123!",
    )
    pp("POST /users/login  (token auto-stored)", login)
    # token is now attached to every subsequent request

    profile = api.users.get_profile(user_id)
    pp(f"GET /users/{user_id}", profile)

    updated_user = api.users.update_profile(user_id, username="johndoe_updated")
    pp(f"PUT /users/{user_id}", updated_user)

    # ── 02 Product Lifecycle ─────────────────────────────────────────
    print("\n╔══════════════════════════════╗")
    print("║   02  Product Lifecycle      ║")
    print("╚══════════════════════════════╝")

    product = api.products.create(
        name="Wireless Headphones",
        description="Premium noise-cancelling wireless headphones",
        category="Electronics",
        price=199.99,
        image_url="https://example.com/images/headphones.jpg",
    )
    pp("POST /products", product)
    product_id = product.get("id", "<product_id>")

    pp(f"GET /products/{product_id}", api.products.get(product_id))

    updated_product = api.products.update(product_id, price=179.99)
    pp(f"PUT /products/{product_id}", updated_product)

    products_list = api.products.list(
        min_rating=1,
        sort_by="createdAt",
        sort_order="desc",
    )
    pp("GET /products (filtered)", products_list)

    # ── 03 Review Lifecycle ──────────────────────────────────────────
    print("\n╔══════════════════════════════╗")
    print("║   03  Review Lifecycle       ║")
    print("╚══════════════════════════════╝")

    review = api.reviews.create(
        product_id=product_id,
        rating=5,
        title="Excellent product!",
        body="I've been using this for 3 months and it's fantastic.",
        user_id=user_id,
    )
    pp(f"POST /products/{product_id}/reviews", review)
    review_id = review.get("id", "<review_id>")

    pp(f"GET /products/{product_id}/reviews/{review_id}",
       api.reviews.get(product_id, review_id))

    updated_review = api.reviews.update(product_id, review_id, title="Still great after 6 months!")
    pp(f"PUT /products/{product_id}/reviews/{review_id}", updated_review)

    pp(f"GET /products/{product_id}/reviews", api.reviews.list(product_id))

    pp(f"DELETE /products/{product_id}/reviews/{review_id}",
       api.reviews.delete(product_id, review_id))

    # ── 04 Supplier Lifecycle ────────────────────────────────────────
    print("\n╔══════════════════════════════╗")
    print("║   04  Supplier Lifecycle     ║")
    print("╚══════════════════════════════╝")

    supplier = api.suppliers.add(
        product_id=product_id,
        name="TechDistributors Inc.",
        email="contact@techdistributors.com",
        phone="+1-800-555-0199",
        address="123 Supply Chain Ave, San Francisco, CA 94105",
        country="US",
        website="https://techdistributors.com",
    )
    pp(f"POST /products/{product_id}/suppliers", supplier)
    supplier_id = supplier.get("id", "<supplier_id>")

    pp(f"GET /products/{product_id}/suppliers/{supplier_id}",
       api.suppliers.get(product_id, supplier_id))

    updated_supplier = api.suppliers.update(product_id, supplier_id, phone="+1-800-555-9999")
    pp(f"PUT /products/{product_id}/suppliers/{supplier_id}", updated_supplier)

    pp(f"GET /products/{product_id}/suppliers", api.suppliers.list(product_id))

    pp(f"DELETE /products/{product_id}/suppliers/{supplier_id}",
       api.suppliers.remove(product_id, supplier_id))

    # ── Cleanup ──────────────────────────────────────────────────────
    pp(f"DELETE /products/{product_id}", api.products.delete(product_id))

    print("\n✅  Full lifecycle demo complete.")


if __name__ == "__main__":
    main()
