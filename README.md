# AnkiTools

An Anki \*.apkg and \*.anki2 reader/editor to work with in Python. Also included a module on [AnkiConnect](https://github.com/FooSoft/anki-connect).

## Installation

`pip install AnkiTools`

## Parsing \*.apkg and \*.anki2 in a human readable and easily manageable format.

```python
from AnkiTools.tools.read import readApkg

with readApkg('Chinese.apkg')) as anki:
    anki.models[mid]
    anki.decks[did]
    anki.notes[nid]
    anki.cards[cid]

Also,

with readAnki2('collection.anki2')) as anki:
    ...
```

Result formats
```
models[mid] = {
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
decks[did] = {
    'did': deck_id,
    'name': deck_name
}
notes[nid] = {
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
cards[cid] = {
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

I also added searching with regex
```python
    anki.getDecks('^Chinese::Hanzi')
    anki.getNotesByField(model_id, field_number, regex)
```

`anki.loadQuery()` is now obsolete. You can search cards by iterating through `anki.cards`. A function may be implemented later, if I feel the need.

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
