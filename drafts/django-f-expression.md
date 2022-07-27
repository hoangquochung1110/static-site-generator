---
title: Upgrade django queries with F() expression
date: 2022-07-27 17:00
---

# TL; DR
- Query of multiple objects: reduce queries
- for a single instance: no much difference in query time but it update value relative to what it is in the database -> avoid dirty read -> for example:
- need to refresh_from_db after query because Python only knows about experession instead of actual result

Suppose the government in your country raise tax rate by 5% which makes you have to raise your listing product price by 20%. What would your django query look like ?
A naive implementation may be like this:
```
products = Product.objects.all()
for product in products:
    product.price =* 1.2
    product.save()
```

Think of it more carefully, we can realize that the new price is relative to the current price no matter what it is. Intuitively, we want to reference to `price` field of `Product` model when running update process.

And here it comes, F() expression. The Django official doc states:
> An F() object represents the value of a model field, transformed value of a model field, or annotated column. 
> It makes it possible to refer to model field values and perform database operations using them without actually having to pull them out of the database into Python memory.

Let's try the problem with `F()` and `update()` queryset method

```
from django.db.models import F

Product.objects.update(price=F("price")*1.2)
```
Although the above query looks like a normal Python assignment of value to an instance attribute, in fact it is a SQL expression. This expression instruct database to increase the price field in database by 1.

New price value is based on current price value so we don't need to load it into Python memory. That's why F() comes into play.
