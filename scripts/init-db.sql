-- Initialize database for AliFrzngn Development
-- This script runs when the PostgreSQL container starts for the first time

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE ali_frzngn_dev'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ali_frzngn_dev')\gexec

-- Connect to the database
\c ali_frzngn_dev;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create initial admin user (will be handled by migrations)
-- This is just a placeholder for any initial setup