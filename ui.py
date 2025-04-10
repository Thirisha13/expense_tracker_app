import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"
st.title("Expense Tracker")
menu = st.sidebar.radio("Choose an action", [
    "Create User",
    "Add Expense",
    "Set Budget",
    "View Monthly Report",
    "View Budget Alert"
])
if menu == "Create User":
    st.header("👤 Create New User")
    email = st.text_input("Enter Email")
    if st.button("Create"):
        r = requests.post(f"{BASE_URL}/user/", params={"email": email})
        st.success(f"User created with ID: {r.json()['user_id']}")
elif menu == "Add Expense":
    st.header("Add Expense")
    user_id = st.number_input("User ID", min_value=1)
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Others"])
    amount = st.number_input("Amount", min_value=0.0)
    date = st.date_input("Date")
    if st.button("Add"):
        r = requests.post(f"{BASE_URL}/expense/", params={
            "user_id": user_id,
            "category": category,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d")
        })
        st.success(r.json()['msg'])
elif menu == "Set Budget":
    st.header("Set Monthly Budget")
    user_id = st.number_input("User ID", min_value=1)
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Others"])
    month = st.text_input("Month (e.g., 2025-04)")
    amount = st.number_input("Budget Amount", min_value=0.0)
    if st.button("Set Budget"):
        r = requests.post(f"{BASE_URL}/budget/", params={
            "user_id": user_id,
            "category": category,
            "month": month,
            "amount": amount
        })
        st.success(r.json()['msg'])
elif menu == "View Monthly Report":
    st.header("Monthly Report")
    user_id = st.number_input("User ID", min_value=1)
    month = st.text_input("Month (e.g., 2025-04)")
    if st.button("Get Report"):
        r = requests.get(f"{BASE_URL}/report/", params={
            "user_id": user_id,
            "month": month
        })
        if r.status_code == 200:
            data = r.json()
            st.dataframe(data.items(), use_container_width=True)
        else:
            st.error(f"Request failed !!! with status code {r.status_code}")
            st.error(r.text)
        if data:
            st.subheader("Category-wise Spending")
            st.dataframe(data.items(), use_container_width=True)
        else:
            st.warning("No expenses found for this month.")

elif menu == "View Budget Alert":
    st.header("Budget Alert")
    user_id = st.number_input("User ID", min_value=1, key="alert_user_id")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Others"], key="alert_category")
    month = st.text_input("Month (e.g., 2025-04)", key="alert_month")
    if st.button("Check Alert"):
        try:
            response = requests.get(
                f"{BASE_URL}/alert/",
                params={
                    "user_id": user_id,
                    "category": category,
                    "month": month
                }
            )
            if response.status_code == 200:
                resp = response.json()
                # Safely extract fields
                status = resp.get("status")
                spent = resp.get("spent")
                budget = resp.get("budget")

                if status is not None and spent is not None and budget is not None:
                    st.success("Budget alert retrieved successfully!")
                    st.info(f"Status: {status}")
                    st.write(f"Spent: ₹{spent} / ₹{budget}")
                else:
                    st.warning(" !!! The response is missing expected keys. Full response below:")
                    st.json(resp)
            else:
                st.error(f"Request failed with status code {response.status_code}")
                st.code(response.text)
        except Exception as e:
            st.error("An error occurred while making the request.")
            st.exception(e)
        
