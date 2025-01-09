---
title: Recap of my take of 'Amazon DynamoDB for Serverless Architectures' course
date: 2025-01-04 17:00
description: A brief recap on Amazon DynamoDB capabilities, how it works, how to operate it and a few design considerations
category: blog
tags:
    - nosql
---

### TL;DR
- DynamoDB is well designed for at **Online Transaction Processing (OLTP)** workloads where you need consistent single-digit millisecond response times at any scale
- Unlike traditional databases, the key to unlocking DynamoDB's power lies in **knowing your request patterns** upfront - not as an afterthought, but as a fundamental part of your design process. You can't just throw any query at it; instead, you design your data model around specific questions you need to answer. This approach makes it ideal for applications with well-defined workflows, like e-commerce carts, user sessions, or game states, but less suitable for exploratory analytics or ad-hoc queries.

### How it works

Data is stored in tables. A table contains items with attributes.
You can think of items as rows or tuples in a relational database and attributes as columns.
![Tables and Partitions](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/tables-and-partitions-dynamo-db.png "Tables and Partitions")

#### Primary keys
![Primary keys](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/dynamo-db-primary-keys.png "Primary keys")

#### Basic item requests:

Write

- PutItem: Write item to specified primary key.
- UpdateItem: Change attributes for item with specified primary key.
- BatchWriteItem: Write bunch of items to the specified primary keys.
- DeleteItem: Remove item associated with specified primary key.

Read

- GetItem:  Retrieve item associated with specified primary key.
- BatchGetItem: Retrieve items with this bunch of specified primary keys.
- Query: For specified partition key, retrieve items matching sort key expression (forward/reverse order).
- Scan: Give me every item in my table.

Details: [Working with items and attributes in DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html?t)

#### Secondary indexes: allow to query data based on other attributes than your table's primary key.

- Local secondary indexes
    * index is local to partition key
    * allow you to query items with the same partition key
- Global secondary indexes:
    * allow you to query over the entire table
    * index is across all partitions

Pros:

- Improved query performance
- Support complex queries
- Non-Unique Indexing: They allow for indexing on non-unique attributes, which broadens the range of query possibilities, such as searching for products by category or timestamps in logs

Cons:

- Write Performance Overhead: Each time an item in the base table is updated, corresponding entries in the secondary index must also be updated. This can slow down insert and update operations, especially if there are multiple secondary indexes on a table
- Storage Costs: While secondary indexes reduce data retrieval time, they also consume additional storage space, which can be a consideration in environments with limited resources
- Limited Use Cases: Secondary indexes should not be applied to attributes with low or very high cardinality; low cardinality can lead to inefficient queries, while high cardinality can result in excessive scanning across nodes

Important notes:

- The secondary index should not apply to the values with too low (e.g. gender -> male/female) or too high cardinality (e.g. user's unique id)
    * former case: querying won't be efficient as leads to wide index partitions and automatically we've a lot of data to scan
    * latter case: queries can be executed at best on 1 node and at worst in all nodes
    * Learn more: https://www.waitingforcode.com/general-big-data/secondary-index-nosql-data-stores/read?t#sample_implementation


### Operating DynamoDb (skipped)

### Design considerations

#### Partition keys
When selecting an attribute as a partition key in a NoSQL database, it is crucial to consider several key factors to ensure that read and write operations are evenly distributed across partitions. Here are the primary considerations:

- High Cardinality (that means there are lots of unique values):
	•	Definition: Choose attributes that have a large number of distinct values (high cardinality). For instance, using `user_id`, `email`, or `order_id` can help ensure that data is spread across many partitions.
	•	Impact: High cardinality minimizes the risk of “hot partitions,” where one partition receives significantly more traffic than others, leading to performance bottlenecks .

- Avoid Monotonically Increasing Values:
	•	Examples: Attributes like timestamps or sequential IDs can lead to uneven distribution because new entries will always be directed to the same partition until it reaches its capacity.
	•	Recommendation: Instead, consider using composite keys or appending random suffixes to create variability in the partition key .

#### Hot and Cold Data
Separate data that is frequently accessed (hot) from data that is not accessed frequently (cold)

#### Large attributes

Ideally should keep item size small
- Compress large data before storing it
- Store large data in external storage like S3
- Break it up into smaller items

#### One-to-many tables

### Closing Thoughts

DynamoDB represents a shift in database design thinking – instead of adapting queries to our data, we design our data model around known access patterns. This approach might feel constraining at first, but it enables DynamoDB to deliver its core promise: consistent, millisecond-level performance at any scale. For serverless architectures where predictable performance is crucial, this intentional limitation becomes a powerful advantage.
