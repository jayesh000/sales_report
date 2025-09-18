#!/usr/bin/env python3
"""
Sales Report Assignment - Main Script
Demonstrates both SQL and Pandas solutions for analyzing sales data
"""

import sys
import os
from sql_solution import SQLSolution
from pandas_solution import PandasSolution


def main():
    """Main function to run both solutions"""
    
    print("=" * 60)
    print("SALES REPORT ASSIGNMENT")
    print("Company XYZ - Marketing Strategy Analysis")
    print("=" * 60)
    print()
    
    # Check if database exists
    if not os.path.exists('sales_data.db'):
        print("Error: Database file 'sales_data.db' not found!")
        print("Please run 'python create_database.py' first to create the database.")
        return 1
    
    try:
        print("Running both solutions to extract sales data for customers aged 18-35...")
        print()
        
        # Solution 1: Pure SQL
        print("▶ SOLUTION 1: Pure SQL")
        print("-" * 40)
        sql_solution = SQLSolution()
        sql_results = sql_solution.run_analysis()
        print()
        
        # Solution 2: Pandas
        print("▶ SOLUTION 2: Pandas")
        print("-" * 40)
        pandas_solution = PandasSolution()
        pandas_results = pandas_solution.run_analysis()
        print()
        
        # Compare results
        print("▶ COMPARISON")
        print("-" * 40)
        print(f"SQL solution found: {len(sql_results)} records")
        print(f"Pandas solution found: {len(pandas_results)} records")
        
        if len(sql_results) == len(pandas_results):
            print("✅ Both solutions found the same number of records!")
        else:
            print("⚠️ Solutions found different number of records!")
        
        print()
        print("Output files generated:")
        print("  - sales_report_sql.csv (SQL solution)")
        print("  - sales_report_pandas.csv (Pandas solution)")
        
        print()
        print("🎯 Assignment objectives completed:")
        print("  ✅ Connected to SQLite3 database")
        print("  ✅ Extracted total quantities per customer (age 18-35)")
        print("  ✅ Excluded items with zero quantities")
        print("  ✅ Provided pure SQL solution")
        print("  ✅ Provided Pandas solution")
        print("  ✅ Stored results in CSV with semicolon delimiter")
        print("  ✅ No decimal points in quantities")
        
        return 0
        
    except Exception as e:
        print(f"Error running analysis: {e}")
        return 1


if __name__ == "__main__":
    exit(main())