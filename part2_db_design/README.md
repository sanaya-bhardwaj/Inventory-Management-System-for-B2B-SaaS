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
