# Expense Tracker App

## Setup

```bash
git clone <repo-url>
cd expense_tracker
pip install -r requirements.txt
uvicorn app:app --reload

change your credentials of the psql 

App usage-----
click create user to create a new user in user section by entering emailid then you can get the user id which should be used further to use the application
click add expenses in expenses section
click set budgets of your expenses criteria
click view budget report to see the budgets set here we can retrieve the budget alerts that is how much amount still we can have to spend within budget.
click view monthly report to see the expenses on categories.
