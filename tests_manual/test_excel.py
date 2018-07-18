import openpyxl

import simplejson as json

from AnkiTools._excel import AnkiExcelSync as ObsoleteAnkiExcelSync
from AnkiTools.excel.app import AnkiExcelSync
from AnkiTools.tools.path import get_collection_path
from AnkiTools.dir import excel_path


def get_file():
    axsync = ObsoleteAnkiExcelSync('formatting.xlsx', get_collection_path())
    axsync.save()


def get_data():
    axsync = AnkiExcelSync('test.xlsx', get_collection_path())
    with open('AnkiExcelSync.excel_raw.json', 'w') as f:
        json.dump(axsync.excel_raw, f, ensure_ascii=False, indent=2)


def save_data():
    axsync = AnkiExcelSync('output/generated.xlsx', get_collection_path())
    axsync.save()


def read_formatting():
    formatted_wb = openpyxl.load_workbook(excel_path('default.xlsx'))
    unformatted_wb = openpyxl.Workbook()

    ws = formatted_wb.active
    params = dict()
    for col_letter, col_data in ws.column_dimensions.items():
        params[col_letter] = col_data.__dict__

    ws = unformatted_wb.active
    for col_letter, col_format in params.items():
        ws.column_dimensions[col_letter].__dict__ = col_format
    print([(col_letter, col_data.__dict__) for col_letter, col_data in ws.column_dimensions.items()])


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)

    save_data()
