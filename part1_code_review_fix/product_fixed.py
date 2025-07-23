from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from app import db
from models import Product, Inventory

@app.route('/api/products', methods=['POST'])
def create_product():
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 400

    data = request.get_json()

    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Validate and convert inputs
    try:
        price = Decimal(data['price'])
        initial_qty = int(data['initial_quantity'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types for price or quantity"}), 400

    # Check for duplicate SKU
    if Product.query.filter_by(sku=data['sku']).first():
        return jsonify({"error": "SKU already exists"}), 409

    try:
        # Start a single transaction
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=price
        )
        db.session.add(product)
        db.session.flush()  # Get product.id before commit

        # Add inventory record for the warehouse
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=initial_qty
        )
        db.session.add(inventory)

        db.session.commit()

        return jsonify({
            "message": "Product created",
            "product_id": product.id,
            "sku": product.sku
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
