# FlexiMart Data Architecture Project

**Student Name:** Lavlesh Mishrilal Gupta
**Student ID:** bitsom_ba_25071702
**Email:** lavleshgupta01@gmail.com
**Date:** 21-12-2025

## Project Overview

This project implements a comprehensive data architecture solution for FlexiMart, an e-commerce platform, covering three key components: a robust ETL pipeline that processes and cleans raw customer, product, and sales data into a normalized MySQL database; a NoSQL analysis using MongoDB for flexible product catalog management; and a data warehouse design with a star schema for advanced analytics and reporting. The solution addresses real-world data quality challenges including duplicate records, missing values, inconsistent formats, and provides business intelligence through SQL queries for customer analytics, product sales analysis, and monthly sales trends.

## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

- Python 3.x, pandas, mysql-connector-python
- MySQL 8.0 / PostgreSQL 14
- MongoDB 6.0

## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


### MongoDB Setup

mongosh < part2-nosql/mongodb_operations.js

## Key Learnings

Through this project, I gained hands-on experience in building end-to-end data pipelines, understanding the critical importance of data quality validation and transformation in ETL processes. I learned how to design normalized database schemas (3NF) that prevent data anomalies while maintaining referential integrity through proper foreign key relationships. The project deepened my understanding of SQL window functions for calculating running totals and cumulative metrics, as well as advanced query techniques using GROUP BY, HAVING clauses, and complex joins across multiple tables. Additionally, I developed skills in handling real-world data quality issues such as duplicate records, missing values, inconsistent date formats, and standardizing data formats programmatically using Python and pandas.

## Challenges Faced

1. The raw CSV files used string-based IDs (C001, P001, etc.), but the database schema uses auto-increment integer IDs. This created a challenge when loading sales data that referenced these original IDs. **Solution**: I implemented ID mapping dictionaries during the customer and product load processes, storing the relationship between original CSV IDs and generated database IDs, which were then used to correctly link order_items to the right customers and products.

2. The raw data contained dates in various formats (YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY, etc.), making it difficult to parse and standardize. **Solution**: I created a robust `parse_date()` function that attempts multiple date format patterns sequentially using Python's `datetime.strptime()`, ensuring all dates are converted to the standard YYYY-MM-DD format before database insertion.

3. One key challenge in implementing the FlexiMart star schema was maintaining data consistency while generating and managing surrogate keys, especially for the dim_date, dim_product, and dim_customer tables. Since the data warehouse uses surrogate keys instead of natural keys, the ETL process must ensure accurate mapping between operational data and dimension records. Any mismatch or duplicate surrogate key generation can lead to incorrect fact-to-dimension relationships, resulting in inaccurate analytical results. This challenge becomes more complex when loading incremental data, as existing dimension records must be identified correctly to avoid duplication while preserving historical accuracy.