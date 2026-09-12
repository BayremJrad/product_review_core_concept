"""
Suppliers resource — wraps the /products/:productId/suppliers endpoints.

Endpoints covered:
  GET    /products/:productId/suppliers              → list(product_id)
  POST   /products/:productId/suppliers              → add(product_id, ...)
  GET    /products/:productId/suppliers/:supplierId  → get(product_id, supplier_id)
  PUT    /products/:productId/suppliers/:supplierId  → update(product_id, supplier_id, ...)
  DELETE /products/:productId/suppliers/:supplierId  → remove(product_id, supplier_id)
"""

from .client import ProductReviewClient


class SuppliersResource:
    def __init__(self, client: ProductReviewClient):
        self._c = client

    def list(self, product_id: str) -> dict:
        """
        List all suppliers associated with a product.
        """
        return self._c._get(f"/products/{product_id}/suppliers")

    def add(
        self,
        product_id: str,
        name: str,
        email: str,
        phone: str,
        address: str,
        country: str,
        website: str | None = None,
    ) -> dict:
        """
        Add a new supplier and associate them with a product.

        Mirrors the POST Add Supplier to Product request body.
        """
        payload: dict = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "country": country,
        }
        if website is not None:
            payload["website"] = website
        return self._c._post(f"/products/{product_id}/suppliers", payload)

    def get(self, product_id: str, supplier_id: str) -> dict:
        """
        Retrieve a single supplier for a product.
        """
        return self._c._get(f"/products/{product_id}/suppliers/{supplier_id}")

    def update(
        self,
        product_id: str,
        supplier_id: str,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        country: str | None = None,
        website: str | None = None,
    ) -> dict:
        """
        Update a supplier's fields (only provided fields are sent).
        """
        payload = {}
        if name is not None:
            payload["name"] = name
        if email is not None:
            payload["email"] = email
        if phone is not None:
            payload["phone"] = phone
        if address is not None:
            payload["address"] = address
        if country is not None:
            payload["country"] = country
        if website is not None:
            payload["website"] = website
        return self._c._put(f"/products/{product_id}/suppliers/{supplier_id}", payload)

    def remove(self, product_id: str, supplier_id: str) -> dict:
        """
        Remove a supplier from a product.
        """
        return self._c._delete(f"/products/{product_id}/suppliers/{supplier_id}")
