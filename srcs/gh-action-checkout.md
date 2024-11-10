---
title: The fetch-depth parameter in actions/checkout
date: 2024-11-10 11:00
description:
category: git
---

I was learning how to take advantages of GH Actions on AWS Lambda deployments. To save resources, I'd like to deploy the Lambda function only when there're changes in the lambda functions themselves rather than an arbitrary commit pushed.

We can just use `git diff` to check for changes in the Lambda function directory.

```bash
git diff --name-only HEAD~1 HEAD
```

My GH Actions workflow is as follows:

```yaml
...
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

    ...

      - name: Check for changes in Lambda function directory
        id: check_changes
        run: |
          echo "Checking for changes in /src directory..."
          if git diff --name-only HEAD~1 HEAD | grep '^src/'; then
            echo "src-changes=true" >> $GITHUB_ENV
          else
            echo "src-changes=false" >> $GITHUB_ENV
          fi
```

### How actions/checkout works

I found out that

> Only a single commit is fetched by default, for the ref/SHA that triggered the workflow.

As a result, `check_changes` never worked as there's only the latest commit pulled down to GH Action server.

Most likely, we may see this error log like this:

```
Run echo "Checking for changes in /src directory..."

Checking for changes in /src directory...
fatal: ambiguous argument 'HEAD~1': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
```

### The fetch-depth parameter
This parameter to set number of commits to fetch

To tackle above issue, I added `fetch-depth: 2` to the checkout step so that we can compare diff between the latest commit and the second latest commit.

```yaml
...
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
            fetch-depth: 2  # Fetch the previous commit to check for changes
...
```

Now, `check_changes` works as expected.
