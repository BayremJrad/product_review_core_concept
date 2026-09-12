"""
Reviews resource — wraps the /products/:productId/reviews endpoints.

Endpoints covered:
  GET    /products/:productId/reviews              → list(product_id)
  POST   /products/:productId/reviews              → create(product_id, ...)
  GET    /products/:productId/reviews/:reviewId    → get(product_id, review_id)
  PUT    /products/:productId/reviews/:reviewId    → update(product_id, review_id, ...)
  DELETE /products/:productId/reviews/:reviewId    → delete(product_id, review_id)
"""

from .client import ProductReviewClient


class ReviewsResource:
    def __init__(self, client: ProductReviewClient):
        self._c = client

    def list(self, product_id: str) -> dict:
        """
        List all reviews for a product.
        """
        return self._c._get(f"/products/{product_id}/reviews")

    def create(
        self,
        product_id: str,
        rating: int,
        title: str,
        body: str,
        user_id: str,
    ) -> dict:
        """
        Submit a new review for a product.

        Args:
            product_id: The product being reviewed.
            rating:     1–5 star rating.
            title:      Short review headline.
            body:       Full review text.
            user_id:    ID of the reviewing user (mirrors `it_userId` variable).
        """
        return self._c._post(f"/products/{product_id}/reviews", {
            "rating": rating,
            "title": title,
            "body": body,
            "userId": user_id,
        })

    def get(self, product_id: str, review_id: str) -> dict:
        """
        Retrieve a single review.
        """
        return self._c._get(f"/products/{product_id}/reviews/{review_id}")

    def update(
        self,
        product_id: str,
        review_id: str,
        rating: int | None = None,
        title: str | None = None,
        body: str | None = None,
    ) -> dict:
        """
        Update a review's fields (only provided fields are sent).
        """
        payload = {}
        if rating is not None:
            payload["rating"] = rating
        if title is not None:
            payload["title"] = title
        if body is not None:
            payload["body"] = body
        return self._c._put(f"/products/{product_id}/reviews/{review_id}", payload)

    def delete(self, product_id: str, review_id: str) -> dict:
        """
        Delete a review.
        """
        return self._c._delete(f"/products/{product_id}/reviews/{review_id}")
