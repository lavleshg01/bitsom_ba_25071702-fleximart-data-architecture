# Part 2: NoSQL Analysis with MongoDB

## Overview

Part 2 of the FlexiMart Data Architecture project explores the use of MongoDB, a NoSQL document database, for managing the product catalog. This component demonstrates how MongoDB's flexible schema and document-based architecture can handle diverse product attributes, nested data structures (like customer reviews), and provide scalability advantages over traditional relational databases.

## Objectives

- Analyze limitations of relational databases (RDBMS) for diverse product catalogs
- Demonstrate MongoDB's benefits for flexible product data management
- Implement MongoDB operations for product catalog management
- Perform complex aggregations and queries on document data
- Evaluate trade-offs between NoSQL and relational database approaches

## Components

### 1. MongoDB Operations (`mongodb_operations.js`)
A comprehensive MongoDB shell script implementing five key operations:

- **Operation 1: Load Data**
  - Imports product catalog JSON file into MongoDB collection
  - Uses Node.js `fs` module to read and parse JSON data
  - Inserts products into the `products` collection

- **Operation 2: Basic Query**
  - Finds all Electronics products with price less than 50,000
  - Returns only name, price, and stock fields
  - Demonstrates simple filtering and projection

- **Operation 3: Review Analysis**
  - Uses aggregation pipeline to calculate average ratings from reviews array
  - Filters products with average rating >= 4.0
  - Shows how to work with nested/embedded documents

- **Operation 4: Update Operation**
  - Adds a new review to a specific product (ELEC001)
  - Uses `$push` operator to append to reviews array
  - Demonstrates document updates with nested data

- **Operation 5: Complex Aggregation**
  - Calculates average price by category
  - Groups products by category and computes statistics
  - Returns category, average price, and product count
  - Sorted by average price in descending order

### 2. NoSQL Analysis (`nosql_analysis.md`)
Comprehensive analysis document covering:

- **Section A: Limitations of RDBMS (150 words)**
  - Challenges with diverse product attributes
  - Schema rigidity and frequent changes
  - Difficulties storing nested data (reviews)

- **Section B: NoSQL Benefits (150 words)**
  - Flexible schema advantages
  - Embedded documents for nested data
  - Horizontal scalability with sharding

- **Section C: Trade-offs (100 words)**
  - ACID transaction limitations
  - Complex analytical query challenges

### 3. Product Catalog Data (`products_catalog.json`)
- JSON file containing diverse product data
- Includes products from multiple categories (Electronics, Clothing, etc.)
- Each product contains:
  - Basic information (name, category, price, stock)
  - Category-specific specifications (nested objects)
  - Customer reviews (nested arrays)
  - Metadata (tags, warranty, timestamps)

## Key Features

- **Flexible Schema**: Products with different attributes stored in the same collection
- **Embedded Documents**: Reviews stored directly within product documents
- **Aggregation Pipelines**: Complex data analysis using MongoDB aggregation framework
- **Document Updates**: Dynamic updates to nested arrays and objects
- **No JOINs Required**: Single-query retrieval of products with all related data

## Technologies

- **MongoDB 6.0**: NoSQL document database
- **MongoDB Shell (mongosh)**: Interactive shell for MongoDB operations
- **Node.js fs module**: File system operations for reading JSON data

## Setup and Execution

1. Install MongoDB and MongoDB Shell:
   ```bash
   # Using npm (if Node.js is installed)
   npm install -g mongosh
   
   # Or download from MongoDB website
   # https://www.mongodb.com/try/download/shell
   ```

2. Start MongoDB service (if running locally):
   ```bash
   # MongoDB should be running on localhost:27017
   ```

3. Execute MongoDB operations:
   ```bash
   mongosh --file mongodb_operations.js
   # Or
   mongosh < mongodb_operations.js
   ```

4. Verify operations:
   - Check import success and document counts
   - Review query results for each operation
   - Inspect updated documents

## Output

- MongoDB database with product catalog collection
- Query results demonstrating flexible data retrieval
- Aggregation results showing analytical capabilities
- Updated documents with new reviews
- Analysis document comparing RDBMS and NoSQL approaches

