from AnkiTools.tools.tables import *


if __name__ == '__main__':
    for table in get_tables().values():
        print(table())
