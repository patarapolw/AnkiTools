# AnkiTools

[![Build Status](https://travis-ci.org/patarapolw/AnkiTools.svg?branch=master)](https://travis-ci.org/patarapolw/AnkiTools)
[![PyPI version shields.io](https://img.shields.io/pypi/v/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)
[![PyPI license](https://img.shields.io/pypi/l/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)
[![PyPI status](https://img.shields.io/pypi/status/AnkiTools.svg)](https://pypi.python.org/pypi/AnkiTools/)

An Anki \*.apkg and \*.anki2 reader/editor to work with in Python. Also included a module on [AnkiConnect](https://github.com/FooSoft/anki-connect).

## Installation

    pip install AnkiTools

## Parsing \*.apkg and \*.anki2 in a human readable and easily manageable format.

    >>> from AnkiTools.tools.read import readApkg
    >>> anki = readApkg('test/testfile/Chinese.apkg')
    >>> anki.models
    {'1514177308904': {'mid': '1514177308904',
      'name': 'Chinese Hanzi Freq',
      'fields': ['frequency', 'Hanzi', 'Count', ...],
      'templates': [{'name': 'Writing',
        'qfmt': '<a href="http://hanzi.koohii.com/study/?framenum={{text:Count}}">{{English}}</a>',
        'did': None,
        'bafmt': '',
        'afmt': '{{FrontSide}}\n\n<hr id=answer>\n ...',
        'ord': 0,
        'bqfmt': ''},
       {'name': 'Meaning',
        'qfmt': '<span class="hanzi"><a href="http://www.nciku.com/search/zh/{{text:Hanzi}}" style="text-decoration:none; color: black">{{Hanzi}}</a></span>\n<br>\nMeaning:\n{{type:English}}',
        'did': None,
        'bafmt': '',
        'afmt': '{{FrontSide}}\n\n<hr id=answer>\n ...',
        'ord': 1,
        'bqfmt': ''},
       {'name': 'Reading',
        'qfmt': '<span class="hanzi"><a href="http://www.nciku.com/search/zh/{{text:Hanzi}}" style="text-decoration:none; color: black">{{Hanzi}}</a></span><br>\nReading:\n{{type:Pinyin}}',
        'did': None,
        'bafmt': '',
        'afmt': '{{FrontSide}}\n\n<hr id=answer>\n ...',
        'ord': 2,
        'bqfmt': ''}]},
     ...
    }
    >>> anki.decks
    {'1518095427151': {'did': '1518095427151',
      'name': 'Chinese::Vocab::English::21-30 Death::Level 21'},
     '1518098032250': {'did': '1518098032250',
      'name': 'Chinese::Hanzi::Meaning::61-100 Infinity::Level 77'},
     '1518097744745': {'did': '1518097744745',
      'name': 'Chinese::Hanzi::Writing::41-50 Paradise::Level 49'},
      ...
    }
    >>> anki.notes
    {'1419644212689': {'nid': '1419644212689',
      'mid': '1377171239634',
      'model': {'mid': '1377171239634',
       'name': 'SpoonFed',
       'fields': ['English', 'Pinyin', 'Hanzi', 'Audio'],
       'templates': [{'name': 'CE',
         'qfmt': '<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n[sound:silence.mp3]\n{{Audio}}',
         'did': None,
         'bafmt': '',
         'afmt': '<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n{{Pinyin}}<br>\n{{English}}<br>\n{{Audio}}',
         'ord': 0,
         'bqfmt': ''},
        {'name': 'EC',
         'qfmt': '{{English}}',
         'did': None,
         'bafmt': '',
         'afmt': '{{English}}<br>\n{{Pinyin}}<br>\n<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n{{Audio}}',
         'ord': 1,
         'bqfmt': ''}]},
      'content': ['Hello!', 'Nǐ hǎo!', '你好！', '[sound:tmp1cctcn.mp3]'],
      'tags': ['']},
      ...
    }
    >>> anki.cards
    {'1419644220831': {'cid': '1419644220831',
      'nid': '1419644212689',
      'note': {'nid': '1419644212689',
       'mid': '1377171239634',
       'model': {'mid': '1377171239634',
        'name': 'SpoonFed',
        'fields': ['English', 'Pinyin', 'Hanzi', 'Audio'],
        'templates': [{'name': 'CE',
          'qfmt': '<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n[sound:silence.mp3]\n{{Audio}}',
          'did': None,
          'bafmt': '',
          'afmt': '<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n{{Pinyin}}<br>\n{{English}}<br>\n{{Audio}}',
          'ord': 0,
          'bqfmt': ''},
         {'name': 'EC',
          'qfmt': '{{English}}',
          'did': None,
          'bafmt': '',
          'afmt': '{{English}}<br>\n{{Pinyin}}<br>\n<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n{{Audio}}',
          'ord': 1,
          'bqfmt': ''}]},
       'content': ['Hello!', 'Nǐ hǎo!', '你好！', '[sound:tmp1cctcn.mp3]'],
       'tags': ['']},
      'did': '1518099616462',
      'deck': {'did': '1518099616462',
       'name': 'Chinese::sentence::CE:: 1-10 Pleasant::Level  1'},
      'ord': 0},
      ...
    }
    >>> anki.close()

Using `readApkg()` as a context manager also works.

```python
from AnkiTools.tools.read import readApkg
with readApkg('Chinese.apkg') as anki:
    pass
```

`readAnki2()` also works the same way, but without `readAnki2.close()` function.

```python
from AnkiTools.tools.read import readAnki2
with readAnki2('collection.anki2') as anki:
    pass
```

Result formats
```
# Model
{
    'mid': model_id,
    'name': model_name,
    'fields': fieldNames,
    'templates': [{
            "name": template_name,
            "qfmt": question_markup,
            "did":null,
            "bafmt":"",
            "afmt": answer_markup,
            "ord": order_in_template,
            "bqfmt":""
         }, ... ]
}

# Deck
{
    'did': deck_id,
    'name': deck_name
}

# Note
{
    'nid': note_id,
    'mid': model_id,
    'model': {
        'mid': model_id,
        'name': model_name,
        'fields': fieldNames,
        'templates': templateNames
    }
    'content': list_of_contents,
    'tags': list_of_tags
}

# Card
{
    'cid': card_id
    'nid': note_id,
    'note': {
        'nid': note_id,
        'mid': model_id,
        'model': {
            'name': model_name,
            'fields': fieldNames,
            'templates': list_of_templates
        }
        'content': content,
        'tags': tags
    }
    'did': deck_id,
    'deck': {
        'did': deck_id,
        'name': v['name']
    }
    'ord': ord
}
```

See also the \*.apkg format documentation from [Anki decks collaboration Wiki](http://decks.wikia.com/wiki/Anki_APKG_format_documentation) and [AnkiDroid](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure)

## Editing a \*.apkg and \*.anki2 file without Anki

It will also generate a new model/deck/note/card, if one doesn't exist. The ID's are Unix timestamp in milliseconds.

Subdecks can be made by putting in `::`; for example, `Chinese::SpoonFedChinese`.

```python
from AnkiTools.tools.edit import editApkg

with edit.editApkg('Chinese.apkg') as anki:
    anki.updateModels([{
                        'mid': model_id,  # May be left out
                        'name': model_name,
                        'fields': list_of_field_names,
                        'templates': list_of_template_names

                    }])

    anki.updateDecks([{
                        'did': deck_id,  # May be left out
                        'name': deck_name
                    }])

    anki.updateNotes([{
                        'nid': note_id,  # May be left out
                        'mid': model_id,  # Must specify either mid or model
                        'model': {         # Will be ignored if mid is specified
                            'name': model_name,
                            'fields': list_of_field_names,
                            'templates': list_of_template_names

                        }
                        'content': list_of_field_contents,
                        'tags': list_of_tags
                    }])

    anki.updateCards([{
                        'cid': card_id,  # May be left out
                        'nid': note_id,  # Must specify either nid or note
                        'note': {
                            'model': {
                                'name': model_name,
                                'fields': list_of_field_names,
                                'templates': list_of_template_names

                            }
                            'content': list_of_field_contents,
                            'tags': list_of_tags
                        }
                        'did': deck_id,  # Must specify either did or deck
                        'deck': {
                            'name': deck_name
                        }
                        'ord': order_in_list_of_template_names
                    }])
```

## Exporting \*.anki2 to \*.apkg

```python
from AnkiTools.tools.edit import editAnki2

with edit.editAnki2('Chinese.anki2') as anki:
    anki.export()
```

## AnkiConnect module

```python
from AnkiTools.AnkiConnect import POST

POST('deckNames')
```

You can also specify `params=dict()` in POST. Version is set to `5` as per default. For what you can put in, please refer to [AnkiConnect](https://github.com/FooSoft/anki-connect).
