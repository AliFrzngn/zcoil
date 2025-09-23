"""Product model."""

from sqlalchemy import Column, String, Text, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Product(Base):
    """Product model."""
    
    __tablename__ = "products"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=True)
    quantity = Column(Integer, default=0, nullable=False)
    min_quantity = Column(Integer, default=0, nullable=False)
    max_quantity = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    brand = Column(String(100), nullable=True, index=True)
    weight = Column(Float, nullable=True)
    dimensions = Column(String(100), nullable=True)  # e.g., "10x20x30"
    
    # Customer relationship (for CRM integration)
    customer_id = Column(String(100), nullable=True, index=True)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "sku": self.sku,
            "price": self.price,
            "cost": self.cost,
            "quantity": self.quantity,
            "min_quantity": self.min_quantity,
            "max_quantity": self.max_quantity,
            "is_active": self.is_active,
            "category": self.category,
            "brand": self.brand,
            "weight": self.weight,
            "dimensions": self.dimensions,
            "customer_id": self.customer_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
