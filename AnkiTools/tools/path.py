import appdirs
from pathlib import Path
import logging

debug_logger = logging.getLogger('debug')


def get_collection_path(account_name: str=None):
    if account_name is None:
        account_name = 'User 1'

    collection_path = Path(appdirs.user_data_dir('Anki2')).joinpath(account_name).joinpath('collection.anki2')

    debug_logger.debug(collection_path.absolute())

    return collection_path
