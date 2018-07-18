from time import time
from collections import OrderedDict
from bs4 import BeautifulSoup
from hashlib import sha1
import simplejson as json

from .defaults import DEFAULT_API_MODEL_DEFINITION, DEFAULT_MODEL, DEFAULT_COLLECTION
from .records import (ModelRecord, TemplateRecord, FieldRecord, NoteRecord, CardRecord, DeckRecord, CollectionRecord)
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
        self.guids = set()

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

        model = ModelRecord()
        model._update(kwargs)

        model.id = model_id
        model.tmpls = tmpls
        model.css = css
        model.mod = modified

        model.name = model_name
        model.flds = [self.new_field(field_name, i, **kwargs.get('flds_kwargs', dict()))
                      for i, field_name in enumerate(model_header)]

        self.creation_check(model)

        return model

    def new_field(self, field_name: str, ordering: int, **kwargs):
        """
        Fields have no unique ID.
        :param field_name:
        :param ordering:
        :param kwargs:
        :return:
        """
        field = FieldRecord()
        field._update(kwargs)

        field.name = field_name
        field.ord = ordering

        self.creation_check(field)

        return field

    def new_template(self, template_name: str, ordering: int, formatting: dict=None, header: list=None,
                     **kwargs):
        """
        Templates have no unique ID.
        :param template_name:
        :param ordering:
        :param formatting:
        :param list of str header: header names / keys of a note
        :param kwargs:
        :return:
        """
        if formatting is None:
            default_tmpl = DEFAULT_API_MODEL_DEFINITION['templates'][0]
            formatting = {
                'qfmt': default_tmpl['data']['qfmt'] % header[0],
                'afmt': default_tmpl['data']['afmt'] % header[1]
            }

        kwargs.update(**formatting)

        template = TemplateRecord()
        template._update(kwargs)

        template.name = template_name
        template.ord = ordering

        self.creation_check(template)

        return template

    def new_note(self, flds_list: iter, model_id: int, modified: int=None, tags_list: iter=None, **kwargs):
        if tags_list is None:
            tags_list = []
        if modified is None:
            modified = int(time())

        sfld = BeautifulSoup(str(flds_list[0]), 'html.parser').text

        note = NoteRecord()
        note._update(kwargs)

        note.id = self._unique_id('notes')
        note.guid = self._unique_guid()
        note.mid = model_id

        note.mod = modified
        note.flds = '\u001f'.join([str(fld) for fld in flds_list])
        note.sfld = sfld
        note.csum = sha1(sfld.encode('utf8')).hexdigest()
        note.tags = ' '.join(tags_list)

        self.creation_check(note)

        return note

    def new_card(self, note_id: int, deck_id: int, ordering: int, modified: int, **kwargs):
        card = CardRecord()
        card._update(kwargs)

        card.id = self._unique_id('cards')
        card.nid = note_id
        card.did = deck_id
        card.ord = ordering
        card.mod = modified
        card.due = note_id

        self.creation_check(card)

        return card

    def new_deck(self, deck_name, **kwargs):
        deck = DeckRecord()
        deck._update(kwargs)

        deck.name = deck_name
        deck.mod = int(time())

        self.creation_check(deck)

        return deck

    def new_collection(self, modified: int=None, models_list=None, decks_list=None, **kwargs):
        """

        :param int modified:
        :param list of ModelRecord models_list:
        :param list of DeckRecord decks_list:
        :param kwargs:
        :return:
        """
        if modified is None:
            modified = int(time() * 1000)

        if models_list is None:
            models_dict = DEFAULT_COLLECTION['models']
        else:
            models_dict = dict()
            for model in models_list:
                models_dict[model.id] = model

        if decks_list is None:
            decks_dict = DEFAULT_COLLECTION['decks']
        else:
            decks_dict = dict()
            for deck in decks_list:
                decks_dict[deck.id] = deck

        collection = CollectionRecord()
        collection._update(kwargs)

        collection.mod = modified
        collection.models = kwargs.get('models', json.dumps(models_dict))
        collection.decks = kwargs.get('decks', json.dumps(decks_dict))

        self.creation_check(collection)

        return collection

    def _unique_id(self, item_type: str):
        item_id = int(time() * 1000)
        while item_id in self.ids[item_type]:
            item_id += 1
        self.ids[item_type].add(item_id)

        return item_id

    def _unique_guid(self):
        guid = guid64()
        while guid in self.guids:
            guid = guid64()

        return guid

    @staticmethod
    def creation_check(namedlist):
        for item_type, item in namedlist._asdict().items():
            assert item is not NotImplemented, "{} is NotImplemented".format(item_type)
