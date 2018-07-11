# AnkiTools

[![Build Status](https://travis-ci.org/patarapolw/AnkiTools.svg?branch=master)](https://travis-ci.org/patarapolw/AnkiTools)
[![PyPI version shields.io](https://img.shields.io/pypi/v/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)
[![PyPI license](https://img.shields.io/pypi/l/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)

An Anki *.apkg and collection.anki2 reader and editor to work with in Python. Also included a module on [AnkiConnect](https://github.com/FooSoft/anki-connect).

I also created a new sync system called AnkiDirect.

The \*.apkg format specification can be viewed from [Anki decks collaboration Wiki](http://decks.wikia.com/wiki/Anki_APKG_format_documentation) and [AnkiDroid](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure). In my AnkiDirect, I tried to comply with the format specification as much as possible.

## Installation

```commandline
pip install AnkiTools
```

## Featured modules

### Anki file conversion

```pydocstring
>>> from AnkiTools import anki_convert
>>> anki_convert('Chinese.apkg', out_file='Chinese_anki.xlsx')
>>> anki_convert('my_workbook.xlsx', out_format='.apkg')
```

The supported formats are `.xlsx`, `.apkg` and `.anki2`.

### AnkiDirect API

You can directly edit the Anki app data in user's Application Data path.

```python
from AnkiTools import AnkiDirect
import json

with open('payload.json') as f:
    payload = json.load(f)
with AnkiDirect() as api
    api.add(payload)
```

Some supported payloads include:

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
      "css": ".card {\r\n font-family: arial;\r\n font-size: 20px;\r\n text-align: center;\r\n color: black;\r\n background-color: white;\r\n}\r\n"
    }
  }
}
```

### AnkiConnect

```pydocstring
>>> from AnkiTools import AnkiConnect
>>> AnkiConnect.is_online()
True
>>> params = {'actions': [{'action': 'deckNames'}, {'action': 'browse', 'params': {'query': 'deck:current'}}]}
>>> AnkiConnect.post('multi', params=params)
{'result': [['Default', 'SpoonFed', 'Chinese Hanzi Freq', 'Chinese Vocab'], None], 'error': None}
```
The actual addable actions and parameters can be viewed from [AnkiConnect](https://foosoft.net/projects/anki-connect/).

## Plans

- AnkiDirect two-way sync between Excel file and the Anki app.
- Specifying metadata (e.g. card distribution, decks) in the Excel file and make it convertible and syncable.
- Add CRUD to `AnkiDirect` ("update" and "remove" pending.)

## Contributions

- Testing on other OS's, e.g. Windows XP, Windows 10, Ubuntu Linux. (I tested on Mac.)
- Manual testing of whether the generated `*.apkg` can be opened without subsequent errors in the Anki app.
- Writing test cases and testing parameters. The current ones are viewable at [/tests/parameters.json](https://github.com/patarapolw/AnkiTools/blob/master/tests/parameters.json) and [/tests/files/](https://github.com/patarapolw/AnkiTools/tree/master/tests/files).
- Specifying challenging payloads for AnkiDirect.
