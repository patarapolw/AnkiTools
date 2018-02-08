from time import time
from hashlib import sha1

from AnkiTools.tools import guid64


def intTime(scale=1000):
    return str(int(time()*scale))


def newModel(model):

    result = {
        model['mid']:{
            "vers":[],
            "name": model['name'],
            "tags":[],
            "did": None, ### deck id
            "usn":-1,
            "req":[[0, "all",[0]]],
            "flds": newFields(model['fields']),
            "sortf":0,
            "latexPre":"\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\
                \n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\
                \\parindent}{0in}\n\\begin{document}\n",
            "tmpls":newTemplates(model['templates']),
            "latexPost":"\\end{document}",
            "type":0,
            "id":model['mid'],
            "css":".card {\n font-family: arial;\n font-size: 30px;\n text-align: center;\
                \n color: black;\n white;\n}\n\n.card1 { #FFFFFF; }",
            "mod": intTime(1000)
        }
    }

    return result


def newFields(fields):
    flds = []
    for field in fields:
        flds.append(newField(field))
    return flds


def newField(field):
    return {
            "name": field,
            "rtl": False,
            "sticky": False,
            "media": [],
            "ord": 0,
            "font": "Arial",
            "size": 12
        }


def newTemplates(templates):
    tmpls = []
    for template in templates:
        tmpls.append(newTemplate(template))
    return tmpls


def newTemplate(template):
    return {
            "name": template,
            "qfmt": "{{Front}}",
            "did": None,
            "bafmt": "",
            "afmt": "{{FrontSide}}\n\n<hr id=answer/>\n\n{{Back}}",
            "ord": 0,
            "bqfmt": ""
        }


def newDeck(deck):
    result = {
        deck['did'] : {
            "desc": "",
            "name": deck['name'],
            "extendRev": 50,
            "usn": -1,
            "collapsed": False,
            "newToday": [
                754,
                0
            ],
            "timeToday": [
                754,
                0
            ],
            "dyn": 0,
            "extendNew": 10,
            "conf": 1,
            "revToday": [
                754,
                0
            ],
            "lrnToday": [
                754,
                0
            ],
            "id": deck['id'],
            "mod": intTime()
        }
    }
    return result


def newNote(note):
    nid = note['nid']
    guid = guid64.guid64() # Generate GUID
    mid = note['mid']
    mod = intTime()
    usn = -1
    tags = '' # type?
    flds = note['content'].join('\x1f')
    sfld = note['content'][0]
    csum = sha1(sfld.encode('utf8')).hexdigest()
    flags = 0
    data = '' # type?

    return nid, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data


def newCard(card):
    cid = card['cid']
    nid = card['nid']
    did = card['did']
    order = card['ord']
    mod = intTime() # Same as note's mod field
    usn = -1
    ctype = 0
    queue = 0
    due = 484332854 # what?
    ivl = 0
    factor = 0
    reps = 0
    lapses = 0
    left = 0
    odue = 0
    odid = 0
    flags = 0
    data = '' # type?

    return cid, nid, did, order, mod, usn, ctype, queue, due, ivl, \
           factor, reps, lapses, left, odue, odid, flags, data
