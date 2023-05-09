---
title: 'Understanding Dirty Read and Non-Repeatable Phenomena in Postgres: A Visual Demo'
date: 2023-04-25 15:00
description: In this video, we provide a step-by-step demonstration of dirty read and non-repeatable phenomena in Postgres using two transactions and a table. By visualizing the effects of these phenomena, viewers can gain a deeper understanding of the importance of transaction isolation levels and their impact on data consistency in a database system.
category: blog
---

In this video, you'll see a demonstration of **dirty read** and **non-repeatable phenomena** in Postgres at **Read Committed** isolation level.

### Dirty read is blocked:
- The first transaction issues an update statement but not committed yet.
- The second transaction should not read uncommitted changes made by the first one.

### Non-repeated read is active:
- The first transaction: read the same row twice
- The second transaction: update this row between these 2 reads -> the first transactions gets different results each time.


<iframe width="560" height="315" src="https://www.youtube.com/embed/wPMy3143xRQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
