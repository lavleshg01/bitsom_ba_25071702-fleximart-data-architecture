# FlexiMart Database Schema Documentation

## Entity-Relationship Description (Text Format)

### ENTITY: customers
**Purpose:** Stores customer information and registration details for FlexiMart e-commerce platform.

**Attributes:**
- `customer_id`: Unique identifier for each customer (Primary Key, Auto-increment)
- `first_name`: Customer's first name (Required, VARCHAR(50))
- `last_name`: Customer's last name (Required, VARCHAR(50))
- `email`: Customer's email address (Required, Unique, VARCHAR(100))
- `phone`: Customer's contact phone number (Optional, VARCHAR(20))
- `city`: Customer's city of residence (Optional, VARCHAR(50))
- `registration_date`: Date when customer registered with FlexiMart (Optional, DATE)

**Relationships:**
- One customer can place MANY orders (1:M relationship with orders table)

---

### ENTITY: products
**Purpose:** Stores product catalog information including pricing and inventory details.

**Attributes:**
- `product_id`: Unique identifier for each product (Primary Key, Auto-increment)
- `product_name`: Name of the product (Required, VARCHAR(100))
- `category`: Product category classification (Required, VARCHAR(50))
- `price`: Unit price of the product in INR (Required, DECIMAL(10,2))
- `stock_quantity`: Current inventory quantity available (Default: 0, INT)

**Relationships:**
- One product can appear in MANY order items (1:M relationship with order_items table)

---

### ENTITY: orders
**Purpose:** Stores order header information including customer, date, total amount, and status.

**Attributes:**
- `order_id`: Unique identifier for each order (Primary Key, Auto-increment)
- `customer_id`: Reference to the customer who placed the order (Required, Foreign Key → customers.customer_id)
- `order_date`: Date when the order was placed (Required, DATE)
- `total_amount`: Total amount of the order in INR (Required, DECIMAL(10,2))
- `status`: Current status of the order (Default: 'Pending', VARCHAR(20))
  - Possible values: 'Pending', 'Completed', 'Cancelled'

**Relationships:**
- One order belongs to ONE customer (M:1 relationship with customers table)
- One order contains MANY order items (1:M relationship with order_items table)

---

### ENTITY: order_items
**Purpose:** Stores individual line items within an order, linking products to orders with quantity and pricing details.

**Attributes:**
- `order_item_id`: Unique identifier for each order item (Primary Key, Auto-increment)
- `order_id`: Reference to the parent order (Required, Foreign Key → orders.order_id)
- `product_id`: Reference to the product being ordered (Required, Foreign Key → products.product_id)
- `quantity`: Number of units ordered (Required, INT)
- `unit_price`: Price per unit at the time of order (Required, DECIMAL(10,2))
- `subtotal`: Calculated total for this line item (quantity × unit_price) (Required, DECIMAL(10,2))

**Relationships:**
- One order item belongs to ONE order (M:1 relationship with orders table)
- One order item references ONE product (M:1 relationship with products table)

---

## Normalization Explanation

### Third Normal Form (3NF) Compliance

The FlexiMart database schema is designed in Third Normal Form (3NF), which ensures data integrity and eliminates redundancy while maintaining referential integrity through proper foreign key relationships.

**Functional Dependencies:**
- **customers table:** `customer_id` → `first_name`, `last_name`, `email`, `phone`, `city`, `registration_date`
- **products table:** `product_id` → `product_name`, `category`, `price`, `stock_quantity`
- **orders table:** `order_id` → `customer_id`, `order_date`, `total_amount`, `status`
- **order_items table:** `order_item_id` → `order_id`, `product_id`, `quantity`, `unit_price`, `subtotal`

**3NF Compliance:**
The schema satisfies 3NF requirements because:
1. **No transitive dependencies:** Each non-key attribute depends directly on the primary key, not on other non-key attributes. For example, in order_items, `subtotal` is calculated from `quantity` and `unit_price`, but these are stored independently without creating transitive dependencies.
2. **Separation of concerns:** Customer information is isolated in the customers table, preventing duplication across orders. Product details are stored once in the products table, avoiding redundancy when products appear in multiple orders.
3. **Referential integrity:** Foreign keys maintain relationships without storing redundant data. The `customer_id` in orders references customers without duplicating customer information.

**Anomaly Prevention:**
- **Update anomalies avoided:** Changing a customer's email or a product's price requires updates in only one location (customers or products table), not across multiple order records.
- **Insert anomalies avoided:** New products can be added without requiring an order, and new customers can be registered without placing orders.
- **Delete anomalies avoided:** Deleting an order does not remove customer or product information, and deleting a product does not cascade to customer records.

This normalized design ensures data consistency, reduces storage requirements, and simplifies maintenance while supporting efficient querying through proper indexing and relationships.

---

## Sample Data Representation

### customers Table

| customer_id | first_name | last_name | email | phone | city | registration_date |
|-------------|------------|-----------|-------|-------|------|-------------------|
| 1 | Rahul | Sharma | rahul.sharma@gmail.com | +91-9876543210 | Bangalore | 2023-01-15 |
| 2 | Priya | Patel | priya.patel@yahoo.com | +91-9988776655 | Mumbai | 2023-02-20 |
| 3 | Amit | Kumar | amit.kumar.C003@fleximart.placeholder.com | +91-9765432109 | Delhi | 2023-03-10 |

---

### products Table

| product_id | product_name | category | price | stock_quantity |
|------------|--------------|----------|--------|----------------|
| 1 | Samsung Galaxy S21 | Electronics | 45999.00 | 150 |
| 2 | Nike Running Shoes | Fashion | 3499.00 | 80 |
| 3 | Basmati Rice 5kg | Groceries | 650.00 | 300 |

---

### orders Table

| order_id | customer_id | order_date | total_amount | status |
|----------|-------------|------------|--------------|--------|
| 1 | 1 | 2024-01-15 | 45999.00 | Completed |
| 2 | 2 | 2024-01-16 | 5998.00 | Completed |
| 3 | 3 | 2024-01-20 | 1950.00 | Completed |

---

### order_items Table

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|---------------|----------|------------|-----------|------------|----------|
| 1 | 1 | 1 | 1 | 45999.00 | 45999.00 |
| 2 | 2 | 4 | 2 | 2999.00 | 5998.00 |
| 3 | 3 | 9 | 3 | 650.00 | 1950.00 |

---

## Entity Relationship Diagram (Text Representation)

```
customers (1) ────────< (M) orders
                              │
                              │ (1)
                              │
                              │
                              └───────< (M) order_items
                                        │
                                        │ (M)
                                        │
                                        │
products (1) ───────────────────────────┘
```

**Legend:**
- (1) = One
- (M) = Many
- ──────── = Relationship line
- < = Relationship direction
