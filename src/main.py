import random
import time
import os
from mido import MidiFile, MidiTrack
import mido
from midi2audio import FluidSynth
import json
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

with open('chords.json') as json_file:
    chordDict = json.load(json_file)

with open('config.json') as json_file:
    config = json.load(json_file)

assembledChords = []
outStr = ''
progressionLength = 4
sequencesStr = ''
arduinoStr = '#include <Adafruit_NeoPixel.h>\n#define LED_PIN    '
arduinoStr += str(config['LED_PIN'])
arduinoStr += '\n#define LED_COUNT '
arduinoStr += str(config['LED_COUNT'])
arduinoStr += '\nAdafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);\nint a = 0;\nint b = 0;\nconst int hues[] = {'

for i in range(0, progressionLength):
    b = {
        'root': {},
        'chord': {}
    }
    a = {
        'name': random.choice(root),
    }
    a['value'] = root.index(a['name'])
    b['root'] = a
    b['chord'] = random.choice(chordDict)
    outStr += b['root']['name'] + b['chord']['name'] + ' '
    assembledChords.append(b)

sequences = []
for i in range(0, 8):
    temp = []
    tempStrs = []
    for j in range(0, progressionLength):
        temp.append(assembledChords[j]['chord']['values'])
        tempStrs.append(assembledChords[j]['root']['name'] + assembledChords[j]['chord']['name'])
    segment = []
    for j in range(0, progressionLength):
        k = random.randint(j, progressionLength - 1) - j
        segment.append(temp.pop(k))
        sequencesStr = sequencesStr + tempStrs.pop(k) + ' '
    sequences.append(segment)

bpm = random.randint(90, 180)

d = 800000 / 24 / config['LED_COUNT'] / (bpm / 60) * .9

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
            arduinoStr = arduinoStr + str(sequences[a][b][0] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][3] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][1] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][2] - 48)
            if (not(a == 7 and b == progressionLength - 1)):
                arduinoStr += ", "
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
            arduinoStr = arduinoStr + str(sequences[a][b][0] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][2] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][1] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][3] - 48)
            if (not(a == 7 and b == progressionLength - 1)):
                arduinoStr += ", "
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
            arduinoStr = arduinoStr + str(sequences[a][b][0] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][3] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][1] - 48) + ", "
            arduinoStr = arduinoStr + str(sequences[a][b][2] - 48)
            if (not(a == 7 and b == progressionLength - 1)):
                arduinoStr += ", "
guitarTrack.append(mido.MetaMessage('end_of_track'))

arduinoStr += '};\nvoid setup() {\n  strip.begin();\n  strip.show();\n}\nint getColor() {\n  return (int)(65536.0 * ((hues[a] * ('
arduinoStr += str(int(d))
arduinoStr += ' - b)) * '
arduinoStr += str(float.hex(1 / int(d)))
arduinoStr += ' + (hues[a + 1] * b) * '
arduinoStr += str(float.hex(1 / int(d)))
arduinoStr += ') * 0.0833333333333333);\n}\nvoid loop() {\n  if (a < '
arduinoStr += str(progressionLength * 8 * 4)
arduinoStr += ') {\n    strip.fill(strip.ColorHSV(getColor()));\n  }\n  b++;\n  strip.show();\n  if (b == '
arduinoStr += str(int(d))
arduinoStr += ') {\n    a++;\n    b = 0;\n  }\n}'

drumTrack = MidiTrack()
mid.tracks.append(drumTrack)

for a in range(0, 8 * progressionLength):
    drum(drumTrack)

drumTrack.append(mido.MetaMessage('end_of_track'))

timestamp = time.strftime('%Y-%m-%d_%H_%M_%S', time.gmtime())
try:
    os.mkdir("output")
    print("Created output directory.")
except FileExistsError:
    print()
try:
    os.mkdir('output\\' + timestamp)
except FileExistsError:
    print()
mid.save("output\\" + timestamp + '.mid')
ardFile = open('output\\' + timestamp + '\\' + timestamp + '.ino', 'w')
ardFile.write(arduinoStr)
ardFile.close()
print(os.system('"C:\\Program Files (x86)\\Arduino\\arduino.exe" --upload --board SparkFun:avr:RedBoard --port COM3 -v output\\' + timestamp + "\\" + timestamp + '.ino'))
time.sleep(11)
FluidSynth().play_midi("output\\" + timestamp + '.mid')

quit()
