---
title: Commit message with title and body with one-liner git command
date: 2022-08-11 15:00
description: Use multiple message flag (-m) allow developers to define commit message with title and body without opening an editor.
category: blog
tags:
    - git
---

When you use git, one of the most frequent used command is

```bash
git commit -m "my commit message"
```

But most of the time, you would give a more meaningful commit message. Meaningful I mean here is that the message should consist of subject line (a short description of your changes in code) and body (to give more detailed description of what you did)

Today I learn that `git commit` accept multiple message flag 😉
If you run this command
```bash
git commit -m "Title of the commit" -m "Body message describing the changes in more detail."
```

It will result in this
```bash
Author: hunghoang-saritasa <hung.hoang@saritasa.com>
Date:   Thu Aug 11 16:29:07 2022 +0700

    Title of the commit

    Body message describing the changes in more detail.
```

This new finding helps me save time a lot. No need to open a vim editor when committing message with subject and body. And actually [the git documentation](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt--mltmsggt) do mention it.
