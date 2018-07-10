import shutil
import atexit
import os
from zipfile import ZipFile

from AnkiTools.AnkiExcelSync import AnkiExcelSync


class AnkiFormatEditor:
    def __init__(self, tmp_path='tmp/'):
        self.tmp_path = tmp_path
        atexit.register(self.close)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        shutil.rmtree(self.tmp_path)

    def convert(self, in_file, out_file):
        in_file_type = os.path.splitext(in_file)[1]
        out_file_type = os.path.splitext(out_file)[1]

        assert in_file_type != out_file_type, 'File types must be different'

        convert_process = {
            ('.apkg', '.anki2'): self.unzip(in_file, out_file=out_file, out_path=''),
            ('.apkg', '.xlsx'): self.export_anki_sqlite(self.unzip(in_file, out_path=self.tmp_path), out_file),
            ('.anki2', '.apkg'): self.zip(in_file, out_file),
            ('.anki2', '.xlsx'): self.export_anki_sqlite(in_file, out_file),
            ('.xlsx', '.anki2'): self.import_anki_sqlite(in_file, out_file, out_path=''),
            ('.xlsx', '.apkg'): self.zip(self.import_anki_sqlite(in_file, out_path=self.tmp_path), out_file)
        }.get((in_file_type, out_file_type), False)

        assert convert_process is False, "Unsupported conversion."

    @staticmethod
    def unzip(in_file, out_file='collection.anki2', out_path=''):
        with ZipFile(in_file) as zf:
            zf.extract('collection.anki2', path=out_path)
        os.rename(os.path.join(out_path, 'collection.anki2'),
                  os.path.join(out_path, out_file))

        return os.path.join(out_path, out_file)

    @staticmethod
    def zip(in_file, out_file):
        with ZipFile(out_file, 'w') as zf:
            zf.write(in_file, arcname='collection.anki2')

    @staticmethod
    def export_anki_sqlite(in_file, out_file):
        with AnkiExcelSync(anki_database=in_file, excel=out_file) as sync_portal:
            sync_portal.to_excel()

    @staticmethod
    def import_anki_sqlite(in_file, out_file='collection.anki2', out_path=''):
        with AnkiExcelSync(anki_database=out_file, excel=in_file) as sync_portal:
            sync_portal.to_sqlite()

        return os.path.join(out_path, out_file)


def anki_convert(in_file, out_file):
    with AnkiFormatEditor() as afe:
        afe.convert(in_file, out_file)
