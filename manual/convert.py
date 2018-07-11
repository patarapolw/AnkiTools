from tests.files import get_testing_file

from AnkiTools import anki_convert

if __name__ == '__main__':
    anki_convert(get_testing_file('testfile.xlsx'), out_file='testfile.apkg')
