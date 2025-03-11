---
title: "Django 5.2's Smart Shell: Goodbye Manual Model Imports!"
date: 2025-03-11 11:00
description: Django 5.2 has been released and one of the new features is auto-import models in shell mode. This is a great feature that makes it easier to play with your models in the shell.
category: blog
python: true
---

One of the most convenient features from `django-extensions` has finally made its way into Django's core. Starting with Django 5.2, the shell comes with automatic model imports, streamlining your development workflow.

### The Old Way
Remember how we used to start our Django shell sessions? It typically looked something like this:

```
from myapp.models import User, Product, Order
# More imports...
```

### The New Way
![](https://static.ssan.me/Django+5.2+Shell+Auto+Import+Tip.webp)

### Behind the Scene
This feature was previously available through the excellent `shell_plus` command in `django-extensions` package. The Django core team recognized its value and integrated it into the main framework, making development just a bit more pleasant for everyone.

### Why This Matters
This small but meaningful improvement:
- Reduces boilerplate code
- Speeds up debugging sessions
- Makes interactive development more fluid
- Eliminates a common source of frustration
