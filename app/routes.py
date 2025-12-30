from flask import Blueprint, request
from decimal import Decimal
from app import db
from app.models import (
    Product, Inventory, Supplier, ProductSupplier,
    Warehouse, ReorderRequest, User
)
from app.utils import get_avg_daily_sales, get_threshold
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError

api = Blueprint("api", __name__, url_prefix="/api")

# ---------------- AUTH ----------------
@api.route("/auth/login", methods=["POST"])
def login():
    user = User.query.filter_by(email=request.json["email"]).first()
    if not user:
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=user.id)
    return {"access_token": token}

# ---------------- PRODUCTS ----------------
@api.route("/products", methods=["POST"])
@jwt_required()
def create_product():
    data = request.json

    product = Product(
        name=data["name"],
        sku=data["sku"],
        price=Decimal(data["price"]),
        product_type=data.get("product_type")
    )

    try:
        db.session.add(product)
        db.session.flush()

        if "warehouse_id" in data:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data["warehouse_id"],
                quantity=data.get("initial_quantity", 0)
            )
            db.session.add(inventory)

        db.session.commit()
        return {"message": "Product created", "id": product.id}, 201

    except IntegrityError:
        db.session.rollback()
        return {"error": "SKU must be unique"}, 409

# ---------------- LOW STOCK ALERTS ----------------
@api.route("/companies/<int:company_id>/alerts/low-stock")
@jwt_required()
def low_stock_alerts(company_id):
    alerts = []

    inventories = db.session.query(
        Inventory, Product, Warehouse, Supplier
    ).join(Product)\
     .join(Warehouse)\
     .join(ProductSupplier, Product.id == ProductSupplier.product_id)\
     .join(Supplier, Supplier.id == ProductSupplier.supplier_id)\
     .filter(Warehouse.company_id == company_id).all()

    for inv, product, warehouse, supplier in inventories:
        avg_sales = get_avg_daily_sales(product.id, warehouse.id)
        if avg_sales == 0:
            continue

        threshold = get_threshold(product.product_type)

        if inv.quantity < threshold:
            alerts.append({
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_name": warehouse.name,
                "current_stock": inv.quantity,
                "threshold": threshold,
                "days_until_stockout": int(inv.quantity / avg_sales),
                "supplier": {
                    "id": supplier.id,
                    "name": supplier.name,
                    "email": supplier.contact_email
                }
            })

    return {"alerts": alerts, "total_alerts": len(alerts)}

# ---------------- REORDER ----------------
@api.route("/reorders", methods=["POST"])
@jwt_required()
def create_reorder():
    data = request.json

    reorder = ReorderRequest(
        product_id=data["product_id"],
        supplier_id=data["supplier_id"],
        warehouse_id=data["warehouse_id"],
        quantity=data["quantity"]
    )

    db.session.add(reorder)
    db.session.commit()
    return {"message": "Reorder placed"}, 201
