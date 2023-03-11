---
title: sed command to replace string in Unix
date: 2023-02-06 10:00
description: A non-interactive way to modify and manipulate text files with ease
category: blog
til: true
---

SED is a text stream editor used on Unix systems to edit files quickly and efficiently. The tool searches through, replaces, adds, and deletes lines in a text file without opening the file in a text editor.

### Replace String Using the sed Command
The Linux sed command is most commonly used for substituting text. It searches for the specified pattern in a file and replaces it with the wanted string.

Example:
```shell
sed -i 's/old_string/new_string/' filename.txt
```
option `i` means overwriting original file.

By default, sed only replaces the first occurrence of the specified string in each line. It searches for the first instance of the specified word in a line, replaces it, and moves on to the next line.

If you have multiple instances of the same word within a single line, add the g flag to the command to change all of them.

The command for substituting each occurrence of a given string within a text is:

```shell
sed 's/old_string/new_string/g' filename.txt
```

### Replace Specific Occurrence in a Line Using the sed Command

The sed command lets you choose which occurrence of a specified string you want to replace within each line. To do so, add a number flag such as 1, 2, etc.:

```shell
sed 's/old_string/new_string/#' filename.txt
```

For example, to substitute the second occurrence of the word box in each line of the text with the word bin, use this command:

```shell
sed 's/box/bin/2' foxinbox.txt
```

For advance usage, please refer [this post](https://phoenixnap.com/kb/linux-sed)
