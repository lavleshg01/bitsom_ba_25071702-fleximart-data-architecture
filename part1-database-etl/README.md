# Part 1: Database ETL Pipeline

## Overview

Part 1 of the FlexiMart Data Architecture project focuses on building a robust Extract, Transform, and Load (ETL) pipeline that processes raw customer, product, and sales data into a normalized MySQL relational database. This component addresses real-world data quality challenges and implements a comprehensive data cleaning and transformation process.

## Objectives

- Extract data from raw CSV files (customers, products, sales)
- Transform and clean data to handle quality issues:
  - Remove duplicate records
  - Handle missing values (emails, phone numbers, prices, stock)
  - Standardize date formats (multiple formats to YYYY-MM-DD)
  - Standardize phone number formats
  - Normalize category names
- Load cleaned data into a normalized MySQL database (3NF)
- Generate data quality reports
- Execute business intelligence queries for analytics

## Components

### 1. ETL Pipeline (`etl_pipeline.py`)
- Python script that orchestrates the entire ETL process
- Handles data extraction from CSV files
- Implements data transformation and cleaning logic
- Manages database connections and data loading
- Tracks data quality metrics throughout the process
- Generates comprehensive data quality reports

### 2. Database Schema (`schema_documentation.md`)
- Documents the normalized database design
- Defines table structures and relationships
- Explains foreign key constraints and referential integrity
- Describes the 3NF normalization approach

### 3. Business Queries (`business_queries.sql`)
- SQL queries for business intelligence and analytics
- Customer analytics queries
- Product sales analysis
- Monthly sales trends and reporting
- Advanced SQL techniques (window functions, aggregations, joins)

### 4. Data Quality Report (`data_quality_report.txt`)
- Generated report showing data quality metrics
- Tracks duplicates removed, missing values handled
- Records format standardization statistics
- Provides insights into data cleaning effectiveness

## Key Features

- **Data Quality Handling**: Comprehensive approach to handling duplicates, missing values, and inconsistent formats
- **ID Mapping**: Intelligent mapping between string-based CSV IDs and auto-increment database IDs
- **Date Parsing**: Robust date format handling supporting multiple input formats
- **Normalized Schema**: 3NF database design preventing data anomalies
- **Referential Integrity**: Proper foreign key relationships ensuring data consistency

## Technologies

- **Python 3.x**: Core programming language
- **pandas**: Data manipulation and processing
- **mysql-connector-python**: MySQL database connectivity
- **MySQL 8.0**: Relational database management system

## Setup and Execution

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create MySQL database:
   ```bash
   mysql -u root -p -e "CREATE DATABASE fleximart;"
   ```

3. Update database credentials in `etl_pipeline.py`:
   - Modify `DB_CONFIG` dictionary with your MySQL credentials

4. Ensure raw data files are in the `data/` directory:
   - `customers_raw.csv`
   - `products_raw.csv`
   - `sales_raw.csv`

5. Run the ETL pipeline:
   ```bash
   python etl_pipeline.py
   ```

6. Execute business queries:
   ```bash
   mysql -u root -p fleximart < business_queries.sql
   ```

## Output

- Normalized MySQL database with cleaned data
- Data quality report showing transformation statistics
- Business intelligence insights from SQL queries

