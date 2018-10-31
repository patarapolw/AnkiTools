import pytest
from pathlib import Path

from AnkiTools.convert import anki_convert
from AnkiTools.tools.verify import is_valid_anki


@pytest.mark.parametrize('in_file', [
    'test.apkg'
])
@pytest.mark.parametrize('out_format', [
    '.xlsx'
])
def test_convert_to_excel(in_file, out_format):
    in_file = Path('tests/input').joinpath(in_file)

    out_file = Path('tests/output').joinpath(in_file.name).with_suffix(out_format)
    anki_convert(in_file, out_file=out_file)
    assert out_file.exists()


# @pytest.mark.parametrize('in_file', [
#     'generated.xlsx',
#     'regular.xlsx'
# ])
# @pytest.mark.parametrize('out_format', [
#     '.apkg'
# ])
# def test_convert_from_excel(in_file, out_format):
#     in_file = Path('tests/input').joinpath(in_file)
#
#     out_file = Path('tests/output').joinpath(in_file.name).with_suffix(out_format)
#     anki_convert(in_file, out_file=out_file)
#     assert out_file.exists()
#
#     # One might have to test manually that the out_file is openable and valid.
#     assert is_valid_anki(out_file)
