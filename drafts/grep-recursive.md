---
title: grep -r to search for a pattern recursively within a directory
date: 2022-11-29 15:00
description: Search for a pattern within a directory using grep
category: TIL
---

There's a situation that I don't know which file contains the specific pattern that you are looking for. Then `grep -r` comes into play.

```shell
$ grep 'ˆZ' -r ~/Desktop
```

The above grep command search for any line starting with `Z` in Desktop directory.

### grep -v to search for the whole word

```shell
$ cat examples.txt

grep examples
linux exam on 19th

$ grep exam examples.txt

grep examples
linux exam on 19th

$ grep -w examples.txt

linux exam on 19th
```

### grep -A and grep -B to print number of lines after and before matching line

```shell
hunghoang@MacBook-Pro Desktop % cat premier-league-table.txt
1. Arsenal
2. Liverpool
3. Man City
4. Chelsea
hunghoang@MacBook-Pro Desktop % grep -A2 Arsenal premier-league-table.txt
1. Arsenal
2. Liverpool
3. Man City
hunghoang@MacBook-Pro Desktop % grep -B1 'Man City' premier-league-table.txt
2. Liverpool
3. Man City
```
 
`grep -A2 Arsenal premier-league-table.txt` indicates that we want to show **2** lines **after** the line which contains `Arsenal` pattern while `grep -B1 'Man City' premier-league-table.txt` means the terminal should display **1** line **before** the line which matches `Man City` pattern.


### grep -v to perform invert match

Given `premier-league-table.txt` file as above example:
This will print only the lines that don’t match the pattern given:

```shell
hunghoang@MacBook-Pro Desktop % grep -v Arsenal premier-league-table.txt    
2. Liverpool
3. Man City
4. Chelsea
```

