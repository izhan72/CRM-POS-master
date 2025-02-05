from pydantic import BaseModel

class DashboardSummaryResponse(BaseModel):
    income_today: float
    income_month: float
    total_sales: int
    products_sold: int
    net_profit: float
    products_in_stock: int
