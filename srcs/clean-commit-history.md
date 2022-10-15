---
title: Do you have readable Git commit history ?
date: 2022-05-06 10:00
description: Advance uses of git commit and git rebase in feature branch workflow.
category: blog
---


# Reuse the most recent commit message with `git commit --amend` 

Recall back to the time when I haven't been familiarized with code quality assurance (aka linters), I very often failed those linter checks. As a result, there were commit messages look like this
```
$ git commit -m "Improve code style"
```
The command is tedious and the message does not provide any meaningful information. Then `git commit --amend --no-edit` comes into play. It allows you to reuse your last commit message for the current commit.
Suppose you want to remove trailing white space in `apps/users/views.py`:
```
$ git add apps/users/views.py apps/users/serializers.py
$ git commit -m "Provide UserViewSet"
$ git add apps/users/views.py
$ git commit --amend --no-edit
```

# Clean up lengthy commit history with `git rebase`
During my feature branch workflow, it's very often to have several commits as a result of code review or 
I have to leave the task till the next day.

At the end of the task, my commit history may end up this like
```
(cs50w-network) hunghoang@MacBook-Pro project4 % git log --oneline
58701f5 (HEAD -> feature/migrate-to-htmx-alpinejs, origin/feature/migrate-to-htmx-alpinejs) Remove unused vanilla js
bf2f1b7 Fix navbar offsetHeight
c798ff0 minor change
05c3b93 Provide separate api directory
202f666 Disable follow-btn on host user timeline
93b22fd Support followers_count update
93e8647 Improve the feature of prevent editing 2 post simultaneously
e4e5aa5 Reuse PostViewSet
88b55b9 Refine post/list.html
09b9acf Re-arrange auth templates
0250ecb Re-arrange template to project-level
30ae17b Integrate htmx into post/list.html
```

These logs of changes are important while the feature is in development phase but they looks scattered and unnessary when looking through entire history of the `main` branch. Squashing commits not only make commit history neater so that others can understand but also easy to resolve conflicts at once when I `git merge` afterwards.

**First**, make sure you're at the feature-branch:
```
$ git switch feature-branch
```
**Second**, use rebase to squash the branch on top of its original base commit:
```
$ git rebase --keep-base -i main
```

What are these flag for ?
[`--keep-base`](https://git-scm.com/docs/git-rebase) flag to tell git rebase on to the base commit from `main` which feature-branch was branched off.
`-i` stands for interactive which enables rebase [interactive mode](https://git-scm.com/docs/git-rebase#_interactive_mode). This will open your text editor with a file you can use to select rebase operations.

**Third**, change the rebase file to squash all commits into the first one
Please notice when rebasing, commits are listed in the opposite order when compared to using `git log`
```
pick 30ae17b Integrate htmx into post/list.html
pick 93e8647 Improve the feature of prevent editing 2 post simultaneously
pick 93b22fd Support followers_count update
pick 202f666 Disable follow-btn on host user timeline
pick 05c3b93 Provide separate api directory
pick c798ff0 minor change
pick bf2f1b7 Fix navbar offsetHeight
pick f98b90a Remove unused vanilla js

# Rebase 3349b96..f98b90a onto 8b92fd6 (12 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amendingx
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup [-C | -c] <commit> = like "squash" but keep only the previous
#                    commit's log message, unless -C is used, in which case
#                    keep only this commit's message; -c is same as -C but
#                    opens the editor
...
```
(Further comments removed for brevity.)

The block of comments below commits is the mini cheatsheet of possible operations
To tell squash all commits into the first one, let's change all the commit lines except the first one with `f`:
```
pick 30ae17b Integrate htmx into post/list.html
f 93e8647 Improve the feature of prevent editing 2 post simultaneously
f 93b22fd Support followers_count update
f 202f666 Disable follow-btn on host user timeline
f 05c3b93 Provide separate api directory
f c798ff0 minor change
f bf2f1b7 Fix navbar offsetHeight
f f98b90a Remove unused vanilla js

# Rebase 3349b96..f98b90a onto 8b92fd6 (12 commands)
#
# Commands:
```

**Fourth**, save and close the file, and Git will perform the squashing. Upon completion, let's `git log --oneline` to see the result.

**Fifth**, you may want to pull the latest version of your main branch then merge `feature-branch`

# Conclusion
`git commit --amend --no-edit` and `git rebase --keep-base -i main` are two of most used Git command I take advantage of during feature branch workflow. Hope they can help you.
