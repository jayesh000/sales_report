#!/usr/bin/env python3
"""
Sales Report Assignment - Solution 2: Pandas
Extracts total quantities per customer (age 18-35) for each item using Pandas
"""

import sqlite3
import pandas as pd
import csv
from typing import Tuple


class PandasSolution:
    """Pandas solution for sales data analysis"""
    
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
    
    def load_data_to_dataframes(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load all tables into Pandas DataFrames"""
        
        conn = self.connect_to_database()
        
        try:
            # Load all tables into DataFrames
            customers_df = pd.read_sql_query("SELECT * FROM Customer", conn)
            items_df = pd.read_sql_query("SELECT * FROM Items", conn)
            sales_df = pd.read_sql_query("SELECT * FROM Sales", conn)
            orders_df = pd.read_sql_query("SELECT * FROM Orders", conn)
            
            print("Data loaded into Pandas DataFrames successfully")
            print(f"Customers: {len(customers_df)} records")
            print(f"Items: {len(items_df)} records")
            print(f"Sales: {len(sales_df)} records")
            print(f"Orders: {len(orders_df)} records")
            
            return customers_df, items_df, sales_df, orders_df
            
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
        finally:
            conn.close()
    
    def get_sales_data_pandas(self) -> pd.DataFrame:
        """
        Extract and process sales data using Pandas
        Returns: DataFrame with customer_id, age, item_name, total_quantity
        """
        
        # Load data
        customers_df, items_df, sales_df, orders_df = self.load_data_to_dataframes()
        
        # Step 1: Filter customers aged 18-35
        customers_filtered = customers_df[
            (customers_df['age'] >= 18) & (customers_df['age'] <= 35)
        ].copy()
        
        print(f"Customers in age range 18-35: {len(customers_filtered)}")
        
        # Step 2: Merge sales with filtered customers
        sales_customers = pd.merge(
            sales_df, 
            customers_filtered, 
            on='customer_id', 
            how='inner'
        )
        
        # Step 3: Merge with orders (exclude NULL quantities)
        orders_filtered = orders_df[orders_df['quantity'].notna()].copy()
        sales_orders = pd.merge(
            sales_customers,
            orders_filtered,
            on='sales_id',
            how='inner'
        )
        
        # Step 4: Merge with items to get item names
        sales_complete = pd.merge(
            sales_orders,
            items_df,
            on='item_id',
            how='inner'
        )
        
        # Step 5: Group by customer and item, sum quantities
        result_df = sales_complete.groupby(
            ['customer_id', 'age', 'item_name'], 
            as_index=False
        )['quantity'].sum()
        
        # Step 6: Filter out zero quantities (though shouldn't exist due to NULL filtering)
        result_df = result_df[result_df['quantity'] > 0].copy()
        
        # Step 7: Ensure quantities are integers (no decimals)
        result_df['quantity'] = result_df['quantity'].astype(int)
        
        # Step 8: Sort by customer_id and item_name for consistent output
        result_df = result_df.sort_values(['customer_id', 'item_name']).reset_index(drop=True)
        
        print(f"Pandas processing complete. Found {len(result_df)} records.")
        
        return result_df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = 'sales_report_pandas.csv'):
        """Save DataFrame to CSV file with semicolon delimiter"""
        
        try:
            # Create a copy with proper column names for output
            output_df = df.copy()
            output_df.columns = ['Customer', 'Age', 'Item', 'Quantity']
            
            # Save to CSV with semicolon delimiter
            output_df.to_csv(filename, sep=';', index=False)
            
            print(f"Data successfully saved to {filename}")
            
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            raise
    
    def run_analysis(self) -> pd.DataFrame:
        """Run the complete analysis and return results"""
        
        print("=== Pandas Solution ===")
        print("Extracting sales data using Pandas...")
        
        # Get data using Pandas
        results_df = self.get_sales_data_pandas()
        
        # Display results
        print("\nResults:")
        print("Customer;Age;Item;Quantity")
        for _, row in results_df.iterrows():
            print(f"{row['customer_id']};{row['age']};{row['item_name']};{row['quantity']}")
        
        # Save to CSV
        self.save_to_csv(results_df)
        
        return results_df


def main():
    """Main function to run the Pandas solution"""
    
    try:
        # Create and run Pandas solution
        pandas_solution = PandasSolution()
        results_df = pandas_solution.run_analysis()
        
        print(f"\nAnalysis complete! Found {len(results_df)} records for customers aged 18-35.")
        
    except Exception as e:
        print(f"Error running analysis: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())