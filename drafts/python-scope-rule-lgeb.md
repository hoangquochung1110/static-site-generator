
## The LEBG rule in python
LEGB rule encapsulates the concept of scope rules how variables and names are looked up in your code. Whenever we mention variables and names in Python, we mean a name that could be referencing data, a function or a class. Python tries to find in four different places (in order): **L**ocal (function) scope, the **E**nclosing function’s scope, the **G**lobal scope, and finally in the **B**uiltins namespace.

- Local: body of any Python function or lambda expression
- Enclosing: is a special scope that only exists for nested functions. If the local scope is an inner or nested function, then the enclosing scope is the scope of the outer or enclosing function. This scope contains the names that you define in the enclosing function. The names in the enclosing scope are visible from the code of the inner and enclosing functions.
- Global (or module) scope: contains all of the names that you define at the top level of a program or a module.
- Built-in scope: is a special Python scope that’s created or loaded whenever you run a script or open an interactive session. This scope contains names such as keywords, functions, exceptions, and other attributes that are built into Python. Names in this Python scope are also available from everywhere in your code. It’s automatically loaded by Python when you run a program or script.

The LEGB rule is a kind of name lookup strategy, which determines the order in which Python looks up names. For example, if you reference a given name, then Python will look that name up sequentially in the local, enclosing, global, and built-in scope. If the name exists, then you’ll get the first occurrence of it. Otherwise, you’ll get an error.
