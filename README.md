# AnkiTools

An Anki \*.apkg and \*.anki2 reader/editor to work with in Python. Also included a module on [AnkiConnect](https://github.com/FooSoft/anki-connect).

## Parsing \*.apkg and \*.anki2 in a human readable and easily manageable format.

```python
from AnkiTools.tools.read import readApkg

with readApkg('Chinese.apkg')) as anki:
    anki.midToModel('xxxxxxx')
    anki.didToDeck('xxxxxxx')
    anki.nidToNote('xxxxxxx')
    anki.cidToCard('xxxxxxx')

Also,

with readAnki2('collection.anki2')) as anki:
    ...
```

Result formats
```
model = {
    'mid': mid,
    'name': v['name'],
    'fields': fieldNames,
    'templates': templateNames
}
deck = {
    'did': did,
    'name': v['name']
}
note = {
    'nid': nid,
    'mid': mid,
    'content': content,
    'tags': tags
}
card = {
    'cid': cid,
    'nid': nid,
    'did': did,
    'ord': ord
}
```

I also added searching with regex
```python
    anki.getDecks('^Chinese::Hanzi')
    anki.getNotesByField(model_id, field_number, regex)
```

For searching cards, you will need querying, which take a little long to load, so I created a separate function `loadQuery()`.
```python
    anki.loadQuery() # Takes around 90 seconds to load
    params = {
        'type': type,
        'key': key,
        'i': field_number or something_of_that_sort
    }
    anki.getCardQuery(regex, params)
```

Query format
```
query = {
    'cid': card['cid'],
    'note': self.nidToNote(card['nid']),
    'deck': self.didToDeck(card['did']),
    'ord': card['ord'],
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
                        'mid': model_id,
                        'name': model_name,
                        'fields': list_of_field_names,
                        'templates': list_of_template_names

                    }])

    anki.updateDecks([{
                        'did': deck_id,
                        'name': deck_name
                    }])

    anki.updateNotes([{
                        'nid': note_id,
                        'mid': model_id,
                        'content': list_of_field_contents.join('\x1f'),
                        'tags': list_of_tags.join(' ')
                    }])

    anki.updateCards([{
                        'cid': card_id,
                        'nid': note_id,
                        'did': deck_id,
                        'ord': order_in_list_of_template_names
                    }])
    anki.updateCardQueries([{
                              'cid': card_id,
                              'note': {
                                           'nid': note_id,
                                           'mid': model_id,
                                           'content': list_of_field_contents.join('\x1f'),
                                           'tags': list_of_tags.join(' ')
                                       }
                              'deck': {
                                          'did': deck_id,
                                          'name': deck_name
                                      }
                              'ord': order_in_list_of_template_names,
                          }])
```

## AnkiConnect module

```python
from AnkiTools.AnkiConnect import POST

POST('deckNames')
```

You can also specify `params=dict()` in POST. Version is set as `5` as per default. For what you can put in, please refer to [AnkiConnect](https://github.com/FooSoft/anki-connect).
