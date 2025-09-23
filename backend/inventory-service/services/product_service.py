"""Product service business logic."""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException, status

from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate, ProductFilter


class ProductService:
    """Product service for business logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product."""
        # Check if SKU already exists
        existing_product = self.db.query(Product).filter(Product.sku == product_data.sku).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with SKU '{product_data.sku}' already exists"
            )
        
        # Create new product
        product = Product(**product_data.dict())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def get_product(self, product_id: int) -> Product:
        """Get product by ID."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product
    
    def get_products(self, filters: ProductFilter) -> Tuple[List[Product], int]:
        """Get products with filtering and pagination."""
        query = self.db.query(Product)
        
        # Apply filters
        if filters.name:
            query = query.filter(Product.name.ilike(f"%{filters.name}%"))
        
        if filters.category:
            query = query.filter(Product.category == filters.category)
        
        if filters.brand:
            query = query.filter(Product.brand == filters.brand)
        
        if filters.is_active is not None:
            query = query.filter(Product.is_active == filters.is_active)
        
        if filters.customer_id:
            query = query.filter(Product.customer_id == filters.customer_id)
        
        if filters.min_price is not None:
            query = query.filter(Product.price >= filters.min_price)
        
        if filters.max_price is not None:
            query = query.filter(Product.price <= filters.max_price)
        
        if filters.min_quantity is not None:
            query = query.filter(Product.quantity >= filters.min_quantity)
        
        if filters.max_quantity is not None:
            query = query.filter(Product.quantity <= filters.max_quantity)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (filters.page - 1) * filters.size
        products = query.offset(offset).limit(filters.size).all()
        
        return products, total
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        """Update product."""
        product = self.get_product(product_id)
        
        # Check if SKU is being changed and if it already exists
        if product_data.sku and product_data.sku != product.sku:
            existing_product = self.db.query(Product).filter(
                and_(Product.sku == product_data.sku, Product.id != product_id)
            ).first()
            if existing_product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product with SKU '{product_data.sku}' already exists"
                )
        
        # Update fields
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def delete_product(self, product_id: int) -> bool:
        """Delete product."""
        product = self.get_product(product_id)
        self.db.delete(product)
        self.db.commit()
        return True
    
    def get_products_by_customer(self, customer_id: str) -> List[Product]:
        """Get products associated with a customer."""
        return self.db.query(Product).filter(
            and_(Product.customer_id == customer_id, Product.is_active == True)
        ).all()
    
    def update_quantity(self, product_id: int, quantity_change: int) -> Product:
        """Update product quantity."""
        product = self.get_product(product_id)
        new_quantity = product.quantity + quantity_change
        
        if new_quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient quantity in stock"
            )
        
        product.quantity = new_quantity
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def get_low_stock_products(self, threshold: Optional[int] = None) -> List[Product]:
        """Get products with low stock."""
        query = self.db.query(Product).filter(Product.is_active == True)
        
        if threshold is not None:
            query = query.filter(Product.quantity <= threshold)
        else:
            query = query.filter(Product.quantity <= Product.min_quantity)
        
        return query.all()