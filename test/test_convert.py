import pytest


from AnkiTools.tools.convert import *

APKG = 'testfile/Chinese.apkg'
ANKI2 = 'testfile/Chinese.anki2'


class TestFromApkg:
    def test_apkg2anki(self):
        apkg2anki(APKG)

    def test_apkg2csv(self):
        apkg2csv(APKG)

    def test_apkg2tsv(self):
        apkg2tsv(APKG)


@pytest.mark.skipif(not int(os.getenv('ALL_TESTS', '0')), reason='slow')
class TestFromApkgSlow:
    def test_apkg2sqlite(self):
        """ 43 seconds """
        apkg2sqlite(APKG)

    @pytest.mark.skipIf(int(os.getenv('NO_XLSX', '0')), reason='slow')
    def test_apkg2xlsx(self):
        """ 7 min 22 sec"""
        apkg2xlsx(APKG)


class TestFromAnki2:
    def test_anki2apkg(self):
        anki2apkg(ANKI2)

    def test_anki2csv(self):
        anki2csv(ANKI2)

    def test_anki2tsv(self):
        anki2tsv(ANKI2)


@pytest.mark.skipif(not int(os.getenv('ALL_TESTS', '0')), reason='slow')
class FromAnki2Slow:
    def test_anki2sqlite(self):
        """ 43 seconds """
        anki2sqlite(ANKI2)

    @pytest.mark.skipif(int(os.getenv('NO_XLSX', '0')), reason='slow')
    def test_anki2xlsx(self):
        """ 7 min 22 sec"""
        anki2xlsx(ANKI2)


if __name__ == '__main__':
    pytest.main(__file__)
