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
from src.guitar_gen import read_patterns, filter_patterns, create_track, get_patterns, choose_patterns
from tests.test_main import type_sequences
from mido import MidiFile
from filecmp import cmp
from src.main import simple_pick_chords, simple_chord_order, create_simple_meta_track, get_config
from os import mkdir
from typing import List, Dict, Union, cast


def test_guitar():
    """Generates each guitar pattern and compares it to a 'known good' file of each pattern"""
    file_list: List[str] = glob.glob("data/guitar_patterns/*.json")
    for i in range(0, len(file_list)):
        progression_length: int = 4
        mid: MidiFile = MidiFile()
        mid.tracks.append(create_simple_meta_track()[0])
        read_patterns(get_config()['guitar_path'])
        filter_patterns([i])
        chosen_patterns = choose_patterns(progression_length)
        mid.ticks_per_beat = int(chosen_patterns[1] / 4)
        sequences: Dict[str, Union[List[List[List[int]]], List[str]]] = simple_chord_order(simple_pick_chords(progression_length))
        pattern: dict = get_patterns()[0]
        guitar_patterns_types(pattern)
        type_sequences(sequences)
        mid.tracks.append(create_track(progression_length, sequences['values'], 1, chosen_patterns[0], mid.ticks_per_beat))
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
        file_name: str = pattern['name'] + '.mid'
        mid.save('tests/output/guitar/' + file_name)
        assert abs(mid.length - 8) < .001
        assert cmp('tests/output/guitar/' + file_name, 'tests/data/guitar/' + file_name, shallow=False)


def recursive_parse_patterns(pattern: Dict[str, Union[str, Dict[str, Union[str, list]], int]]):
    """Recurisvely tests the patterns for validity

    :param pattern: The guitar pattern to test
    :type pattern: Dict[str, Union[str, int, Dict[str, Union[str, list]]]]
    """
    if "repeat_count" in pattern:
        assert isinstance(pattern['repeat_count'], int)
        assert pattern['repeat_count'] > 1
        assert isinstance(pattern['subpattern'], list)
        assert len(pattern['subpattern']) > 1
        for a in range(0, cast(int, pattern["repeat_count"])):
            for b in cast(List[Dict[str, Union[str, Dict[str, Union[str, list]], int]]], pattern["subpattern"]):
                recursive_parse_patterns(cast(Dict[str, Union[str, Dict[str, Union[str, list]], int]], b))
    else:
        assert isinstance(pattern['note_event'], str)
        assert pattern['note_event'] == 'note_on' or pattern['note_event'] == 'note_off'
        assert isinstance(pattern['pitchIndex'], int)
        assert pattern['pitchIndex'] >= 0 and pattern['pitchIndex'] <= 3
        assert isinstance(pattern['time'], int)
        assert pattern['time'] >= 0


def guitar_patterns_types(pattern: Dict[str, Union[str, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]):
    """Tests a pattern for validity

    :param pattern: The guitar pattern to test
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
