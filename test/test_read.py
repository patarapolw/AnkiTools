import unittest

from AnkiTools.tools.read import readApkg, readAnki2


class Test(unittest.TestCase):
    def test_read_apkg(self):
        with readApkg('testfile/Chinese.apkg') as anki:
            self.assertEqual(anki.notes['1419644212689']['content'][2], '你好！')
            self.assertEqual(anki.cards['1419644220831']['nid'], '1419644212689')

    def test_read_anki2(self):
        anki = readAnki2('testfile/Chinese.anki2')
        self.assertEqual(anki.notes['1419644212689']['content'][2], '你好！')
        self.assertEqual(anki.cards['1419644220831']['nid'], '1419644212689')


if __name__ == '__main__':
    unittest.main()
