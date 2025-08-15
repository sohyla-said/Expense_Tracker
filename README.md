# 💰 Expense Tracker CLI Application

A simple command-line **Expense Tracker** application built in Python to help manage personal finances.  
The application allows users to **add, update, delete, view, filter, summarize, and export expenses** with monthly budget tracking.

---

## 📌 Features

- **Add Expenses** with description, amount, category, and date.
- **Update Expenses** by ID (update amount or description).
- **Delete Expenses** by ID.
- **View All Expenses** in a readable format.
- **View Summary of All Expenses** (total amount spent).
- **View Monthly Summary** for the current year.
- **Filter by Category** to see only specific expenses.
- **Summary by Category** (total spent in a category).
- **Set and Check Monthly Budget** (warn if exceeded).
- **Export to CSV** for further analysis in Excel or Google Sheets.
- **Data Persistence** — stores all data in a JSON file (`expenses.txt`).

---

## 🛠️ Technologies Used

- **Python 3**
- `datetime` (for handling dates)
- `json` (for saving & loading expenses)
- `csv` (for exporting data)

---

## 📂 Project Structure

expense-tracker/
│
├── expenses.py # Contains the Expenses class and related functions
├── main.py # Interactive CLI menu for the user
├── expenses.txt # JSON file where all expenses are stored
├── expenses.csv # CSV file generated when exporting expenses
└── project_description.txt # Project documentation


---

## 🚀 How to Run

1. **Clone or Download the Project**  
   ```bash
   git clone https://github.com/your-username/expense-tracker.git
   cd expense-tracker

## Example Usage
===== Expense Tracker Menu =====
1. Add Expense
2. Update Expense
3. Delete Expense
4. View All Expenses
5. View Summary of All Expenses
6. View Summary for a Specific Month
7. Filter Expenses by Category
8. Summary of Expenses by Category
9. Check Monthly Budget
10. Export Expenses to CSV
0. Exit
