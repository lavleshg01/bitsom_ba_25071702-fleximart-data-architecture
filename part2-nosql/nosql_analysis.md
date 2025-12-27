# NoSQL Analysis: MongoDB for FlexiMart Product Catalog

## Section A: Limitations of RDBMS 

Relational database management systems (RDBMS) face significant challenges when handling the diverse product catalog of FlexiMart. The primary limitation stems from the rigid schema requirement: products have vastly different attributes depending on their category. For instance, laptops require fields like RAM, processor, and storage capacity, while shoes need size, color, and material specifications. In a normalized relational model, this would necessitate either creating separate tables for each product type (leading to schema proliferation) or using a sparse table with numerous nullable columns (wasting storage and complicating queries).

Additionally, frequent schema changes become problematic. When introducing new product categories like "Smart Home Devices" with unique attributes, MySQL requires ALTER TABLE operations that can lock tables and disrupt operations. The normalized structure also struggles with storing customer reviews as nested data. Reviews would need separate tables with foreign keys, requiring complex JOIN operations to retrieve a product with its reviews, increasing query complexity and reducing performance for read-heavy e-commerce workloads.

## Section B: NoSQL Benefits

MongoDB addresses these RDBMS limitations through its flexible document-based architecture. The flexible schema allows each product document to have a unique structure tailored to its category. A laptop document can contain specifications like `{ram: "16GB", processor: "M2 Pro"}` while a shoe document includes `{size: "10", color: "Black"}` - all within the same collection without schema conflicts. This eliminates the need for ALTER TABLE operations when adding new product types; new attributes are simply added to new documents.

Embedded documents enable storing reviews directly within product documents as arrays, creating a natural one-to-many relationship. Retrieving a product with all its reviews requires a single query without JOINs, significantly improving read performance. MongoDB's horizontal scalability allows FlexiMart to distribute the product catalog across multiple servers using sharding, enabling the system to handle growing inventory and traffic by adding commodity hardware rather than expensive vertical scaling. This makes MongoDB ideal for e-commerce platforms with diverse product catalogs.

## Section C: Trade-offs

While MongoDB offers flexibility, it comes with notable disadvantages compared to MySQL for product catalogs. First, MongoDB lacks ACID transactions across multiple documents, making it challenging to maintain referential integrity. For example, updating product stock levels while simultaneously recording sales transactions requires careful application-level coordination, whereas MySQL's transactional guarantees ensure data consistency automatically.

Second, complex analytical queries requiring aggregations across multiple collections are more difficult and less performant in MongoDB compared to SQL's mature JOIN capabilities. Business intelligence queries like "total sales by product category with customer demographics" become complex in MongoDB, requiring multiple queries or complex aggregation pipelines, whereas SQL's declarative syntax makes such queries straightforward and optimized.

