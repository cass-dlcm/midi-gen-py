import json
from drum_gen import getPatterns


def createPatternFile():
    patternFile = open('drum_patterns.json', 'w')
    a = []
    drumPatterns = getPatterns()
    for pattern in drumPatterns:
        b = {}
        c = []
        for note in pattern:
            print(note)
            d = {
                'noteEvent': note[0],
                'drumType': note[1],
                'time': note[2]
            }
            c.append(d)
        b['name'] = ''
        b['pattern'] = c
        a.append(b)
    patternFile.write(json.dumps(a, indent=2))


createPatternFile()
