from random import randint, choice
from time import strftime, gmtime
from os import mkdir
from mido import MidiFile, MidiTrack, MetaMessage, bpm2tempo
from midi2audio import FluidSynth
from json import load
from typing import Tuple, List, Dict, Any, Union, cast
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

root: Tuple[str, str, str, str, str, str, str, str, str, str, str, str] = (
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
bpm: int = 0

with open('data/chords.json') as json_file:
    chordDict: List[Dict[str, Union[str, List[int]]]] = load(json_file)

with open('config.json') as json_file:
    config: dict = load(json_file)


def simple_pick_chords(progression_length: int) -> List[Dict[str, Dict[str, Union[str, int, List[int]]]]]:
    assembledChords: List[Dict[str, Dict[str, Union[str, int, List[int]]]]] = []
    for a in range(0, progression_length):
        b: Dict[str, Dict[str, Union[str, int, List[int]]]] = {
            'root': {
                'name': root[a],
                'value': a
            },
            'chord': cast(Dict[str, Union[str, int, List[int]]], chordDict[a].copy())
        }
        assembledChords.append(b)
    return assembledChords


def pick_chords(progression_length: int) -> List[Dict[str, Dict[str, Union[str, int, List[int]]]]]:
    assembledChords: List[Dict[str, Dict[str, Union[str, int, List[int]]]]] = []
    for _ in range(0, progression_length):
        a: Dict[str, Union[str, int]] = {
            'name': choice(root),
            'value': 0
        }
        a['value'] = root.index(a['name'])
        b: Dict[str, Dict[str, Union[str, int, List[int]]]] = {
            'root': cast(Dict[str, Union[str, int, List[int]]], a),
            'chord': cast(Dict[str, Union[str, int, List[int]]], choice(chordDict)).copy()
        }
        assembledChords.append(b)
    return assembledChords


def simple_chord_order(assembledChords: List[Dict[str, Dict[str, Any]]]) -> Dict[str, Union[List[str], List[List[List[int]]]]]:
    sequencesVals: List[List[List[int]]] = []
    sequencesStr: List[str] = []
    sequences: Dict[str, Union[List[List[List[int]]], List[str]]] = {
        'values': sequencesVals,
        'strings': sequencesStr
    }
    temp: List[List[int]] = []
    for a in assembledChords:
        temp.append(a['chord']['values'].copy())
    for b in range(0, len(temp)):
        for c in range(0, len(temp[b])):
            temp[b][c] += assembledChords[b]['root']['value']
    sequencesVals.append(temp)
    return sequences


def randomize_chord_order(assembledChords: List[Dict[str, Dict[str, Any]]]) -> Dict[str, Union[List[str], List[List[List[int]]]]]:
    sequencesVals: List[List[List[int]]] = []
    sequencesStr: List[str] = []
    sequences: Dict[str, Union[List[str], List[List[List[int]]]]] = {
        'values': sequencesVals,
        'strings': sequencesStr
    }
    for _ in range(0, 8):
        temp: List[List[int]] = []
        tempStrs: List[str] = []
        for j in range(0, len(assembledChords)):
            temp.append(assembledChords[j]['chord']['values'].copy())
            tempStrs.append(assembledChords[j]['root']['name'] + assembledChords[j]['chord']['name'])
            for b in range(0, len(temp[j])):
                temp[j][b] += assembledChords[j]['root']['value']
        segment: List[List[int]] = []
        for j in range(0, len(assembledChords)):
            k: int = randint(0, len(assembledChords) - j - 1)
            segment.append(temp.pop(k))
            sequencesStr.append(tempStrs.pop(k))
        sequencesVals.append(segment)
    return sequences


def create_simple_meta_track(midi_file: MidiFile):
    metaTrack: MidiTrack = MidiTrack()
    metaTrack.append(MetaMessage(
        'set_tempo',
        tempo=bpm2tempo(120)))
    midi_file.tracks.append(metaTrack)


def create_meta_track(mid: MidiFile):
    global bpm
    bpm = randint(90, 180)
    metaTrack: MidiTrack = MidiTrack()
    metaTrack.append(MetaMessage(
        'set_tempo',
        tempo=bpm2tempo(bpm)))
    mid.tracks.append(metaTrack)


def write_file(mid: MidiFile) -> str:
    timestamp: str = strftime('%Y-%m-%d_%H_%M_%S', gmtime())
    try:
        mkdir("output")
        print("Created output directory.")
    except FileExistsError:
        pass
    mid.save("output/" + timestamp + '.mid')
    return timestamp


def main():
    progression_length: int = 4
    sequences: Dict[str, Union[List[str], List[List[List[int]]]]] = randomize_chord_order(pick_chords(progression_length))
    mid: MidiFile = MidiFile()
    mid.ticksPerBeat = 480
    create_meta_track(mid)
    create_piano_track(mid, progression_length, sequences)
    create_guitar_track(mid, progression_length, sequences['values'], 8)
    create_drum_track(mid, progression_length)
    timestamp: str = write_file(mid)
    if config['lights_enabled']:
        writeToFile(timestamp, bpm, progression_length)
    if config['sound_enabled'] and __name__ == "__main__":
        FluidSynth().play_midi("output/" + timestamp + '.mid')


if __name__ == '__main__':
    main()
