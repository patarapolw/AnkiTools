import shutil
from tempfile import mkdtemp, mktemp
import os
from zipfile import ZipFile

from .excel.app import AnkiExcelSync


class AnkiFormatEditor:
    def __init__(self):
        self.tempdir = mkdtemp()

    def convert(self, in_file, out_file=None, out_format=None):
        in_file_type = os.path.splitext(in_file)[1]

        if out_format is None:
            assert out_file is not None, "Either out_file or out_format must be specified."

            out_file_type = os.path.splitext(out_file)[1]
        else:
            if out_format[0] == '.':
                out_file_type = out_format
            else:
                out_file_type = '.' + out_format

            if out_file is not None:
                out_file_header = os.path.splitext(out_file)[0]
            else:
                out_file_header = os.path.splitext(in_file)[0]

            out_file = '{}{}'.format(out_file_header, out_file_type)

        assert in_file_type != out_file_type, 'File types must be different'

        conversion = (in_file_type, out_file_type)
        if conversion == ('.apkg', '.anki2'):
            self.unzip(in_file, out_file=out_file)
        elif conversion == ('.apkg', '.xlsx'):
            self.export_anki_sqlite(self.unzip(in_file,
                                               os.path.join(self.tempdir, mktemp())),
                                    out_file)
        elif conversion == ('.anki2', '.apkg'):
            self.zip(in_file, out_file)
        elif conversion == ('.anki2', '.xlsx'):
            self.export_anki_sqlite(in_file, out_file)
        elif conversion == ('.xlsx', '.anki2'):
            self.import_anki_sqlite(in_file, out_file, out_path='')
        elif conversion == ('.xlsx', '.apkg'):
            self.zip(self.import_anki_sqlite(in_file), out_file)
        else:
            raise Exception("Unsupported conversion.")

    def unzip(self, in_file, out_file):
        with ZipFile(in_file) as zf:
            zf.extract('collection.anki2', path=self.tempdir)
        shutil.move(os.path.join(self.tempdir, 'collection.anki2'),
                    out_file)

        return out_file

    @staticmethod
    def zip(in_file, out_file):
        with ZipFile(out_file, 'w') as zf:
            zf.write(in_file, arcname='collection.anki2')
            zf.writestr('media', '{}')

    @staticmethod
    def export_anki_sqlite(in_file, out_file):
        with AnkiExcelSync(anki_database=in_file, excel_filename=out_file) as sync_portal:
            sync_portal.to_excel()

    def import_anki_sqlite(self, in_file, out_file=None, out_path=''):
        if out_file is None:
            out_file = os.path.join(self.tempdir, 'collection.anki2')

        with AnkiExcelSync(anki_database=out_file, excel_filename=in_file, read_only=True) as sync_portal:
            sync_portal.to_sqlite()

        return os.path.join(out_path, out_file)


def anki_convert(in_file, out_file=None, out_format=None, out_path=None):
    AnkiFormatEditor().convert(in_file, out_file, out_format)
