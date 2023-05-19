---
title: Run additional script when Postgres container starts
date: 2023-05-19 18:00
description: Learn how to run additional scripts during the initialization of a Postgres container in Docker. This feature allows you to set up initial data, create roles, and grant privileges. Discover how to leverage the power of initialization scripts and explore an example code snippet that demonstrates the process. Find out more about this Docker feature and its usage in this informative blog post.
category: blog
---

Today, I've just explored a feature when you start a postgres instance on Docker which allows you to set up initial data like `CREATE ROLE` or `GRANT <PRIVILEGE>`.

You may learn more details [here](https://github.com/docker-library/docs/tree/master/postgres#initialization-scripts)

### TL;DR:
We create `*.sql` or `*.sh` script to run SQL statement or bash script to prepare initial data.
Postgres container will run any `*.sql` and `*.sh` found in the directory (which containing `docker-compose.yml`) to do further initialization before starting the service.

NOTE: scripts in /docker-entrypoint-initdb.d are only run if you start the container with a data directory that is empty; any pre-existing database will be left untouched on container startup.

And visit my example code [at my gist](https://gist.github.com/hoangquochung1110/5486440c7e2b43f98135ff7803750b5f)
