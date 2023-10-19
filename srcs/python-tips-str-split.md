---
title: "Python tip: don't split on space or newlines"
date: 2023-10-19 16:00
description:
category: python
---

### Whitespace splitting

```
text = '   1   2   3   '
```
You probably don't need to split on a space character:
```
>>> numbers = text.split(" ")
['', '', '', '1', '', '', '2', '', '', '3', '', '', '']
```

Instead let's split without specifying a delimiter:
```
>>> numbers = text.split()
['1', '2', '3']
```

When called without a delimiter, the `split` method regards a chain of of consecutive whitespace as a single separator. In addition, using the `split` method without a delimiter will strip any leading and trailing whitespace, which is often desirable.


### Line splitting

Need to split your string into lines ?
```
poem = "Old silent pond.\nA frog jumps into the pond—\nSplash! Silence again.\n"
```

If you split on \n you may notice an empty string at the end of your list:
```
>>> poem.split("\n")
['Old silent pond.', 'A frog jumps into the pond—', 'Splash! Silence again.', '']
```

And if your text has carriage returns (\r) in it, as is common in text sent from web browsers, then you'll find those carriage returns are still in the string as well!

The string splitlines method is the better way to split a string into lines:
```
>>> poem.splitlines()
['Old silent pond.', 'A frog jumps into the pond—', 'Splash! Silence again.']
```

The splitlines method strips a trailing newline from the end of the string (if there is one) and it'll split on any line ending (\r\n, \n, or \r).
