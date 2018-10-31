from .editor import AnkiFormatEditor


def anki_convert(in_file, out_file=None, out_format=None):
    AnkiFormatEditor().convert(in_file, out_file, out_format)
