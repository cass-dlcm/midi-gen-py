import json

chords =    ('M',            'm',            '5',            '7',  # noqa E222
             'M7',           'm7',           'mM7',          '6',
             'm6',           'add9',         'madd9',        '7b5',
             '7#5',          'm7b5',         'm7#5')
chordVals = ((0, 4, 7, 12),  (0, 3, 7, 12),  (0, 7, 12, 19), (0, 4, 7, 10),
             (0, 4, 7, 11),  (0, 3, 7, 10),  (0, 3, 7, 11),  (0, 4, 7, 9),
             (0, 3, 7, 9),   (0, 2, 4, 7),   (0, 2, 3, 7),   (0, 4, 6, 10),
             (0, 4, 8, 10),  (0, 3, 6, 10),  (0, 3, 8, 10))


def createChordFile():
    chordFile = open('chords.json', 'w')
    a = []
    for i in range(0, len(chords)):
        b = {
            'name': chords[i],
            'values': []
        }
        for note in chordVals[i]:
            b['values'].append(note)
        a.append(b)
    chordFile.write(json.dumps(a, indent=2))


createChordFile()
