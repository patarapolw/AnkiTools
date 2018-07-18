import sqlite3

from AnkiTools.tools.read import read_anki_json
from AnkiTools.tools.path import get_collection_path


def create_note_type():
    with sqlite3.connect(get_collection_path()) as conn:
        models = read_anki_json(conn, 'models')
        for model_id, model_dict in models.items():
            print(model_id)
            print(model_dict['name'])
            print([fld['name'] for fld in model_dict['flds']])
            print([(tmpl['name'], tmpl['qfmt'], tmpl['afmt']) for tmpl in model_dict['tmpls']])
            print(model_dict['css'])
            print()


if __name__ == '__main__':
    create_note_type()
