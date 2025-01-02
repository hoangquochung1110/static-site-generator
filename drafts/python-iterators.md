More formally, a Python object is **iterable** if it meets one of these two criteria:
• It defines a method called \__iter\__(), which creates and returns an iterator over the elements in the container; or
• It defines \__getitem\__()—the magic method for square brackets—and lets you reference foo[0], foo[1], etc., raising an IndexError once you go past the last element.

More formally, an object in Python is an **iterator** if it follows the iterator protocol. And an object follows the iterator protocol if it meets the following criteria:
• It defines a method named \__next\__(), called with no arguments.
• Each time \__next\__() is called, it produces the next item in the sequence.
• Until all items have been produced. Then, subsequent calls to \__next\__() raise StopIteration.
 The Iterator Protocol | 17
• It also defines a boilerplate method named \__iter\__(), called with no arguments, and returning the same iterator. Its body is literally return self.

Any object with these methods can call itself a Python iterator. You are not intended to call the \__next\__() method directly. Instead, you will use the built-in next() function.


- iterators are lazy single-use iterables <- they compute their next value as you loop over them (and you can loop over them but only once)

- generators are the "easy" way to make an iterator

Pros:
Iterators help make more more memory-efficient code
Wrapping iterators-in-iterators can break up big and scary loops into small understandable steps