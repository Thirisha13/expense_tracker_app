def check_budget_alert(budget_amount, spent_amount):
    if spent_amount > budget_amount:
        return "Budget exceeded!"
    elif spent_amount >= 0.9 * budget_amount:
        return "Only 10 percentage budget left!"
    return "Within budget"
