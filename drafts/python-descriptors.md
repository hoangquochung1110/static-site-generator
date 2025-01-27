

### Descriptors
A descriptor lets you customize what should be done when you refer to an attribute of an object. Descriptors are the basis of complex attribute access in Python. They are used internally to implement properties, methods, class methods, static methods, and super. They are objects that define how attributes of another class can be accessed. In other words, a class can delegate the management of an attribute to another class.

The descriptor classes are based on three special methods that form the descriptor protocol:
• \__set\__(self, obj, value): This is called whenever the attribute is set. In the following examples, we will refer to this as a setter.
• \__get\__(self, obj, owner=None): This is called whenever the attribute is read (referred to as a getter).
• \__delete\__(self, obj): This is called when del is invoked on the attribute.
