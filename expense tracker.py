import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT
)
""")
conn.commit()

# Functions
def add_expense():
    try:
        amount = float(input("Enter expense amount: "))
        category = input("Enter expense category (e.g., Food, Travel, etc.): ").strip()
        description = input("Enter a short description: ").strip()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                       (amount, category, description, date))
        conn.commit()
        print("Expense added successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number for the amount.")

def view_expenses():
    print("\nAll Expenses:")
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    if rows:
        print("{:<5} {:<10} {:<15} {:<20} {:<20}".format("ID", "Amount", "Category", "Description", "Date"))
        print("-" * 70)
        for row in rows:
            print("{:<5} {:<10} {:<15} {:<20} {:<20}".format(row[0], row[1], row[2], row[3], row[4]))
    else:
        print("No expenses recorded yet.")
    print()

def view_expenses_by_category():
    category = input("Enter category to filter by: ").strip()
    print(f"\nExpenses in category: {category}")
    cursor.execute("SELECT * FROM expenses WHERE category = ?", (category,))
    rows = cursor.fetchall()
    if rows:
        print("{:<5} {:<10} {:<15} {:<20} {:<20}".format("ID", "Amount", "Category", "Description", "Date"))
        print("-" * 70)
        for row in rows:
            print("{:<5} {:<10} {:<15} {:<20} {:<20}".format(row[0], row[1], row[2], row[3], row[4]))
    else:
        print(f"No expenses found for category '{category}'.")
    print()

def delete_expense():
    try:
        expense_id = int(input("Enter the ID of the expense to delete: "))
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print("Expense deleted successfully!")
        else:
            print("Expense ID not found.")
    except ValueError:
        print("Invalid input. Please enter a valid ID.")

#menu_function
def show_menu():
    print("\n--- Personal Expense Tracker ---")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Expenses by Category")
    print("4. Delete Expense")
    print("5. Exit")

# Main loop
while True:
    show_menu()
    choice = input("Enter your choice (1-5): ").strip()
    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        view_expenses_by_category()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()

