#!/usr/bin/env python3
"""
Database setup script for Sales Report Assignment
Creates SQLite database with sample data matching the test case
"""

import sqlite3
import os

def create_database():
    """Create the SQLite database with schema and sample data"""
    
    # Remove existing database if it exists
    if os.path.exists('sales_data.db'):
        os.remove('sales_data.db')
    
    # Connect to SQLite database
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()
    
    # Create tables based on the schema
    
    # Customer table
    cursor.execute('''
        CREATE TABLE Customer (
            customer_id INTEGER PRIMARY KEY,
            age INTEGER NOT NULL
        )
    ''')
    
    # Items table
    cursor.execute('''
        CREATE TABLE Items (
            item_id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL
        )
    ''')
    
    # Sales table
    cursor.execute('''
        CREATE TABLE Sales (
            sales_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE Orders (
            order_id INTEGER PRIMARY KEY,
            sales_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER,  -- NULL means item not purchased
            FOREIGN KEY (sales_id) REFERENCES Sales(sales_id),
            FOREIGN KEY (item_id) REFERENCES Items(item_id)
        )
    ''')
    
    # Insert sample data based on test case
    
    # Insert customers
    customers = [
        (1, 21),  # Customer 1, age 21
        (2, 23),  # Customer 2, age 23
        (3, 35),  # Customer 3, age 35
        (4, 45),  # Customer 4, age 45 (outside target range)
        (5, 17),  # Customer 5, age 17 (outside target range)
    ]
    cursor.executemany('INSERT INTO Customer (customer_id, age) VALUES (?, ?)', customers)
    
    # Insert items (x, y, z)
    items = [
        (1, 'x'),
        (2, 'y'),
        (3, 'z'),
    ]
    cursor.executemany('INSERT INTO Items (item_id, item_name) VALUES (?, ?)', items)
    
    # Insert sales transactions
    sales = [
        (1, 1),  # Customer 1's first transaction
        (2, 1),  # Customer 1's second transaction
        (3, 2),  # Customer 2's transaction
        (4, 3),  # Customer 3's first transaction
        (5, 3),  # Customer 3's second transaction
        (6, 4),  # Customer 4's transaction (age 45, outside range)
        (7, 5),  # Customer 5's transaction (age 17, outside range)
    ]
    cursor.executemany('INSERT INTO Sales (sales_id, customer_id) VALUES (?, ?)', sales)
    
    # Insert orders based on test case requirements
    orders = [
        # Customer 1's purchases - totaling 10 for Item X only
        (1, 1, 1, 6),    # Sales 1: Item x, quantity 6
        (2, 1, 2, None), # Sales 1: Item y, not purchased (NULL)
        (3, 1, 3, None), # Sales 1: Item z, not purchased (NULL)
        
        (4, 2, 1, 4),    # Sales 2: Item x, quantity 4 (total 10 for customer 1)
        (5, 2, 2, None), # Sales 2: Item y, not purchased (NULL)
        (6, 2, 3, None), # Sales 2: Item z, not purchased (NULL)
        
        # Customer 2's purchases - 1 of each item
        (7, 3, 1, 1),    # Sales 3: Item x, quantity 1
        (8, 3, 2, 1),    # Sales 3: Item y, quantity 1
        (9, 3, 3, 1),    # Sales 3: Item z, quantity 1
        
        # Customer 3's purchases - totaling 2 for Item Z only
        (10, 4, 1, None), # Sales 4: Item x, not purchased (NULL)
        (11, 4, 2, None), # Sales 4: Item y, not purchased (NULL)
        (12, 4, 3, 1),    # Sales 4: Item z, quantity 1
        
        (13, 5, 1, None), # Sales 5: Item x, not purchased (NULL)
        (14, 5, 2, None), # Sales 5: Item y, not purchased (NULL)
        (15, 5, 3, 1),    # Sales 5: Item z, quantity 1 (total 2 for customer 3)
        
        # Customer 4 (age 45, outside range) - should be excluded
        (16, 6, 1, 5),    # Sales 6: Item x, quantity 5
        (17, 6, 2, 2),    # Sales 6: Item y, quantity 2
        (18, 6, 3, None), # Sales 6: Item z, not purchased (NULL)
        
        # Customer 5 (age 17, outside range) - should be excluded
        (19, 7, 1, 3),    # Sales 7: Item x, quantity 3
        (20, 7, 2, None), # Sales 7: Item y, not purchased (NULL)
        (21, 7, 3, 2),    # Sales 7: Item z, quantity 2
    ]
    cursor.executemany('INSERT INTO Orders (order_id, sales_id, item_id, quantity) VALUES (?, ?, ?, ?)', orders)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database 'sales_data.db' created successfully!")
    print("\nExpected output for customers aged 18-35:")
    print("Customer;Age;Item;Quantity")
    print("1;21;x;10")
    print("2;23;x;1")
    print("2;23;y;1")
    print("2;23;z;1")
    print("3;35;z;2")

if __name__ == "__main__":
    create_database()