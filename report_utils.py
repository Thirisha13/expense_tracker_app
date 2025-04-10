from sqlalchemy import func,cast,String
from models import Expense

def total_spending_per_month(db, user_id: int, month: str):
    result = db.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id,
        cast(Expense.date, String).like(f"{month}-%")
    ).group_by(Expense.category).all()

    return {category: float(total) for category, total in result}
