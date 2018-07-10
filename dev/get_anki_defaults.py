import json
import sqlite3
from collections import OrderedDict

from AnkiTools.tools.path import get_collection_path
from AnkiTools.tools.read import read_anki_json
from AnkiTools.dir import module_path


if __name__ == '__main__':
    defaults = OrderedDict()

    with sqlite3.connect(get_collection_path()) as conn:
        defaults['decks'] = read_anki_json(conn, 'decks')
        defaults['models'] = read_anki_json(conn, 'models')

    with open(module_path('defaults.json'), 'w') as f:
        json.dump(defaults, f, indent=2)
