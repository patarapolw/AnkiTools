import sqlite3
from time import time
import psutil
import os

from AnkiTools.tools.path import get_collection_path
from AnkiTools.tools.create import AnkiContentCreator
from AnkiTools.tools.write import write_anki_json, write_anki_table, write_anki_schema
from AnkiTools.tools.read import read_anki_json, read_anki_table

from .verify import AnkiContentVerify


class AnkiDirect:
    def __init__(self, anki_database: str=None):
        if anki_database is None:
            anki_database = get_collection_path()
            try:
                assert 'Anki' not in (p.name() for p in psutil.process_iter()), \
                    "Please close Anki first before accessing Application Data collection.anki2 directly."
            except psutil.ZombieProcess as e:
                print(e)

        do_init = False
        if not os.path.exists(anki_database):
            do_init = True

        self.conn = sqlite3.connect(anki_database)

        if do_init:
            self.creator = AnkiContentCreator()
            write_anki_schema(self.conn)
            anki_collection = self.creator.new_collection()
            write_anki_table(self.conn, 'col', [anki_collection], do_commit=True)

            self.models = self.get_models()
            self.decks = self.get_decks()
            self.notes = dict()
            self.cards = dict()
        else:
            self.models = self.get_models()
            self.decks = self.get_decks()
            self.notes = self.get_notes()
            self.cards = self.get_cards()

            self.creator = AnkiContentCreator({'notes': self.notes, 'cards': self.cards,
                                               'models': self.models, 'decks': self.decks})

        self._name_to_id = self.name_to_id

        self.verify = AnkiContentVerify({'notes': self.notes, 'cards': self.cards,
                                         'models': self.models, 'decks': self.decks})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.conn.close()

    @property
    def name_to_id(self):
        name_to_id = {
            'models': dict(),
            'decks': dict()
        }

        for k, v in self.models.items():
            name_to_id['models'][v['name']] = k

        for k, v in self.decks.items():
            name_to_id['decks'][v['name']] = k

        return name_to_id

    def _get_model_id(self, model_name, model_header, model_definition, **kwargs):
        try:
            model_id = self._name_to_id['models'][model_name]
        except KeyError:
            anki_model = self.creator.new_model(model_name, model_header, model_definition,
                                                modified=kwargs.get('modified', None))
            self.models[str(anki_model['id'])] = anki_model
            write_anki_json(self.conn, 'models', [anki_model], do_commit=True)

            model_id = anki_model['id']
            self._name_to_id['models'][model_name] = model_id

        return model_id

    def _get_card_ordering(self, model_id, note_side):
        note_sides = [template['name'] for template in self.models[str(model_id)]['tmpls']]
        return note_sides.index(note_side)

    def get_models(self):
        return read_anki_json(self.conn, 'models')

    def get_decks(self):
        return read_anki_json(self.conn, 'decks')

    def get_notes(self):
        note_dict = dict()
        for note in read_anki_table(self.conn, 'notes'):
            note_dict[str(note['id'])] = note

        return note_dict

    def get_cards(self):
        card_dict = dict()
        for card in read_anki_table(self.conn, 'cards'):
            card_dict[str(card['id'])] = card

        return card_dict

    def add(self, data):
        if not self.verify.verify_add_info(data):
            return False

        modified = int(time())

        for model_name, notes in data['data'].items():
            model_id = self._get_model_id(model_name,
                                          notes[0]['data'].keys(),
                                          data.get('definitions', dict()).get(model_name, dict()))
            anki_notes = []
            anki_cards = []
            anki_decks = []
            for note in notes:
                anki_note = self.creator.new_note(flds_list=list(note['data'].values()),
                                                  model_id=model_id,
                                                  modified=modified)
                self.notes[str(anki_note['id'])] = anki_note
                anki_notes.append(anki_note)

                for note_side, deck_name in note['decks'].items():
                    try:
                        deck_id = self._name_to_id['decks'][deck_name]
                    except KeyError:
                        anki_deck = self.creator.new_deck(deck_name)
                        self.decks[str(anki_deck['id'])] = anki_deck
                        anki_decks.append(anki_deck)

                        deck_id = anki_deck['id']
                        self._name_to_id['decks'][deck_name] = deck_id

                    anki_card = self.creator.new_card(anki_note['id'],
                                                      deck_id,
                                                      self._get_card_ordering(model_id, note_side),
                                                      modified=modified)
                    self.cards[str(anki_card['id'])] = anki_card
                    anki_cards.append(anki_card)

            missing_deck_names = self.verify.missing_decks()
            for deck_name in missing_deck_names:
                anki_deck = self.creator.new_deck(deck_name)
                self.decks[str(anki_deck['id'])] = anki_deck
                anki_decks.append(anki_deck)

            write_anki_table(self.conn, 'notes', anki_notes, do_commit=False)
            write_anki_table(self.conn, 'cards', anki_cards, do_commit=False)
            write_anki_json(self.conn, 'decks', anki_decks, do_commit=False)

        self.conn.commit()

        return True
