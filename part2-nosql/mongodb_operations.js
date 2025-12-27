// Operation 1: Load Data
// Import the provided JSON file into collection 'products'

// Switch to the database (create if it doesn't exist)
use('fleximart');

// Clear existing collection if needed
db.products.drop();

// Read and parse the JSON file using Node.js fs module
// Note: Run this script from the project root directory
const fs = require('fs');
const path = require('path');

// Get the absolute path to the JSON file
const jsonPath = path.resolve('part2-nosql/products_catalog.json');
const jsonContent = fs.readFileSync(jsonPath, 'utf8');
const products = JSON.parse(jsonContent);

// Insert all products into the collection
const result = db.products.insertMany(products);

// Display results
print('Successfully imported products into the \'products\' collection.');
print('Number of products in JSON file: ' + products.length);
print('Total documents in collection: ' + db.products.countDocuments());
print('\n' + '='.repeat(60) + '\n');

// Operation 2: Basic Query
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock

print('Operation 2: Basic Query');
print('Finding all Electronics products with price < 50000\n');

const electronicsProducts = db.products.find(
    { 
        category: "Electronics",
        price: { $lt: 50000 }
    },
    {
        _id: 0,
        name: 1,
        price: 1,
        stock: 1
    }
);

print('Results:');
print(electronicsProducts);
print('\n' + '='.repeat(60) + '\n');

// Operation 3: Review Analysis
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array

print('Operation 3: Review Analysis');
print('Finding all products with average rating >= 4.0\n');

const highRatedProducts = db.products.aggregate([
    // Unwind the reviews array to get individual review documents
    { $unwind: "$reviews" },
    
    // Group by product and calculate average rating
    {
        $group: {
            _id: "$_id",
            product_id: { $first: "$product_id" },
            name: { $first: "$name" },
            category: { $first: "$category" },
            price: { $first: "$price" },
            averageRating: { $avg: "$reviews.rating" },
            reviewCount: { $sum: 1 }
        }
    },
    
    // Filter products with average rating >= 4.0
    {
        $match: {
            averageRating: { $gte: 4.0 }
        }
    },
    
    // Project final output
    {
        $project: {
            _id: 0,
            product_id: 1,
            name: 1,
            category: 1,
            price: 1,
            averageRating: { $round: ["$averageRating", 2] },
            reviewCount: 1
        }
    },
    
    // Sort by average rating descending
    {
        $sort: { averageRating: -1 }
    }
]);

print('Results:');
print(highRatedProducts);
print('\n' + '='.repeat(60) + '\n');

// Operation 4: Update Operation
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}

print('Operation 4: Update Operation');
print('Adding a new review to product ELEC001\n');

const updateResult = db.products.updateOne(
    { product_id: "ELEC001" },
    {
        $push: {
            reviews: {
                user: "U999",
                rating: 4,
                comment: "Good value",
                date: new Date()
            }
        }
    }
);

print('Update result:');
print('Matched documents: ' + updateResult.matchedCount);
print('Modified documents: ' + updateResult.modifiedCount);

// Verify the update by retrieving the product
const updatedProduct = db.products.findOne(
    { product_id: "ELEC001" },
    { 
        _id: 0,
        product_id: 1,
        name: 1,
        reviews: 1
    }
);

print('\nUpdated product reviews:');
print(updatedProduct);
print('\n' + '='.repeat(60) + '\n');

// Operation 5: Complex Aggregation
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending

print('Operation 5: Complex Aggregation');
print('Calculating average price by category\n');

const avgPriceByCategory = db.products.aggregate([
    // Group by category and calculate statistics
    {
        $group: {
            _id: "$category",
            avg_price: { $avg: "$price" },
            product_count: { $sum: 1 }
        }
    },
    
    // Project final output with rounded average price
    {
        $project: {
            _id: 0,
            category: "$_id",
            avg_price: { $round: ["$avg_price", 2] },
            product_count: 1
        }
    },
    
    // Sort by average price descending
    {
        $sort: { avg_price: -1 }
    }
]);

print('Results:');
print(avgPriceByCategory);
