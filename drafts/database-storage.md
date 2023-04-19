## My keynotes of `Lecture #03: Database Storage (Part I)`: How DBMS represents the database in files on disk
### Links: https://www.youtube.com/watch?v=1D81vXw2T_w&list=PLSE8ODhjZXjbohkNBWQs_otTrBTrjyohi&index=3&ab_channel=CMUDatabaseGroup
### Notes: https://15445.courses.cs.cmu.edu/fall2019/notes/03-storage1.pdf


#### **File Storage**
In its most basic form, a DBMS stores a database as files on disk. Some may use a file hierarchy, others may use a single file (e.g., SQLite).

The DBMS’s storage manager is responsible for managing a database’s files. It represents the files as a collection of pages.


#### **Database Pages**
A page is a fixed-size block of data. (Page size in Postgres is 8kB, max is 32kB)

There're 3 concepts of page in DBMS:
1. Hardware page (usually 4 KB).
2. OS page (4 KB).
3. Database page (1-16 KB). (what we mainly talk about in this lecture)

There are a couple ways to find the location of the page a DBMS wants on the disk, and a heap file organization is one of the ways.
A heap file is an unordered collection of pages where tuples are stored in random order.


#### **Page layout**: how to organize data stored inside of the page
Two approaches:
- slotted-pages
- log-structured

Every page has a header storing metadata

The most common layout scheme is **slotted pages**


#### **Tuple layout**
A tuple is essentially a sequence of bytes. It is DBMS’s job to interpret those bytes into attribute types and values.


#### **Conclusion**
Database is organized in pages.
Different ways to track pages.
Different ways to store pages.
Pages may contain tuples.
Different ways to store tuples.
