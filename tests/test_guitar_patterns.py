import glob
from src.guitar_gen import read_patterns, filter_patterns, guitar, get_patterns
from mido import MidiTrack, MetaMessage, MidiFile, Message
from filecmp import cmp
from src.main import simple_pick_chords, simple_chord_order, create_simple_meta_track
from os import mkdir
from typing import List, Dict, Union, cast


def test_guitar():
    file_list: List[str] = glob.glob("data/guitar_patterns/*.json")
    for i in range(0, len(file_list)):
        progression_length: int = 4
        mid: MidiFile = MidiFile()
        create_simple_meta_track(mid)
        read_patterns()
        filter_patterns([i])
        guitar_track: MidiTrack = MidiTrack()
        guitar_track.append(MetaMessage('instrument_name', name='Guitar'))
        sequences: Dict[str, Union[List[List[List[int]]], List[str]]] = simple_chord_order(simple_pick_chords(progression_length))
        guitar_track.append(Message('program_change', program=25, channel=1, time=0))
        assert isinstance(get_patterns()[0], dict)
        assert isinstance(get_patterns()[0]['name'], str)
        assert isinstance(get_patterns()[0]['pattern'], list)
        assert isinstance(sequences, dict)
        assert isinstance(sequences['values'], list)
        for a in sequences['values']:
            assert isinstance(a, list)
            for b in a:
                assert isinstance(b, list)
                for c in b:
                    assert isinstance(c, int)
        assert isinstance(sequences['strings'], list)
        for a in sequences['strings']:
            assert isinstance(a, str)
        guitar(guitar_track, progression_length, sequences['values'], 1)
        guitar_track.append(MetaMessage('end_of_track'))
        mid.tracks.append(guitar_track)
        try:
            mkdir("tests/output")
            print("Created tests/output directory.")
        except FileExistsError:
            pass
        try:
            mkdir("tests/output/guitar")
            print("Created tests/output/guitar directory.")
        except FileExistsError:
            pass
        file_name: str = get_patterns()[0]['name'] + '.mid'
        mid.save('tests/output/guitar/' + file_name)
        assert abs(mid.length - 8) < .001
        assert cmp('tests/output/guitar/' + file_name, 'tests/data/guitar/' + file_name, shallow=False)


def recursive_parse_patterns(pattern: Dict[str, Union[str, Dict[str, Union[str, list]], int]]):
    if "repeat_count" in pattern:
        assert isinstance(pattern['repeat_count'], int)
        assert pattern['repeat_count'] > 1
        assert isinstance(pattern['subpattern'], list)
        assert len(pattern['subpattern']) > 1
        for a in range(0, cast(int, pattern["repeat_count"])):
            for b in cast(List[Dict[str, Union[str, Dict[str, Union[str, list]], int]]], pattern["subpattern"]):
                recursive_parse_patterns(cast(Dict[str, Union[str, Dict[str, Union[str, list]], int]], b))
    else:
        assert isinstance(pattern['noteEvent'], str)
        assert pattern['noteEvent'] == 'note_on' or pattern['noteEvent'] == 'note_off'
        assert isinstance(pattern['pitchIndex'], int)
        assert pattern['pitchIndex'] >= 0 and pattern['pitchIndex'] <= 3
        assert isinstance(pattern['time'], int)
        assert pattern['time'] >= 0


def test_guitar_patterns_types():
    file_list: List[str] = glob.glob("data/guitar_patterns/*.json")
    for i in range(0, len(file_list)):
        read_patterns()
        filter_patterns([i])
        pattern: Dict[str, Union[str, List[Dict[str, Union[str, Dict[str, Union[str, list]], int]]]]] = get_patterns()[0]
        assert isinstance(pattern, dict)
        assert isinstance(pattern['name'], str)
        assert isinstance(pattern['pattern'], list)
        assert len(pattern['pattern']) > 0
        for event in pattern['pattern']:
            recursive_parse_patterns(event)
