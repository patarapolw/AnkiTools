# -*- coding: utf-8 -*-

"""
>>> from AnkiTools.tools.read import readApkg
>>> anki = readApkg('test/testfile/Chinese.apkg')
>>> anki.models
# {'1514177308904': {'mid': '1514177308904',
#   'name': 'Chinese Hanzi Freq',
#   'fields': ['frequency', 'Hanzi', 'Count', ...],
#   'templates': [{'name': 'Writing',
#     'qfmt': '<a href="http://hanzi.koohii.com/study/?framenum={{text:Count}}">{{English}}</a>',
#     'did': None,
#     'bafmt': '',
#     'afmt': '{{FrontSide}}\n\n<hr id=answer>\n ...',
#     'ord': 0,
#     'bqfmt': ''},
#    {'name': 'Meaning',
#     'qfmt': '<span class="hanzi"><a href="http://www.nciku.com/search/zh/{{text:Hanzi}}" style="text-decoration:none; color: black">{{Hanzi}}</a></span>\n<br>\nMeaning:\n{{type:English}}',
#     'did': None,
#     'bafmt': '',
#     'afmt': '{{FrontSide}}\n\n<hr id=answer>\n ...',
#     'ord': 1,
#     'bqfmt': ''},
#    {'name': 'Reading',
#     'qfmt': '<span class="hanzi"><a href="http://www.nciku.com/search/zh/{{text:Hanzi}}" style="text-decoration:none; color: black">{{Hanzi}}</a></span><br>\nReading:\n{{type:Pinyin}}',
#     'did': None,
#     'bafmt': '',
#     'afmt': '{{FrontSide}}\n\n<hr id=answer>\n ...',
#     'ord': 2,
#     'bqfmt': ''}]},
#  ...
# }
>>> anki.decks
# {'1518095427151': {'did': '1518095427151',
#   'name': 'Chinese::Vocab::English::21-30 Death::Level 21'},
#  '1518098032250': {'did': '1518098032250',
#   'name': 'Chinese::Hanzi::Meaning::61-100 Infinity::Level 77'},
#  '1518097744745': {'did': '1518097744745',
#   'name': 'Chinese::Hanzi::Writing::41-50 Paradise::Level 49'},
#   ...
# }
>>> anki.notes
# {'1419644212689': {'nid': '1419644212689',
#   'mid': '1377171239634',
#   'model': {'mid': '1377171239634',
#    'name': 'SpoonFed',
#    'fields': ['English', 'Pinyin', 'Hanzi', 'Audio'],
#    'templates': [{'name': 'CE',
#      'qfmt': '<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n[sound:silence.mp3]\n{{Audio}}',
#      'did': None,
#      'bafmt': '',
#      'afmt': '<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n{{Pinyin}}<br>\n{{English}}<br>\n{{Audio}}',
#      'ord': 0,
#      'bqfmt': ''},
#     {'name': 'EC',
#      'qfmt': '{{English}}',
#      'did': None,
#      'bafmt': '',
#      'afmt': '{{English}}<br>\n{{Pinyin}}<br>\n<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n{{Audio}}',
#      'ord': 1,
#      'bqfmt': ''}]},
#   'content': ['Hello!', 'Nǐ hǎo!', '你好！', '[sound:tmp1cctcn.mp3]'],
#   'tags': ['']},
#   ...
# }
# >>> anki.cards
# {'1419644220831': {'cid': '1419644220831',
#   'nid': '1419644212689',
#   'note': {'nid': '1419644212689',
#    'mid': '1377171239634',
#    'model': {'mid': '1377171239634',
#     'name': 'SpoonFed',
#     'fields': ['English', 'Pinyin', 'Hanzi', 'Audio'],
#     'templates': [{'name': 'CE',
#       'qfmt': '<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n[sound:silence.mp3]\n{{Audio}}',
#       'did': None,
#       'bafmt': '',
#       'afmt': '<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n{{Pinyin}}<br>\n{{English}}<br>\n{{Audio}}',
#       'ord': 0,
#       'bqfmt': ''},
#      {'name': 'EC',
#       'qfmt': '{{English}}',
#       'did': None,
#       'bafmt': '',
#       'afmt': '{{English}}<br>\n{{Pinyin}}<br>\n<font style="font-family:SimSun;">{{Hanzi}}</font><br>\n{{Audio}}',
#       'ord': 1,
#       'bqfmt': ''}]},
#    'content': ['Hello!', 'Nǐ hǎo!', '你好！', '[sound:tmp1cctcn.mp3]'],
#    'tags': ['']},
#   'did': '1518099616462',
#   'deck': {'did': '1518099616462',
#    'name': 'Chinese::sentence::CE:: 1-10 Pleasant::Level  1'},
#   'ord': 0},
#   ...
# }
>>> anki.close()
"""
import doctest
doctest.testmod()

__doctest_skip__ = ['*']
