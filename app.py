from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal, engine
from models import Base, Expense, User
from budget_utils import set_budget, get_total_spent
from report_utils import total_spending_per_month
from alerts import check_budget_alert
from models import Budget

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user/")
def create_user(email: str, db: Session = Depends(get_db)):
    user = User(email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.id}

@app.post("/expense/")
def add_expense(user_id: int, category: str, amount: float, date: str, db: Session = Depends(get_db)):
    expense = Expense(user_id=user_id, category=category, amount=amount, date=datetime.strptime(date, "%Y-%m-%d"))
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return {"msg": "Expense logged", "expense_id": expense.id}

@app.post("/budget/")
def update_budget(user_id: int, category: str, month: str, amount: float, db: Session = Depends(get_db)):
    set_budget(db, user_id, category, month, amount)
    return {"msg": "Budget set/updated"}

@app.get("/report/")
def get_report(user_id: int, month: str, db: Session = Depends(get_db)):
    return total_spending_per_month(db, user_id, month)

@app.get("/alert/")
def get_alert(user_id: int, category: str, month: str, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter_by(user_id=user_id, category=category, month=month).first()
    if not budget:
        return {"msg": "No budget set"}
    spent = get_total_spent(db, user_id, category, month)
    status = check_budget_alert(budget.amount, spent)
    return {"status": status, "spent": spent, "budget": budget.amount}
