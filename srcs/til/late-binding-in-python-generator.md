---
title: "Late binding of inner for-expressions in Python generators"
date: 2024-11-21 10:00
description: The first (outermost) for-expression should be evaluated immediately and that the remaining expressions be evaluated when the generator is executed.
category: python
til: true
---

```python
array_1 = [1, 2, 3]
array_2 = [10, 20, 30]
gen = (i + j for i in array_1 for j in array_2)

array_1 = [4, 5, 6]
array_2 = [400, 500, 600]
```

Output:
```python
>>> print(list(gen))
[401, 501, 601, 402, 502, 602, 403, 503, 603]
```

The reason why (only) array_1 values got updated is explained in **PEP-289**:

> Only the outermost for-expression is evaluated immediately, the other expressions are deferred until the generator is run.
