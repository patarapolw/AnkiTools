import pytest
import os

from AnkiTools.convert import anki_convert
from AnkiTools.tools.verify import is_valid_anki

from .input import get_testing_file


@pytest.mark.parametrize('in_file', [
    'test.anki2',
    'test.apkg',
    'clean_collection.anki2',
    'dirty_collection.anki2',
    'generated.xlsx',
    'generated_old.xlsx',
    'regular.xlsx'
])
@pytest.mark.parametrize('out_format', [
    '.xlsx'
])
def test_convert_to_excel(in_file, out_format, tmpdir):
    in_file = get_testing_file(in_file)

    out_file = os.path.join(tmpdir.mkdir('tmp'), os.path.splitext(os.path.split(in_file)[1])[0] + out_format)
    anki_convert(in_file, out_file=out_file)
    assert os.path.exists(out_file)

    # TODO: out_file *.xlsx verify


@pytest.mark.parametrize('in_file', [
    'generated.xlsx',
    'generated_old.xlsx',
    'regular.xlsx'
])
@pytest.mark.parametrize('out_format', [
    '.apkg',
    '.anki2'
])
def test_convert_from_excel(in_file, out_format, tmpdir):
    in_file = get_testing_file(in_file)

    out_file = os.path.join(tmpdir.mkdir('tmp'), os.path.splitext(os.path.split(in_file)[1])[0] + out_format)
    anki_convert(in_file, out_file=out_file)
    assert os.path.exists(out_file)

    # One might have to test manually that the out_file is openable and valid.
    assert is_valid_anki(out_file)


@pytest.mark.parametrize('in_file', [
    'test.anki2',
    'test.apkg',
    'clean_collection.anki2',
    'dirty_collection.anki2'
])
@pytest.mark.parametrize('out_format', [
    '.apkg',
    '.anki2'
])
def test_convert_others(in_file, out_format, tmpdir):
    in_file = get_testing_file(in_file)
    in_format = os.path.splitext(in_file)[1]

    out_file = os.path.join(tmpdir.mkdir('tmp'), os.path.splitext(os.path.split(in_file)[1])[0] + out_format)
    if in_format == out_format:
        with pytest.raises(AssertionError) as excinfo:
            anki_convert(in_file, out_file=out_file)

        assert excinfo.value.args[0] == 'File types must be different'
    else:
        anki_convert(in_file, out_file=out_file)
        assert os.path.exists(out_file)

        # One might have to test manually that the out_file is openable and valid.
        if os.path.splitext(in_file)[1] in ('.anki2', '.apkg') and out_format == '.apkg':
            assert is_valid_anki(out_file, check_notes=False)
        else:
            assert is_valid_anki(out_file)
