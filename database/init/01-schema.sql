-- IBM Blueboard Database Schema
-- PostgreSQL 18+
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (for development)
DROP TABLE IF EXISTS promotions CASCADE;

DROP TABLE IF EXISTS
    RETURNS CASCADE;

DROP TABLE IF EXISTS inventory CASCADE;

DROP TABLE IF EXISTS satisfaction CASCADE;

DROP TABLE IF EXISTS sales CASCADE;

DROP TABLE IF EXISTS customers CASCADE;

DROP TABLE IF EXISTS products CASCADE;

-- Products table
CREATE TABLE products (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
    name varchar(200) NOT NULL,
    category varchar(100) NOT NULL,
    brand varchar(100) NOT NULL,
    price numeric(10, 2) NOT NULL CHECK (price >= 0),
    sku varchar(50) UNIQUE NOT NULL,
    description text,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for products
CREATE INDEX idx_products_category ON products (category);

CREATE INDEX idx_products_brand ON products (brand);

CREATE INDEX idx_products_sku ON products (sku);

-- Customers table
CREATE TABLE customers (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
    email varchar(255) UNIQUE NOT NULL,
    first_name varchar(100) NOT NULL,
    last_name varchar(100) NOT NULL,
    birth_date date,
    gender varchar(20),
    segment varchar(50) NOT NULL,
    region varchar(100) NOT NULL,
    registration_date date NOT NULL,
    is_active boolean DEFAULT TRUE,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for customers
CREATE INDEX idx_customers_email ON customers (email);

CREATE INDEX idx_customers_segment ON customers (segment);

CREATE INDEX idx_customers_region ON customers (region);

-- Sales table
CREATE TABLE sales (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
    product_id uuid NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    customer_id uuid NOT NULL REFERENCES customers (id) ON DELETE CASCADE,
    quantity integer NOT NULL CHECK (quantity > 0),
    unit_price numeric(10, 2) NOT NULL CHECK (unit_price >= 0),
    total_amount numeric(10, 2) NOT NULL CHECK (total_amount >= 0),
    discount_amount numeric(10, 2) DEFAULT 0 CHECK (discount_amount >= 0),
    sale_date date NOT NULL,
    region varchar(100) NOT NULL,
    channel varchar(50) NOT NULL,
    payment_method varchar(50) NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for sales
CREATE INDEX idx_sales_product_id ON sales (product_id);

CREATE INDEX idx_sales_customer_id ON sales (customer_id);

CREATE INDEX idx_sales_sale_date ON sales (sale_date);

CREATE INDEX idx_sales_region ON sales (region);

CREATE INDEX idx_sales_channel ON sales (channel);

-- Satisfaction (Reviews) table
CREATE TABLE satisfaction (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
    product_id uuid NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    customer_id uuid NOT NULL REFERENCES customers (id) ON DELETE CASCADE,
    overall_rating integer NOT NULL CHECK (overall_rating BETWEEN 1 AND 5),
    quality_rating integer NOT NULL CHECK (quality_rating BETWEEN 1 AND 5),
    price_rating integer NOT NULL CHECK (price_rating BETWEEN 1 AND 5),
    packaging_rating integer NOT NULL CHECK (packaging_rating BETWEEN 1 AND 5),
    delivery_rating integer NOT NULL CHECK (delivery_rating BETWEEN 1 AND 5),
    comment text,
    review_date date NOT NULL,
    verified_purchase boolean DEFAULT FALSE,
    helpful_count integer DEFAULT 0,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for satisfaction
CREATE INDEX idx_satisfaction_product_id ON satisfaction (product_id);

CREATE INDEX idx_satisfaction_customer_id ON satisfaction (customer_id);

CREATE INDEX idx_satisfaction_review_date ON satisfaction (review_date);

CREATE INDEX idx_satisfaction_overall_rating ON satisfaction (overall_rating);

-- Inventory table
CREATE TABLE inventory (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
    product_id uuid UNIQUE NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    stock_quantity integer NOT NULL CHECK (stock_quantity >= 0),
    reserved_quantity integer DEFAULT 0 CHECK (reserved_quantity >= 0),
    warehouse_location varchar(100) NOT NULL,
    last_restock_date date,
    reorder_level integer NOT NULL CHECK (reorder_level >= 0),
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for inventory
CREATE INDEX idx_inventory_product_id ON inventory (product_id);

CREATE INDEX idx_inventory_warehouse_location ON inventory (warehouse_location);

-- Returns table
CREATE TABLE
    RETURNS (
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
        product_id uuid NOT NULL REFERENCES products (id) ON DELETE CASCADE,
        customer_id uuid NOT NULL REFERENCES customers (id) ON DELETE CASCADE,
        sale_id uuid NOT NULL REFERENCES sales (id) ON DELETE CASCADE,
        quantity integer NOT NULL CHECK (quantity > 0),
        reason varchar(200) NOT NULL,
        status varchar(50) NOT NULL,
        return_date date NOT NULL,
        refund_amount numeric(10, 2) NOT NULL CHECK (refund_amount >= 0),
        notes text,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for returns
CREATE INDEX idx_returns_product_id ON
    RETURNS (product_id);

CREATE INDEX idx_returns_customer_id ON
    RETURNS (customer_id);

CREATE INDEX idx_returns_sale_id ON
    RETURNS (sale_id);

CREATE INDEX idx_returns_status ON
    RETURNS (status);

CREATE INDEX idx_returns_return_date ON
    RETURNS (return_date);

-- Promotions table
CREATE TABLE promotions (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
    sale_id uuid NOT NULL REFERENCES sales (id) ON DELETE CASCADE,
    promo_code varchar(50),
    promo_type varchar(50) NOT NULL,
    discount_percentage numeric(5, 2) CHECK (discount_percentage BETWEEN 0 AND 100),
    start_date date NOT NULL,
    end_date date NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date >= start_date)
);

-- Create indexes for promotions
CREATE INDEX idx_promotions_sale_id ON promotions (sale_id);

CREATE INDEX idx_promotions_promo_type ON promotions (promo_type);

CREATE INDEX idx_promotions_dates ON promotions (start_date, end_date);

-- Create views for common queries
-- View: Product performance
CREATE OR REPLACE VIEW product_performance AS
SELECT
    p.id,
    p.name,
    p.category,
    p.brand,
    p.price,
    COUNT(DISTINCT s.id) AS total_sales,
    SUM(s.quantity) AS units_sold,
    SUM(s.total_amount) AS total_revenue,
    AVG(sat.overall_rating) AS avg_rating,
    COUNT(DISTINCT sat.id) AS review_count
FROM
    products p
    LEFT JOIN sales s ON p.id = s.product_id
    LEFT JOIN satisfaction sat ON p.id = sat.product_id
GROUP BY
    p.id,
    p.name,
    p.category,
    p.brand,
    p.price;

-- View: Customer lifetime value
CREATE OR REPLACE VIEW customer_lifetime_value AS
SELECT
    c.id,
    c.email,
    c.first_name,
    c.last_name,
    c.segment,
    c.region,
    COUNT(DISTINCT s.id) AS total_orders,
    SUM(s.total_amount) AS lifetime_value,
    AVG(s.total_amount) AS avg_order_value,
    MAX(s.sale_date) AS last_purchase_date
FROM
    customers c
    LEFT JOIN sales s ON c.id = s.customer_id
GROUP BY
    c.id,
    c.email,
    c.first_name,
    c.last_name,
    c.segment,
    c.region;

-- View: Monthly sales summary
CREATE OR REPLACE VIEW monthly_sales_summary AS
SELECT
    DATE_TRUNC('month', sale_date) AS month,
    COUNT(DISTINCT id) AS total_orders,
    SUM(quantity) AS total_units,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM
    sales
GROUP BY
    DATE_TRUNC('month', sale_date)
ORDER BY
    month DESC;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO blueboard;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO blueboard;
-- Success message
DO $$
BEGIN
    RAISE NOTICE 'IBM Blueboard database schema created successfully!';
    RAISE NOTICE 'Tables: products, customers, sales, satisfaction, inventory, returns, promotions';
    RAISE NOTICE 'Views: product_performance, customer_lifetime_value, monthly_sales_summary';
END
$$;

