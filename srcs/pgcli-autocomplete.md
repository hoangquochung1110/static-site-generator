---
title: Ease Postgres SQL queries with auto-completion and syntax-highlighting
date: 2022-12-14 22:00
description: This is a postgres client that does auto-completion and syntax highlighting.
category: blog
---

Recently, I've just explored some wonderful postgres CLI extensions/plugins which make data query much comfortable.
One of my favorite one is [pgcli](https://github.com/dbcli/pgcli) - a postgres client that does auto-completion and syntax highlighting.

To install on macOS with Homebrew:
```shell
brew install pgcli
```

Connect to your postgres db:
```shell
pgcli -h <HOST_ADDRESS> -d <DB_NAME> -U <USERNAME> -W
```

My quick demo:
![screenshots/pgcli.gif](https://media.giphy.com/media/qmRqWCQrUdtmXtf0Lj/giphy.gif)


