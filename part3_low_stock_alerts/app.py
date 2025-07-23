from flask import Flask, jsonify
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from models import db, Product, Inventory, Warehouse, Supplier, Sales, LowStockThreshold

app = Flask(__name__)

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    try:
        warehouses = db.session.query(Warehouse).filter_by(company_id=company_id).all()
        warehouse_ids = [w.id for w in warehouses]
        warehouse_map = {w.id: w.name for w in warehouses}

        if not warehouse_ids:
            return jsonify({"alerts": [], "total_alerts": 0}), 200

        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        active_sales = (
            db.session.query(Sales.product_id)
            .filter(
                and_(
                    Sales.warehouse_id.in_(warehouse_ids),
                    Sales.sale_date >= thirty_days_ago
                )
            )
            .distinct()
            .all()
        )
        active_product_ids = [row.product_id for row in active_sales]

        alerts = []

        for pid in active_product_ids:
            product = db.session.query(Product).get(pid)
            threshold = db.session.query(LowStockThreshold.threshold).filter_by(product_type=product.type).scalar() or 10

            product_inventories = (
                db.session.query(Inventory)
                .filter(
                    Inventory.product_id == pid,
                    Inventory.warehouse_id.in_(warehouse_ids)
                )
                .all()
            )

            for inv in product_inventories:
                if inv.quantity < threshold:
                    avg_sales = (
                        db.session.query(func.sum(Sales.quantity) / 30)
                        .filter(
                            Sales.product_id == pid,
                            Sales.warehouse_id == inv.warehouse_id,
                            Sales.sale_date >= thirty_days_ago
                        )
                        .scalar() or 0
                    )

                    days_until_stockout = int(inv.quantity / avg_sales) if avg_sales > 0 else None

                    supplier = db.session.query(Supplier).get(product.supplier_id)
                    supplier_info = {
                        "id": supplier.id,
                        "name": supplier.name,
                        "contact_email": supplier.contact_email
                    } if supplier else None

                    alerts.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "sku": product.sku,
                        "warehouse_id": inv.warehouse_id,
                        "warehouse_name": warehouse_map.get(inv.warehouse_id, "Unknown"),
                        "current_stock": inv.quantity,
                        "threshold": threshold,
                        "days_until_stockout": days_until_stockout,
                        "supplier": supplier_info
                    })

        return jsonify({"alerts": alerts, "total_alerts": len(alerts)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
