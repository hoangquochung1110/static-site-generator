---
title: "Uncovering 4 Lesser-Known but Essential Options of `grep` command"
date: 2022-11-29 15:00
description: Search for a pattern within a directory using grep
category: TIL
til: true
---

### `grep -r` for pattern matching in all files within a directory and its subdirectories. 

There's a situation that I don't know which file contains the specific pattern that you are looking for. Then `grep -r` comes into play.

```shell
$ grep 'ˆZ' -r ~/Desktop
```

The above grep command search for any line starting with `Z` in Desktop directory.

## `grep -v` to search for the whole word

```shell
hunghoang@MacBook-Pro Desktop % cat examples.txt
my example
linux exam on 19th
hunghoang@MacBook-Pro Desktop % grep "exam" examples.txt                  
my example
linux exam on 19th
hunghoang@MacBook-Pro Desktop % grep -w "exam" examples.txt               
linux exam on 19th
```

## `grep -A` and `grep -B` to print number of lines after and before matching line

The grep -A option stands for "after" and specifies the number of lines to be displayed after a match is found. When using this option, grep will display the matched line followed by the specified number of lines after it.

The grep -B option stands for "before" and similarly specifies the number of lines to be displayed before a match is found. With this option, grep will display the specified number of lines before the matched line.

Both -A and -B options are useful for context sensitive searching, when you need to see some lines before or after the match to understand it better. For example, grep -A 3 error log.txt would show three lines after each line containing the word "error" in the file "log.txt".

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


## `grep -v` to perform invert match

This option is to display all lines that do NOT match the specified pattern.

Given `premier-league-table.txt` file as above example:
This will print only the lines that don’t match the pattern given:

```shell
hunghoang@MacBook-Pro Desktop % grep -v Arsenal premier-league-table.txt    
2. Liverpool
3. Man City
4. Chelsea
```
