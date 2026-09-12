"""
Products resource — wraps the /products endpoints.

Endpoints covered:
  GET    /products                → list(...)
  POST   /products                → create(...)
  GET    /products/:productId     → get(product_id)
  PUT    /products/:productId     → update(product_id, ...)
  DELETE /products/:productId     → delete(product_id)
"""

from .client import ProductReviewClient


class ProductsResource:
    def __init__(self, client: ProductReviewClient):
        self._c = client

    def list(
        self,
        min_price: int | None = None,
        max_price: int | None = None,
        min_rating: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        search: str | None = None,
    ) -> dict:
        """
        List products with optional filters.

        Query params mirror the Postman collection:
          minPrice, maxPrice, minRating, sortBy, sortOrder, search
        """
        params = {}
        if min_price is not None:
            params["minPrice"] = min_price
        if max_price is not None:
            params["maxPrice"] = max_price
        if min_rating is not None:
            params["minRating"] = min_rating
        if sort_by is not None:
            params["sortBy"] = sort_by
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if search is not None:
            params["search"] = search
        return self._c._get("/products", params=params)

    def create(
        self,
        name: str,
        description: str,
        category: str,
        price: float,
        image_url: str | None = None,
    ) -> dict:
        """
        Create a new product.

        Returns the created product object (id, name, category, price, …).
        """
        payload: dict = {
            "name": name,
            "description": description,
            "category": category,
            "price": price,
        }
        if image_url is not None:
            payload["imageUrl"] = image_url
        return self._c._post("/products", payload)

    def get(self, product_id: str) -> dict:
        """
        Retrieve a single product by ID.
        """
        return self._c._get(f"/products/{product_id}")

    def update(
        self,
        product_id: str,
        name: str | None = None,
        description: str | None = None,
        category: str | None = None,
        price: float | None = None,
        image_url: str | None = None,
    ) -> dict:
        """
        Update a product's fields (only provided fields are sent).
        """
        payload = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if category is not None:
            payload["category"] = category
        if price is not None:
            payload["price"] = price
        if image_url is not None:
            payload["imageUrl"] = image_url
        return self._c._put(f"/products/{product_id}", payload)

    def delete(self, product_id: str) -> dict:
        """
        Delete a product by ID.
        """
        return self._c._delete(f"/products/{product_id}")
