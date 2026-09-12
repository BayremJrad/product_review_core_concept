"""
Configuration for the Product Review API Python client.
Mirrors the {{baseUrl}} variable used in Postman collections.
"""

import os

BASE_URL = os.getenv("PRODUCT_REVIEW_BASE_URL", "https://api.productreview.com/v1")
