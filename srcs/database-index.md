---
title: Database indexing in a nutshell with B+tree and Hash in comparison
date: 2022-04-25 10:00
description: introduction to b-tree and hash indexing.
category: blog
---

People is often said that indexing is a go-to technique to process efficiently queries in database. This post is for summarizing what database index is and revisiting hash and B+Tree.

Index is a data structure that organizes records to optimize certain kinds of retrieval operations. We may create index on a field of the table then retrieve all records that satisfy search conditions on `search-key` field. Without index, our query would end up scanning linearly the entire content of the table to fetch only one or a few records.

In this post, I'd like to summarize the performance and use cases of two common indexing techniques: **Hash index** and **B+tree**

## Hash index
This technique is widely used for creating indices in _main memory_ because its fast retrieval by nature. It has average O(1) operation complexity and O(n) storage complexity.
In many books, people use the term `bucket` to denote a unit of storage that stores one or more records
There are two things to discuss when it comes to hashing:

- Hash function: maps search keys (as its input) to an integer representing that key in the bucket.
- Hashing scheme: how to deal with key collision after hashing.


![hash function](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/khkm46v11z8o3geabglx.png)

Some people ask: why collision ? Does a [perfect hash function](https://en.wikipedia.org/wiki/Perfect_hash_function) ever exist ? In fact, let's say your keys is an infinite set, it's impossible to map them into a set of 32-bit integers without having no collision. There should be a trade-off between computation and collision rate.

There are a few hashing scheme worth mentioning: [linear probing](https://en.wikipedia.org/wiki/Linear_probing#:~:text=Linear%20probing%20is%20a%20scheme,by%20Gene%20Amdahl%2C%20Elaine%20M.), [chained hashing](https://www.tutorialspoint.com/hashing-with-chaining-in-data-structure) and [extendible hashing](https://en.wikipedia.org/wiki/Extendible_hashing). Lookup/insert/delete algorithms vary by hashing scheme, for example, chained hashing deal with key collisions by placing elements have the same hash value in the same bucket.

### Pros
- Hash index is suitable for equality or primary key lookup. Queries can benefit from hash index to get amortized O(1) lookup cost. For example: `SELECT name, id FROM student WHERE id = '1315';`

### Cons
Hash table has some limitations:

- Range queries are not efficient. Hash table is based on uniform distribution. In other words, you have no control of where an index entry is going to be placed.
- Low scalability: performance of lookup operation can degrade when there a lot of collisions and it requires to resize the hash table then rehash existing index entries.


## B+Tree
This is a self-balancing tree data structure that keeps data in sorted order and allows fast search within each node, typically using binary search.
B+Tree is a standard index implementation in almost all relational database system.

B+Tree is basically a M-way search tree that have the following structure:

- perfectly balance: leaf nodes always have the same height.
- every inner node other than the root is at least half full (M/2 − 1 <= num of keys <= M − 1).
- every inner node with k keys has k+1 non-null children.

Every node of the tree has an array of sorted key-value pairs. The key-value pair is constructed from (search-key value, pointer) for root and inner nodes. Leaf node values can be 2 possibilities:

- the actual record
- the pointer to actual record

### Lookup a value _v_
* Start with root node
* While node is not a leaf node, we do:
    - Find the smallest Ki where Ki >= v
    - If Ki == v: set current node to the node pointed by Pi+1
    - Otherwise, set current node to node pointed by Pi


![Look up a key using B+Tree index](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xwhs1v0ck8o3ddoibfzw.png)

### Duplicate keys
In general, search-key can be duplicate, to solve this, most database implementations come up with composite search key. For example, we want to create an index on `student_name` then our composite search key should be (student_name, Ap) where Ap is the primary key of the table.

### Pros
There're two major pros that B+tree offers:

- Minimizing I/O operations:

    * Reduced height: B+Tree has quite large [branching factor](https://en.wikipedia.org/wiki/Branching_factor) which makes the tree fat and short. The figure below illustrates a B+Tree with height of 2. As we can see nodes are spread out, it takes fewer nodes to traverse down to a leaf. The cost of looking up a single value is the height of the tree + 1 for the random access to the table

- Scalability:

    * You have predictable performance for all cases, O(log(n)) in particular. For databases, it is usually more important than having better best or average case performance.
    * The tree always remain balanced by its implementation. A B+Tree with n keys always has a depth of O(log(n)). Thus, the performance will not degrade if the database grows bigger. A four-level tree with a branching factor of 500 can store up to 256 TB provided that a page is size of 4KB.

![Figure 2](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k6colaz4amph93f1ikpq.gif)

- B+Tree is most suited for range queries, for example `"SELECT * FROM student WHERE age > 20 AND age < 22"`


## Conclusion
Although hash index performs better in terms of exact match queries, B+Tree is arguably the most widely used index structure in RDBMS thanks to its consistent performance in overall and high scalability.

|               | B+Tree    | Hash      |
| :---          | :----:    | :---:     |
| Lookup Time   | O(log(n)) | O(log(1)) |
| Insertion Time| O(log(n)) | O(log(1)) |
| Deletion Time | O(log(n)) | O(log(1)) |


Recently, the log-structured merge tree (LSM-tree) has attracted significant interest as a contender to B+-tree, because its data structure could enable better storage space usage efficiency. I'll investigate it further and make a post about it in the near future.
