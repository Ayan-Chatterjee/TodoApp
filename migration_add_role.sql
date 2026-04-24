-- Migration script to add role column to users table
-- Run this in PostgreSQL directly

ALTER TABLE users 
ADD COLUMN IF NOT EXISTS role VARCHAR(45) DEFAULT NULL;
