import sqlite3
from time import time

from AnkiTools.tools.path import get_collection_path
from AnkiTools.tools.create import AnkiContentCreator
from AnkiTools.tools.write import write_anki_json, write_anki_table
from AnkiTools.tools.read import read_anki_json, read_anki_table
from AnkiTools.tools.verify import AnkiContentVerify


class AnkiDirect:
    def __init__(self, anki_database: str=None):
        if anki_database is None:
            anki_database = get_collection_path()

        self.conn = sqlite3.connect(anki_database)
        self.ids = {
            'notes': dict(),
            'cards': dict(),
            'models': dict(),
            'decks': dict()
        }
        self.name_to_id = {
            'models': dict(),
            'decks': dict()
        }
        self.anki_creator = AnkiContentCreator(self.ids)
        self.anki_verify = AnkiContentVerify(self.ids)

    def add(self, data):
        modified = int(time())

        for model_name, notes in data['data'].items():
            model_id = self.get_model_id(model_name,
                                         notes[0]['data'].keys(),
                                         data['definitions'].get(model_name, dict()))
            anki_notes = []
            anki_cards = []
            anki_decks = []
            for note in notes:
                anki_note = self.anki_creator.new_note(flds_list=list(note['data'].values()),
                                                       model_id=model_id,
                                                       modified=modified)
                self.ids['notes'][str(anki_note['id'])] = anki_note
                anki_notes.append(anki_note)

                for note_side, deck_name in note['decks'].items():
                    try:
                        deck_id = self.name_to_id['decks'][deck_name]
                    except KeyError:
                        anki_deck = self.anki_creator.new_deck(deck_name)
                        self.ids['decks'][str(anki_deck['id'])] = anki_deck
                        anki_decks.append(anki_deck)

                        deck_id = anki_deck['id']
                        self.name_to_id['decks'][deck_name] = deck_id

                    anki_card = self.anki_creator.new_card(anki_note['id'],
                                                           deck_id,
                                                           self.get_card_ordering(model_id, note_side),
                                                           modified=modified)
                    self.ids['cards'][str(anki_card['id'])] = anki_card
                    anki_cards.append(anki_card)

            missing_deck_names = self.anki_verify.missing_decks()
            for deck_name in missing_deck_names:
                anki_deck = self.anki_creator.new_deck(deck_name)
                self.ids['decks'][str(anki_deck['id'])] = anki_deck
                anki_decks.append(anki_deck)

            write_anki_table(self.conn, 'notes', anki_notes, do_commit=False)
            write_anki_table(self.conn, 'cards', anki_cards, do_commit=False)
            write_anki_json(self.conn, 'decks', anki_decks, do_commit=False)

        self.conn.commit()

    def get_model_id(self, model_name, model_header, model_definition, **kwargs):
        try:
            model_id = self.name_to_id['models'][model_name]
        except KeyError:
            anki_model = self.anki_creator.new_model(model_name, model_header, model_definition,
                                                     modified=kwargs.get('modified', None))
            self.ids['models'][str(anki_model['id'])] = anki_model
            write_anki_json(self.conn, 'models', [anki_model], do_commit=True)

            model_id = anki_model['id']
            self.name_to_id['models'][model_name] = model_id

        return model_id

    def get_card_ordering(self, model_id, note_side):
        note_sides = [template['name'] for template in self.ids['models'][str(model_id)]['tmpls']]
        return note_sides.index(note_side)

    @property
    def models_dict(self):
        return read_anki_json(self.conn, 'models')

    @property
    def decks_dict(self):
        return read_anki_json(self.conn, 'decks')

    @property
    def notes(self):
        yield from read_anki_table(self.conn, 'notes')

    @property
    def cards(self):
        yield from read_anki_table(self.conn, 'cards')
