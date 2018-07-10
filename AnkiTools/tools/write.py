import json


def write_anki_table(conn, table_name, new_records, do_commit=True):
    """

    :param sqlite3.Connection conn:
    :param 'notes'|'cards' table_name:
    :param iter of OrderedDict new_records:
    :param bool do_commit:
    :return:
    """
    for new_record in new_records:
        conn.execute('INSERT INTO {} ({}) VALUES ({})'
                     .format(table_name,
                             ','.join(new_record.keys()), ','.join(['?' for _ in range(len(new_record))])),
                     tuple(new_record.values()))
    if do_commit:
        conn.commit()


def write_anki_json(conn, json_name, new_dicts, do_commit=True):
    """

    :param sqlite3.Connection conn:
    :param 'models'|'decks' json_name:
    :param iter of dict new_dicts:
    :param bool do_commit:
    :return:
    """
    cursor = conn.execute('SELECT {} FROM col'.format(json_name))
    json_item = json.loads(cursor.fetchone()[0])

    for new_dict in new_dicts:
        json_item[new_dict['id']] = new_dict

    conn.execute('UPDATE col SET {}=?'.format(json_name), (json.dumps(json_item),))

    if do_commit:
        conn.commit()
