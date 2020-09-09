from random import randint, choice
from time import strftime, gmtime
from os import mkdir
from mido import MidiFile, MidiTrack, MetaMessage, bpm2tempo
from midi2audio import FluidSynth
from json import load
from typing import Tuple, List, Dict, Union, cast
if __name__ == "__main__":
    import drum_gen
    import guitar_gen
    from piano_gen import create_piano_track
    from lights import writeToFile
else:
    from src import guitar_gen, drum_gen
    from src.piano_gen import create_piano_track
    from src.lights import writeToFile

root: Tuple[str, str, str, str, str, str, str, str, str, str, str, str] = (
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

with open('data/chords.json') as json_file:
    chordDict: List[Dict[str, Union[str, List[int]]]] = load(json_file)

with open('config.json') as json_file:
    config: dict = load(json_file)


def simple_pick_chords(progression_length: int) -> List[Dict[str, Dict[str, Union[str, int, List[int]]]]]:
    """Creates a specific set of chords

    :param progression_length: The length of the chord progression to be generated
    :type progression_length: int
    :returns: A dictionary of chords, consisting of pitches and offsets, with names
    :rtype: List[Dict[str, Dict[str, Union[str, int, List[int]]]]]
    """
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
    """Randomly creates a set of chords

    :param progression_length: The length of the chord progression to be generated
    :type progression_length: int
    :returns: A dictionary of chords, consisting of pitches and offsets, with names
    :rtype: List[Dict[str, Dict[str, Union[str, int, List[int]]]]]
    """
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


def simple_chord_order(assembled_chords: List[Dict[str, Dict[str, Union[str, int, List[int]]]]]) -> Dict[str, Union[List[str], List[List[List[int]]]]]:
    """Creates an order for the chords to be played in

    :param assembled_chords: The dictionary of chords, consisting of pitches and offsets, with names
    :type assembled_chords: List[Dict[str, Dict[str, Union[str, int, List[int]]]]]
    :returns: A dictonary containing a three-dimensional list of notes, and a list of chord names.
    :rtype: Dict[str, Union[List[str], List[List[List[int]]]]]
    """
    sequencesVals: List[List[List[int]]] = []
    sequencesStr: List[str] = []
    sequences: Dict[str, Union[List[List[List[int]]], List[str]]] = {
        'values': sequencesVals,
        'strings': sequencesStr
    }
    temp: List[List[int]] = []
    for a in assembled_chords:
        temp.append(cast(List[int], a['chord']['values']).copy())
    for b in range(0, len(temp)):
        for c in range(0, len(temp[b])):
            temp[b][c] += cast(int, assembled_chords[b]['root']['value'])
    sequencesVals.append(temp)
    return sequences


def randomize_chord_order(assembledChords: List[Dict[str, Dict[str, Union[str, int, List[int]]]]]) -> Dict[str, Union[List[str], List[List[List[int]]]]]:
    """Creates a random order for the chords to be played in

    :param assembled_chords: The dictionary of chords, consisting of pitches and offsets, with names
    :type assembled_chords: List[Dict[str, Dict[str, Union[str, int, List[int]]]]]
    :returns: A dictonary containing a three-dimensional list of notes, and a list of chord names.
    :rtype: Dict[str, Union[List[str], List[List[List[int]]]]]
    """
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
            temp.append(cast(List[int], assembledChords[j]['chord']['values']).copy())
            tempStrs.append(cast(str, assembledChords[j]['root']['name']) + cast(str, assembledChords[j]['chord']['name']))
            for b in range(0, len(temp[j])):
                temp[j][b] += cast(int, assembledChords[j]['root']['value'])
        segment: List[List[int]] = []
        for j in range(0, len(assembledChords)):
            k: int = randint(0, len(assembledChords) - j - 1)
            segment.append(temp.pop(k))
            sequencesStr.append(tempStrs.pop(k))
        sequencesVals.append(segment)
    return sequences


def create_simple_meta_track() -> Tuple[MidiTrack, int]:
    """Creates a Midi meta track containg a fixed tempo of 120 bpm

    :return: The track
    :rtype: MidiTrack
    """
    bpm: int = 120
    meta_track: MidiTrack = MidiTrack()
    meta_track.append(MetaMessage(
        'set_tempo',
        tempo=bpm2tempo(bpm)))
    return meta_track, bpm


def create_meta_track() -> Tuple[MidiTrack, int]:
    """Creates a Midi meta track containing a randomized tempo ranging from 90 to 120 bpm

    :return: The track
    :rtype: mido.MidiTrack
    """
    bpm = randint(90, 180)
    meta_track: MidiTrack = MidiTrack()
    meta_track.append(MetaMessage(
        'set_tempo',
        tempo=bpm2tempo(bpm)))
    return meta_track, bpm


def write_file(mid: MidiFile) -> str:
    """ Writes the MIDI information to a file and gives a timestamp

    :param mid: The MIDI file to write
    :type mid: mido.MidiFile
    :return: The timestamp formatted '%Y-%m-%d_%H_%M_%S'
    :rtype: str
    """
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
    segments: int = 8
    sequences: Dict[str, Union[List[str], List[List[List[int]]]]] = randomize_chord_order(pick_chords(progression_length))
    mid: MidiFile = MidiFile()
    mid.ticksPerBeat = 480
    meta: Tuple(MidiTrack, int) = create_meta_track()
    mid.tracks.append(meta[0])
    bpm = meta[1]
    create_piano_track(mid, progression_length, sequences)
    guitar_gen.setup_patterns()
    mid.tracks.append(guitar_gen.create_track(progression_length, sequences['values'], segments))
    drum_gen.setup_patterns()
    mid.tracks.append(drum_gen.create_track(progression_length * segments))
    timestamp: str = write_file(mid)
    if config['lights_enabled']:
        writeToFile(timestamp, bpm, progression_length, segments)
    if config['sound_enabled'] and __name__ == "__main__":
        FluidSynth().play_midi("output/" + timestamp + '.mid')


if __name__ == '__main__':
    main()
