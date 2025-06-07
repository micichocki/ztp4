import requests
from typing import List, Optional
from app.models.product import Product

class ProductService:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def get_products(self) -> List[Product]:
        """Get list of all products"""
        response = requests.get(f"{self.base_url}/products")
        response.raise_for_status()
        return [Product.from_dict(item) for item in response.json()]
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get details of a specific product"""
        response = requests.get(f"{self.base_url}/products/{product_id}")
        response.raise_for_status()
        return Product.from_dict(response.json()) 