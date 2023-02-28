---
title: "Python comes with two rare string method: `str.maketrans` and `str.translate`"
date: 2023-02-28 20:00
description: str.maketrans and str.translate are helpful for complex string manipulation and translation
category: blog
til: true
---

In Python, the `str.maketrans()` and `str.translate()` methods are used for string manipulation and translation. The str.maketrans() method creates a translation table that can be used with the str.translate() method to replace specified characters in a string with other characters.

Let's say we want replacements like this:
```python
>>> mapping = {
...     " ": "_",
...     " ": "_",
...     "!": "",
... }
```

Use `maketrans()` to make translation table
```python
>>> trans_table = str.maketrans(mapping)
```

Then apply translation:
```python
>>> s = "Replace-hyphens and spaces!"
>>> s.translate(trans_table)
'Replace-hyphens_and_spaces'
>>> 
```
