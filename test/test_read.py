import pytest

from AnkiTools.tools.read import readApkg, readAnki2


def test_read_apkg():
    with readApkg('testfile/Chinese.apkg') as anki:
        assert anki.notes['1419644212689']['content'][2] == '你好！'
        assert anki.cards['1419644220831']['nid'] == '1419644212689'


def test_read_anki2():
    anki = readAnki2('testfile/Chinese.anki2')
    assert anki.notes['1419644212689']['content'][2] == '你好！'
    assert anki.cards['1419644220831']['nid'] == '1419644212689'


if __name__ == '__main__':
    pytest.main()
