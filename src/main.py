from random import randint, choice
from time import strftime, gmtime
from os import mkdir
from mido import MidiFile, MidiTrack, MetaMessage, bpm2tempo
from midi2audio import FluidSynth
from json import load
if __name__ == "__main__":
    from drum_gen import create_drum_track
    from guitar_gen import create_guitar_track
    from piano_gen import create_piano_track
    from lights import writeToFile
else:
    from src.drum_gen import create_drum_track
    from src.guitar_gen import create_guitar_track
    from src.piano_gen import create_piano_track
    from src.lights import writeToFile

root = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
c_val = 48
timestamp = ""
assembledChords = []
progression_length = 4
sequencesStr = []
bpm = 0
sequences = []

with open('data/chords.json') as json_file:
    chordDict = load(json_file)

with open('config.json') as json_file:
    config = load(json_file)


def get_sequence():
    return sequences.copy()


def simple_pick_chords():
    global assembledChords
    assembledChords = []
    for a in range(0, progression_length):
        b = {
            'root': {
                'name': root[a],
            },
            'chord': chordDict[a]
        }
        b['root']['value'] = root.index(b['root']['name'])
        assembledChords.append(b)


def pick_chords():
    global assembledChords
    assembledChords = []
    for _ in range(0, progression_length):
        global outStr
        b = {
            'root': {},
            'chord': {}
        }
        a = {
            'name': choice(root),
        }
        a['value'] = root.index(a['name'])
        b['root'] = a
        b['chord'] = choice(chordDict)
        assembledChords.append(b)


def simple_chord_order():
    print(assembledChords)
    global sequences
    sequences = []
    temp = []
    for a in range(0, progression_length):
        temp.append(assembledChords[a]['chord']['values'].copy())
    for b in range(0, len(temp)):
        for c in range(0, len(temp[b])):
            temp[b][c] += assembledChords[b]['root']['value']
    sequences.append(temp)


def randomize_chord_order():
    global sequences
    sequences = []
    for _ in range(0, 8):
        temp = []
        tempStrs = []
        for j in range(0, progression_length):
            temp.append(assembledChords[j]['chord']['values'].copy())
            for a in temp:
                for b in range(0, len(a)):
                    a[b] += assembledChords[j]['root']['value']
            tempStrs.append(assembledChords[j]['root']['name'] + assembledChords[j]['chord']['name'])
        segment = []
        for j in range(0, progression_length):
            k = randint(0, progression_length - j - 1)
            segment.append(temp.pop(k))
            sequencesStr.append(tempStrs.pop(k))
        sequences.append(segment)


mid = MidiFile()
mid.ticksPerBeat = 480


def create_simple_meta_track(midi_file):
    metaTrack = MidiTrack()
    metaTrack.append(MetaMessage(
        'set_tempo',
        tempo=bpm2tempo(120)))
    midi_file.tracks.append(metaTrack)


def create_meta_track():
    global bpm
    bpm = randint(90, 180)
    metaTrack = MidiTrack()
    metaTrack.append(MetaMessage(
        'set_tempo',
        tempo=bpm2tempo(bpm)))
    mid.tracks.append(metaTrack)


def write_file():
    global timestamp
    timestamp = strftime('%Y-%m-%d_%H_%M_%S', gmtime())
    try:
        mkdir("output")
        print("Created output directory.")
    except FileExistsError:
        pass
    mid.save("output/" + timestamp + '.mid')


def main():
    pick_chords()
    randomize_chord_order()
    create_meta_track()
    # print(bpm)
    # print(sequencesStr)
    create_piano_track(mid, progression_length, sequences, sequencesStr)
    create_guitar_track(mid, progression_length, sequences, 8)
    create_drum_track(mid, progression_length)
    write_file()
    if config['lights_enabled']:
        writeToFile(timestamp, bpm, progression_length)
    if config['sound_enabled'] and __name__ == "__main__":
        FluidSynth().play_midi("output/" + timestamp + '.mid')


if __name__ == '__main__':
    main()
