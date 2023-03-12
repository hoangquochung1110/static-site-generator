For a list, += operator accepts any iterable and loops over it an appends the items.
Which means the right hand side doesn't need to be a list.
This is different from how it behaves in tuples and other types

```python
>>> t = [1,2,[3,4]]
>>> my_list = []
>>> my_list += t
>>> my_list
[1, 2, [3, 4]]
```
