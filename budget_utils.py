from sqlalchemy.orm import Session
from models import Budget, Expense
from sqlalchemy import func,cast,String

def set_budget(db: Session, user_id: int, category: str, month: str, amount: float):
    budget = db.query(Budget).filter_by(user_id=user_id, category=category, month=month).first()
    if budget:
        budget.amount = amount
    else:
        budget = Budget(user_id=user_id, category=category, month=month, amount=amount)
        db.add(budget)
    db.commit()

def get_total_spent(db: Session, user_id: int, category: str, month: str):
    total = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        Expense.category == category,
         cast(Expense.date, String).like(f"{month}-%")
    ).scalar()
    return total or 0
