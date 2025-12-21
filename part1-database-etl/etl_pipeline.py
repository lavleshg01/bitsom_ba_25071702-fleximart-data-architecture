"""
ETL Pipeline for FlexiMart Data Processing
Extracts, transforms, and loads customer, product, and sales data into MySQL database
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'fleximart',
    'user': 'root',
    'password': 'LawSue$#$#8377'  # Change this to your MySQL password
}

# File paths
DATA_DIR = 'data'
CUSTOMERS_FILE = os.path.join(DATA_DIR, 'customers_raw.csv')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products_raw.csv')
SALES_FILE = os.path.join(DATA_DIR, 'sales_raw.csv')

# Data quality tracking
quality_report = {
    'customers': {
        'records_read': 0,
        'duplicates_removed': 0,
        'missing_emails_handled': 0,
        'missing_phones_handled': 0,
        'date_format_fixed': 0,
        'phone_format_standardized': 0,
        'records_loaded': 0
    },
    'products': {
        'records_read': 0,
        'duplicates_removed': 0,
        'missing_prices_handled': 0,
        'missing_stock_handled': 0,
        'category_standardized': 0,
        'records_loaded': 0
    },
    'sales': {
        'records_read': 0,
        'duplicates_removed': 0,
        'missing_customer_id_dropped': 0,
        'missing_product_id_dropped': 0,
        'date_format_fixed': 0,
        'records_loaded': 0
    }
}


def standardize_phone(phone):
    """
    Standardize phone number to format: +91-XXXXXXXXXX
    """
    if pd.isna(phone) or phone == '':
        return None
    
    # Remove all non-digit characters except +
    phone_str = str(phone).strip()
    
    # Extract digits only
    digits = re.sub(r'\D', '', phone_str)
    
    # Handle different formats
    if len(digits) == 10:
        # 10-digit number without country code
        return f"+91-{digits}"
    elif len(digits) == 12 and digits.startswith('91'):
        # 12-digit number with country code
        return f"+91-{digits[2:]}"
    elif len(digits) == 11 and digits.startswith('0'):
        # 11-digit number starting with 0
        return f"+91-{digits[1:]}"
    elif len(digits) == 13 and digits.startswith('9191'):
        # 13-digit number
        return f"+91-{digits[3:]}"
    elif len(digits) >= 10:
        # Take last 10 digits
        return f"+91-{digits[-10:]}"
    else:
        return None


def standardize_category(category):
    """
    Standardize category name to title case (e.g., Electronics, Fashion, Groceries)
    """
    if pd.isna(category) or category == '':
        return None
    
    category_str = str(category).strip()
    
    # Map common variations
    category_lower = category_str.lower()
    
    if 'electronic' in category_lower:
        return 'Electronics'
    elif 'fashion' in category_lower:
        return 'Fashion'
    elif 'grocery' in category_lower or 'groceries' in category_lower:
        return 'Groceries'
    else:
        # Default to title case
        return category_str.title()


def parse_date(date_str):
    """
    Parse various date formats and convert to YYYY-MM-DD
    """
    if pd.isna(date_str) or date_str == '':
        return None
    
    date_str = str(date_str).strip()
    
    # Try different date formats
    formats = [
        '%Y-%m-%d',      # 2024-01-15
        '%d/%m/%Y',      # 15/01/2024
        '%m-%d-%Y',      # 01-22-2024
        '%d-%m-%Y',      # 15-04-2023
        '%m/%d/%Y',      # 02/02/2024
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    # If all formats fail, return None
    return None


def extract_customers():
    """
    Extract customer data from CSV file
    """
    print("Extracting customers data...")
    df = pd.read_csv(CUSTOMERS_FILE)
    quality_report['customers']['records_read'] = len(df)
    return df


def transform_customers(df):
    """
    Transform customer data: remove duplicates, handle missing values, standardize formats
    """
    print("Transforming customers data...")
    
    # Remove duplicates based on customer_id
    initial_count = len(df)
    df = df.drop_duplicates(subset=['customer_id'], keep='first')
    duplicates_removed = initial_count - len(df)
    quality_report['customers']['duplicates_removed'] = duplicates_removed
    
    # Handle missing emails - generate placeholder email
    missing_emails = df['email'].isna() | (df['email'] == '')
    quality_report['customers']['missing_emails_handled'] = missing_emails.sum()
    
    # Generate placeholder emails for missing ones
    for idx in df[missing_emails].index:
        customer_id = df.loc[idx, 'customer_id']
        first_name = df.loc[idx, 'first_name'].lower()
        last_name = df.loc[idx, 'last_name'].lower()
        df.loc[idx, 'email'] = f"{first_name}.{last_name}.{customer_id}@fleximart.placeholder.com"
    
    # Standardize phone numbers
    phone_changed = 0
    for idx in df.index:
        old_phone = df.loc[idx, 'phone']
        new_phone = standardize_phone(old_phone)
        if new_phone != old_phone and pd.notna(new_phone):
            phone_changed += 1
        df.loc[idx, 'phone'] = new_phone
    
    quality_report['customers']['phone_format_standardized'] = phone_changed
    
    # Handle missing phones
    quality_report['customers']['missing_phones_handled'] = df['phone'].isna().sum()
    
    # Standardize date formats
    date_fixed = 0
    for idx in df.index:
        old_date = df.loc[idx, 'registration_date']
        new_date = parse_date(old_date)
        if new_date != old_date:
            date_fixed += 1
        df.loc[idx, 'registration_date'] = new_date
    
    quality_report['customers']['date_format_fixed'] = date_fixed
    
    # Remove rows with missing critical fields (first_name, last_name, email)
    df = df.dropna(subset=['first_name', 'last_name', 'email'])
    
    return df


def extract_products():
    """
    Extract product data from CSV file
    """
    print("Extracting products data...")
    df = pd.read_csv(PRODUCTS_FILE)
    quality_report['products']['records_read'] = len(df)
    return df


def transform_products(df):
    """
    Transform product data: remove duplicates, handle missing values, standardize formats
    """
    print("Transforming products data...")
    
    # Remove duplicates based on product_id
    initial_count = len(df)
    df = df.drop_duplicates(subset=['product_id'], keep='first')
    duplicates_removed = initial_count - len(df)
    quality_report['products']['duplicates_removed'] = duplicates_removed
    
    # Handle missing prices - drop records with missing prices (required field)
    missing_prices = df['price'].isna() | (df['price'] == '')
    quality_report['products']['missing_prices_handled'] = missing_prices.sum()
    df = df[~missing_prices]
    
    # Convert price to numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
    
    # Handle missing stock - default to 0
    missing_stock = df['stock_quantity'].isna() | (df['stock_quantity'] == '')
    quality_report['products']['missing_stock_handled'] = missing_stock.sum()
    df['stock_quantity'] = df['stock_quantity'].fillna(0)
    df['stock_quantity'] = pd.to_numeric(df['stock_quantity'], errors='coerce').fillna(0).astype(int)
    
    # Standardize category names
    category_changed = 0
    for idx in df.index:
        old_category = df.loc[idx, 'category']
        new_category = standardize_category(old_category)
        if new_category != old_category:
            category_changed += 1
        df.loc[idx, 'category'] = new_category
    
    quality_report['products']['category_standardized'] = category_changed
    
    # Remove rows with missing critical fields
    df = df.dropna(subset=['product_name', 'category', 'price'])
    
    return df


def extract_sales():
    """
    Extract sales data from CSV file
    """
    print("Extracting sales data...")
    df = pd.read_csv(SALES_FILE)
    quality_report['sales']['records_read'] = len(df)
    return df


def transform_sales(df):
    """
    Transform sales data: remove duplicates, handle missing values, standardize formats
    """
    print("Transforming sales data...")
    
    # Remove duplicates based on transaction_id
    initial_count = len(df)
    df = df.drop_duplicates(subset=['transaction_id'], keep='first')
    duplicates_removed = initial_count - len(df)
    quality_report['sales']['duplicates_removed'] = duplicates_removed
    
    # Drop records with missing customer_id
    missing_customer = df['customer_id'].isna() | (df['customer_id'] == '')
    quality_report['sales']['missing_customer_id_dropped'] = missing_customer.sum()
    df = df[~missing_customer]
    
    # Drop records with missing product_id
    missing_product = df['product_id'].isna() | (df['product_id'] == '')
    quality_report['sales']['missing_product_id_dropped'] = missing_product.sum()
    df = df[~missing_product]
    
    # Standardize date formats
    date_fixed = 0
    for idx in df.index:
        old_date = df.loc[idx, 'transaction_date']
        new_date = parse_date(old_date)
        if new_date != old_date:
            date_fixed += 1
        df.loc[idx, 'transaction_date'] = new_date
    
    quality_report['sales']['date_format_fixed'] = date_fixed
    
    # Remove rows with missing transaction_date
    df = df.dropna(subset=['transaction_date'])
    
    # Convert quantity and unit_price to numeric
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    
    # Remove rows with invalid numeric values
    df = df.dropna(subset=['quantity', 'unit_price'])
    
    return df


def create_database_connection():
    """
    Create and return database connection
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def create_tables(connection):
    """
    Create database tables if they don't exist
    """
    cursor = connection.cursor()
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            city VARCHAR(50),
            registration_date DATE
        )
    """)
    
    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            stock_quantity INT DEFAULT 0
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT NOT NULL,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # Create order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            subtotal DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    
    connection.commit()
    cursor.close()
    print("Database tables created/verified successfully")


def load_customers(connection, df):
    """
    Load customer data into database
    Returns mapping of original customer_id to database customer_id
    """
    print("Loading customers data...")
    cursor = connection.cursor()
    
    # Clear existing data (optional - remove if you want to append)
    cursor.execute("DELETE FROM customers")
    
    insert_query = """
        INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    records_loaded = 0
    customer_id_mapping = {}  # Maps original customer_id to database customer_id
    
    for _, row in df.iterrows():
        try:
            cursor.execute(insert_query, (
                row['first_name'],
                row['last_name'],
                row['email'],
                row['phone'] if pd.notna(row['phone']) else None,
                row['city'] if pd.notna(row['city']) else None,
                row['registration_date'] if pd.notna(row['registration_date']) else None
            ))
            db_customer_id = cursor.lastrowid
            original_customer_id = row['customer_id']
            customer_id_mapping[original_customer_id] = db_customer_id
            records_loaded += 1
        except Error as e:
            print(f"Error inserting customer {row.get('customer_id', 'unknown')}: {e}")
    
    connection.commit()
    cursor.close()
    quality_report['customers']['records_loaded'] = records_loaded
    print(f"Loaded {records_loaded} customer records")
    return customer_id_mapping


def load_products(connection, df):
    """
    Load product data into database
    Returns mapping of original product_id to database product_id
    """
    print("Loading products data...")
    cursor = connection.cursor()
    
    # Clear existing data (optional - remove if you want to append)
    cursor.execute("DELETE FROM products")
    
    insert_query = """
        INSERT INTO products (product_name, category, price, stock_quantity)
        VALUES (%s, %s, %s, %s)
    """
    
    records_loaded = 0
    product_id_mapping = {}  # Maps original product_id to database product_id
    
    for _, row in df.iterrows():
        try:
            cursor.execute(insert_query, (
                row['product_name'],
                row['category'],
                float(row['price']),
                int(row['stock_quantity'])
            ))
            db_product_id = cursor.lastrowid
            original_product_id = row['product_id']
            product_id_mapping[original_product_id] = db_product_id
            records_loaded += 1
        except Error as e:
            print(f"Error inserting product {row.get('product_id', 'unknown')}: {e}")
    
    connection.commit()
    cursor.close()
    quality_report['products']['records_loaded'] = records_loaded
    print(f"Loaded {records_loaded} product records")
    return product_id_mapping


def load_orders_improved(connection, sales_df, customer_id_mapping, product_id_mapping):
    """
    Improved version: Load sales data as orders and order_items with proper ID mapping
    """
    print("Loading orders and order_items data...")
    cursor = connection.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    
    # Group sales by customer_id and transaction_date to create orders
    sales_df['order_key'] = sales_df['customer_id'].astype(str) + '_' + sales_df['transaction_date'].astype(str)
    
    records_loaded = 0
    
    for order_key, group in sales_df.groupby('order_key'):
        first_row = group.iloc[0]
        customer_id_orig = first_row['customer_id']
        order_date = first_row['transaction_date']
        
        # Get database customer_id from mapping
        if customer_id_orig not in customer_id_mapping:
            continue
        
        db_customer_id = customer_id_mapping[customer_id_orig]
        
        # Calculate total amount for this order
        total_amount = (group['quantity'] * group['unit_price']).sum()
        
        # Get status (use most common status)
        status = group['status'].mode()[0] if len(group['status'].mode()) > 0 else 'Completed'
        
        # Insert order
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, total_amount, status)
            VALUES (%s, %s, %s, %s)
        """, (db_customer_id, order_date, float(total_amount), status))
        
        order_id = cursor.lastrowid
        
        # Insert order items
        for _, item in group.iterrows():
            product_id_orig = item['product_id']
            
            # Get database product_id from mapping
            if product_id_orig not in product_id_mapping:
                continue
            
            db_product_id = product_id_mapping[product_id_orig]
            
            subtotal = float(item['quantity']) * float(item['unit_price'])
            
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                order_id,
                db_product_id,
                int(item['quantity']),
                float(item['unit_price']),
                subtotal
            ))
            records_loaded += 1
    
    connection.commit()
    cursor.close()
    quality_report['sales']['records_loaded'] = records_loaded
    print(f"Loaded {records_loaded} order item records")


def generate_quality_report():
    """
    Generate data quality report
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("FLEXIMART DATA QUALITY REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Customers section
    report_lines.append("CUSTOMERS DATA QUALITY METRICS")
    report_lines.append("-" * 80)
    cust = quality_report['customers']
    report_lines.append(f"Records read from file: {cust['records_read']}")
    report_lines.append(f"Duplicates removed: {cust['duplicates_removed']}")
    report_lines.append(f"Missing emails handled: {cust['missing_emails_handled']}")
    report_lines.append(f"Missing phones handled: {cust['missing_phones_handled']}")
    report_lines.append(f"Phone formats standardized: {cust['phone_format_standardized']}")
    report_lines.append(f"Date formats fixed: {cust['date_format_fixed']}")
    report_lines.append(f"Records loaded successfully: {cust['records_loaded']}")
    report_lines.append("")
    
    # Products section
    report_lines.append("PRODUCTS DATA QUALITY METRICS")
    report_lines.append("-" * 80)
    prod = quality_report['products']
    report_lines.append(f"Records read from file: {prod['records_read']}")
    report_lines.append(f"Duplicates removed: {prod['duplicates_removed']}")
    report_lines.append(f"Missing prices handled (dropped): {prod['missing_prices_handled']}")
    report_lines.append(f"Missing stock handled (defaulted to 0): {prod['missing_stock_handled']}")
    report_lines.append(f"Category names standardized: {prod['category_standardized']}")
    report_lines.append(f"Records loaded successfully: {prod['records_loaded']}")
    report_lines.append("")
    
    # Sales section
    report_lines.append("SALES DATA QUALITY METRICS")
    report_lines.append("-" * 80)
    sales = quality_report['sales']
    report_lines.append(f"Records read from file: {sales['records_read']}")
    report_lines.append(f"Duplicates removed: {sales['duplicates_removed']}")
    report_lines.append(f"Records with missing customer_id (dropped): {sales['missing_customer_id_dropped']}")
    report_lines.append(f"Records with missing product_id (dropped): {sales['missing_product_id_dropped']}")
    report_lines.append(f"Date formats fixed: {sales['date_format_fixed']}")
    report_lines.append(f"Order items loaded successfully: {sales['records_loaded']}")
    report_lines.append("")
    
    report_lines.append("=" * 80)
    
    report_text = "\n".join(report_lines)
    
    # Write to file in the part1-database-etl directory
    report_file_path = os.path.join(os.path.dirname(__file__), 'data_quality_report.txt')
    with open(report_file_path, 'w') as f:
        f.write(report_text)
    
    # Print to console
    print("\n" + report_text)
    
    return report_text


def main():
    """
    Main ETL pipeline execution
    """
    print("=" * 80)
    print("FLEXIMART ETL PIPELINE")
    print("=" * 80)
    print()
    
    try:
        # Extract
        customers_df = extract_customers()
        products_df = extract_products()
        sales_df = extract_sales()
        
        # Transform
        customers_df = transform_customers(customers_df)
        products_df = transform_products(products_df)
        sales_df = transform_sales(sales_df)
        
        # Load
        connection = create_database_connection()
        create_tables(connection)
        
        customer_id_mapping = load_customers(connection, customers_df)
        product_id_mapping = load_products(connection, products_df)
        load_orders_improved(connection, sales_df, customer_id_mapping, product_id_mapping)
        
        connection.close()
        print("Database connection closed")
        
        # Generate report
        generate_quality_report()
        
        print("\n" + "=" * 80)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError in ETL pipeline: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
