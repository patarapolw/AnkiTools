import os
from tools import edit
from collections import OrderedDict

anki = edit.editApkg(os.path.join('sample','Chinese_Sentences_and_audio_spoon_fed.apkg'))
humanNotes = [{'content': OrderedDict([('English', 'Hello!'),
                          ('Pinyin', 'Nǐ hǎo!'),
                          ('Hanzi', '你好！'),
                          ('Audio', '[sound:tmp1cctcn.mp3]')]),
               'model name': 'MarkAudio-787e4'}]
anki.updateHumanNotes(humanNotes)

humanCards = [{'content': OrderedDict([('English', 'Hello!'),
                          ('Pinyin', 'Nǐ hǎo!'),
                          ('Hanzi', '你好！'),
                          ('Audio', '[sound:tmp1cctcn.mp3]')]),
               'deck name': 'SpoonFedChinese',
               'model name': 'MarkAudio-787e4',
               'template': 'Card 1'},
              {'content': OrderedDict([('English', 'Hello!'),
                                       ('Pinyin', 'Nǐ hǎo!'),
                                       ('Hanzi', '你好！'),
                                       ('Audio', '[sound:tmp1cctcn.mp3]')]),
               'deck name': 'SpoonFedChinese',
               'model name': 'MarkAudio-787e4',
               'template': 'Card 2'}]
anki.updateHumanCards(humanCards)