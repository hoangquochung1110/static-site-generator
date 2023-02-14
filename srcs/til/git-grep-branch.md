---
title: grep a pattern on a Git branch
date: 2023-02-14 15:00
description: Learn how to use Git grep to search for patterns in specified files on a Git branch. Our step-by-step guide will show you how to quickly and efficiently find text in your codebase. Boost your productivity and streamline your workflow with this essential Git command.
category: blog
til: true
---

To grep a pattern in a git branch in specified HTML files, you can use the following command:

```shell
git grep <pattern> <branch> -- '*.html'
```

The -- '*.html' option specifies that the search should be limited to HTML files.
