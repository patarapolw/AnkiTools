import json
from collections import OrderedDict

from AnkiTools import AnkiDirect


if __name__ == '__main__':
    with open('notes.json') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    api = AnkiDirect()
    api.add(data)
    api.conn.commit()
