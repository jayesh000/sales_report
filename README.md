# Sales Report Assignment

## Overview

This project analyzes sales data for Company XYZ to identify purchasing patterns by age group. The solution extracts total quantities of items purchased by customers aged 18-35, providing insights for targeted marketing strategies.

## Problem Statement

Company XYZ held a promotional sale for their signature items (x, y, z) and wants to analyze purchasing patterns by age group. The database follows these business rules:

- A sales receipt can have multiple items in an order
- For every order, quantities are recorded for all items (NULL for items not purchased)
- Each customer can have multiple sales transactions
- Customer ages are stored in the database

## Database Schema

The database consists of 4 tables with the following relationships:

```
Customer (customer_id PK, age)
    ↓ (1:N)
Sales (sales_id PK, customer_id FK)
    ↓ (1:N)
Orders (order_id PK, sales_id FK, item_id FK, quantity)
    ↓ (N:1)
Items (item_id PK, item_name)
```

## Solution Approach

This project provides **two different solutions** as requested:

1. **Pure SQL Solution** (`sql_solution.py`): Uses only SQL queries for data extraction and aggregation
2. **Pandas Solution** (`pandas_solution.py`): Uses Pandas DataFrames for data manipulation and analysis

Both solutions:
- Filter customers aged 18-35
- Sum quantities by customer and item
- Exclude items with NULL quantities (not purchased)
- Exclude items with zero total quantities
- Export results to CSV with semicolon delimiter
- Ensure integer quantities (no decimals)

## Files Structure

```
sales_report/
│
├── README.md                    # This documentation
├── create_database.py          # Database setup script
├── sql_solution.py             # Pure SQL implementation
├── pandas_solution.py          # Pandas implementation
├── main.py                     # Main script running both solutions
├── sales_data.db              # SQLite database (generated)
├── sales_report_sql.csv       # SQL solution output
└── sales_report_pandas.csv    # Pandas solution output
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Required packages:
  - `sqlite3` (built-in with Python)
  - `pandas` (install with: `pip install pandas`)

### Installation & Usage

1. **Clone or download** this repository to your local machine

2. **Navigate** to the project directory:
   ```bash
   cd sales_report
   ```

3. **Install dependencies**:
   ```bash
   pip install pandas
   ```

4. **Create the database** with sample data:
   ```bash
   python create_database.py
   ```

5. **Run the analysis** (both solutions):
   ```bash
   python main.py
   ```

   Or run individual solutions:
   ```bash
   python sql_solution.py      # SQL-only solution
   python pandas_solution.py   # Pandas-only solution
   ```

## Expected Output

Based on the test case, the output should be:

```
Customer;Age;Item;Quantity
1;21;x;10
2;23;x;1
2;23;y;1
2;23;z;1
3;35;z;2
```

This shows:
- Customer 1 (age 21): Total 10 of item 'x'
- Customer 2 (age 23): 1 each of items 'x', 'y', 'z'
- Customer 3 (age 35): Total 2 of item 'z'

## Technical Implementation

### SQL Solution Highlights

- Uses `INNER JOIN` to connect all tables
- Filters with `WHERE age BETWEEN 18 AND 35`
- Excludes NULL quantities with `AND quantity IS NOT NULL`
- Groups by customer, age, and item with `GROUP BY`
- Filters zero totals with `HAVING SUM(quantity) > 0`

### Pandas Solution Highlights

- Loads tables into separate DataFrames
- Filters customers by age range using boolean indexing
- Uses `pd.merge()` for table joins
- Excludes NULL quantities with `notna()`
- Groups and aggregates with `groupby().sum()`
- Ensures integer output with `astype(int)`

### Key Features

- **Error handling**: Comprehensive exception handling for database and file operations
- **Data validation**: Ensures data integrity and proper formatting
- **Code organization**: Clean, modular code with type hints and documentation
- **Output verification**: Both solutions produce identical results for validation

## Assignment Requirements Checklist

✅ **Connect to SQLite3 database**  
✅ **Extract total quantities per customer aged 18-35**  
✅ **Sum quantities for each item per customer**  
✅ **Omit items with zero total quantity**  
✅ **No decimal points in quantities**  
✅ **Provide pure SQL solution**  
✅ **Provide Pandas solution**  
✅ **Store results in CSV with semicolon delimiter**  
✅ **Match expected output format**  

## Testing

The solution includes comprehensive test data that matches the provided test case:

- **Customer 1** (age 21): Multiple purchases totaling 10 of item X
- **Customer 2** (age 23): Single purchase of 1 each item (X, Y, Z)
- **Customer 3** (age 35): Multiple purchases totaling 2 of item Z
- **Customers 4 & 5**: Outside age range (excluded from results)

Both solutions are validated to produce identical output, ensuring correctness.

## License

This project is created for assessment purposes.

---

**Author**: Jayesh  
**Date**: September 2025  
**Purpose**: Interview Assignment - Data Analysis with Python and SQL