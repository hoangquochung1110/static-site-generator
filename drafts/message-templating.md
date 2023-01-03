---
title: My quick demo of message templating
date: 2023-01-03 14:00
description: Short explanation about Kubernetes core concepts
category: python
---

Last year, we started building a messaging system/webapp which delivers customized sms and emails to receivers at a given time.


## Introduction
### Template

Template is an entity within the system which can be simply a plain text.
And in templates, we define `placeholders`, when we send template (message) to receiver, we may want to replace `placeholders` with actual values (receiver's name, mobile phones, etc).


For example, a template may look like this
```python
template = "Hello <ClientName>. This is <ClinicName>. We wanted to follow-up with you to confirm <PatientName>'s appointment on tomorrow. Please call <LocationPhone> if you need to reschedule.\n"
```


And the actual message we want receiver (client) to see:

![actual message content](https://hlogs-bucket.s3.ap-southeast-1.amazonaws.com/Screen+Shot+2023-01-03+at+2.56.38+PM.png)


## Implementation

To replace every `placeholder` with desired values, we rely on regular expression. Here is our implementation:

```python
import re

class Renderer:
    """Class to implement regex."""

    def __init__(self, placeholder_to_value_map: dict):
        self.placeholder_to_value_map = placeholder_to_value_map
        self.re_pattern: re.Pattern = self.build_pattern()

    def build_pattern(self) -> re.Pattern:
        """Return regex pattern object."""
        return re.compile(
            "|".join(map(re.escape, self.placeholder_to_value_map))
        )

    def repl_placeholders(self, match_obj: re.match) -> str:
        """Return actual values if match."""
        return self.placeholder_to_value_map[match_obj.group(0)]

    def render(self, template: str) -> str:
        """Replace placeholders with actual values."""
        return self.re_pattern.sub(self.repl_placeholders, template)


if __name__ == "__main__":

    template = "Hello <ClientName>. This is <ClinicName>."\
                " We wanted to follow-up with "\
                "you to confirm <PatientName>'s appointment"\
                " on tomorrow. Please call"\
                "<ClinicPhoneNumber> if you need to reschedule.\n"
    placeholder_to_value_map = {
        "<ClientName>": "Michael",
         "<ClinicName>": "Saritasa",
        "<PatientName>": "Luca",
        "<ClinicPhoneNumber>":  "123456789"
    }
    renderer = Renderer(
        placeholder_to_value_map=placeholder_to_value_map,
    )
    msg = renderer.render(template)
    print(msg)

```

Output
```shell
hunghoang@localhost project4 % python re_revise.py
Hello Michael. This is Saritasa. We wanted to follow-up with you 
to confirm Luca's appointment on tomorrow. 
Please call123456789 if you need to reschedule.
```


- Firstly, we prepare a placeholder-to-real-value map called `placeholder_to_value_map`.

- Then, we construct [re_pattern](https://docs.python.org/3/library/re.html) which helps us do matching and substitution later on.
Operator `|` (A | B) features in this pattern to tell that it will match either A or B.

- Thirdly, we will make substitution by calling `.sub(self.repl_placeholders, template)`.
In arguments, we have a callable `repl_placeholders` which returns replacement strings so that `re_pattern` substitutes `placeholders` present in template for them.
This method is called for every occurrence of pattern. Let's say we have 4 matches. `repl_placeholders` should be executed 4 times.

Let's try to print it out to see if it's true
```python
...
class Renderer:
    """Class to implement regex."""
    time = 0
...
    def repl_placeholders(self, match_obj: re.match) -> str:
        """Return actual values if match."""
        self.time += 1
        print(f"run {self.time}")
        return self.placeholder_to_value_map[match_obj.group(0)]
...
```

Result as we expected   :
```shell
hunghoang@localhost project4 % python re_revise.py
run 1
run 2
run 3
run 4
Hello Michael. This is Saritasa. We wanted to follow-up with you to confirm Luca's appointment on tomorrow. Please call123456789 if you need to reschedule.
```


## Conclusion

A few key takeaways:

* Special character `|`: A|B, where A and B can be arbitrary REs, creates a regular expression that will match either A or B. An arbitrary number of REs can be separated by the '|' in this way.
* `re.compile(pattern)` function: Compile a regular expression pattern into a regular expression object, which can be used for matching using its match(), search() and other methods.
* `Pattern.sub(repl, string, count=0)` function: replace compiled pattern in string by repl callable
