iterators are lazy single-use iterables <- they compute their next value as you loop over them (and you can loop over them but only once)
generators are the "easy" way to make an iterator

Pros:
Iterators help make more more memory-efficient code
Wrapping iterators-in-iterators can break up big and scary loops into small understandable steps
