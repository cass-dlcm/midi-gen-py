import glob
from src.drum_gen import read_patterns, filterDrumPatterns, drum, get_drum_types
from src.drum_gen import get_patterns
from src.main import create_simple_meta_track
from mido import MidiTrack, MetaMessage, MidiFile
from filecmp import cmp
from os import mkdir
from typing import List, Union, Dict, cast


def test_drums():
    file_list: List[str] = glob.glob("data/drum_patterns/*.json")
    for i in range(0, len(file_list)):
        mid: MidiFile = MidiFile()
        create_simple_meta_track(mid)
        read_patterns()
        filterDrumPatterns([i])
        drumTrack: MidiTrack = MidiTrack()
        drumTrack.append(MetaMessage('instrument_name', name='Drum set'))
        drum(drumTrack)
        drumTrack.append(MetaMessage('end_of_track'))
        mid.tracks.append(drumTrack)
        try:
            mkdir("tests/output")
            print("Created tests/output directory.")
        except FileExistsError:
            pass
        try:
            mkdir("tests/output/drums")
            print("Created tests/output/drums directory.")
        except FileExistsError:
            pass
        file_name: str = get_patterns()[0]['name'] + '.mid'
        mid.save('tests/output/drums/' + file_name)
        assert abs(mid.length - 2) < .001
        assert cmp('tests/output/drums/' + file_name,
                   'tests/data/drums/' + file_name, shallow=False)


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
        assert pattern['noteEvent'] == 'on' or pattern['noteEvent'] == 'off'
        assert isinstance(pattern['drumType'], str)
        assert isinstance(get_drum_types()[pattern['drumType']], int)
        assert get_drum_types()[pattern['drumType']] != 0
        assert isinstance(pattern['time'], int)
        assert pattern['time'] >= 0


def test_drum_patterns_types():
    file_list: List[str] = glob.glob("data/drum_patterns/*.json")
    for i in range(0, len(file_list)):
        read_patterns()
        filterDrumPatterns([i])
        pattern: Dict[str, Union[str, List[Dict[str, Union[str, Dict[str, Union[str, list]], int]]]]] = get_patterns()[0]
        assert isinstance(pattern, dict)
        assert isinstance(pattern['name'], str)
        assert isinstance(pattern['pattern'], list)
        assert len(pattern['pattern']) > 0
        for event in pattern['pattern']:
            recursive_parse_patterns(event)
