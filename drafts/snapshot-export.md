---
title: Exporting Snapshots
date: 2023-05-09 13:00
description:
category: blog
---

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
