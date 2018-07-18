import simplejson as json
from collections import OrderedDict

from .records import NoteRecord, FormattedNoteRecord, CardRecord, FormattedCardRecord, MinimalModelRecord, DeckRecord


def read_anki_table(conn, table_name):
    """

    :param sqlite3.Connection conn:
    :param str table_name:
    :return generator of OrderedDict:
    """
    cursor = conn.execute('SELECT * FROM {}'.format(table_name))
    header = [description[0] for description in cursor.description]

    for record in cursor:
        output = OrderedDict(zip(header, record))

        yield output


def read_anki_json(conn, json_name):
    """

    :param sqlite3.Connection conn:
    :param str json_name:
    :return dict:
    """
    cursor = conn.execute('SELECT {} FROM col'.format(json_name))
    record = cursor.fetchone()

    if record is not None:
        return json.loads(record[0])
    else:
        return dict()


def read_anki_notes_iter(conn):
    for note in read_anki_table(conn, 'notes'):
        output = NoteRecord(**note)

        yield output


def read_anki_formatted_notes_iter(conn):
    for note in read_anki_table(conn, 'notes'):
        note['flds'] = note['flds'].split('\x1f')
        note['tags'] = note['tags'].split(' ')

        output = FormattedNoteRecord(*(note[k] for k in FormattedNoteRecord._fields))

        yield output


def read_anki_cards_iter(conn):
    for card in read_anki_table(conn, 'cards'):
        output = CardRecord(**card)

        yield output


def read_anki_formatted_cards_iter(conn):
    for card in read_anki_table(conn, 'cards'):
        output = FormattedCardRecord(*(card[k] for k in FormattedCardRecord._fields))

        yield output


def read_anki_minimal_models_dict_iter(conn):
    for model_id, model_dict in read_anki_json(conn, 'models').items():
        minimal_model_record = MinimalModelRecord(*(model_dict[k] for k in MinimalModelRecord._fields))

        yield model_id, minimal_model_record


def read_anki_decks_dict_iter(conn):
    for deck_id, deck_dict in read_anki_json(conn, 'decks').items():
        deck_record = DeckRecord(**deck_dict)

        yield deck_id, deck_record
