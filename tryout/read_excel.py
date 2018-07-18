import openpyxl

from conftest import module_path


if __name__ == '__main__':
    wb = openpyxl.load_workbook(module_path('default.xlsx'))
    ws = wb['.default']
    print(list(ws.column_dimensions.values())[0])
