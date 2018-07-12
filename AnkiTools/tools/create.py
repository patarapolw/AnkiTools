from time import time
from collections import OrderedDict
from bs4 import BeautifulSoup
from hashlib import sha1
import json

from .defaults import (DEFAULT_COLLECTION,
                       DEFAULT_TEMPLATE,
                       DEFAULT_MODEL,
                       DEFAULT_API_MODEL_DEFINITION)
from .guid import guid64


class AnkiContentCreator:
    def __init__(self, ids=None, formatted_defaults=True):
        """

        :param dict ids:
        :param bool formatted_defaults:
        """
        if not ids:
            ids = {
                'models': dict(),
                'decks': dict(),
                'cards': dict(),
                'notes': dict()
            }

        self.ids = dict()
        for k, v in ids.items():
            self.ids[k] = set(ids[k].keys())

        self.formatted_defaults = formatted_defaults

    def new_model(self, model_name, model_header, model_definition=None, modified=None, **kwargs):
        """

        :param str model_name:
        :param list model_header:
        :param OrderedDict model_definition:
        :param int modified:
        :param kwargs:
        :return:
        """
        if not model_definition:
            model_definition = DEFAULT_API_MODEL_DEFINITION
        if not modified:
            modified = int(time())

        tmpls = kwargs.get('tmpls', [self.new_template(template['name'], i, formatting=template['data'])
                                     for i, template in enumerate(model_definition['templates'])])

        css = kwargs.get('css', model_definition.get('css', None))
        if css is None:
            css = DEFAULT_MODEL['css']

        model_id = self._unique_id('models')

        model = dict([
            ("vers", []),
            ("name", model_name),
            ("tags", []),
            ("did", None),
            ("usn", -1),
            ("req", [[0, "all", [0]]]),
            ("flds", [self.new_field(field_name, i, **kwargs.get('flds_kwargs', dict()))
                      for i, field_name in enumerate(model_header)]),
            ("sortf", 0),
            ("latexPre", DEFAULT_MODEL['latexPre']),
            ("tmpls", tmpls),
            ("latexPost", DEFAULT_MODEL['latexPost']),
            ("type", 0),
            ("id", model_id),
            ("css", css),
            ("mod", modified)
        ])

        for k, v in model.items():
            if k in kwargs.keys():
                model[k] = kwargs[k]

        return model

    @staticmethod
    def new_field(field_name: str, ordering: int, **kwargs):
        """
        Fields have no unique ID.
        :param field_name:
        :param ordering:
        :param kwargs:
        :return:
        """
        field = dict([
            ('name', field_name),
            ('rtl', False),
            ('sticky', False),
            ('media', []),
            ('ord', ordering),
            ('font', 'Arial'),
            ('size', 12)
        ])

        for k, v in field.items():
            if k in kwargs.keys():
                field[k] = kwargs[k]

        return field

    @staticmethod
    def new_template(template_name: str, ordering: int, formatting: dict=None, **kwargs):
        """
        Templates have no unique ID.
        :param template_name:
        :param ordering:
        :param formatting:
        :param kwargs:
        :return:
        """
        if formatting is not None:
            kwargs.update(formatting)

        template = dict([
            ('name', template_name),
            ('qfmt', DEFAULT_TEMPLATE['qfmt']),
            ('did', None),
            ('bafmt', DEFAULT_TEMPLATE['bafmt']),
            ('afmt', DEFAULT_TEMPLATE['afmt']),
            ('ord', ordering),
            ('bqfmt', DEFAULT_TEMPLATE['bqfmt'])
        ])

        for k, v in template.items():
            if k in kwargs.keys():
                template[k] = kwargs[k]

        return template

    def new_note(self, flds_list: iter, model_id: int, modified: int=None, tags_list: iter=None, **kwargs):
        if tags_list is None:
            tags_list = []
        if modified is None:
            modified = int(time())

        sfld = BeautifulSoup(flds_list[0], 'html.parser').text

        note = OrderedDict([
            ('id', self._unique_id('notes')),
            ('guid', guid64()),
            ('mid', model_id),
            ('mod', modified),
            ('usn', -1),
            ('tags', ' '.join(tags_list)),
            ('flds', '\x1f'.join(flds_list)),
            ('sfld', sfld),
            ('csum', sha1(sfld.encode('utf8')).hexdigest()),
            ('flags', 0),
            ('data', '')
        ])

        for k, v in note.items():
            if k in kwargs.keys():
                note[k] = kwargs[k]

        assert len(note) == 11, 'Invalid Anki Note format.'

        return note

    def new_card(self, note_id: int, deck_id: int, ordering: int, modified: int, **kwargs):
        card = OrderedDict([
            ('id', self._unique_id('cards')),
            ('nid', note_id),
            ('did', deck_id),
            ('ord', ordering),
            ('mod', modified),
            ('usn', -1),
            ('type', 0),
            ('queue', 0),
            ('due', note_id),  # Due is used differently for different card types:
                               #   new: note id or random int
                               #   due: integer day, relative to the collection's creation time
                               #   learning: integer timestamp
            ('ivl', 0),
            ('factor', 0),
            ('reps', 0),
            ('lapses', 0),
            ('left', 0),
            ('odue', 0),
            ('odid', 0),
            ('flags', 0),
            ('data', '')
        ])

        for k, v in card.items():
            if k in kwargs.keys():
                card[k] = kwargs[k]

        assert len(card) == 18, 'Invalid Anki Card format.'

        return card

    def new_deck(self, deck_name, **kwargs):
        deck = dict([
            ('desc', ''),
            ('name', deck_name),
            ('extendRev', 50),
            ('usn', 0),
            ('collapsed', False),
            ('newToday', [0, 0]),
            ('timeToday', [0, 0]),
            ('dyn', 0),
            ('extendNew', 10),
            ('conf', 1),
            ('revToday', [0, 0]),
            ('lrnToday', [0, 0]),
            ('id', self._unique_id('decks')),
            ('mod', int(time()))
        ])

        for k, v in deck.items():
            if k in kwargs.keys():
                deck[k] = kwargs[k]

        return deck

    def new_collection(self, modified: int=None, models=None, decks=None, **kwargs):
        """

        :param int modified:
        :param OrderedDict models:
        :param OrderedDict decks:
        :param kwargs:
        :return:
        """
        if modified is None:
            modified = int(time() * 1000)
        if models is None:
            models = DEFAULT_COLLECTION['models']
        if decks is None:
            decks = DEFAULT_COLLECTION['decks']

        collection = OrderedDict([
            ('id', 1),
            ('crt', int(time())),
            ('mod', modified),
            ('scm', int(time() * 1000)),
            ('ver', DEFAULT_COLLECTION['ver']),
            ('dty', 0),
            ('usn', 0),
            ('ls', 0),
            ('conf', json.dumps(DEFAULT_COLLECTION['conf'])),
            ('models', json.dumps(models)),
            ('decks', json.dumps(decks)),
            ('dconf', json.dumps(DEFAULT_COLLECTION['dconf'])),
            ('tags', json.dumps(DEFAULT_COLLECTION['tags']))
        ])

        for k, v in kwargs.items():
            if k in collection.keys():
                collection[k] = v

        return collection

    # @staticmethod
    # def stringify_for_sqlite(item_type, item):
    #     for header_item, is_json in IS_JSON[item_type].items():
    #         if is_json:
    #             item[header_item] = json.dumps(item[header_item], default=lambda obj: obj.__dict__)
    #
    #     return item

    def _unique_id(self, item_type: str):
        item_id = int(time() * 1000)
        while item_id in self.ids[item_type]:
            item_id += 1
        self.ids[item_type].add(item_id)

        return item_id
