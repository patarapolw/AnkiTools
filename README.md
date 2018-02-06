# AnkiTools

An Anki *.apkg reader/editor to work with in Python.

## Parsing in a human readable and easily manageable format.

```python
from tools import read, edit
import os

with read.readApkg(os.path.join('sample','Chinese_Sentences_and_audio_spoon_fed.apkg')) as anki:
    print(anki.findNotes('Pinyin','Nǐ hǎo!'))
    print()
    print(anki.findCards('Pinyin','Nǐ hǎo!'))
```

Result:-
```
[{'content': OrderedDict([('English', 'Hello!'),
               ('Pinyin', 'Nǐ hǎo!'),
               ('Hanzi', '你好！'),
               ('Audio', '[sound:tmp1cctcn.mp3]')]),
  'model name': 'MarkAudio-787e4'}]

[{'content': OrderedDict([('English', 'Hello!'),
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
```

## Editing a *.apkg file without Anki

Currently, it is safer to edit in a machine-readable format, rather than human-readable, but I try to create a human-oriented one.

```python
from collections import OrderedDict

with edit.editApkg(os.path.join('sample','Chinese_Sentences_and_audio_spoon_fed.apkg')) as anki:
    humanNotes = [{'content': OrderedDict([('English', 'Hello!xxxxx'),
                               ('Pinyin', 'Nǐ hǎo!xxxxx'),
                               ('Hanzi', '你好！xxxxx'),
                               ('Audio', '[sound:xxxxx.mp3]')]),
                   'model name': 'MarkAudioaaaaaaa'}]
    anki.updateHumanNotes(humanNotes)
    
    humanCards = [{'content': OrderedDict([('English', 'Hello!'),
                               ('Pinyin', 'Nǐ hǎo!'),
                               ('Hanzi', '你好！'),
                               ('Audio', '[sound:tmp1cctcn.mp3]')]),
                  'deck name': 'Chinese::SpoonFedChinese',
                  'model name': 'MarkAudio',
                  'template': 'Card M'},
                 {'content': OrderedDict([('English', 'Hello!'),
                               ('Pinyin', 'Nǐ hǎo!'),
                               ('Hanzi', '你好！'),
                               ('Audio', '[sound:tmp1cctcn.mp3]')]),
                  'deck name': 'Chinese::SpoonFedChinese',
                  'model name': 'MarkAudio-X',
                  'template': 'Card N'}]
    anki.updateHumanCards(humanCards)
```
