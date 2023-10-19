## Connection parameters:
1. listen_addresses

| Description      | Suggested Value | Context | Default Value |
|------------------|-----------------|---------|---------------|
| Set the host name or IP address(es) to listen to.        | '*'              | postmaster    | localhost             |

This configuration sometimes trip people up because most packages when you initialize a cluster by default `listen_addresses` is set to localhost which means you can only accept connects from loopback connection so you'll get an error message as below if you try to connect it from anywhere else.
```
"Is the server running on that host and accepting TCP/IP connections?"
```

- max_connection
- idle_in_transaction_session_timeout

Memory
- shared_buffers
- work_mem
- maintenance_work_mem
- log_min_duration_statement
- log_line_prefix

WAL
- wal_buffers
- checkpoint_timeout
- max_wal_size

Query tuning
- effective_cache_size
- random_page_cost