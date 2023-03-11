---
title: How to exclude commits from git blame
date: 2022-03-11 11:00
description: blame.ignoreRevsFile help us configure Git local to exclude formatting commits
category: blog
tags:
  - git
---

`git blame` allows users to view the revision history of a file line-by-line. It provides information about the author of each line, the commit in which the line was last modified, and the time of the modification.

At a point of time, I decided to set up [pre-commit](https://pre-commit.com/), a powerful tool to ensure code quality. After the tool has done its job (reformating files like remove trailing whites paces and adding new line at end of file), I messed up with my Git history. `git blame` becomes useless in such cases. Thousands of lines will be marked with an unimportant formatting change.

![Before apply .git-blame-ignore-revs](https://user-images.githubusercontent.com/99159244/224463554-bf525dd6-57b3-45e2-ad75-fc1d8048a314.png)

## `--ignore-rev` option comes to rescue
This options help you blame a file without considering an unwanted commit
```bash
git blame --ignore-rev d87e05 build.py
```

This is good didn't help much as I rarely use `git blame` in CLI.

## Exclude commits with `blame.ignoreRevsFile` option
According to [Black documentation](https://black.readthedocs.io/en/stable/guides/introducing_black_to_your_project.html#avoiding-ruining-git-blame):
> You can configure Git to automatically ignore revisions listed in a file on every call to git blame.

So I created `.git-blame-ignore-rev` and put the full 40 characters commit identifier(s) into it:
```
# Ignore code re-formation after pre-commit setup
d78d0325fac64bfb69d5c47110e8c1b999dfcd18
```

then apply this configuration to my local Git config:
```
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

Restarted VSCode and it picked up new Git config and didn't show the reformatting commit anymore!

![After apply .git-blame-ignore-revs](https://user-images.githubusercontent.com/99159244/224464197-afd8a4ec-94ab-4af8-b85c-a21390fc4114.png)
