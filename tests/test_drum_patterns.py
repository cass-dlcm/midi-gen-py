# This file is part of midi-gen-py.
# midi-gen-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# midi-gen-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with midi-gen-py.  If not, see <https://www.gnu.org/licenses/>.

import glob
from src.drum_gen import read_patterns, filter_patterns, get_drum_types, create_track, get_patterns, choose_patterns
from src.main import create_simple_meta_track, get_config
from mido import MidiFile
from filecmp import cmp
from os import mkdir
from typing import List, Union, Dict, cast


def test_drums():
    """Generates each drum pattern and compares it to a 'known good' file of each pattern"""
    file_list: List[str] = glob.glob(get_config()['drum_path'])
    for i in range(0, len(file_list)):
        mid: MidiFile = MidiFile()
        mid.tracks.append(create_simple_meta_track()[0])
        read_patterns(get_config()['drum_path'])
        filter_patterns([i])
        chosen_patterns = choose_patterns(1)
        mid.ticks_per_beat = int(chosen_patterns[1] / 4)
        pattern = get_patterns()[0]
        drum_patterns_types(pattern)
        mid.tracks.append(create_track(chosen_patterns[0], 1, mid.ticks_per_beat))
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
        assert abs(mid.length - 2 * pattern['measures']) < .001
        assert cmp('tests/output/drums/' + file_name, 'tests/data/drums/' + file_name, shallow=False)


def recursive_parse_patterns(pattern: Dict[str, Union[str, int, Dict[str, Union[str, list]]]]):
    """Recurisvely tests the patterns for validity

    :param pattern: The drum pattern to test
    :type pattern: Dict[str, Union[str, int, Dict[str, Union[str, list]]]]
    """
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
        assert 'note_event' in pattern
        assert isinstance(pattern['note_event'], str)
        assert pattern['note_event'] == 'note_on' or pattern['note_event'] == 'note_off'
        assert 'drum_type' in pattern
        assert isinstance(pattern['drum_type'], str)
        assert isinstance(get_drum_types()[pattern['drum_type']], int)
        assert get_drum_types()[pattern['drum_type']] != 0
        assert 'time' in pattern
        assert isinstance(pattern['time'], int)
        assert pattern['time'] >= 0


def drum_patterns_types(pattern: Dict[str, Union[str, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]):
    """Tests a pattern for validity

    :param pattern: The drum pattern to test
    :type pattern: Dict[str, Union[str, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]
    """
    assert isinstance(pattern, dict)
    assert 'name' in pattern
    assert isinstance(pattern['name'], str)
    assert len(pattern['name']) > 0
    assert 'ticks_per_measure' in pattern
    assert isinstance(pattern['ticks_per_measure'], int)
    assert pattern['ticks_per_measure'] > 0
    assert 'measures' in pattern
    assert isinstance(pattern['measures'], int)
    assert pattern['measures'] > 0
    assert 'pattern' in pattern
    assert isinstance(pattern['pattern'], list)
    assert len(pattern['pattern']) > 0
    for event in pattern['pattern']:
        assert isinstance(event, dict)
        recursive_parse_patterns(event)
