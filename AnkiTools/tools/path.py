import os
import appdirs


def get_collection_path(account_name: str=None):
    if account_name is None:
        account_name = 'User 1'

    collection_path = os.path.join(appdirs.user_data_dir('Anki2'), account_name, 'collection.anki2')
    return collection_path
