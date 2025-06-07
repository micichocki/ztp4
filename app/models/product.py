from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Product:
    id: int
    name: str
    price: float
    description: str
    quantity: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            price=float(data.get('price', 0.0)),
            description=data.get('description', ''),
            quantity=int(data.get('quantity', 0)),
            created_at=datetime.fromisoformat(data.get('created_at')) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data.get('updated_at')) if data.get('updated_at') else None
        )
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 