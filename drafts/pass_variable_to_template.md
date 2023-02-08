```javascript
// DON'T EVER DO THIS
const username = "{{username}}";
```

Let's say `username` is `"Hung <3"` then the output would be

```javascript
const username = "Hung &lt;3";
```
