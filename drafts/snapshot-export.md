---
title: Exporting Snapshots
date: 2023-05-09 13:00
description:
category: blog
---

### What is snapshots ?

<details>
<summary>Snapshots control which tuples are visible to SQL statements.</summary>

    - A snapshot includes only the current data committed by the time it was taken, thus providing a consistent (in the ACID sense) view of the data for this particular moment.
    - To ensure isolation, each transaction uses its own snapshot. It means that different transactions can see different snapshots taken at different points in time, which are nevertheless consistent.
</details>

* At the **Read Committed** isolation level, a snapshot is taken at the beginning of each statement, and it remains active only for the duration of this statement. -> Non-repeatable may happen.
* At the **Repeatable Read** and **Serializable** levels, a snapshot is taken at the beginning of the first statement of a transaction, and it remains active until the whole transaction is complete. -> Reading data may be stale -> Should be ready to retry transactions.

### Export snapshots

In some situations, concurrent transactions must see one and the same snapshot by all means

For example, if the pg_dump utility is run in the parallel mode, all its processes must see the same database state to produce a consistent backup.

Two steps:

1. To begin a new transaction with the same snapshot as an already existing transaction, first export the snapshot from the existing transaction. That will return the snapshot identifier, for example:
```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT pg_export_snapshot();
 pg_export_snapshot
---------------------
 00000003-0000001B-1
(1 row)
```

2. Then give the snapshot identifier in a SET TRANSACTION SNAPSHOT command at the beginning of the newly opened transaction:
```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION SNAPSHOT '00000003-0000001B-1';
```
