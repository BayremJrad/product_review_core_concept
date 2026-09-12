"""
Top-level API facade.

Usage:
    from python_app.api import ProductReviewAPI

    api = ProductReviewAPI()                          # uses BASE_URL from config / env
    api = ProductReviewAPI(base_url="http://localhost:3000/v1")  # custom URL

    # Auth
    login_resp = api.users.login("john.doe@example.com", "SecurePass123!")
    # Token is automatically stored — all subsequent calls are authenticated.

    # Products
    products = api.products.list(min_rating=4, sort_by="createdAt", sort_order="desc")
    product  = api.products.create("Wireless Headphones", "Premium headphones", "Electronics", 199.99)

    # Reviews
    review = api.reviews.create(product["id"], rating=5, title="Great!", body="Love it.", user_id=login_resp["id"])

    # Suppliers
    supplier = api.suppliers.add(product["id"], name="TechDistributors Inc.", email="contact@td.com",
                                  phone="+1-800-555-0199", address="123 Supply Chain Ave", country="US")
"""

from .client import ProductReviewClient
from .users import UsersResource
from .products import ProductsResource
from .reviews import ReviewsResource
from .suppliers import SuppliersResource
from .config import BASE_URL


class ProductReviewAPI:
    """
    Unified entry-point for the Product Review API.

    Attributes:
        users     — /users endpoints
        products  — /products endpoints
        reviews   — /products/:id/reviews endpoints
        suppliers — /products/:id/suppliers endpoints
    """

    def __init__(self, base_url: str = BASE_URL):
        self._client = ProductReviewClient(base_url=base_url)
        self.users = UsersResource(self._client)
        self.products = ProductsResource(self._client)
        self.reviews = ReviewsResource(self._client)
        self.suppliers = SuppliersResource(self._client)

    # Expose token helpers at the top level for convenience
    def set_token(self, token: str) -> None:
        """Manually set a bearer token (e.g. loaded from storage)."""
        self._client.set_token(token)

    def clear_token(self) -> None:
        """Remove the current bearer token."""
        self._client.clear_token()
