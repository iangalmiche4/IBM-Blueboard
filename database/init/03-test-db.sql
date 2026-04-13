-- Create dedicated test user and database for pytest
-- This provides complete isolation from production data and credentials
-- Create test user
CREATE USER blueboard_test WITH PASSWORD 'blueboard_password_test';

-- Create test database
CREATE DATABASE blueboard_test OWNER blueboard_test;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE blueboard_test TO blueboard_test;

