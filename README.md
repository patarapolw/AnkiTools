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

with edit.editApkg(os.path.join(apkg,'Chinese_Sentences_and_audio_spoon_fed.apkg')) as anki:
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

Although, you can always use below, which is much safer (for now).

```python
import os
from tools import edit
from collections import OrderedDict

with edit.editApkg(os.path.join('sample','Chinese_Sentences_and_audio_spoon_fed.apkg')) as anki:
    anki.updateModels({
                        'mid': model_id,
                        'name': model_name,
                        'fields': list_of_field_names,
                        'templates': list_of_template_names

                    })

    anki.updateDecks({
                        'did': deck_id,
                        'name': deck_name
                    })

    anki.updateNotes({
                        'nid': note_id,
                        'mid': model_id,
                        'content': list_of_field_contents.join('\x1f')
                    })

    anki.updateCards({
                        'cid': card_id,
                        'nid': note_id,
                        'did': deck_id,
                        'ord': order_in_list_of_template_names
                    })
```

See also the \*.apkg format documentation from [Anki decks collaboration Wiki](http://decks.wikia.com/wiki/Anki_APKG_format_documentation) and [AnkiDroid](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure)

Model id, deck id, card id, and note id are Unix time in milliseconds.

Subdecks can be made by putting in `::`; for example, `Chinese::SpoonFedChinese`.
