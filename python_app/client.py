"""
Base HTTP client for the Product Review API.
Handles authentication, headers, and shared request logic.
"""

import requests
from .config import BASE_URL


class ProductReviewClient:
    """
    Base client that manages the session, base URL, and auth token.
    All resource clients (users, products, reviews, suppliers) inherit from this.
    """

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self._token: str | None = None

    # ------------------------------------------------------------------
    # Auth helpers
    # ------------------------------------------------------------------

    def set_token(self, token: str) -> None:
        """Store a bearer token and attach it to every subsequent request."""
        self._token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self) -> None:
        """Remove the stored bearer token."""
        self._token = None
        self.session.headers.pop("Authorization", None)

    # ------------------------------------------------------------------
    # Low-level request helpers
    # ------------------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _get(self, path: str, params: dict | None = None) -> dict:
        resp = self.session.get(self._url(path), params=params)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, json: dict | None = None) -> dict:
        resp = self.session.post(self._url(path), json=json)
        resp.raise_for_status()
        return resp.json()

    def _put(self, path: str, json: dict | None = None) -> dict:
        resp = self.session.put(self._url(path), json=json)
        resp.raise_for_status()
        return resp.json()

    def _delete(self, path: str) -> dict:
        resp = self.session.delete(self._url(path))
        resp.raise_for_status()
        return resp.json()
