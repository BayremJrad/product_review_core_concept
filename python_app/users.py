"""
Users resource — wraps the /users endpoints.

Endpoints covered:
  POST   /users/register      → register(...)
  POST   /users/login         → login(...)
  GET    /users/:userId       → get_profile(user_id)
  PUT    /users/:userId       → update_profile(user_id, ...)
"""

from .client import ProductReviewClient


class UsersResource:
    def __init__(self, client: ProductReviewClient):
        self._c = client

    def register(self, username: str, email: str, password: str) -> dict:
        """
        Register a new user account.

        Returns the created user object (id, username, email, …).
        """
        return self._c._post("/users/register", {
            "username": username,
            "email": email,
            "password": password,
        })

    def login(self, email: str, password: str) -> dict:
        """
        Authenticate a user and receive a token.

        Automatically stores the returned token on the client so that
        subsequent calls are authenticated — mirrors the pm.collectionVariables
        `it_token` capture in the integration-test collection.

        Returns the full login response (token, id, …).
        """
        data = self._c._post("/users/login", {
            "email": email,
            "password": password,
        })
        if "token" in data:
            self._c.set_token(data["token"])
        return data

    def get_profile(self, user_id: str) -> dict:
        """
        Retrieve a user's public profile.

        Returns user object (id, username, email, createdAt, …).
        """
        return self._c._get(f"/users/{user_id}")

    def update_profile(
        self,
        user_id: str,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> dict:
        """
        Update a user's profile fields (only provided fields are sent).

        Returns the updated user object.
        """
        payload = {}
        if username is not None:
            payload["username"] = username
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        return self._c._put(f"/users/{user_id}", payload)
