import openpyxl

from AnkiTools.dir import excel_path


if __name__ == '__main__':
    wb = openpyxl.load_workbook(excel_path('default.xlsx'))
    ws = wb['.default']
    print(list(ws.column_dimensions.values())[0])
