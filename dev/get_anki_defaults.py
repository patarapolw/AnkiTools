import json
from json.decoder import JSONDecodeError
import sqlite3
from collections import OrderedDict

from AnkiTools.tools.path import get_collection_path
from AnkiTools.tools.read import read_anki_table
from AnkiTools.dir import module_path


def get_anki_defaults(file_output=None, formatted=False):
    """

    :param None|bool|str file_output:
    :param bool formatted:
    :return:
    """
    if formatted:
        default_filename = 'defaults_formatted.json'
    else:
        default_filename = 'defaults.json'

    file_output = {
        None: None,
        False: None,
        True: module_path(default_filename)
    }.get(file_output, file_output)

    defaults = OrderedDict()

    with sqlite3.connect(get_collection_path()) as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for row in cursor:
            table_name = row[0]

            try:
                defaults[table_name] = next(read_anki_table(conn, table_name))
            except StopIteration:
                defaults[table_name] = None
                continue

            if formatted is not None:
                for k, v in defaults[table_name].items():
                    if formatted is True:
                        if isinstance(v, str):
                            try:
                                defaults[table_name][k] = {
                                    'is_json': True,
                                    'data': json.loads(v, object_pairs_hook=OrderedDict)
                                }
                            except JSONDecodeError:
                                pass

    if file_output is None:
        print(json.dumps(defaults, indent=2))
    else:
        with open(file_output, 'w') as f:
            json.dump(defaults, f, indent=2)


if __name__ == '__main__':
    get_anki_defaults(file_output=True, formatted=False)
    get_anki_defaults(file_output=True, formatted=True)
