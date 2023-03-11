---
title: Pytest introduction in 5 minutes
date: 2023-03-09 11:00
description: Short introduction of pytest fixture, parametrize and scope
category: blog
tags:
    - python
---

## Pytest
Pytest is a popular testing framework for Python that allows developers to write simple, scalable, and readable tests for their code. It is a powerful and flexible tool that provides features such as automatic test discovery, fixtures for managing test data, and plugins for extending its functionality

Pytest emphasizes on the use of plain Python functions as test cases, making it easy to write and maintain tests. With its intuitive syntax and powerful features, pytest has become a go-to choice for developers looking to test their Python code efficiently.

## Three core concepts of Pytest

### Fixture

Fixture: are functions that are run by pytest before (and sometimes after) the actual test functions. The code in the fixture can do whatever you want it to.

It has 2 main parts: setup and teardown:

```python
import pytest
import tasks
from tasks import Task

@pytest.fixture(scope="module")
def tasks_db(tmpdir):
"""Connect to db before tests, disconnect after."""
    # Setup : start db
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    yield # this is where the testing happens
    # Teardown : stop db
    tasks.stop_tasks_db()
```

Teardown code is guaranteed to run regardless of what happens during the tests.

### Parametrize: a way to send multiple sets of data through the same test

```python
import pytest

def two_sum(nums: list[int], target: int) -> list[int]:
    """Given an array of integers nums and an integer target,

    return indices of the two numbers such that they add up to target.
    """
    hashmap = {}
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in hashmap:
            return [i, hashmap[complement]]
        hashmap[nums[i]] = i

@pytest.mark.parametrize(
    "nums, target, result",
    [
        [[2,7,11,15], 9, [1,0]],
        [[3,2,4], 6, [2,1]],
    ]
)
def test_two_sum(nums: list[int], target: int, result: list[int]):
    assert two_sum(nums, target) == result
```

### Scope
- It's an optional parameter of `fixture`.
- Scope controls how often a fixture gets setup and torn down.
    * `scope="function"`: Run once per test function. Default scope of pytest
    * `scope="class"`: Run once per test class, regardless of how many test methods are in the class
    * `scope="module"`: Run once per module, regardless of how many test functions or methods or other fixtures in the module use it.
    * `scope="session"`: Run once per session. All test methods and functions using a fixture of session scope share one setup and teardown call.

## Run pytest with options

#### `-k EXPRESSION`: use an expression to find what test functions to run
#### `--lf, --last-failed`: When one or more tests fails, having a convenient way to run just the failing tests is helpful for debugging
