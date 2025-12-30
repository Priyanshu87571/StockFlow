from datetime import datetime, timedelta
from app.models import Sale
from app import db

def get_avg_daily_sales(product_id, warehouse_id):
    since = datetime.utcnow() - timedelta(days=30)

    sales = db.session.query(Sale).filter(
        Sale.product_id == product_id,
        Sale.warehouse_id == warehouse_id,
        Sale.sold_at >= since
    ).all()

    if not sales:
        return 0

    total = sum(s.quantity for s in sales)
    return total / 30

def get_threshold(product_type):
    thresholds = {
        "fast": 50,
        "standard": 20,
        "slow": 10
    }
    return thresholds.get(product_type, 15)
