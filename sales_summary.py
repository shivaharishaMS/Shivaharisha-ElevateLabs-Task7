# sales_summary.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Create & populate the database
def create_database():
    conn = sqlite3.connect("sales_data.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        quantity INTEGER,
        price REAL
    )
    """)

    # Insert sample sales data
    sales_data = [
        ("Laptop", 3, 800),
        ("Laptop", 2, 800),
        ("Mouse", 10, 20),
        ("Mouse", 5, 20),
        ("Keyboard", 4, 50),
        ("Keyboard", 6, 50)
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sales_data)

    conn.commit()
    conn.close()
    print("✅ Database created and sample data inserted.")

# 2. Query data & create summary
def get_sales_summary():
    conn = sqlite3.connect("sales_data.db")

    query = """
    SELECT product, 
           SUM(quantity) AS total_qty, 
           SUM(quantity * price) AS revenue
    FROM sales
    GROUP BY product
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 3. Plot bar chart
def plot_chart(df):
    df.plot(kind='bar', x='product', y='revenue', legend=False)
    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue ($)")
    plt.tight_layout()
    plt.savefig("sales_chart.png")
    plt.show()
    print("📊 Chart saved as 'sales_chart.png'.")

# Main script
if __name__ == "__main__":
    create_database()
    df = get_sales_summary()
    print("\n📋 Sales Summary:")
    print(df)
    plot_chart(df)
