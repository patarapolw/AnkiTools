from dotenv import load_dotenv
import os
import psutil

from AnkiTools.ankiconnect import AnkiConnect

if 'CI' in os.environ:
    env_path = '.env'
else:
    if os.path.exists(os.path.join('user', '.env')):
        env_path = os.path.join('user', '.env')
    else:
        env_path = '.env'

    if 'Anki' in (p.name() for p in psutil.process_iter()):
        os.environ['ANKI_APP_OPENED'] = '1'

load_dotenv(verbose=True, dotenv_path=env_path)

if AnkiConnect.is_online():
    os.environ['ANKI_APP_OPENED'] = '1'
    os.environ['ANKICONNECT_INSTALLED'] = '1'
