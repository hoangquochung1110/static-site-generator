## Summary of **Postgresql Internals 14** Part I: Isolation

### Isolation level
- Read Committed
    * Default level in Postgres
- Repeatable Read
    * perfect for read-only transaction like: building reports
- Serializable Read
    * allow you not to worry about data consistency at all
    * but require application ability to retry any transaction aborted by a serialization failure


|          | lost update | dirty read | non-repeatable read | phantom reads | other anomalies |
|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
| Read Committed |   yes   |   -   |   yes   |   yes   |   yes    |
| Repeatable Read |   -   |    -  |   -   |    -  |      yes    |
| Serializable |    -  |    -  |   -   |   -   |     -     |


### Anomalies
- Dirty read: a transaction reads uncommitted changes made by another transaction. (Prohibited by Read Committed level)
- Non-repeatable read: read the same row multiple times and get different results each time. (occurs when a transaction reads one and the same row twice, whereas another transaction updates (or deletes) this row between these reads and commits the change.). Read Committed allows this to happen.
- Phantom read: you run two identical queries returning a set of rows while another transaction inserts/deletes between these queries. As a result, the first transaction gets two different sets of rows. Repeatable Read level or lower allow this to happen.
