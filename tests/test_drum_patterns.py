import glob
from src.drum_gen import read_patterns, filter_patterns, get_drum_types, create_track, get_patterns
from src.main import create_simple_meta_track
from mido import MidiFile
from filecmp import cmp
from os import mkdir
from typing import List, Union, Dict, cast


def test_drums():
    file_list: List[str] = glob.glob("data/drum_patterns/*.json")
    for i in range(0, len(file_list)):
        mid: MidiFile = MidiFile()
        mid.tracks.append(create_simple_meta_track()[0])
        read_patterns()
        filter_patterns([i])
        pattern = get_patterns()[0]
        drum_patterns_types(pattern)
        mid.tracks.append(create_track(1))
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
        file_name: str = pattern['name'] + '.mid'
        mid.save('tests/output/drums/' + file_name)
        assert abs(mid.length - 2) < .001
        assert cmp('tests/output/drums/' + file_name, 'tests/data/drums/' + file_name, shallow=False)


def recursive_parse_patterns(pattern: Dict[str, Union[str, Dict[str, Union[str, list]], int]]):
    if "repeat_count" in pattern:
        assert isinstance(pattern['repeat_count'], int)
        assert pattern['repeat_count'] > 1
        assert 'subpattern' in pattern
        assert isinstance(pattern['subpattern'], list)
        assert len(pattern['subpattern']) > 1
        for a in range(0, cast(int, pattern["repeat_count"])):
            for b in cast(List[Dict[str, Union[str, Dict[str, Union[str, list]], int]]], pattern["subpattern"]):
                assert isinstance(b, dict)
                recursive_parse_patterns(cast(Dict[str, Union[str, Dict[str, Union[str, list]], int]], b))
    else:
        assert 'noteEvent' in pattern
        assert isinstance(pattern['noteEvent'], str)
        assert pattern['noteEvent'] == 'on' or pattern['noteEvent'] == 'off'
        assert 'drumType' in pattern
        assert isinstance(pattern['drumType'], str)
        assert isinstance(get_drum_types()[pattern['drumType']], int)
        assert get_drum_types()[pattern['drumType']] != 0
        assert 'time' in pattern
        assert isinstance(pattern['time'], int)
        assert pattern['time'] >= 0


def drum_patterns_types(pattern: Dict[str, Union[str, List[Dict[str, Union[str, Dict[str, Union[str, list]], int]]]]]):
    assert isinstance(pattern, dict)
    assert 'name' in pattern
    assert isinstance(pattern['name'], str)
    assert len(pattern['name']) > 0
    assert 'ticksPerMeasure' in pattern
    assert isinstance(pattern['ticksPerMeasure'], int)
    assert pattern['ticksPerMeasure'] > 0
    assert 'measures' in pattern
    assert isinstance(pattern['measures'], int)
    assert pattern['measures'] > 0
    assert 'pattern' in pattern
    assert isinstance(pattern['pattern'], list)
    assert len(pattern['pattern']) > 0
    for event in pattern['pattern']:
        assert isinstance(event, dict)
        recursive_parse_patterns(event)
