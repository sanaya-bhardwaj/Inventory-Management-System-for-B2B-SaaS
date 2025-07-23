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
