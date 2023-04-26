**Repeatable Read Isolation Level**
- Only sees data committed before the transaction began -> eliminate non-repeatable reads
- Applications using this level must be prepared to retry transactions due to serialization failures because a repeatable read transaction (aka the 2nd transaction) cannot modify or lock rows changed by other transactions (let's say the first transaction) after the repeatable read transaction began -> so the second transaction will be rolled back with the message
```
ERROR:  could not serialize access due to concurrent update
```
