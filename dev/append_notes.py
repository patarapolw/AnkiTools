import json
from collections import OrderedDict

from AnkiTools.api import ankidirect

if __name__ == '__main__':
    with open('add_info.json') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    api = ankidirect()
    api.add(data)
    api.conn.commit()
