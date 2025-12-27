-- Data Warehouse Sample Data
-- Database: fleximart_dw

-- ============================================
-- DIM_DATE: 30 dates (January-February 2024)
-- ============================================

INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, FALSE),
(20240102, '2024-01-02', 'Tuesday', 2, 1, 'January', 'Q1', 2024, FALSE),
(20240103, '2024-01-03', 'Wednesday', 3, 1, 'January', 'Q1', 2024, FALSE),
(20240104, '2024-01-04', 'Thursday', 4, 1, 'January', 'Q1', 2024, FALSE),
(20240105, '2024-01-05', 'Friday', 5, 1, 'January', 'Q1', 2024, FALSE),
(20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, TRUE),
(20240107, '2024-01-07', 'Sunday', 7, 1, 'January', 'Q1', 2024, TRUE),
(20240108, '2024-01-08', 'Monday', 8, 1, 'January', 'Q1', 2024, FALSE),
(20240109, '2024-01-09', 'Tuesday', 9, 1, 'January', 'Q1', 2024, FALSE),
(20240110, '2024-01-10', 'Wednesday', 10, 1, 'January', 'Q1', 2024, FALSE),
(20240111, '2024-01-11', 'Thursday', 11, 1, 'January', 'Q1', 2024, FALSE),
(20240112, '2024-01-12', 'Friday', 12, 1, 'January', 'Q1', 2024, FALSE),
(20240113, '2024-01-13', 'Saturday', 13, 1, 'January', 'Q1', 2024, TRUE),
(20240114, '2024-01-14', 'Sunday', 14, 1, 'January', 'Q1', 2024, TRUE),
(20240115, '2024-01-15', 'Monday', 15, 1, 'January', 'Q1', 2024, FALSE),
(20240116, '2024-01-16', 'Tuesday', 16, 1, 'January', 'Q1', 2024, FALSE),
(20240117, '2024-01-17', 'Wednesday', 17, 1, 'January', 'Q1', 2024, FALSE),
(20240118, '2024-01-18', 'Thursday', 18, 1, 'January', 'Q1', 2024, FALSE),
(20240119, '2024-01-19', 'Friday', 19, 1, 'January', 'Q1', 2024, FALSE),
(20240120, '2024-01-20', 'Saturday', 20, 1, 'January', 'Q1', 2024, TRUE),
(20240121, '2024-01-21', 'Sunday', 21, 1, 'January', 'Q1', 2024, TRUE),
(20240122, '2024-01-22', 'Monday', 22, 1, 'January', 'Q1', 2024, FALSE),
(20240123, '2024-01-23', 'Tuesday', 23, 1, 'January', 'Q1', 2024, FALSE),
(20240124, '2024-01-24', 'Wednesday', 24, 1, 'January', 'Q1', 2024, FALSE),
(20240125, '2024-01-25', 'Thursday', 25, 1, 'January', 'Q1', 2024, FALSE),
(20240126, '2024-01-26', 'Friday', 26, 1, 'January', 'Q1', 2024, FALSE),
(20240127, '2024-01-27', 'Saturday', 27, 1, 'January', 'Q1', 2024, TRUE),
(20240128, '2024-01-28', 'Sunday', 28, 1, 'January', 'Q1', 2024, TRUE),
(20240201, '2024-02-01', 'Thursday', 1, 2, 'February', 'Q1', 2024, FALSE),
(20240202, '2024-02-02', 'Friday', 2, 2, 'February', 'Q1', 2024, FALSE);

-- ============================================
-- DIM_PRODUCT: 15 products across 3 categories
-- ============================================

INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
-- Electronics (5 products)
('ELEC001', 'Samsung Galaxy S21 Ultra', 'Electronics', 'Smartphones', 79999.00),
('ELEC002', 'Apple MacBook Pro 14-inch', 'Electronics', 'Laptops', 189999.00),
('ELEC003', 'Sony WH-1000XM5 Headphones', 'Electronics', 'Audio', 29990.00),
('ELEC004', 'Canon EOS R6 Camera', 'Electronics', 'Cameras', 189999.00),
('ELEC005', 'iPad Air 5th Gen', 'Electronics', 'Tablets', 54999.00),

-- Clothing (5 products)
('CLO001', 'Nike Air Max 270', 'Clothing', 'Footwear', 8999.00),
('CLO002', 'Levi\'s 501 Jeans', 'Clothing', 'Apparel', 2999.00),
('CLO003', 'Adidas Ultraboost 22', 'Clothing', 'Footwear', 12999.00),
('CLO004', 'Zara Cotton T-Shirt', 'Clothing', 'Apparel', 999.00),
('CLO005', 'Puma Running Shoes', 'Clothing', 'Footwear', 4999.00),

-- Home & Kitchen (5 products)
('HOME001', 'Instant Pot Duo 7-in-1', 'Home & Kitchen', 'Kitchen Appliances', 8999.00),
('HOME002', 'Dyson V15 Vacuum Cleaner', 'Home & Kitchen', 'Home Appliances', 49999.00),
('HOME003', 'Philips Air Fryer', 'Home & Kitchen', 'Kitchen Appliances', 12999.00),
('HOME004', 'KitchenAid Stand Mixer', 'Home & Kitchen', 'Kitchen Appliances', 59999.00),
('HOME005', 'Bamboo Cutting Board Set', 'Home & Kitchen', 'Kitchen Accessories', 1299.00);

-- ============================================
-- DIM_CUSTOMER: 12 customers across 4 cities
-- ============================================

INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
-- Mumbai (3 customers)
('C001', 'Rajesh Kumar', 'Mumbai', 'Maharashtra', 'VIP'),
('C002', 'Priya Sharma', 'Mumbai', 'Maharashtra', 'Regular'),
('C003', 'Amit Patel', 'Mumbai', 'Maharashtra', 'New'),

-- Delhi (3 customers)
('C004', 'Sneha Gupta', 'Delhi', 'Delhi', 'Regular'),
('C005', 'Vikram Singh', 'Delhi', 'Delhi', 'VIP'),
('C006', 'Anjali Mehta', 'Delhi', 'Delhi', 'Regular'),

-- Bangalore (3 customers)
('C007', 'Rahul Nair', 'Bangalore', 'Karnataka', 'Regular'),
('C008', 'Kavita Reddy', 'Bangalore', 'Karnataka', 'VIP'),
('C009', 'Suresh Iyer', 'Bangalore', 'Karnataka', 'New'),

-- Chennai (3 customers)
('C010', 'Lakshmi Venkatesh', 'Chennai', 'Tamil Nadu', 'Regular'),
('C011', 'Arjun Krishnan', 'Chennai', 'Tamil Nadu', 'VIP'),
('C012', 'Meera Raman', 'Chennai', 'Tamil Nadu', 'New');

-- ============================================
-- FACT_SALES: 40 sales transactions
-- Pattern: Higher sales on weekends, varied quantities
-- ============================================

-- Weekday Sales (January 1-5, 8-12, 15-19, 22-26) - Lower volume
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- January 1 (Monday)
(20240101, 1, 1, 1, 79999.00, 0.00, 79999.00),
(20240101, 6, 4, 2, 8999.00, 500.00, 17498.00),

-- January 2 (Tuesday)
(20240102, 3, 7, 1, 29990.00, 0.00, 29990.00),
(20240102, 10, 10, 1, 8999.00, 0.00, 8999.00),

-- January 3 (Wednesday)
(20240103, 2, 5, 1, 189999.00, 10000.00, 179999.00),
(20240103, 8, 2, 1, 12999.00, 0.00, 12999.00),

-- January 4 (Thursday)
(20240104, 5, 8, 1, 54999.00, 0.00, 54999.00),
(20240104, 12, 6, 1, 12999.00, 0.00, 12999.00),

-- January 5 (Friday)
(20240105, 4, 11, 1, 189999.00, 5000.00, 184999.00),
(20240105, 9, 3, 3, 999.00, 0.00, 2997.00),

-- January 8 (Monday)
(20240108, 1, 4, 1, 79999.00, 0.00, 79999.00),
(20240108, 7, 9, 1, 2999.00, 0.00, 2999.00),

-- January 9 (Tuesday)
(20240109, 3, 1, 1, 29990.00, 0.00, 29990.00),
(20240109, 11, 7, 1, 49999.00, 2000.00, 47999.00),

-- January 10 (Wednesday)
(20240110, 2, 2, 1, 189999.00, 0.00, 189999.00),
(20240110, 13, 10, 1, 12999.00, 0.00, 12999.00),

-- January 11 (Thursday)
(20240111, 5, 5, 1, 54999.00, 0.00, 54999.00),
(20240111, 15, 12, 2, 1299.00, 0.00, 2598.00),

-- January 12 (Friday)
(20240112, 4, 8, 1, 189999.00, 0.00, 189999.00),
(20240112, 6, 6, 1, 8999.00, 0.00, 8999.00),

-- January 15 (Monday)
(20240115, 1, 11, 1, 79999.00, 0.00, 79999.00),
(20240115, 8, 3, 2, 12999.00, 1000.00, 24998.00),

-- January 16 (Tuesday)
(20240116, 3, 4, 1, 29990.00, 0.00, 29990.00),
(20240116, 10, 9, 1, 8999.00, 0.00, 8999.00),

-- January 17 (Wednesday)
(20240117, 2, 1, 1, 189999.00, 15000.00, 174999.00),
(20240117, 7, 7, 2, 2999.00, 0.00, 5998.00),

-- January 18 (Thursday)
(20240118, 5, 2, 1, 54999.00, 0.00, 54999.00),
(20240118, 12, 10, 1, 12999.00, 0.00, 12999.00),

-- January 19 (Friday)
(20240119, 4, 5, 1, 189999.00, 0.00, 189999.00),
(20240119, 9, 11, 4, 999.00, 0.00, 3996.00),

-- January 22 (Monday)
(20240122, 1, 8, 1, 79999.00, 0.00, 79999.00),
(20240122, 6, 12, 1, 8999.00, 0.00, 8999.00),

-- January 23 (Tuesday)
(20240123, 3, 6, 1, 29990.00, 0.00, 29990.00),
(20240123, 11, 2, 1, 49999.00, 0.00, 49999.00),

-- January 24 (Wednesday)
(20240124, 2, 3, 1, 189999.00, 0.00, 189999.00),
(20240124, 13, 11, 1, 12999.00, 0.00, 12999.00),

-- January 25 (Thursday)
(20240125, 5, 4, 1, 54999.00, 0.00, 54999.00),
(20240125, 15, 1, 3, 1299.00, 0.00, 3897.00),

-- January 26 (Friday)
(20240126, 4, 7, 1, 189999.00, 0.00, 189999.00),
(20240126, 8, 9, 1, 12999.00, 0.00, 12999.00);

-- Weekend Sales (January 6-7, 13-14, 20-21, 27-28) - Higher volume
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- January 6 (Saturday) - Weekend shopping
(20240106, 1, 1, 1, 79999.00, 5000.00, 74999.00),
(20240106, 6, 2, 2, 8999.00, 1000.00, 16998.00),
(20240106, 3, 5, 1, 29990.00, 0.00, 29990.00),
(20240106, 10, 8, 1, 8999.00, 0.00, 8999.00),

-- January 7 (Sunday) - Weekend shopping
(20240107, 2, 11, 1, 189999.00, 10000.00, 179999.00),
(20240107, 8, 3, 2, 12999.00, 500.00, 25498.00),
(20240107, 5, 6, 1, 54999.00, 0.00, 54999.00),
(20240107, 12, 10, 1, 12999.00, 0.00, 12999.00),

-- January 13 (Saturday) - Weekend shopping
(20240113, 4, 4, 1, 189999.00, 0.00, 189999.00),
(20240113, 7, 9, 3, 2999.00, 0.00, 8997.00),
(20240113, 1, 7, 1, 79999.00, 0.00, 79999.00),
(20240113, 11, 2, 1, 49999.00, 3000.00, 46999.00),

-- January 14 (Sunday) - Weekend shopping
(20240114, 3, 1, 1, 29990.00, 0.00, 29990.00),
(20240114, 9, 5, 5, 999.00, 0.00, 4995.00),
(20240114, 2, 8, 1, 189999.00, 0.00, 189999.00),
(20240114, 13, 12, 1, 12999.00, 0.00, 12999.00),

-- January 20 (Saturday) - Weekend shopping
(20240120, 5, 3, 1, 54999.00, 0.00, 54999.00),
(20240120, 6, 10, 2, 8999.00, 500.00, 17498.00),
(20240120, 1, 11, 1, 79999.00, 5000.00, 74999.00),
(20240120, 15, 6, 2, 1299.00, 0.00, 2598.00),

-- January 21 (Sunday) - Weekend shopping
(20240121, 4, 7, 1, 189999.00, 0.00, 189999.00),
(20240121, 8, 1, 1, 12999.00, 0.00, 12999.00),
(20240121, 2, 4, 1, 189999.00, 15000.00, 174999.00),
(20240121, 12, 9, 1, 12999.00, 0.00, 12999.00),

-- January 27 (Saturday) - Weekend shopping
(20240127, 3, 2, 1, 29990.00, 0.00, 29990.00),
(20240127, 10, 5, 1, 8999.00, 0.00, 8999.00),
(20240127, 1, 8, 1, 79999.00, 0.00, 79999.00),
(20240127, 7, 12, 2, 2999.00, 0.00, 5998.00),

-- January 28 (Sunday) - Weekend shopping
(20240128, 5, 10, 1, 54999.00, 0.00, 54999.00),
(20240128, 11, 3, 1, 49999.00, 0.00, 49999.00),
(20240128, 2, 6, 1, 189999.00, 0.00, 189999.00),
(20240128, 13, 11, 1, 12999.00, 0.00, 12999.00);

-- February Sales
INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- February 1 (Thursday)
(20240201, 1, 1, 1, 79999.00, 0.00, 79999.00),
(20240201, 6, 4, 1, 8999.00, 0.00, 8999.00),

-- February 2 (Friday)
(20240202, 3, 7, 1, 29990.00, 0.00, 29990.00),
(20240202, 10, 10, 1, 8999.00, 0.00, 8999.00);

