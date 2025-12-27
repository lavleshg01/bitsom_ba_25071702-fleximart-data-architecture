# Star Schema Design for FlexiMart Data Warehouse

## Section 1: Schema Overview

### FACT TABLE: fact_sales

**Grain:** One row per product per order line item

**Business Process:** Sales transactions

**Measures (Numeric Facts):**
- `quantity_sold`: Number of units sold (INTEGER, NOT NULL)
- `unit_price`: Price per unit at time of sale (DECIMAL(10,2), NOT NULL)
- `discount_amount`: Discount applied to the line item (DECIMAL(10,2), DEFAULT 0.00)
- `total_amount`: Final amount for the line item, calculated as (quantity_sold × unit_price - discount_amount) (DECIMAL(10,2), NOT NULL)

**Foreign Keys:**
- `date_key`: References dim_date.date_key (INTEGER, NOT NULL)
- `product_key`: References dim_product.product_key (INTEGER, NOT NULL)
- `customer_key`: References dim_customer.customer_key (INTEGER, NOT NULL)

**Primary Key:** Composite key on (date_key, product_key, customer_key) or a surrogate key `sales_key` (INTEGER, AUTO_INCREMENT)

**Additional Attributes:**
- `order_id`: Original order identifier from source system (VARCHAR(50), optional for traceability)
- `transaction_id`: Original transaction identifier (VARCHAR(50), optional)

---

### DIMENSION TABLE: dim_date

**Purpose:** Date dimension for time-based analysis and reporting

**Type:** Conformed dimension (can be shared across multiple fact tables)

**Attributes:**
- `date_key` (PK): Surrogate key, integer format YYYYMMDD (e.g., 20240115 for January 15, 2024) (INTEGER, PRIMARY KEY)
- `full_date`: Actual date value (DATE, NOT NULL)
- `day_of_week`: Day name (Monday, Tuesday, Wednesday, etc.) (VARCHAR(10))
- `day_of_month`: Day number 1-31 (INTEGER)
- `day_of_year`: Day number 1-366 (INTEGER)
- `week_of_year`: Week number 1-53 (INTEGER)
- `month`: Month number 1-12 (INTEGER)
- `month_name`: Full month name (January, February, etc.) (VARCHAR(20))
- `month_abbreviation`: Short month name (Jan, Feb, etc.) (VARCHAR(3))
- `quarter`: Quarter identifier (Q1, Q2, Q3, Q4) (VARCHAR(2))
- `quarter_number`: Quarter number 1-4 (INTEGER)
- `year`: Year value (e.g., 2023, 2024) (INTEGER)
- `is_weekend`: Boolean flag indicating if date falls on weekend (BOOLEAN, DEFAULT FALSE)
- `is_holiday`: Boolean flag indicating if date is a holiday (BOOLEAN, DEFAULT FALSE)
- `fiscal_year`: Fiscal year if different from calendar year (INTEGER, optional)
- `fiscal_quarter`: Fiscal quarter if different from calendar quarter (VARCHAR(2), optional)

**Indexes:**
- Primary key on `date_key`
- Index on `full_date` for date range queries
- Index on `year`, `quarter`, `month` for time-based aggregations

---

### DIMENSION TABLE: dim_product

**Purpose:** Product dimension containing product attributes for analysis and filtering

**Type:** Slowly Changing Dimension (SCD) - Type 2 for historical tracking of price/category changes

**Attributes:**
- `product_key` (PK): Surrogate key, auto-increment integer (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- `product_id`: Natural key from source system (INTEGER, NOT NULL)
- `product_name`: Name of the product (VARCHAR(100), NOT NULL)
- `category`: Product category (Electronics, Clothing, etc.) (VARCHAR(50), NOT NULL)
- `subcategory`: Product subcategory if applicable (VARCHAR(50), optional)
- `brand`: Product brand name (VARCHAR(50), optional)
- `current_price`: Current price of the product (DECIMAL(10,2), optional)
- `price_at_sale`: Price at time of sale (for historical accuracy) (DECIMAL(10,2), optional)
- `stock_status`: Current stock status (In Stock, Out of Stock, Low Stock) (VARCHAR(20), optional)
- `is_active`: Boolean flag indicating if product is currently active (BOOLEAN, DEFAULT TRUE)
- `effective_date`: Date when this product version became effective (DATE, NOT NULL)
- `expiry_date`: Date when this product version expired (DATE, NULL for current version)
- `is_current`: Boolean flag indicating if this is the current version (BOOLEAN, DEFAULT TRUE)

**Indexes:**
- Primary key on `product_key`
- Index on `product_id` for lookups
- Index on `category` for category-based analysis
- Index on `is_current` for filtering current products

---

### DIMENSION TABLE: dim_customer

**Purpose:** Customer dimension containing customer attributes for segmentation and analysis

**Type:** Slowly Changing Dimension (SCD) - Type 1 for current customer information

**Attributes:**
- `customer_key` (PK): Surrogate key, auto-increment integer (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
- `customer_id`: Natural key from source system (INTEGER, NOT NULL)
- `customer_name`: Full name (concatenated first_name + last_name) (VARCHAR(100), NOT NULL)
- `first_name`: Customer's first name (VARCHAR(50), NOT NULL)
- `last_name`: Customer's last name (VARCHAR(50), NOT NULL)
- `email`: Customer's email address (VARCHAR(100), optional)
- `phone`: Customer's contact phone number (VARCHAR(20), optional)
- `city`: Customer's city of residence (VARCHAR(50), optional)
- `state`: Customer's state (VARCHAR(50), optional)
- `country`: Customer's country (VARCHAR(50), DEFAULT 'India')
- `registration_date`: Date when customer registered (DATE, optional)
- `customer_segment`: Customer segmentation (New, Regular, VIP, etc.) (VARCHAR(20), optional)
- `lifetime_value`: Calculated customer lifetime value (DECIMAL(12,2), optional)
- `is_active`: Boolean flag indicating if customer is active (BOOLEAN, DEFAULT TRUE)

**Indexes:**
- Primary key on `customer_key`
- Index on `customer_id` for lookups
- Index on `city` for geographic analysis
- Index on `customer_segment` for segmentation analysis

---

## Section 2: Design Decisions

The star schema design for FlexiMart's data warehouse is based on transaction line-item granularity, which provides maximum analytical flexibility while maintaining query performance. This granularity was chosen because it captures the most atomic level of sales data—each product sold in each order—enabling drill-down to individual transactions and roll-up to any desired aggregation level (daily, monthly, by product, by customer, or combinations thereof).

Surrogate keys are used instead of natural keys for several critical reasons. First, they provide independence from source system changes—if product IDs or customer IDs change in the operational system, the data warehouse remains stable. Second, surrogate keys (especially date_key in YYYYMMDD format) enable efficient indexing and partitioning strategies. Third, they support slowly changing dimensions (SCD) by allowing multiple versions of the same product or customer to coexist with different effective dates, preserving historical accuracy.

This design excellently supports drill-down and roll-up operations. Analysts can start with high-level aggregates (total sales by quarter) and drill down to monthly, weekly, or daily levels using the rich date dimension. Similarly, they can roll up from individual products to categories or from specific customers to segments. The denormalized dimension tables eliminate the need for complex joins during analysis, significantly improving query performance for business intelligence and reporting workloads.

---

## Section 3: Sample Data Flow

### Source Transaction (Operational Database):

**Order Table:**
- Order #101
- Customer ID: 12 (John Doe)
- Order Date: 2024-01-15
- Status: Completed

**Order Items Table:**
- Order #101, Line Item 1
- Product ID: 5 (Laptop)
- Quantity: 2
- Unit Price: 50000
- Discount: 0
- Subtotal: 100000

**Customer Table:**
- Customer ID: 12
- First Name: John
- Last Name: Doe
- City: Mumbai
- Email: john.doe@email.com

**Product Table:**
- Product ID: 5
- Product Name: Laptop
- Category: Electronics
- Current Price: 50000

---

### Transformed Data in Data Warehouse:

**fact_sales:**
```sql
{
  sales_key: 1001,
  date_key: 20240115,
  product_key: 5,
  customer_key: 12,
  quantity_sold: 2,
  unit_price: 50000.00,
  discount_amount: 0.00,
  total_amount: 100000.00,
  order_id: '101'
}
```

**dim_date:**
```sql
{
  date_key: 20240115,
  full_date: '2024-01-15',
  day_of_week: 'Monday',
  day_of_month: 15,
  month: 1,
  month_name: 'January',
  quarter: 'Q1',
  quarter_number: 1,
  year: 2024,
  is_weekend: FALSE,
  is_holiday: FALSE
}
```

**dim_product:**
```sql
{
  product_key: 5,
  product_id: 5,
  product_name: 'Laptop',
  category: 'Electronics',
  subcategory: 'Computers',
  brand: 'TechBrand',
  current_price: 50000.00,
  price_at_sale: 50000.00,
  stock_status: 'In Stock',
  is_active: TRUE,
  effective_date: '2024-01-01',
  expiry_date: NULL,
  is_current: TRUE
}
```

**dim_customer:**
```sql
{
  customer_key: 12,
  customer_id: 12,
  customer_name: 'John Doe',
  first_name: 'John',
  last_name: 'Doe',
  email: 'john.doe@email.com',
  phone: '+91-9876543210',
  city: 'Mumbai',
  state: 'Maharashtra',
  country: 'India',
  registration_date: '2023-06-10',
  customer_segment: 'Regular',
  is_active: TRUE
}
```

### Data Flow Process:

1. **Extract:** ETL process extracts the order, order_items, customer, and product records from the operational database.

2. **Transform:**
   - Date dimension lookup/creation: Converts '2024-01-15' to date_key 20240115 and populates all date attributes
   - Product dimension lookup: Retrieves product_key 5 for product_id 5, or creates new entry if product is new
   - Customer dimension lookup: Retrieves customer_key 12 for customer_id 12, or creates new entry if customer is new
   - Calculate measures: Computes total_amount = quantity_sold × unit_price - discount_amount

3. **Load:** Inserts the transformed fact record into fact_sales table with appropriate foreign key references to all dimension tables.

This design allows analysts to query sales by any combination of time periods, products, and customers with simple joins, enabling powerful business intelligence capabilities.

