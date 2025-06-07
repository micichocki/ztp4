import requests
import os
from typing import List, Optional
from app.models.product import Product


class ProductService:
    @staticmethod
    def get_products() -> List[Product]:
        base_url = os.getenv("API_GATEWAY_URL", "http://127.0.0.1:5001").rstrip('/')
        try:
            response = requests.get(f"{base_url}/products/")
            response.raise_for_status()
            products = [Product.from_dict(item) for item in response.json()]
            return products
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch products: {str(e)}")

    @staticmethod
    def get_product(product_id: int) -> Optional[Product]:
        base_url = os.getenv("API_GATEWAY_URL", "http://127.0.0.1:5001").rstrip('/')
        try:
            response = requests.get(f"{base_url}/products/{product_id}")
            response.raise_for_status()
            product = Product.from_dict(response.json())
            return product
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch product {product_id}: {str(e)}")
