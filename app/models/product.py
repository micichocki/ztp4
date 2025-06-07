from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: int
    name: str
    price: float
    description: str
    quantity: int
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            price=float(data.get('price', 0.0)),
            description=data.get('description', ''),
            quantity=int(data.get('quantity', 0))
        ) 