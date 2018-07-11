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


def write_anki_schema(conn):
    """

    :param sqlite3.Connection conn:
    :return:
    """

    conn.executescript("""
CREATE TABLE col (
    id              integer primary key,
    crt             integer not null,
    mod             integer not null,
    scm             integer not null,
    ver             integer not null,
    dty             integer not null,
    usn             integer not null,
    ls              integer not null,
    conf            text not null,
    models          text not null,
    decks           text not null,
    dconf           text not null,
    tags            text not null
);
CREATE TABLE notes (
    id              integer primary key,   /* 0 */
    guid            text not null,         /* 1 */
    mid             integer not null,      /* 2 */
    mod             integer not null,      /* 3 */
    usn             integer not null,      /* 4 */
    tags            text not null,         /* 5 */
    flds            text not null,         /* 6 */
    sfld            integer not null,      /* 7 */
    csum            integer not null,      /* 8 */
    flags           integer not null,      /* 9 */
    data            text not null          /* 10 */
);
CREATE TABLE cards (
    id              integer primary key,   /* 0 */
    nid             integer not null,      /* 1 */
    did             integer not null,      /* 2 */
    ord             integer not null,      /* 3 */
    mod             integer not null,      /* 4 */
    usn             integer not null,      /* 5 */
    type            integer not null,      /* 6 */
    queue           integer not null,      /* 7 */
    due             integer not null,      /* 8 */
    ivl             integer not null,      /* 9 */
    factor          integer not null,      /* 10 */
    reps            integer not null,      /* 11 */
    lapses          integer not null,      /* 12 */
    left            integer not null,      /* 13 */
    odue            integer not null,      /* 14 */
    odid            integer not null,      /* 15 */
    flags           integer not null,      /* 16 */
    data            text not null          /* 17 */
);
CREATE TABLE revlog (
    id              integer primary key,
    cid             integer not null,
    usn             integer not null,
    ease            integer not null,
    ivl             integer not null,
    lastIvl         integer not null,
    factor          integer not null,
    time            integer not null,
    type            integer not null
);
CREATE TABLE graves (
    usn             integer not null,
    oid             integer not null,
    type            integer not null
);
-- CREATE TABLE sqlite_stat1(tbl,idx,stat);
CREATE INDEX ix_notes_usn on notes (usn);
CREATE INDEX ix_cards_usn on cards (usn);
CREATE INDEX ix_revlog_usn on revlog (usn);
CREATE INDEX ix_cards_nid on cards (nid);
CREATE INDEX ix_cards_sched on cards (did, queue, due);
CREATE INDEX ix_revlog_cid on revlog (cid);
CREATE INDEX ix_notes_csum on notes (csum);
    """)
    conn.commit()
