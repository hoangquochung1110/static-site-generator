---
title: Learning the ropes: understanding Python generics
date: 2024-05-04 20:00
description: 'Learning the ropes: understanding Python generics'
category: blog
tags:
  - python
---

I've come across this EuroPython Conference talk on Python type system `Generics`. The presenter gave explanatory code snippets to cover a few concepts:
- how generics work and how the type system interacts with inheritance
- variance of generic types (how generics work and how the type system interacts with inheritance)
- a case study

<iframe width="560" height="315" src="https://www.youtube.com/embed/PmgHNls70eQ?si=Vddoe-kBdIpZRi4m" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Also, a select code snippet to highlight use case of `Generic` and `TypeVar``

```python
from typing import TypeVar, Generic


class Food:
    pass


T = TypeVar("T", bound=Food)


class CatFood(Food):
    pass


class Animal(Generic[T]):

    def feed(self, food: T):
        print("Yum!")


class Cat(Animal[CatFood]):

    def feed(self, food: CatFood):
        print("Yum!")


class Dog(Animal[Food]):

    def feed(self, food: Food):
        ...
```

`def feed(self, food: CatFood):`
will break without `Generic` and `TypeVar`, because by default callable behaves contravariant in types of arguments.

Contravariant means that a data type can be substituted with a more general type. A more general type of `Animal` is `object`
so `def feed(self, food: object` would be expected.

Read more:
- https://www.playfulpython.com/type-hinting-covariance-contra-variance/
