import pandas as pd
import sqlite3

# Load your Excel file
file_path = r"D:\database\UPDATED 2nd SEPTEMBER .xlsx"  # Adjust this path

# Load the relevant sheet from the Excel file
try:
    data = pd.read_excel(file_path, sheet_name="Sheet1")
except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit()

# Connect to SQLite database (creates a new one if it doesn't exist)
db_path = 'drug_database.db'  # Database file path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table to store drug data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY,
        product TEXT,
        packing TEXT,
        qty INTEGER,
        trade_price REAL,
        nett_price REAL,
        unit_price REAL,
        retail_price REAL
    )
''')

# Insert data into the database
for _, row in data.iterrows():
    try:
        cursor.execute('''
            INSERT INTO drugs (product, packing, qty, trade_price, nett_price, unit_price, retail_price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['PRODUCT'],
            row['PACKING'],
            row['QTY'],
            row['TRADE'],
            row['NETT PRICE'],
            row['PRICE PER UNIT (DISCOUNT- 15%)'],
            row['RETAIL']
        ))
    except Exception as e:
        print(f"Error inserting row: {e}")

# Commit changes and close the database connection
conn.commit()
print("Database setup complete and data imported successfully.")

# Function to query the database by brand name or composition
def get_drug_info(search_term):
    # Connect to the database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Query to search by product name or composition
        cursor.execute('''
            SELECT product, packing, qty, trade_price, unit_price, retail_price
            FROM drugs
            WHERE product LIKE ?
        ''', (f'%{search_term}%',))

        # Fetch and display results
        results = cursor.fetchall()
        if results:
            for result in results:
                print(f"Product: {result[0]}, Packing: {result[1]}, Quantity: {result[2]}, "
                      f"Trade Price: {result[3]}, Unit Price: {result[4]}, Retail Price: {result[5]}")
        else:
            print("No matching products found.")

# Example usage: replace 'brand_or_composition_name' with the actual search term
get_drug_info("panadol")  # Replace with an actual name or composition
