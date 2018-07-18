import simplejson as json

from AnkiTools.tools.sampling import get_representative_json
from AnkiTools.utils import collapse_json


def make_representative_json(in_file: str, out_file=None, **kwargs):
    if out_file is None:
        out_file = in_file + '.sample.json'

    with open(out_file, 'w') as f:
        json_string = json.dumps(get_representative_json(in_file, formatted=True, **kwargs),
                                 indent=2, ensure_ascii=False)
        f.write(collapse_json(json_string))


if __name__ == '__main__':
    make_representative_json('../tests/files/test.apkg', 'output/test.json')
