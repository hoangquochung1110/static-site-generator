---
title: Implementation of the Factory Method pattern in Python
date: 2022-12-08 16:00
description: This article explores the Factory Method design pattern and its implementation in Python. It's one of the most widely used design patterns.
category: Python
---

Imagine an application that needs to convert a Song object into its string representation using a specified format. Converting an object to a different representation is often called serializing. You’ll often see these requirements implemented in a single function or method that contains all the logic and implementation, like in the following code:

```python
# In serializer_demo.py

import json
import xml.etree.ElementTree as et

class Song:
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist


class SongSerializer:
    def serialize(self, song, format):
        if format == 'JSON':
            song_info = {
                'id': song.song_id,
                'title': song.title,
                'artist': song.artist
            }
            return json.dumps(song_info)
        elif format == 'XML':
            song_info = et.Element('song', attrib={'id': song.song_id})
            title = et.SubElement(song_info, 'title')
            title.text = song.title
            artist = et.SubElement(song_info, 'artist')
            artist.text = song.artist
            return et.tostring(song_info, encoding='unicode')
        else:
            raise ValueError(format)
```

The `serialize()` method support JSON and XML formats. Let's say we're going to support more structures like yaml or csv, if-else structure becomes more complex and harder to read and harder to understand.

Therefore, we need a component which decides an appropriate implementation based on the specified *format*. 

###**Basic implementation of Factory Method**
The central idea in Factory Method is to provide a separate component with the responsibility to decide which concrete implementation should be used based on some specified parameter. That parameter in our example is the *format*.

To complete the implementation of Factory Method, you add a new method ._get_serializer() that takes the desired format. This method evaluates the value of format and returns the matching serialization function:

```python
class SongSerializer:
    def _get_serializer(self, format):
        """`creator` component in Factory Method pattern."""
        if format == 'JSON':
            return self._serialize_to_json
        elif format == 'XML':
            return self._serialize_to_xml
        else:
            raise ValueError(format)
```

Now, you can change the .serialize() method of SongSerializer to use ._get_serializer() to complete the Factory Method implementation. The next example shows the complete code:

```python
class SongSerializer:
    def serialize(self, song, format):
        """`product` component in Factory Method pattern."""
        serializer = self._get_serializer(format)
        return serializer(song)

    def _get_serializer(self, format):
        """`creator` component in Factory Method pattern."""
        if format == 'JSON':
            return self._serialize_to_json
        elif format == 'XML':
            return self._serialize_to_xml
        else:
            raise ValueError(format)

    def _serialize_to_json(self, song):
        payload = {
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        }
        return json.dumps(payload)

    def _serialize_to_xml(self, song):
        song_element = et.Element('song', attrib={'id': song.song_id})
        title = et.SubElement(song_element, 'title')
        title.text = song.title
        artist = et.SubElement(song_element, 'artist')
        artist.text = song.artist
        return et.tostring(song_element, encoding='unicode')
```

as you can see, except `serialize()`, other methods don't use `self` parameter. This is a good indication that they should be methods of the `SongSerializer` class, and they can become externals functions:

```python
class SongSerializer:
    def serialize(self, song, format):
        serializer = get_serializer(format)
        return serializer(song)


def get_serializer(format):
    if format == 'JSON':
        return _serialize_to_json
    elif format == 'XML':
        return _serialize_to_xml
    else:
        raise ValueError(format)


def _serialize_to_json(song):
    payload = {
        'id': song.song_id,
        'title': song.title,
        'artist': song.artist
    }
    return json.dumps(payload)


def _serialize_to_xml(song):
    song_element = et.Element('song', attrib={'id': song.song_id})
    title = et.SubElement(song_element, 'title')
    title.text = song.title
    artist = et.SubElement(song_element, 'artist')
    artist.text = song.artist
    return et.tostring(song_element, encoding='unicode')
```
Note: The .serialize() method in SongSerializer does not use the self parameter.

The rule above tells us it should not be part of the class. This is correct, but you are dealing with existing code.

If you remove SongSerializer and change the .serialize() method to a function, then you’ll have to change all the locations in the application that use SongSerializer and replace the calls to the new function.

Unless you have a very high percentage of code coverage with your unit tests, this is not a change that you should be doing.
