import random
from mido import MidiFile, MidiTrack
import mido
from drum_gen import drum

root = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
cVal = 48
chords =    ('M',            'm',            '5',            '7',  # noqa E222
             'M7',           'm7',           'mM7',          '6',
             'm6',           'add9',         'madd9',        '7b5',
             '7#5',          'm7b5',         'm7#5')
chordVals = ((0, 4, 7, 12),  (0, 3, 7, 12),  (0, 7, 12, 19), (0, 4, 7, 10),
             (0, 4, 7, 11),  (0, 3, 7, 10),  (0, 3, 7, 11),  (0, 4, 7, 9),
             (0, 3, 7, 9),   (0, 2, 4, 7),   (0, 2, 3, 7),   (0, 4, 6, 10),
             (0, 4, 8, 10),  (0, 3, 6, 10),  (0, 3, 8, 10))
chosenRootsStr = []
rootVals = []
chosenChordsStr = []
chosenChordVals = []
outStr = ''
progressionLength = random.choice((4, 8))
sequencesStr = ''

for i in range(0, progressionLength):
    chosenRootsStr.append(random.choice(root))
    rootVals.append(root.index(chosenRootsStr[i]))

for i in range(0, progressionLength):
    chosenChordsStr.append(random.choice(chords))
    chosenChordValsSub = []
    for j in range(0, 4):
        chosenChordValsSub.append(rootVals[i] + cVal + chordVals[chords.index(
            chosenChordsStr[i])][j])
    chosenChordVals.append(chosenChordValsSub)
    outStr = outStr + chosenRootsStr[i] + chosenChordsStr[i] + " "

sequences = []
for i in range(0, 8):
    temp = []
    tempStrs = []
    for j in range(0, progressionLength):
        temp.append(chosenChordVals[j])
        tempStrs.append(chosenRootsStr[j] + chosenChordsStr[j])
    segment = []
    for j in range(0, progressionLength):
        k = random.randint(j, progressionLength - 1) - j
        segment.append(temp.pop(k))
        sequencesStr = sequencesStr + tempStrs.pop(k) + " "
    sequences.append(segment)

bpm = random.randint(90, 180)

print(outStr)
print(bpm)
print(sequencesStr)

mid = MidiFile()
mid.ticksPerBeat = 480

metaTrack = MidiTrack()
metaTrack.append(mido.MetaMessage(
    'set_tempo',
    tempo=mido.bpm2tempo(bpm)))
mid.tracks.append(metaTrack)

chordTrack = MidiTrack()
mid.tracks.append(chordTrack)
chordTrack.append(mido.Message(
    'program_change',
    program=0,
    time=0))
for a in range(0, 8):
    for b in range(0, progressionLength):
        for c in range(0, 4):
            chordTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][c],
                channel=0))
        chordTrack.append(mido.Message(
            'note_on',
            velocity=0,
            note=0,
            channel=0,
            time=1920))
        for c in range(0, 4):
            chordTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][c],
                channel=0))
chordTrack.append(mido.MetaMessage('end_of_track'))
guitarTrack = MidiTrack()
mid.tracks.append(guitarTrack)
guitarTrack.append(mido.Message(
    'program_change',
    program=25,
    channel=1,
    time=0))

for a in range(0, 8):
    pickPattern = random.randint(0, 2)
    if (pickPattern == 0):
        for b in range(0, progressionLength):
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][0],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][3],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_off',
                channel=1,
                time=240,
                note=sequences[a][b][0]))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][1],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                channel=1, time=240,
                note=sequences[a][b][3]))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][2],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                channel=1,
                time=240,
                note=sequences[a][b][1]))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][0],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                channel=1,
                time=240,
                note=sequences[a][b][2]))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][3],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                channel=1,
                time=240,
                note=sequences[a][b][0]))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][1],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                channel=1,
                time=240,
                note=sequences[a][b][3]))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][2],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                channel=1,
                time=240,
                note=sequences[a][b][1]))
            guitarTrack.append(mido.Message(
                'note_off',
                channel=1,
                note=sequences[a][b][2]))
    if (pickPattern == 1):
        for b in range(0, progressionLength):
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][0],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][2],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][0],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][1],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][2],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][3],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][1],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][0],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][3],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][2],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][0],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][1],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][2],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][3],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][1],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][3],
                channel=1))
    if (pickPattern == 2):
        for b in range(0, progressionLength):
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][0],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][3],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][0],
                channel=1,
                time=480))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][1],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][3],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][2],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][1],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][0],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][2],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][3],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][0],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][1],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][3],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_on',
                note=sequences[a][b][2],
                channel=1))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][1],
                channel=1,
                time=240))
            guitarTrack.append(mido.Message(
                'note_off',
                note=sequences[a][b][2],
                channel=1))
guitarTrack.append(mido.MetaMessage('end_of_track'))

drumTrack = MidiTrack()
mid.tracks.append(drumTrack)

for a in range(0, 8 * progressionLength):
    drum(drumTrack)

drumTrack.append(mido.MetaMessage('end_of_track'))

mid.save('out.mid')
quit()
