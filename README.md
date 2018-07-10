# AnkiTools

[![Build Status](https://travis-ci.org/patarapolw/AnkiTools.svg?branch=master)](https://travis-ci.org/patarapolw/AnkiTools)
[![PyPI version shields.io](https://img.shields.io/pypi/v/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)
[![PyPI license](https://img.shields.io/pypi/l/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)
[![PyPI status](https://img.shields.io/pypi/status/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)

An Anki *.apkg and collection.anki2 reader and editor to work with in Python. Also included a module on [AnkiConnect](https://github.com/FooSoft/anki-connect).

I also created a new sync system called AnkiDirect.

The \*.apkg format specification can be viewed from [Anki decks collaboration Wiki](http://decks.wikia.com/wiki/Anki_APKG_format_documentation) and [AnkiDroid](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure). In my AnkiDirect, I tried to comply with the format specification as much as possible.

## Installation

```commandline
pip install AnkiTools
```

## Features

- Read and write to Anki database in Application Data.
- Read and create Anki file without Anki
- Convert back and forth to Excel.

# Examples

```python
import json
from collections import OrderedDict

from AnkiTools import AnkiDirect


if __name__ == '__main__':
    with open('notes.json') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    api = AnkiDirect()
    api.add(data)
    api.conn.commit()
```
where `notes.json` is

```json
{
  "data": {
    "note_type A": [
      {
        "data": {
          "header A": "a",
          "header B": "b"
        },
        "decks": {
          "Forward": "Test Deck::Forward",
          "Backward": "Test Deck::Backward"
        }
      }
    ]
  },
  "definitions": {
    "note_type A": {
      "templates": [
        {
          "name": "Forward",
          "data": {
            "qfmt": "{{header A}}",
            "afmt": "{{FrontSide}}\r\n\r\n<hr id=answer>\r\n\r\n{{header B}}"
          }
        },
        {
          "name": "Backward",
          "data": {
            "qfmt": "{{header B}}",
            "afmt": "{{FrontSide}}\r\n\r\n<hr id=answer>\r\n\r\n{{header A}}"
          }
        }
      ],
      "css": "This is a test css."
    }
  }
}
```
