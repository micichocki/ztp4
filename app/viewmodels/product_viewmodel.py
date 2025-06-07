from typing import List, Optional
from app.models.product import Product
from app.services.product_service import ProductService

class ProductViewModel:
    def __init__(self, product_service: ProductService):
        self._product_service = product_service
        self._products: List[Product] = []
        self._selected_product: Optional[Product] = None
        self._error_message: str = ""
    
    @property
    def products(self) -> List[Product]:
        return self._products
    
    @property
    def selected_product(self) -> Optional[Product]:
        return self._selected_product
    
    @property
    def error_message(self) -> str:
        return self._error_message
    
    def load_products(self) -> None:
        """Load all products from the service"""
        try:
            self._products = self._product_service.get_products()
            self._error_message = ""
        except Exception as e:
            self._error_message = f"Error loading products: {str(e)}"
            self._products = []
    
    def select_product(self, product_id: int) -> None:
        """Load and select a specific product"""
        try:
            self._selected_product = self._product_service.get_product(product_id)
            self._error_message = ""
        except Exception as e:
            self._error_message = f"Error loading product details: {str(e)}"
            self._selected_product = None 