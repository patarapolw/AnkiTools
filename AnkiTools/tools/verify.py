import os
import logging

from .sampling import get_representative_json

debug_logger = logging.getLogger('debug')


def is_valid_anki(anki_file, check_notes=True):
    anki_json = get_representative_json(anki_file)
    file_type = os.path.splitext(anki_file)[1]
    debug_logger.debug(file_type)

    empty_tables_allowed = ['graves', 'revlog']
    if not (file_type == '.apkg' and check_notes):
        empty_tables_allowed += ['notes', 'cards']

    debug_logger.debug(empty_tables_allowed)

    try:
        missing_tables = {'col', 'notes', 'cards'} \
                         - set([table.replace('_sample', '') for table in anki_json.keys()]) \
                         - set(empty_tables_allowed)
        assert len(missing_tables) == 0, "The following tables are missing, {}".format(missing_tables)

        for table_name, records in anki_json.items():
            table_name = table_name.replace('_sample', '')
            if table_name not in empty_tables_allowed:
                assert records is not None, "There are no record in table {}."\
                    .format(table_name)

    except AssertionError as e:
        debug_logger.debug(e)

        return False

    return True
