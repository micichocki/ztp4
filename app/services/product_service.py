import requests
import os
from typing import List, Optional
from app.models.product import Product

class ProductService:
    def __init__(self, base_url: str = None):
        self.base_url = (base_url or
                         os.getenv("API_GATEWAY_URL", "http://127.0.0.1:5000")).rstrip('/')

    def get_products(self) -> List[Product]:
        try:
            response = requests.get(f"{self.base_url}/products/")
            response.raise_for_status()
            return [Product.from_dict(item) for item in response.json()]
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch products: {str(e)}")

    def get_product(self, product_id: int) -> Optional[Product]:
        try:
            response = requests.get(f"{self.base_url}/products/{product_id}")
            response.raise_for_status()
            return Product.from_dict(response.json())
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch product {product_id}: {str(e)}")
