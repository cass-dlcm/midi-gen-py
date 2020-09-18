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


import json
from mido import MetaMessage, MidiTrack, Message
from glob import glob
from random import randint
from typing import List, Dict, Union, cast, Tuple
from numpy import lcm

drum_types: dict = {
    "Acoustic Bass Drum": 0x23,
    "Bass Drum 1": 0x24,
    "Side Stick": 0x25,
    "Acoustic Snare": 0x26,
    "Electric Snare": 0x28,
    "Closed Hi Hat": 0x2a,
    "Pedal Hi Hat": 0x2c,
    "Open Hi Hat": 0x2e,
    "Crash Cymbal 1": 0x31,
    "Ride Cymbal 1": 0x33,
    "Claves": 0x4b
}

# Format as json:
# {
#     "name": a unique name,
#     "pattern": [
#         {
#             "note_event": either "on" or "off",
#             "drum_type": any drum type listed in drum_gen.drum_types,
#             "time": measured in 1/480 of a quarter note
#         },
#         {
#             "repeat_count": a number of times to repeat the subpattern,
#             "subpattern": {
#                 {
#                     "note_event": either "on" or "off",
#                     "drum_type": any drum type listed in drum_gen.drum_types,
#                     "time": measured in 1/480 of a quarter note
#                 },
#                 {
#                     "repeat_count": a number of times to repeat the subpattern,
#                     "subpattern": {}
#                 }#             }
#         }
#     ]
# }
drum_patterns: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]] = []


def get_drum_types() -> Dict[str, int]:
    """Gets a copy of the dictionary of drum types

    :return: The dictionary of drum types
    :rtype: Dict[str, int]
    """
    return drum_types.copy()


def read_patterns(path: str):
    """Reads the drum patterns in from a folder

    :param path: The path to the pattern json files
    :type path: str
    """
    file_list: List[str] = glob(path)
    global drum_patterns
    drum_patterns = []
    for file_path in file_list:
        with open(file_path) as json_file:
            drum_patterns.append(json.load(json_file))


def get_patterns() -> List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]]:
    """Gets a copy of the list of drum patterns

    :return: The list of drum patterns
    :rtype: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]]
    """
    return drum_patterns.copy()


def filter_patterns(chosen: List[int] = None):
    """Filters the drum patterns only to the ones chosen

    :param chosen: A list of numbers of the chosen drum patterns
    :type chosen: List[int]
    :return: the lowest common multiple of ticks per measure from the files
    :rtype: int
    """
    global drum_patterns
    temp: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]] = []
    if chosen is None:
        for i in range(0, len(drum_patterns)):
            print(str(i) + ": " + str(drum_patterns[i]['name']))
        n = input("Enter the pattern numbers, all seperated by spaces: ").split()
        if len(n) == 0:
            for b in range(0, len(drum_patterns)):
                temp.append(drum_patterns[b])
        else:
            for a in n:
                temp.append(drum_patterns[int(a)])
    else:
        for i in chosen:
            temp.append(drum_patterns[i])
    drum_patterns = temp


def drum_pattern_repeat_recursion(level: Dict[str, Union[str, Dict[str, Union[str, list]], int]], drum_track: MidiTrack, ticks_per_measure: int, ticks_per_beat: int):
    """Parses, recurisvely, a drum pattern and adds note events

    :param level: The current level of the nested pattern
    :type level: Dict[str, Union[str, Dict[str, Union[str, list]], int]]
    :param drum_track: The drum track to add note events to
    :type drum_track: mido.MidiTrack
    :param ticks_per_measure: how many ticks in a measure of this pattern
    :type ticks_per_measure: int
    :param ticks_per_beat: how many ticks per beat of this file
    :type ticks_per_beat: int
    """
    if "repeat_count" in level:
        for _ in range(0, cast(int, level["repeat_count"])):
            for b in cast(List[Dict[str, Union[str, Dict[str, Union[str, list]], int]]], level["subpattern"]):
                drum_pattern_repeat_recursion(cast(Dict[str, Union[str, Dict[str, Union[str, list]], int]], b), drum_track, ticks_per_measure, ticks_per_beat)
    else:
        drum_track.append(Message(level['note_event'], note=drum_types[level["drum_type"]], channel=9, time=int(round(cast(int, level["time"]) * ticks_per_beat * 4 / ticks_per_measure))))


def drum(pattern: Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]], track: MidiTrack, ticks_per_beat: int):
    """Picks a drum pattern and adds it to the track

    :param track: The drum track to add patterns to
    :type track: mido.MidiTrack
    :param ticks_per_beat: how many ticks per beat of this file
    :type ticks_per_beat: int
    """
    track.append(MetaMessage('text', text=cast(str, pattern['name'])))
    for i in cast(List[Dict[str, Union[str, Dict[str, Union[str, list]], int]]], pattern['pattern']):
        drum_pattern_repeat_recursion(i, track, cast(int, pattern['ticks_per_measure']), ticks_per_beat)


def choose_patterns(measures: int) -> Tuple[List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]], int]:
    """Returns a set of patterns for the given number of measures

    :param measures: The number of measures to generate
    :type measures: int
    :return: The chosen set of patterns and the ticks per measures
    :rtype: Tuple[List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]], int]
    """
    chosen_patterns: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]] = []
    ticks_per_measure: int = 4
    for _ in range(0, measures):
        i = randint(0, len(drum_patterns) - 1)
        chosen_patterns.append(drum_patterns[i])
        ticks_per_measure = lcm(ticks_per_measure, drum_patterns[i]['ticks_per_measure'])
    return chosen_patterns, ticks_per_measure


def create_track(chosen_patterns: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]], measures: int, ticks_per_beat: int) -> MidiTrack:
    """Creates a drum track given a specific length

    :param measures: The total number of measures for the track
    :type meaures: int
    :param ticks_per_beat: how many ticks per beat of this file
    :type ticks_per_beat: int
    :return: The generated drum track
    :rtype: mido.MidiTrack
    """
    drum_track: MidiTrack = MidiTrack()
    drum_track.append(MetaMessage('instrument_name', name='Drum set'))
    for i in range(0, measures):
        drum(chosen_patterns[i], drum_track, ticks_per_beat)
    drum_track.append(MetaMessage('end_of_track'))
    return drum_track


def setup_patterns(path: str) -> int:
    """Initializes the entire set of drum patterns

    :param path: The path to the pattern json files
    :type path: str
    :return: the lowest common multiple of ticks per measure from the files
    :rtype: int
    """
    read_patterns(path)
    return filter_patterns()
