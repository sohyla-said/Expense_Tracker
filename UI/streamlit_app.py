import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_URL = "http://127.0.0.1:5000/api"


def get_available_categories():
    categories = set(st.session_state.get("custom_categories", []))

    try:
        res = requests.get(f"{API_URL}/categories", timeout=5)
        if res.ok:
            payload = res.json()
            for item in payload.get("categories", []):
                category = item.get("name")
                if category:
                    categories.add(category)
    except requests.RequestException:
        # Keep UI usable even when API is temporarily unavailable.
        pass

    if not categories:
        categories = {"Food", "Transport", "Bills"}

    return sorted(categories)


def get_budget_for_month(month):
    try:
        res = requests.get(f"{API_URL}/budget/month", params={"month": month}, timeout=5)
        if res.ok:
            return res.json()
        return {"error": res.json().get("error", res.text)}
    except requests.RequestException as exc:
        return {"error": str(exc)}


def check_budget_for_month(month):
    try:
        res = requests.get(f"{API_URL}/budget/check", params={"month": month}, timeout=5)
        if res.ok:
            return res.json()
        return {"error": res.json().get("error", res.text)}
    except requests.RequestException as exc:
        return {"error": str(exc)}


if "custom_categories" not in st.session_state:
    st.session_state.custom_categories = []

if "pending_category_select" not in st.session_state:
    st.session_state.pending_category_select = None

if "edit_expense_id" not in st.session_state:
    st.session_state.edit_expense_id = None

if "edit_field" not in st.session_state:
    st.session_state.edit_field = "description"

if "edit_value" not in st.session_state:
    st.session_state.edit_value = ""

if "cached_month" not in st.session_state:
    st.session_state.cached_month = None

if "cached_expenses" not in st.session_state:
    st.session_state.cached_expenses = None

st.title("💰 Expense Tracker")

menu = st.sidebar.selectbox("Menu", [
    "Add Expense",
    "View Current Month Expenses",
    "View Expenses by Month",
    "Filter by Category",
    "Check Budget",
    "Set Budget"
])

# ➕ Add Expense
if menu == "Add Expense":
    current_month = datetime.now().month
    current_budget = get_budget_for_month(current_month)

    st.subheader("Current Month Budget")
    if "error" in current_budget:
        st.info(current_budget["error"])
    else:
        st.write(f"Month Budget: {current_budget.get('amount', 0)}")

    desc = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)
    categories = get_available_categories()

    if st.session_state.pending_category_select in categories:
        st.session_state.category_select = st.session_state.pending_category_select
        st.session_state.pending_category_select = None

    if "category_select" not in st.session_state or st.session_state.category_select not in categories:
        st.session_state.category_select = categories[0]

    category = st.selectbox("Category", options=categories, key="category_select")
    new_category = st.text_input("Add new category")

    if st.button("Add Category"):
        new_category = new_category.strip()
        if not new_category:
            st.warning("Please enter a category name.")
        elif new_category in categories:
            st.info("Category already exists.")
        else:
            try:
                res = requests.post(
                    f"{API_URL}/categories/add",
                    json={"name": new_category},
                    timeout=5
                )
                if res.ok:
                    if new_category not in st.session_state.custom_categories:
                        st.session_state.custom_categories.append(new_category)
                    st.session_state.pending_category_select = new_category
                    st.success("Category added.")
                    st.rerun()
                else:
                    st.error(f"Failed to add category: {res.text}")
            except requests.RequestException as exc:
                st.error(f"Failed to add category: {exc}")

    if st.button("Add Expense"):
        res = requests.post(f"{API_URL}/expenses/add", json={
            "description": desc,
            "amount": amount,
            "category": category
        })
        if res.ok:
            st.success("Expense added!")
            budget_status = check_budget_for_month(datetime.now().month)
            st.subheader("Budget Check")
            if "error" in budget_status:
                st.info(budget_status["error"])
            else:
                st.write(f"Month: {budget_status.get('month', '-')}")
                st.write(f"Budget: {budget_status.get('budget', 0)}")
                st.write(f"Spent: {budget_status.get('spent', 0)}")
                st.write(f"Status: {budget_status.get('status', '-')}")
        else:
            st.error(f"Failed to add expense: {res.text}")

# 📊 View Current Month Expenses
elif menu == "View Current Month Expenses":
    current_month = datetime.now().month
    current_budget = get_budget_for_month(current_month)

    st.subheader("Current Month Budget")
    if "error" in current_budget:
        st.info(current_budget["error"])
    else:
        st.write(f"Budget: {current_budget.get('amount', 0)}")

    current_budget_status = check_budget_for_month(current_month)
    st.subheader("Budget Check")
    if "error" in current_budget_status:
        st.info(current_budget_status["error"])
    else:
        st.write(f"Spent: {current_budget_status.get('spent', 0)}")
        st.write(f"Status: {current_budget_status.get('status', '-')}")

    res = requests.get(f"{API_URL}/expenses")
    if res.ok:
        payload = res.json()

        st.subheader("Current Month Summary")
        st.write(f"Total: {payload.get('total', 0)}")

        expenses = payload.get("expenses", [])
        if expenses:
            st.subheader("Expenses")
            for expense in expenses:
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 1, 1, 1])
                with col1:
                    st.write(f"**{expense.get('description', 'N/A')}**")
                with col2:
                    st.write(f"${expense.get('amount', 0)}")
                with col3:
                    st.write(expense.get('category', 'N/A'))
                with col4:
                    st.write(expense.get('date', 'N/A'))
                with col5:
                    if st.button("Edit", key=f"edit_current_{expense.get('id')}"):
                        st.session_state.edit_expense_id = expense.get('id')
                        st.session_state.edit_field = "description"
                        st.session_state.edit_value = expense.get('description', '')
                        st.rerun()
                with col6:
                    if st.button("Delete", key=f"delete_current_{expense.get('id')}"):
                        delete_res = requests.delete(f"{API_URL}/expenses/delete/{expense.get('id')}")
                        if delete_res.ok:
                            st.success(f"Expense deleted!")
                            st.rerun()
                        else:
                            st.error(f"Failed to delete expense: {delete_res.text}")

            if st.button("Export Current Month as CSV"):
                export_res = requests.get(f"{API_URL}/expenses/export")
                if export_res.ok:
                    st.success(f"Expenses exported: {export_res.json().get('file', 'Data/expenses.csv')}")
                else:
                    st.error(f"Failed to export: {export_res.text}")

            if st.session_state.edit_expense_id:
                st.divider()
                st.subheader(f"Edit Expense #{st.session_state.edit_expense_id}")
                edit_field = st.selectbox(
                    "Field to edit",
                    options=["description", "amount", "category"],
                    key="edit_field_select"
                )
                
                if st.session_state.edit_field != edit_field:
                    st.session_state.edit_field = edit_field
                    st.session_state.edit_value = ""

                if edit_field == "description":
                    new_value = st.text_input("New description", value=st.session_state.edit_value)
                    st.session_state.edit_value = new_value
                elif edit_field == "amount":
                    new_value = st.number_input("New amount", value=float(st.session_state.edit_value) if st.session_state.edit_value and st.session_state.edit_value != "" else 0.0)
                    st.session_state.edit_value = str(new_value)
                else:
                    categories = get_available_categories()
                    new_value = st.selectbox("New category", options=categories, key="edit_category_select")
                    st.session_state.edit_value = new_value

                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("Save Changes", key="save_edit_expense"):
                        edit_data = {edit_field: st.session_state.edit_value}
                        edit_res = requests.put(
                            f"{API_URL}/expenses/update/{st.session_state.edit_expense_id}",
                            json=edit_data
                        )
                        if edit_res.ok:
                            st.success("Expense updated successfully!")
                            st.session_state.edit_expense_id = None
                            st.rerun()
                        else:
                            st.error(f"Failed to update expense: {edit_res.text}")
                with col_cancel:
                    if st.button("Cancel", key="cancel_edit_expense"):
                        st.session_state.edit_expense_id = None
                        st.rerun()
        else:
            st.info("No expenses found for the current month.")
    else:
        st.error(f"Failed to fetch current month expenses: {res.text}")

# 📋 View Expenses by Month
elif menu == "View Expenses by Month":
    month = st.number_input("Month", min_value=1, max_value=12, step=1)

    if st.button("View Month Expenses"):
        st.session_state.cached_month = int(month)
        month_budget = get_budget_for_month(int(month))
        res = requests.get(f"{API_URL}/expenses/month", params={"month": int(month)})
        if res.ok:
            st.session_state.cached_expenses = res.json()
        else:
            st.error(f"Failed to fetch expenses: {res.text}")

    if st.session_state.cached_month is not None and st.session_state.cached_expenses is not None:
        month = st.session_state.cached_month
        payload = st.session_state.cached_expenses
        month_budget = get_budget_for_month(int(month))

        st.subheader("Month Budget")
        if "error" in month_budget:
            st.info(month_budget["error"])
        else:
            st.write(f"Budget: {month_budget.get('amount', 0)}")

        month_budget_status = check_budget_for_month(int(month))
        st.subheader("Budget Check")
        if "error" in month_budget_status:
            st.info(month_budget_status["error"])
        else:
            st.write(f"Spent: {month_budget_status.get('spent', 0)}")
            st.write(f"Status: {month_budget_status.get('status', '-')}")

        st.subheader("Month Summary")
        st.write(f"Total: {payload.get('total', 0)}")

        expenses = payload.get("expenses", [])
        if expenses:
            st.subheader("Expenses")
            for expense in expenses:
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 1, 1, 1])
                with col1:
                    st.write(f"**{expense.get('description', 'N/A')}**")
                with col2:
                    st.write(f"${expense.get('amount', 0)}")
                with col3:
                    st.write(expense.get('category', 'N/A'))
                with col4:
                    st.write(expense.get('date', 'N/A'))
                with col5:
                    if st.button("Edit", key=f"edit_month_{expense.get('id')}_{month}"):
                        st.session_state.edit_expense_id = expense.get('id')
                        st.session_state.edit_field = "description"
                        st.session_state.edit_value = expense.get('description', '')
                        st.rerun()
                with col6:
                    if st.button("Delete", key=f"delete_month_{expense.get('id')}_{month}"):
                        delete_res = requests.delete(f"{API_URL}/expenses/delete/{expense.get('id')}")
                        if delete_res.ok:
                            st.success(f"Expense deleted!")
                            st.session_state.cached_expenses = None
                            st.rerun()
                        else:
                            st.error(f"Failed to delete expense: {delete_res.text}")

            if st.button("Export Month as CSV", key=f"export_month_{month}"):
                export_res = requests.get(f"{API_URL}/expenses/month/export", params={"month": int(month)})
                if export_res.ok:
                    st.success(f"Expenses exported: {export_res.json().get('file', f'Data/expenses_month_{month}.csv')}")
                else:
                    st.error(f"Failed to export: {export_res.text}")

            if st.session_state.edit_expense_id:
                st.divider()
                st.subheader(f"Edit Expense #{st.session_state.edit_expense_id}")
                edit_field = st.selectbox(
                    "Field to edit",
                    options=["description", "amount", "category"],
                    key="edit_field_select_month"
                )
                
                if st.session_state.edit_field != edit_field:
                    st.session_state.edit_field = edit_field
                    st.session_state.edit_value = ""

                if edit_field == "description":
                    new_value = st.text_input("New description", value=st.session_state.edit_value, key="edit_desc_month")
                    st.session_state.edit_value = new_value
                elif edit_field == "amount":
                    new_value = st.number_input("New amount", value=float(st.session_state.edit_value) if st.session_state.edit_value and st.session_state.edit_value != "" else 0.0, key="edit_amount_month")
                    st.session_state.edit_value = str(new_value)
                else:
                    categories = get_available_categories()
                    new_value = st.selectbox("New category", options=categories, key="edit_category_select_month")
                    st.session_state.edit_value = new_value

                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("Save Changes", key="save_edit_expense_month"):
                        edit_data = {edit_field: st.session_state.edit_value}
                        edit_res = requests.put(
                            f"{API_URL}/expenses/update/{st.session_state.edit_expense_id}",
                            json=edit_data
                        )
                        if edit_res.ok:
                            st.success("Expense updated successfully!")
                            st.session_state.edit_expense_id = None
                            st.session_state.cached_expenses = None
                            st.rerun()
                        else:
                            st.error(f"Failed to update expense: {edit_res.text}")
                with col_cancel:
                    if st.button("Cancel", key="cancel_edit_expense_month"):
                        st.session_state.edit_expense_id = None
                        st.rerun()
        else:
            st.info("No expenses found for the selected month.")

# 🏷️ Filter by Category
elif menu == "Filter by Category":
    st.subheader("Available Categories")
    try:
        categories_res = requests.get(f"{API_URL}/categories", timeout=5)
        if categories_res.ok:
            categories_payload = categories_res.json()
            categories = [item.get("name") for item in categories_payload.get("categories", []) if item.get("name")]

            if categories:
                st.table(pd.DataFrame({"Category": sorted(categories)}))
                selected_category = st.selectbox("Select a category", options=sorted(categories))

                if st.button("Filter Expenses"):
                    expenses_res = requests.get(f"{API_URL}/expenses/category", params={"category": selected_category}, timeout=5)
                    if expenses_res.ok:
                        payload = expenses_res.json()
                        st.subheader(f"Expenses for {selected_category}")
                        st.write(f"Total: {payload.get('total', 0)}")

                        expenses = payload.get("expenses", [])
                        if expenses:
                            st.table(pd.DataFrame(expenses))
                        else:
                            st.info("No expenses found for the selected category.")
                    else:
                        st.error(f"Failed to filter expenses: {expenses_res.text}")
            else:
                st.info("No categories available yet.")
        else:
            st.error(f"Failed to load categories: {categories_res.text}")
    except requests.RequestException as exc:
        st.error(f"Failed to load categories: {exc}")

# ✅ Check Budget
elif menu == "Check Budget":
    month = st.number_input("Month", min_value=1, max_value=12, step=1)

    if st.button("Check Month Budget"): 
        budget_status = check_budget_for_month(int(month))
        if "error" in budget_status:
            st.error(budget_status["error"])
        else:
            st.subheader("Budget Status")
            st.write(f"Budget: {budget_status.get('budget', 0)}")
            st.write(f"Spent: {budget_status.get('spent', 0)}")
            st.write(f"Status: {budget_status.get('status', '-')}")

# 💸 Budget
elif menu == "Set Budget":
    month = st.number_input("Month", min_value=1, max_value=12)
    budget = st.number_input("Budget", min_value=0.0)

    if st.button("Set Budget"):
        requests.post(f"{API_URL}/budget", json={
            "month": month,
            "amount": budget
        })
        st.success("Budget saved!")