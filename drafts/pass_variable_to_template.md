---
title: Passing safely data to Javascript in Django templates
date: 2023-02-09 17:00
description: Django templates are often used to pass data to JavaScript code. Unfortunately, if implemented incorrectly, this opens up the possibility of HTML injection, and thus XSS (Cross-Site Scripting) attacks.
category: blog
---

```javascript
// DON'T EVER DO THIS
const username = "{{username}}";
```

Let's say `username` is `"Hung <3"` then the output would be

```javascript
const username = "Hung &lt;3";
```

### `json_script` filter

`json_scrip` safely outputs a Python object as JSON, wrapped in a `<script>` tag, ready for use with JavaScript:

```javascript
{{ username|json_script:"username" }};
```

Then you can use `document.getElementById` to find the element, and `JSON.parse` help us parse contained data.

```javascript
const username = JSON.parse(document.getElementById('username').textContent);
```
