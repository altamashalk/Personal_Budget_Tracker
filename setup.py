import sqlite3

# Create a database connection
conn = sqlite3.connect('budget_tracker.db')
c = conn.cursor()

# Create a table
c.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    date TEXT,
    description TEXT,
    category TEXT,
    type TEXT,
    amount REAL
)
''')

conn.commit()
conn.close()
print("Database and table created successfully.")
