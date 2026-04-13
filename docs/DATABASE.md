# Database Schema

## Overview

PostgreSQL 18 with 7 tables and 3 views for cosmetics analytics.

## Tables

| Table            | Description       | Key Columns                                                   |
| ---------------- | ----------------- | ------------------------------------------------------------- |
| **products**     | Product catalog   | id, name, category, brand, price, sku                         |
| **customers**    | Customer profiles | id, email, segment, region, registration_date                 |
| **sales**        | Transactions      | id, product_id, customer_id, total_amount, sale_date, channel |
| **satisfaction** | Reviews           | id, product_id, customer_id, overall_rating, review_date      |
| **inventory**    | Stock levels      | id, product_id, stock_quantity, warehouse_location            |
| **returns**      | Product returns   | id, sale_id, reason, status, refund_amount                    |
| **promotions**   | Campaigns         | id, sale_id, promo_code, discount_percentage                  |

## Views

- **product_performance** - Aggregated sales and ratings per product
- **customer_lifetime_value** - Total spend and order count per customer
- **monthly_sales_summary** - Monthly revenue and transaction metrics

## Relationships

```
customers ──┬── sales ──┬── products
            │           ├── promotions
            │           └── returns
            │
            └── satisfaction ── products

products ── inventory
```

## Data Volume

- Products: 100
- Customers: 500
- Sales: 2,500 (18 months)
- Satisfaction: 1,200
- Inventory: 100
- Returns: 150
- Promotions: 30

## Categories

**Products:** Skincare, Makeup, Haircare, Fragrance, Body Care, Tools
**Customer Segments:** VIP, Premium, Regular, Occasional, New
**Sales Channels:** Online, In-Store, Mobile App, Marketplace
**Return Reasons:** Defective, Wrong Item, Not as Described, Changed Mind, Better Price Elsewhere, Quality Issues, Damaged in Transit

## Schema Location

`database/init/01-schema.sql`
