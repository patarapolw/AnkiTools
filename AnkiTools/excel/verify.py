import pyexcel_xlsx
import logging

debug_logger = logging.getLogger('debug')


def is_valid_excel(excel_filename):
    raw = pyexcel_xlsx.get_data(excel_filename)

    return is_valid_excel_raw(raw)


def is_valid_excel_raw(excel_raw):
    try:
        for sheet_name, data in excel_raw.items():
            if not sheet_name.startswith('.'):
                assert data, "There is no data in worksheet {}".format(sheet_name)
                assert data[1:], "There is only header in worksheet {}".format(sheet_name)
                assert data[1][0], "There is only header in worksheet {}".format(sheet_name)
    except AssertionError as e:
        debug_logger.debug(e)

        return False

    return True
