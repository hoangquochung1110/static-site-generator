**Repeatable Read** Isolation Level
- Only sees data committed before the transaction began -> eliminate non-repeatable reads
- Applications using this level must be prepared to retry transactions due to serialization failures because a repeatable read transaction (aka the 2nd transaction) cannot modify or lock rows changed by other transactions (let's say the first transaction) after the repeatable read transaction began -> so the second transaction will be rolled back with the message
```
ERROR:  could not serialize access due to concurrent update
```

**Snapshots**

- A snapshot includes only the current visible data committed by the time it was taken, thus providing *consistent* (in ACID) view of the data for a particular moment.
- To ensure isolation, each transaction uses its own snapshot. It means that different transactions can see different snapshots taken at different points in time, which are nevertheless consistent.
- At the Read Committed isolation level, a snapshot is taken at the beginning of each statement, and it remains active only for the duration of this statement.
- At the Repeatable Read and Serializable levels, a snapshot is taken at the beginning of the first statement of a transaction, and it remains active until the whole transaction is complete.
