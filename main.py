import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv

def add_transaction():
    date = date_entry.get()
    description = description_entry.get()
    category = category_entry.get()
    type = type_entry.get()
    amount = amount_entry.get()

    if not date or not description or not category or not type or not amount:
        messagebox.showwarning("Input Error", "All fields are required")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number")
        return

    conn = sqlite3.connect('budget_tracker.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (date, description, category, type, amount) VALUES (?, ?, ?, ?, ?)',
              (date, description, category, type, amount))
    conn.commit()
    conn.close()

    date_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Transaction added successfully")
    update_summary()
    view_transactions()

def update_summary():
    conn = sqlite3.connect('budget_tracker.db')
    c = conn.cursor()
    c.execute('SELECT SUM(amount) FROM transactions WHERE type="Income"')
    total_income = c.fetchone()[0] or 0
    c.execute('SELECT SUM(amount) FROM transactions WHERE type="Expense"')
    total_expense = c.fetchone()[0] or 0
    conn.close()

    net_balance = total_income - total_expense

    income_label.config(text=f"Total Income: ${total_income:.2f}")
    expense_label.config(text=f"Total Expense: ${total_expense:.2f}")
    balance_label.config(text=f"Net Balance: ${net_balance:.2f}")

def view_transactions():
    for row in transactions_tree.get_children():
        transactions_tree.delete(row)

    conn = sqlite3.connect('budget_tracker.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()

    for transaction in transactions:
        transactions_tree.insert("", tk.END, values=transaction)

def export_to_csv():
    conn = sqlite3.connect('budget_tracker.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()

    with open('transactions.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Date', 'Description', 'Category', 'Type', 'Amount'])
        writer.writerows(transactions)

    messagebox.showinfo("Success", "Transactions exported to transactions.csv")

# Create the main application window
root = tk.Tk()
root.title("Personal Budget Tracker")

# Create and place widgets
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

form_frame = tk.LabelFrame(main_frame, text="Add Transaction")
form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

tk.Label(form_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
tk.Label(form_frame, text="Description").grid(row=1, column=0)
tk.Label(form_frame, text="Category").grid(row=2, column=0)
tk.Label(form_frame, text="Type (Income/Expense)").grid(row=3, column=0)
tk.Label(form_frame, text="Amount").grid(row=4, column=0)

date_entry = tk.Entry(form_frame)
description_entry = tk.Entry(form_frame)
category_entry = tk.Entry(form_frame)
type_entry = tk.Entry(form_frame)
amount_entry = tk.Entry(form_frame)

date_entry.grid(row=0, column=1)
description_entry.grid(row=1, column=1)
category_entry.grid(row=2, column=1)
type_entry.grid(row=3, column=1)
amount_entry.grid(row=4, column=1)

tk.Button(form_frame, text="Add Transaction", command=add_transaction).grid(row=5, column=0, columnspan=2, pady=10)

summary_frame = tk.LabelFrame(main_frame, text="Summary")
summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

income_label = tk.Label(summary_frame, text="Total Income: $0.00")
expense_label = tk.Label(summary_frame, text="Total Expense: $0.00")
balance_label = tk.Label(summary_frame, text="Net Balance: $0.00")

income_label.grid(row=0, column=0, padx=5, pady=5)
expense_label.grid(row=1, column=0, padx=5, pady=5)
balance_label.grid(row=2, column=0, padx=5, pady=5)

transactions_frame = tk.LabelFrame(main_frame, text="Transactions")
transactions_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

columns = ("ID", "Date", "Description", "Category", "Type", "Amount")
transactions_tree = ttk.Treeview(transactions_frame, columns=columns, show="headings")
for col in columns:
    transactions_tree.heading(col, text=col)

transactions_tree.pack(fill=tk.BOTH, expand=True)

tk.Button(main_frame, text="Update Summary", command=update_summary).grid(row=3, column=0, pady=10, sticky="ew")
tk.Button(main_frame, text="Export to CSV", command=export_to_csv).grid(row=4, column=0, pady=10, sticky="ew")

# Configure the grid to expand the transactions frame
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

update_summary()
view_transactions()

root.mainloop()
