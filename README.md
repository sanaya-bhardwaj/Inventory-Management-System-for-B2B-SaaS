# Inventory-Management-System-for-B2B-SaaS

# Part 1: Code Review & Debugging - Product API Fix

This module includes a corrected version of the `create_product` API endpoint initially written by a previous developer.

## ✅ Fixes Implemented

- Added input validation for required fields
- Enforced SKU uniqueness
- Used single DB transaction to avoid partial commits
- Handled decimal precision for price
- Added proper error handling and response formatting
- Improved maintainability and security

## 📄 File

- `create_product_fixed.py`: Flask route implementation for POST `/api/products`

## 🚀 Technologies

- Python
- Flask
- SQLAlchemy

# Part 2: Database Design for Inventory System

This folder contains the schema design for a multi-warehouse, multi-company inventory system with support for bundles and suppliers.

## 📦 Key Features

- Products can be stored in multiple warehouses
- Inventory tracked per product-warehouse pair
- Bundles can contain multiple products
- Supplier and sales data supported
- Inventory history logs all stock changes

## 📄 Files

- `schema.sql`: SQL DDL to create tables
- `schema_readme.md`: Design assumptions, decisions, and questions

## ❓ Questions Raised

- Should bundles be nestable?
- How should we handle inventory variants (size/color)?
- Do we soft-delete entities or archive them?

## 🧱 Technologies

- PostgreSQL syntax (can be adapted to MySQL)

# Part 3: Low-Stock Alert API

This folder includes the implementation of an API endpoint that returns low-stock alerts for products with recent sales activity across all warehouses of a company.

## ✅ Business Rules

- Thresholds vary by product type
- Only alert on products with recent sales (last 30 days)
- Product stock calculated per warehouse
- Supplier info is included for easy reordering

## 🧠 Highlights

- Handles avg. daily sales & stockout prediction
- Skips inactive products
- Includes supplier and warehouse metadata

## 📄 Files

- `app.py`: Flask route for `GET /api/companies/<id>/alerts/low-stock`
- `models.py`: Mocked data models for Products, Inventory, etc.
- `sample_response.json`: Sample output JSON

## 🧪 Tech Stack

- Python
- Flask
- SQLAlchemy
