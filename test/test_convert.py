import unittest
import os


from AnkiTools.tools.convert import *

APKG = 'testfile/Chinese.apkg'
ANKI2 = 'testfile/Chinese.anki2'


class FromApkg(unittest.TestCase):
    def test_apkg2anki(self):
        apkg2anki(APKG)

    def test_apkg2csv(self):
        apkg2csv(APKG)

    def test_apkg2tsv(self):
        apkg2tsv(APKG)


@unittest.skipUnless(int(os.getenv('ALL_TESTS', '0')), 'slow')
class FromApkgSlow(unittest.TestCase):
    def test_apkg2sqlite(self):
        """ 43 seconds """
        apkg2sqlite(APKG)

    @unittest.skipIf(int(os.getenv('NO_XLSX', '0')), 'slow')
    def test_apkg2xlsx(self):
        """ 7 min 22 sec"""
        apkg2xlsx(APKG)


class FromAnki2(unittest.TestCase):
    def test_anki2apkg(self):
        anki2apkg(ANKI2)

    def test_anki2csv(self):
        anki2csv(ANKI2)

    def test_anki2tsv(self):
        anki2tsv(APKG)


@unittest.skipUnless(int(os.getenv('ALL_TESTS', '0')), 'slow')
class FromAnki2Slow(unittest.TestCase):
    def test_anki2sqlite(self):
        """ 43 seconds """
        anki2sqlite(APKG)

    @unittest.skipIf(int(os.getenv('NO_XLSX', '0')), 'slow')
    def test_anki2xlsx(self):
        """ 7 min 22 sec"""
        anki2xlsx(APKG)


if __name__ == '__main__':
    unittest.main()
