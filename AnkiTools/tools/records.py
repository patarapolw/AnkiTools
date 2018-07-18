import namedlist as nl

from time import time
from collections import OrderedDict

from .defaults import (DEFAULT_COLLECTION,
                       DEFAULT_TEMPLATE,
                       DEFAULT_MODEL,
                       DEFAULT_NOTE,
                       DEFAULT_CARD,
                       DEFAULT_DECK)


model = DEFAULT_MODEL.to_json_object()
assert isinstance(model, OrderedDict)
minimal_fields = ['id', 'name', 'flds', 'mod']
model.update(dict.fromkeys(minimal_fields, nl.NO_DEFAULT))

ModelRecord = nl.namedlist('ModelRecord', model, default=NotImplemented)
MinimalModelRecord = nl.namedlist('MinimalModelRecord', minimal_fields)

del model, minimal_fields

fld = DEFAULT_MODEL['flds'][0]
assert isinstance(fld, OrderedDict)
minimal_fields = ['name', 'ord']
fld.update(dict.fromkeys(minimal_fields, nl.NO_DEFAULT))

FieldRecord = nl.namedlist('FieldRecord', fld, default=NotImplemented)

del fld, minimal_fields

tmpl = DEFAULT_TEMPLATE.to_json_object()
assert isinstance(tmpl, OrderedDict)
minimal_fields = ['name', 'qfmt', 'afmt']
tmpl.update(dict.fromkeys(minimal_fields, nl.NO_DEFAULT))

TemplateRecord = nl.namedlist('TemplateRecord', tmpl, default=NotImplemented)
MinimalTemplateRecord = nl.namedlist('MinimalTemplateRecord', minimal_fields, default=NotImplemented)

del tmpl, minimal_fields

note = DEFAULT_NOTE.to_json_object()
assert isinstance(note, OrderedDict)
minimal_fields = ['id', 'guid', 'mid', 'mod', 'flds', 'sfld', 'tags', 'csum']
formatted_fields = ['id', 'guid', 'mid', 'mod', 'flds', 'tags']
note.update(dict.fromkeys(minimal_fields, nl.NO_DEFAULT))

NoteRecord = nl.namedlist('NoteRecord', note, default=NotImplemented)

# Specifically, 'flds' and 'tags' must be formatted, that is, are lists.
FormattedNoteRecord = nl.namedlist('FormattedNoteRecord', formatted_fields, default=NotImplemented)

del note, minimal_fields, formatted_fields

card = DEFAULT_CARD.to_json_object()
assert isinstance(card, OrderedDict)
minimal_fields = ['id', 'nid', 'did', 'ord', 'mod', 'due']
formatted_fields = ['id', 'nid', 'did', 'ord', 'mod']
card.update(dict.fromkeys(minimal_fields, nl.NO_DEFAULT))

CardRecord = nl.namedlist('CardRecord', card, default=NotImplemented)

# 'due' is normally created anew as same as 'nid' anyways.
FormattedCardRecord = nl.namedlist('FormattedCardRecord', formatted_fields, default=NotImplemented)

del card, minimal_fields, formatted_fields

deck = DEFAULT_DECK.to_json_object()
assert isinstance(deck, OrderedDict)
minimal_fields = ['name', 'mod']
deck.update(dict.fromkeys(minimal_fields, nl.NO_DEFAULT))

DeckRecord = nl.namedlist('DeckRecord', deck, default=NotImplemented)

del deck, minimal_fields

collection = DEFAULT_COLLECTION.to_json_object()
assert isinstance(collection, OrderedDict)
minimal_fields = ['models', 'decks', 'mod']
collection.update({'crt': int(time()), 'scm': int(time() * 1000)})
collection.update(dict.fromkeys(minimal_fields, nl.NO_DEFAULT))

CollectionRecord = nl.namedlist('CollectionRecord', collection, default=NotImplemented)
MinimalCollectionRecord = nl.namedlist('MinimalCollectionRecord', minimal_fields, default=NotImplemented)

del collection, minimal_fields


def get_tables():
    result = dict()

    for k, v in globals().items():
        if is_camel(k) and '__module__' in v.__dict__.keys():
            result[k] = v

    return result


def is_camel(s):
    return s != s.lower() and s != s.upper() and "_" not in s
