import sqlite3
from time import time
import psutil
from collections import OrderedDict
import logging
from pathlib import Path

from AnkiTools.tools.path import get_collection_path
from AnkiTools.tools.create import AnkiContentCreator
from AnkiTools.tools.write import write_anki_json, write_anki_table, write_anki_schema
from AnkiTools.tools.read import (read_anki_formatted_notes_iter,
                                  read_anki_formatted_cards_iter,
                                  read_anki_minimal_models_dict_iter,
                                  read_anki_decks_dict_iter)

from .verify import AnkiContentVerify

debugger_logger = logging.getLogger('debug')


class AnkiDirect:
    def __init__(self, anki_database=None):
        """

        :param str|Path anki_database:
        """
        if anki_database is None:
            anki_database = get_collection_path()
            try:
                assert 'Anki' not in (p.name() for p in psutil.process_iter()), \
                    "Please close Anki first before accessing Application Data collection.anki2 directly."
            except psutil.ZombieProcess as e:
                pass

        if not isinstance(anki_database, Path):
            anki_database = Path(anki_database)

        do_init = False
        if not anki_database.exists():
            do_init = True

        self.conn = sqlite3.connect(str(anki_database.absolute()))

        if do_init:
            self.creator = AnkiContentCreator()
            write_anki_schema(self.conn)
            anki_collection = self.creator.new_collection()
            write_anki_table(self.conn, 'col', [anki_collection], do_commit=True)
            self._id_to_record = self.data
        else:
            self._id_to_record = self.data
            self.creator = AnkiContentCreator(self._id_to_record)

        self._name_to_id = self.name_to_id

        self.verify = AnkiContentVerify(self._id_to_record)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.conn.close()

    @property
    def data(self):
        data = {
            'decks': OrderedDict(self.decks_dict_iter),
            'models': OrderedDict(self.models_dict_iter),
            'notes': OrderedDict(),
            'cards': OrderedDict()
        }

        for note_record in self.notes:
            data['notes'][str(note_record.id)] = note_record

        for card_record in self.cards:
            data['cards'][str(card_record.id)] = card_record

        return data

    @property
    def name_to_id(self):
        name_to_id = {
            'models': dict(),
            'decks': dict()
        }

        for model_id, model_record in self.models_dict_iter:
            name_to_id['models'][model_record.name] = model_id

        for deck_id, deck_record in self.decks_dict_iter:
            name_to_id['decks'][deck_record.name] = deck_id

        return name_to_id

    def _get_model_id(self, model_name, model_header, model_definition, **kwargs):
        try:
            model_id = self._name_to_id['models'][model_name]
        except KeyError as e:
            anki_model = self.creator.new_model(model_name, model_header, model_definition,
                                                modified=kwargs.get('modified', None))
            self._id_to_record['models'][str(anki_model.id)] = anki_model
            write_anki_json(self.conn, 'models', [anki_model], do_commit=True)

            model_id = anki_model.id
            self._name_to_id['models'][model_name] = model_id

        return model_id

    def _get_card_ordering(self, model_id, note_side):
        note_sides = [template.name for template in self._id_to_record['models'][str(model_id)].tmpls]
        return note_sides.index(note_side)

    @property
    def models_dict_iter(self):
        yield from read_anki_minimal_models_dict_iter(self.conn)

    @property
    def decks_dict_iter(self):
        yield from read_anki_decks_dict_iter(self.conn)

    @property
    def notes(self):
        yield from read_anki_formatted_notes_iter(self.conn)

    @property
    def cards(self):
        yield from read_anki_formatted_cards_iter(self.conn)

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
                self._id_to_record['notes'][str(anki_note.id)] = anki_note
                anki_notes.append(anki_note)

                for note_side, deck_name in note['decks'].items():
                    try:
                        deck_id = self._name_to_id['decks'][deck_name]
                    except KeyError:
                        anki_deck = self.creator.new_deck(deck_name)
                        self._id_to_record['decks'][str(anki_deck.id)] = anki_deck
                        anki_decks.append(anki_deck)

                        deck_id = anki_deck.id
                        self._name_to_id['decks'][deck_name] = deck_id

                    anki_card = self.creator.new_card(anki_note.id,
                                                      deck_id,
                                                      self._get_card_ordering(model_id, note_side),
                                                      modified=modified)
                    self._id_to_record['cards'][str(anki_card.id)] = anki_card
                    anki_cards.append(anki_card)

            missing_deck_names = self.verify.missing_decks()
            for deck_name in missing_deck_names:
                anki_deck = self.creator.new_deck(deck_name)
                self._id_to_record['decks'][str(anki_deck.id)] = anki_deck
                anki_decks.append(anki_deck)

            write_anki_table(self.conn, 'notes', anki_notes, do_commit=False)
            write_anki_table(self.conn, 'cards', anki_cards, do_commit=False)
            write_anki_json(self.conn, 'decks', anki_decks, do_commit=False)

        self.conn.commit()

        return True
