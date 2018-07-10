from time import time
from collections import OrderedDict
from bs4 import BeautifulSoup
from hashlib import sha1

from AnkiTools.tools.defaults import DEFAULT_TEMPLATE, DEFAULT_MODEL, DEFAULT_API_MODEL_DEFINITION
from AnkiTools.tools.guid import guid64


class AnkiContentCreator:
    def __init__(self, ids=None):
        """

        :param dict ids:
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

        css = kwargs.get('css', model_definition['css'])
        if css is None:
            css = DEFAULT_TEMPLATE['css']

        model_id = self._unique_id('models')

        model = {
            "vers": kwargs.get('vers', []),
            "name": model_name,
            "tags": kwargs.get('tags', []),
            "did": kwargs.get('did', None),
            "usn": kwargs.get('usn', -1),
            "req": kwargs.get('req', [[0, "all",[0]]]),
            "flds": [self.new_field(field_name, i, **kwargs.get('flds_kwargs', dict()))
                     for i, field_name in enumerate(model_header)],
            "sortf": kwargs.get('sortf', 0),
            "latexPre": kwargs.get('latexPre', DEFAULT_MODEL['latexPre']),
            "tmpls": tmpls,
            "latexPost": kwargs.get('latexPost', DEFAULT_MODEL['latexPost']),
            "type": kwargs.get('type', 0),
            "id": model_id,
            "css": css,
            "mod": modified
        }

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
        field = {
            'name': field_name,
            'rtl': kwargs.get('rtl', False),
            'sticky': kwargs.get('sticky', False),
            'media': kwargs.get('media', []),
            'ord': ordering,
            'font': kwargs.get('font', 'Arial'),
            'size': kwargs.get('size', 12)
        }

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

        template = {
            'name': template_name,
            'qfmt': kwargs.get('qfmt', DEFAULT_TEMPLATE['qfmt']),
            'did': kwargs.get('did', None),
            'bafmt': kwargs.get('bafmt', DEFAULT_TEMPLATE['bafmt']),
            'afmt': kwargs.get('afmt', DEFAULT_TEMPLATE['afmt']),
            'ord': ordering,
            'bqfmt': kwargs.get('bqfmt', DEFAULT_TEMPLATE['bqfmt'])
        }

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
            ('usn', kwargs.get('usn', -1)),
            ('tags', ' '.join(tags_list)),
            ('flds', '\x1f'.join(flds_list)),
            ('sfld', sfld),
            ('csum', sha1(sfld.encode('utf8')).hexdigest()),
            ('flags', kwargs.get('flags', 0)),
            ('data', kwargs.get('data', ''))
        ])

        assert len(note) == 11, 'Invalid Anki Note format.'

        return note

    def new_card(self, note_id: int, deck_id: int, ordering: int, modified: int, **kwargs):
        card = OrderedDict([
            ('id', self._unique_id('cards')),
            ('nid', note_id),
            ('did', deck_id),
            ('ord', ordering),
            ('mod', modified),
            ('usn', kwargs.get('usn', -1)),
            ('type', kwargs.get('type', 0)),
            ('queue', kwargs.get('queue', 0)),
            ('due', kwargs.get('due', note_id)),
            ('ivl', kwargs.get('ivl', 0)),
            ('factor', kwargs.get('factor', 0)),
            ('reps', kwargs.get('reps', 0)),
            ('lapses', kwargs.get('lapses', 0)),
            ('left', kwargs.get('left', 0)),
            ('odue', kwargs.get('odue', 0)),
            ('odid', kwargs.get('odid', 0)),
            ('flags', kwargs.get('flags', 0)),
            ('data', kwargs.get('data', ''))
        ])

        assert len(card) == 18, 'Invalid Anki Card format.'

        return card

    def new_deck(self, deck_name, **kwargs):
        deck = {
            'desc': kwargs.get('desc', ''),
            'name': deck_name,
            'extendRev': kwargs.get('extendRev', 50),
            'usn': kwargs.get('usn', 0),
            'collapsed': kwargs.get('collapsed', False),
            'newToday': kwargs.get('newToday', [0, 0]),
            'timeToday': kwargs.get('timeToday', [0, 0]),
            'dyn': kwargs.get('dyn', 0),
            'extendNew': kwargs.get('extendNew', 10),
            'conf': kwargs.get('conf', 1),
            'revToday': kwargs.get('revToday', [0, 0]),
            'lrnToday': kwargs.get('lrnToday', [0, 0]),
            'id': self._unique_id('decks'),
            'mod': int(time())
        }

        return deck

    def _unique_id(self, item_type: str):
        item_id = int(time() * 1000)
        while item_id in self.ids[item_type]:
            item_id += 1
        self.ids[item_type].add(item_id)

        return item_id
