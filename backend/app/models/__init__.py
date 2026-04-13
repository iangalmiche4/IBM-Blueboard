"""
Models package - Import all models here for easy access
"""

from app.models.customer import Customer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.promotion import Promotion
from app.models.return_model import Return
from app.models.sale import Sale
from app.models.satisfaction import Satisfaction

__all__ = [
    "Product",
    "Customer",
    "Sale",
    "Satisfaction",
    "Inventory",
    "Return",
    "Promotion",
]
