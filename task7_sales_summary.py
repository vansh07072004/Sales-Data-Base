import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Sample data insertion (optional)
sample_data = [
    ("Laptop", 3, 50000),
    ("Laptop", 2, 50000),
    ("Phone", 5, 15000),
    ("Phone", 3, 15000),
    ("Headphones", 10, 2000),
    ("Headphones", 7, 2000)
]

cursor.execute("DELETE FROM sales")
cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", sample_data)
conn.commit()

# SQL Query
query = """
SELECT 
    product,
    SUM(quantity) AS total_qty,
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""

df = pd.read_sql_query(query, conn)

# Print results
print(df)

# Bar Chart
plt.figure(figsize=(6,4))
plt.bar(df["product"], df["revenue"])
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.title("Revenue by Product")
plt.savefig("sales_chart.png")
plt.close()

print("Chart saved as sales_chart.png")
