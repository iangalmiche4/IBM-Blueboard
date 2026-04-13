"""
Generate fake data for IBM Blueboard database using Faker
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from faker import Faker
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale
from app.models.satisfaction import Satisfaction
from app.models.inventory import Inventory
from app.models.return_model import Return
from app.models.promotion import Promotion

# Initialize Faker with French locale
fake = Faker(['fr_FR', 'en_US'])

# Cosmetics categories and products
CATEGORIES = {
    "Skincare": ["Moisturizer", "Cleanser", "Serum", "Toner", "Eye Cream", "Face Mask", "Sunscreen"],
    "Makeup": ["Foundation", "Lipstick", "Mascara", "Eyeshadow", "Blush", "Concealer", "Eyeliner"],
    "Haircare": ["Shampoo", "Conditioner", "Hair Mask", "Hair Oil", "Styling Gel", "Hair Spray"],
    "Fragrance": ["Eau de Parfum", "Eau de Toilette", "Body Mist", "Perfume Oil"],
    "Body Care": ["Body Lotion", "Body Wash", "Body Scrub", "Hand Cream", "Foot Cream"]
}

BRANDS = ["L'Oréal", "Lancôme", "Maybelline", "Garnier", "NYX", "Essie", "Kiehl's", "Urban Decay", 
          "Biotherm", "Yves Saint Laurent", "Giorgio Armani", "Vichy", "La Roche-Posay"]

REGIONS = ["Île-de-France", "Auvergne-Rhône-Alpes", "Provence-Alpes-Côte d'Azur", 
           "Nouvelle-Aquitaine", "Occitanie", "Hauts-de-France", "Grand Est", "Bretagne"]

CUSTOMER_SEGMENTS = ["Premium", "Regular", "Occasional"]


def clear_database(db: Session):
    """Clear all data from database tables"""
    print("Clearing existing data...")
    db.query(Return).delete()
    db.query(Satisfaction).delete()
    db.query(Sale).delete()
    db.query(Promotion).delete()
    db.query(Inventory).delete()
    db.query(Product).delete()
    db.query(Customer).delete()
    db.commit()
    print("Database cleared")


def generate_products(db: Session, count: int = 100):
    """Generate fake products"""
    print(f"Generating {count} products...")
    products = []
    
    for _ in range(count):
        category = random.choice(list(CATEGORIES.keys()))
        product_type = random.choice(CATEGORIES[category])
        brand = random.choice(BRANDS)
        
        product = Product(
            name=f"{brand} {product_type}",
            category=category,
            brand=brand,
            price=round(random.uniform(9.99, 149.99), 2),
            description=fake.text(max_nb_chars=200),
            sku=fake.unique.bothify(text='??-####-???').upper(),
            created_at=fake.date_time_between(start_date='-2y', end_date='now')
        )
        products.append(product)
    
    db.bulk_save_objects(products)
    db.commit()
    print(f"Created {count} products")
    return db.query(Product).all()


def generate_customers(db: Session, count: int = 500):
    """Generate fake customers"""
    print(f"Generating {count} customers...")
    customers = []
    
    for _ in range(count):
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        registration_date = fake.date_between(start_date='-3y', end_date='today')
        
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            birth_date=birth_date,
            gender=random.choice(["Male", "Female", "Other"]),
            region=random.choice(REGIONS),
            segment=random.choice(CUSTOMER_SEGMENTS),
            registration_date=registration_date,
            is_active=random.choice([True, True, True, True, False])  # 80% active
        )
        customers.append(customer)
    
    db.bulk_save_objects(customers)
    db.commit()
    print(f"Created {count} customers")
    return db.query(Customer).all()


def generate_inventory(db: Session, products: list):
    """Generate inventory for products"""
    print(f"Generating inventory for {len(products)} products...")
    inventory_items = []
    
    for product in products:
        stock_qty = random.randint(0, 500)
        inventory = Inventory(
            product_id=product.id,
            stock_quantity=stock_qty,
            reserved_quantity=random.randint(0, min(50, stock_qty)),
            warehouse_location=f"W{random.randint(1, 5)}-R{random.randint(1, 20)}-S{random.randint(1, 10)}",
            last_restock_date=fake.date_between(start_date='-6m', end_date='today'),
            reorder_level=random.randint(10, 50)
        )
        inventory_items.append(inventory)
    
    db.bulk_save_objects(inventory_items)
    db.commit()
    print(f"Created {len(products)} inventory records")


def generate_promotions(db: Session, sales: list, count: int = 30):
    """Generate promotions linked to sales"""
    print(f"Generating {count} promotions...")
    promotions = []
    
    # Select random sales for promotions
    promo_sales = random.sample(sales, min(count, len(sales)))
    
    for sale in promo_sales:
        start_date = sale.sale_date - timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(7, 90))
        
        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()
        
        promotion = Promotion(
            sale_id=sale.id,
            promo_code=fake.bothify(text='PROMO-####').upper(),
            promo_type=random.choice(["Seasonal", "Flash Sale", "Loyalty", "New Customer", "Clearance"]),
            discount_percentage=round((sale.discount_amount / (sale.total_amount + sale.discount_amount)) * 100, 2) if sale.discount_amount > 0 else random.choice([10, 15, 20, 25, 30]),
            start_date=start_date,
            end_date=end_date
        )
        promotions.append(promotion)
    
    db.bulk_save_objects(promotions)
    db.commit()
    print(f"Created {len(promotions)} promotions")
    return db.query(Promotion).all()


def generate_sales(db: Session, customers: list, products: list, count: int = 2500):
    """Generate sales transactions"""
    print(f"Generating {count} sales...")
    sales = []
    
    for _ in range(count):
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = float(product.price)
        
        # Apply random discount for some sales
        discount_amount = round(unit_price * quantity * random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20]) if random.random() > 0.7 else 0, 2)
        
        sale = Sale(
            customer_id=customer.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            discount_amount=discount_amount,
            total_amount=round(quantity * unit_price - discount_amount, 2),
            sale_date=fake.date_time_between(start_date='-1y', end_date='now'),
            payment_method=random.choice(["Credit Card", "Debit Card", "PayPal", "Cash"]),
            channel=random.choice(["Online", "Store", "Mobile App", "Phone"]),
            region=customer.region
        )
        sales.append(sale)
    
    db.bulk_save_objects(sales)
    db.commit()
    print(f"Created {count} sales")
    return db.query(Sale).all()


def generate_satisfaction(db: Session, customers: list, products: list, count: int = 1200):
    """Generate customer satisfaction reviews"""
    print(f"Generating {count} satisfaction reviews...")
    reviews = []
    
    for _ in range(count):
        overall_rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[5, 10, 20, 35, 30]  # Skewed towards positive reviews
        )[0]
        
        satisfaction = Satisfaction(
            customer_id=random.choice(customers).id,
            product_id=random.choice(products).id,
            overall_rating=overall_rating,
            quality_rating=min(5, max(1, overall_rating + random.randint(-1, 1))),
            price_rating=min(5, max(1, overall_rating + random.randint(-1, 1))),
            packaging_rating=min(5, max(1, overall_rating + random.randint(-1, 1))),
            delivery_rating=min(5, max(1, overall_rating + random.randint(-1, 1))),
            comment=fake.text(max_nb_chars=300) if random.random() > 0.3 else None,
            review_date=fake.date_time_between(start_date='-1y', end_date='now'),
            verified_purchase=random.choice([True, True, True, False]),  # 75% verified
            helpful_count=random.randint(0, 50)
        )
        reviews.append(satisfaction)
    
    db.bulk_save_objects(reviews)
    db.commit()
    print(f"Created {count} satisfaction reviews")


def generate_returns(db: Session, sales: list, count: int = 150):
    """Generate product returns"""
    print(f" Generating {count} returns...")
    returns = []
    
    # Select random sales for returns
    return_sales = random.sample(sales, min(count, len(sales)))
    
    for sale in return_sales:
        return_date = sale.sale_date + timedelta(days=random.randint(1, 30))
        if isinstance(return_date, datetime):
            return_date = return_date.date()
        
        return_obj = Return(
            product_id=sale.product_id,
            customer_id=sale.customer_id,
            sale_id=sale.id,
            quantity=sale.quantity,
            return_date=return_date,
            reason=random.choice([
                "Defective product",
                "Wrong item received",
                "Not as described",
                "Changed mind",
                "Allergic reaction",
                "Better price elsewhere"
            ]),
            refund_amount=sale.total_amount,
            status=random.choice(["Approved", "Approved", "Approved", "Pending", "Rejected"])
        )
        returns.append(return_obj)
    
    db.bulk_save_objects(returns)
    db.commit()
    print(f"Created {count} returns")


def main():
    """Main function to generate all fake data"""
    print("\n" + "="*60)
    print("IBM Blueboard - Fake Data Generator")
    print("="*60 + "\n")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_database(db)
        
        # Generate data in order (respecting foreign key constraints)
        products = generate_products(db, count=100)
        customers = generate_customers(db, count=500)
        generate_inventory(db, products)
        sales = generate_sales(db, customers, products, count=2500)
        promotions = generate_promotions(db, sales, count=30)
        generate_satisfaction(db, customers, products, count=1200)
        generate_returns(db, sales, count=150)
        
        print("\n" + "="*60)
        print("Data generation completed successfully!")
        print("="*60)
        print(f"\nSummary:")
        print(f"   - Products: 100")
        print(f"   - Customers: 500")
        print(f"   - Inventory records: 100")
        print(f"   - Promotions: 30")
        print(f"   - Sales: 2,500")
        print(f"   - Satisfaction reviews: 1,200")
        print(f"   - Returns: 150")
        print("\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()