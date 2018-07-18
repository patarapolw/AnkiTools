import simplejson as json

from conftest import module_path

from AnkiTools.tools.sampling import get_representative_json


def generate_defaults_json(source=module_path().joinpath('tests/input/dirty_collection.anki2'),
                           output=module_path().joinpath('AnkiTools/defaults.json')):
    with open(output, 'w') as f:
        json.dump(get_representative_json(file_input=source, formatted=False,), f,
                  indent=2, ensure_ascii=False)


if __name__ == '__main__':
    generate_defaults_json()
