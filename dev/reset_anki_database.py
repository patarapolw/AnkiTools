import os
from AnkiTools.tools.path import get_collection_path


if __name__ == '__main__':
    os.remove(get_collection_path())
    # Then, open Anki, and it will auto-generate the database
