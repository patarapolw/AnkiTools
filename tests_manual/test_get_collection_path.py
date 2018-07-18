import shutil

from AnkiTools.tools.path import get_collection_path


if __name__ == '__main__':
    shutil.copy2(src=get_collection_path(), dst='output/collection.anki2')
