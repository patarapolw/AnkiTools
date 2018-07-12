import json

from AnkiTools._excel import AnkiExcelSync as ObsoleteAnkiExcelSync
from AnkiTools.excel.app import AnkiExcelSync
from AnkiTools.tools.path import get_collection_path


def get_file():
    axsync = ObsoleteAnkiExcelSync('formatting.xlsx', get_collection_path())
    axsync.save()


def get_data():
    axsync = AnkiExcelSync('test.xlsx', get_collection_path())
    with open('AnkiExcelSync.excel_raw.json', 'w') as f:
        json.dump(axsync.excel_raw, f, ensure_ascii=False, indent=2)


def save_data():
    axsync = AnkiExcelSync('test.xlsx', get_collection_path())
    axsync.save(formatted=True)


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    save_data()
