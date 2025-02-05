from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.database import get_db
from app.products.models import Product
from app.sales.models import Sale
from app.utils.security import get_current_user

dashboard_router = APIRouter()

@dashboard_router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    # Total income today
    today = datetime.utcnow().date()
    total_income_today = (
        db.query(func.sum(Sale.total_price))
        .filter(func.date(Sale.created_at) == today)
        .scalar()
        or 0
    )

    # Total income this month
    current_month = datetime.utcnow().month
    total_income_month = (
        db.query(func.sum(Sale.total_price))
        .filter(func.extract("month", Sale.created_at) == current_month)
        .scalar()
        or 0
    )

    # Total products sold
    total_products_sold = db.query(func.sum(Sale.quantity)).scalar() or 0

    # Total sales (number of transactions)
    total_sales = db.query(Sale).count()

    # Net profit (assume profit = total income for simplicity here)
    net_profit = total_income_month  # Placeholder for profit calculation

    # Total products in stock
    total_products_in_stock = db.query(func.sum(Product.quantity)).scalar() or 0

    # Response
    return {
        "income_today": total_income_today,
        "income_month": total_income_month,
        "total_sales": total_sales,
        "products_sold": total_products_sold,
        "net_profit": net_profit,
        "products_in_stock": total_products_in_stock,
    }
