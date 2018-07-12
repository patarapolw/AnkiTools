import pytest
import os
import tempfile

from AnkiTools import anki_convert

from .files import get_testing_file


@pytest.mark.parametrize('in_format, out_format', [
    ('.apkg', '.anki2'),
    ('.apkg', '.xlsx'),
    ('.anki2', '.apkg'),
    ('.anki2', '.xlsx'),
    ('.xlsx', '.anki2'),
    ('.xlsx', '.apkg')
])
def test_convert(in_format, out_format):
    in_file = get_testing_file('testfile' + in_format)

    out_file = os.path.join(tempfile.tempdir, os.path.splitext(os.path.split(in_file)[1])[0] + out_format)
    anki_convert(in_file, out_file=out_file)

    assert os.path.exists(out_file)
    # One might have to test manually that the out_file is openable and valid.
    # TODO: out_file *.xlsx, *.anki2, *.apkg verify
