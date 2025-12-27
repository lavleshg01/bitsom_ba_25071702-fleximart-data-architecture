# Part 3: Data Warehouse with Star Schema

## Overview

Part 3 of the FlexiMart Data Architecture project focuses on designing and implementing a data warehouse using a star schema architecture. This component transforms normalized operational data into a denormalized dimensional model optimized for business intelligence, analytics, and reporting. The star schema design enables fast query performance and supports complex analytical queries across time, products, and customers.

## Objectives

- Design a star schema data warehouse architecture
- Implement fact and dimension tables for sales analytics
- Create a date dimension for time-based analysis
- Build product and customer dimensions for segmentation
- Load sample data demonstrating realistic sales patterns
- Support drill-down and roll-up operations for multi-dimensional analysis
- Enable efficient analytical queries for business intelligence

## Components

### 1. Star Schema Design (`star_schema_design.md`)
Comprehensive documentation covering:

- **Section 1: Schema Overview**
  - Detailed description of fact table (`fact_sales`) with measures and foreign keys
  - Dimension tables: `dim_date`, `dim_product`, `dim_customer`
  - Complete attribute definitions and data types
  - Primary keys, foreign keys, and relationships

- **Section 2: Design Decisions (150 words)**
  - Rationale for transaction line-item granularity
  - Justification for surrogate keys vs. natural keys
  - Explanation of drill-down and roll-up capabilities

- **Section 3: Sample Data Flow**
  - Example transformation from operational database to data warehouse
  - Step-by-step data flow process
  - Sample records for all tables

### 2. Warehouse Schema (`warehouse_schema.sql`)
SQL DDL scripts creating:

- **fact_sales**: Fact table with sales measures
  - `quantity_sold`, `unit_price`, `discount_amount`, `total_amount`
  - Foreign keys to all dimension tables
  
- **dim_date**: Date dimension for time analysis
  - Date attributes: day_of_week, month, quarter, year, is_weekend
  - Surrogate key in YYYYMMDD format
  
- **dim_product**: Product dimension
  - Product attributes: name, category, subcategory, unit_price
  - Supports product-based analysis and filtering
  
- **dim_customer**: Customer dimension
  - Customer attributes: name, city, state, customer_segment
  - Enables customer segmentation and geographic analysis

### 3. Warehouse Data (`warehouse_data.sql`)
Sample data INSERT statements:

- **30 dates**: January-February 2024 (mix of weekdays and weekends)
- **15 products**: Across 3 categories (Electronics, Clothing, Home & Kitchen)
  - Price range: ₹999 to ₹189,999
- **12 customers**: Across 4 cities (Mumbai, Delhi, Bangalore, Chennai)
  - Customer segments: VIP, Regular, New
- **40 sales transactions**: Realistic sales patterns
  - Higher sales volume on weekends
  - Varied quantities (1-5 units)
  - Discounts applied to selected transactions

### 4. Analytics Queries (`analytics_queries.sql`)
SQL queries for business intelligence (if created):
- Sales analysis by time period (daily, monthly, quarterly)
- Product performance analysis by category
- Customer segmentation and lifetime value
- Geographic sales analysis
- Weekend vs. weekday sales patterns

## Key Features

- **Star Schema Architecture**: Denormalized design optimized for analytical queries
- **Surrogate Keys**: Date keys in YYYYMMDD format for efficient indexing
- **Time Intelligence**: Rich date dimension supporting multiple time-based analyses
- **Multi-Dimensional Analysis**: Support for drill-down and roll-up operations
- **Realistic Data Patterns**: Sample data reflecting real-world sales behaviors
- **Query Performance**: Denormalized structure eliminates complex joins

## Star Schema Benefits

1. **Fast Query Performance**: Denormalized structure reduces join complexity
2. **Easy to Understand**: Intuitive star structure for business users
3. **Flexible Analysis**: Supports multiple analytical perspectives
4. **Scalable Design**: Can accommodate additional dimensions and facts
5. **Time Intelligence**: Comprehensive date dimension for temporal analysis

## Technologies

- **MySQL 8.0**: Relational database management system for data warehouse
- **SQL**: Data Definition Language (DDL) and Data Manipulation Language (DML)
- **Dimensional Modeling**: Star schema design methodology

## Setup and Execution

1. Create data warehouse database:
   ```bash
   mysql -u root -p -e "CREATE DATABASE fleximart_dw;"
   ```

2. Create star schema tables:
   ```bash
   mysql -u root -p fleximart_dw < warehouse_schema.sql
   ```

3. Load sample data:
   ```bash
   mysql -u root -p fleximart_dw < warehouse_data.sql
   ```

4. Execute analytics queries (if available):
   ```bash
   mysql -u root -p fleximart_dw < analytics_queries.sql
   ```

## Schema Structure

```
                    fact_sales
                        |
        +---------------+---------------+---+
        |               |               |
    dim_date      dim_product    dim_customer
```

- **Fact Table**: `fact_sales` (center) contains measurable business events
- **Dimension Tables**: Surrounding tables provide descriptive context
- **Relationships**: Foreign keys link facts to dimensions

## Data Warehouse vs. Operational Database

| Aspect | Operational DB (Part 1) | Data Warehouse (Part 3) |
|--------|------------------------|------------------------|
| **Purpose** | Transaction processing | Analytics and reporting |
| **Schema** | Normalized (3NF) | Denormalized (Star) |
| **Optimization** | Write performance | Read performance |
| **Data Model** | Entity-Relationship | Dimensional |
| **Queries** | Simple, frequent | Complex, analytical |

## Output

- Star schema data warehouse with fact and dimension tables
- Sample data demonstrating realistic sales patterns
- Documentation explaining design decisions and data flow
- Foundation for business intelligence and analytics queries

