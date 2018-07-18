from pathlib import Path

from AnkiTools.convert import anki_convert


def test_convert_from_excel(module_path):
    in_files_list = [
        'generated.xlsx',
        'generated_old.xlsx',
        'regular.xlsx'
    ]

    for in_file in in_files_list:
        assert isinstance(module_path, Path)

        in_file = module_path.joinpath('tests/input').joinpath(in_file)
        out_file = module_path.joinpath('tests/output').joinpath(in_file.stem).with_suffix('.apkg')

        anki_convert(in_file, out_file=out_file)

        print('Please ensure that {} can be opened, and is formatted correctly.'
              .format(in_file.absolute()))
