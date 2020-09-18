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

from src.main import randomize_chord_order, pick_chords, create, get_config
from src import drum_gen, guitar_gen
from mido import MidiFile
from glob import glob
import os
from filecmp import cmp
from time import sleep
from typing import List, Dict, Union, cast
from random import randint


# Fails on extremely rare occasions; if it fails at the assertion, try it again
def test_individuality(monkeypatch):
    """Test that two runs of the program generate different results

    :param monkeypatch: The Monkeypatch object
    :type monkeypatch: pytest.MonkeyPatch
    """
    drum_gen.read_patterns(get_config()['drum_path'])
    drum_pattern_count = randint(1, len(drum_gen.get_patterns()))
    drum_pattern_str: str = ''
    for i in range(0, drum_pattern_count):
        drum_pattern_str += str(randint(0, len(drum_gen.get_patterns()) - 1)) + ' '
    guitar_gen.read_patterns(get_config()['guitar_path'])
    guitar_pattern_count = randint(1, len(guitar_gen.get_patterns()))
    guitar_pattern_str: str = ''
    for i in range(0, guitar_pattern_count):
        guitar_pattern_str += str(randint(0, len(guitar_gen.get_patterns()) - 1)) + ' '
    main_with_input(monkeypatch, drum_pattern_str, guitar_pattern_str)
    list_of_files: List[str] = glob('output/*.mid')
    file_a: str = max(list_of_files, key=os.path.getctime)
    sleep(1)
    main_with_input(monkeypatch, drum_pattern_str, guitar_pattern_str)
    list_of_files: List[str] = glob('output/*.mid')
    file_b: str = max(list_of_files, key=os.path.getctime)
    assert not(cmp(file_a, file_b, shallow=False))


def type_sequences(sequences: Dict[str, Union[List[List[List[int]]], List[str]]]):
    """Checks the structure of the sequences dictionary to make sure it's well formed

    :param sequences: The dictionary of sequence information to test
    :type sequences: Dict[str, Union[List[List[List[int]]], List[str]]]
    """
    assert isinstance(sequences, dict)
    assert 'values' in sequences
    assert isinstance(sequences['values'], list)
    assert len(sequences['values']) > 0
    for a in sequences['values']:
        assert isinstance(a, list)
        assert len(a) > 0
        for b in a:
            assert isinstance(b, list)
            assert len(b) > 0
            for c in b:
                assert isinstance(c, int)
                assert c >= 0
    assert 'strings' in sequences
    assert isinstance(sequences['strings'], list)
    assert len(sequences['strings']) > 0
    for a in sequences['strings']:
        assert isinstance(a, str)
        assert len(a) > 0


def test_type_random_sequences():
    """Checks that the sequences dictionary is built properly"""
    for _ in range(0, 1000):
        sequences: Dict[str, Union[List[List[List[int]]], List[str]]] = randomize_chord_order(pick_chords(4), 8)
        type_sequences(sequences)


def main_with_input(monkeypatch, drum_pattern_str: str, guitar_pattern_str: str):
    """A modified main function to accommodate the monkeypatch

    :param monkeypatch: The Monkeypatch object
    :type monkeypatch: pytest.MonkeyPatch
    :param drum_patterns_str: A string containing the list of drum patterns to use
    :type drum_patterns_str: str
    :param guitar_patterns_str: A string containing the list of guitar patterns to use
    :type guitar_patterns_str: str
    """
    progression_length: int = cast(int, get_config()['progression_length'])
    segments: int = cast(int, get_config()['segments'])
    mid: MidiFile = MidiFile()
    monkeypatch.setattr('builtins.input', lambda _: drum_pattern_str)
    drum_gen.setup_patterns(cast(str, get_config()['drum_path']))
    monkeypatch.setattr('builtins.input', lambda _: guitar_pattern_str)
    guitar_gen.setup_patterns(cast(str, get_config()['guitar_path']))
    monkeypatch.setattr('builtins.input', lambda _: '90 180')
    create(progression_length, segments, mid)
