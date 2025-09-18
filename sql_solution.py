#!/usr/bin/env python3
"""
Sales Report Assignment - Solution 1: Pure SQL
Extracts total quantities per customer (age 18-35) for each item using only SQL
"""

import sqlite3
import csv
from typing import List, Tuple


class SQLSolution:
    """Pure SQL solution for sales data analysis"""
    
    def __init__(self, db_path: str = 'sales_data.db'):
        """Initialize with database path"""
        self.db_path = db_path
    
    def connect_to_database(self) -> sqlite3.Connection:
        """Connect to the SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            print(f"Successfully connected to database: {self.db_path}")
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def get_sales_data_sql(self) -> List[Tuple]:
        """
        Extract sales data using pure SQL
        Returns: List of tuples (customer_id, age, item_name, total_quantity)
        """
        
        # SQL query to get total quantities per customer and item for ages 18-35
        query = """
        SELECT 
            c.customer_id,
            c.age,
            i.item_name,
            SUM(o.quantity) as total_quantity
        FROM Customer c
        INNER JOIN Sales s ON c.customer_id = s.customer_id
        INNER JOIN Orders o ON s.sales_id = o.sales_id
        INNER JOIN Items i ON o.item_id = i.item_id
        WHERE c.age BETWEEN 18 AND 35
          AND o.quantity IS NOT NULL  -- Exclude items not purchased (NULL quantities)
        GROUP BY c.customer_id, c.age, i.item_name
        HAVING SUM(o.quantity) > 0  -- Exclude items with zero total quantity
        ORDER BY c.customer_id, i.item_name
        """
        
        conn = self.connect_to_database()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            
            print(f"SQL Query executed successfully. Found {len(results)} records.")
            return results
            
        except sqlite3.Error as e:
            print(f"Error executing SQL query: {e}")
            raise
        finally:
            conn.close()
    
    def save_to_csv(self, data: List[Tuple], filename: str = 'sales_report_sql.csv'):
        """Save data to CSV file with semicolon delimiter"""
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                # Write header
                writer.writerow(['Customer', 'Age', 'Item', 'Quantity'])
                
                # Write data rows
                for row in data:
                    # Ensure quantity is integer (no decimal points)
                    customer_id, age, item_name, quantity = row
                    writer.writerow([customer_id, age, item_name, int(quantity)])
            
            print(f"Data successfully saved to {filename}")
            
        except IOError as e:
            print(f"Error saving to CSV: {e}")
            raise
    
    def run_analysis(self) -> List[Tuple]:
        """Run the complete analysis and return results"""
        
        print("=== SQL Solution ===")
        print("Extracting sales data using pure SQL...")
        
        # Get data using SQL
        results = self.get_sales_data_sql()
        
        # Display results
        print("\nResults:")
        print("Customer;Age;Item;Quantity")
        for row in results:
            customer_id, age, item_name, quantity = row
            print(f"{customer_id};{age};{item_name};{int(quantity)}")
        
        # Save to CSV
        self.save_to_csv(results)
        
        return results


def main():
    """Main function to run the SQL solution"""
    
    try:
        # Create and run SQL solution
        sql_solution = SQLSolution()
        results = sql_solution.run_analysis()
        
        print(f"\nAnalysis complete! Found {len(results)} records for customers aged 18-35.")
        
    except Exception as e:
        print(f"Error running analysis: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())