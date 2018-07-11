import json
from collections import OrderedDict


def read_anki_table(conn, table_name):
    """

    :param sqlite3.Connection conn:
    :param str table_name:
    :return generator of OrderedDict:
    """
    cursor = conn.execute('SELECT * FROM {}'.format(table_name))
    header = [description[0] for description in cursor.description]

    for record in cursor:
        formatted_record = OrderedDict(zip(header, record))
        if table_name == 'notes':
            formatted_record['formatted_flds'] = formatted_record['flds'].split('\x1f')
            formatted_record['formatted_tags'] = formatted_record['tags'].split(' ')

        yield formatted_record


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
