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

from json import load
from mido import MetaMessage, MidiTrack, Message
from glob import glob
from random import randint
from typing import List, Dict, Union, cast, Tuple
from numpy import lcm

C_VAL: int = 48
patterns: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]] = []

# Format as json:
# {
#     "name": a unique name,
#     "pattern": [
#         {
#             "note_event": either "note_on" or "note_off",
#             "pitchIndex": which pitch in the given chord,
#             "pitch": an absolute pitch, with the root added on,
#             "time": measured in 1/480 of a quarter note
#         },
#         {
#             "repeat_count": a number of times to repeat the subpattern,
#             "subpattern": {
#                 {
#                     "note_event": either "note_on" or "note_off",
#                     "pitchIndex": which pitch in the given chord,
#                     "pitch": an absolute pitch, with the root added on,
#                     "time": measured in 1/480 of a quarter note
#                 },
#                 {
#                     "repeat_count": a number of times to repeat the subpattern,
#                     "subpattern": {}
#                 }
#             }
#         }
#     ]
# }


def read_patterns(path: str):
    """Reads the guitar patterns in from a folder

    :param path: The path to the pattern json files
    :type path: str
    """
    global patterns
    file_list = glob(path)
    patterns = []
    for file in file_list:
        with open(file) as json_file:
            patterns.append(load(json_file))


def get_patterns() -> List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]]:
    """Gets a copy of the list of guitar patterns

    :return: The list of guitar patterns
    :rtype: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]]
    """
    return patterns.copy()


def filter_patterns(chosen: List[int] = None) -> int:
    """Filters the guitar patterns only to the ones chosen

    :param chosen: A list of numbers of the chosen guitar patterns
    :type chosen: List[int]
    :return: the lowest common multiple of ticks per measure from the files
    :rtype: int
    """
    global patterns
    ticks_per_measure: int = 4
    temp: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]] = []
    if chosen is None:
        for i in range(0, len(patterns)):
            print(str(i) + ": " + str(patterns[i]['name']))
        n = input("Enter the pattern numbers, all seperated by spaces: ").split()
        if len(n) == 0:
            for b in range(0, len(patterns)):
                temp.append(patterns[b])
                ticks_per_measure = lcm(ticks_per_measure, patterns[b]['ticks_per_measure'])
        else:
            for a in n:
                temp.append(patterns[int(a)])
                ticks_per_measure = lcm(ticks_per_measure, patterns[int(a)]['ticks_per_measure'])
    else:
        for i in chosen:
            temp.append(patterns[i])
            ticks_per_measure = lcm(ticks_per_measure, patterns[i]['ticks_per_measure'])
    patterns = temp
    return ticks_per_measure


def guitar_pattern_repeat_recursion(level: Dict[str, Union[str, int, Dict[str, Union[str, list]]]], track: MidiTrack, sequences: List[List[List[int]]], a: int, b: int, ticks_per_measure: int, ticks_per_beat: int):
    """Parses, recurisvely, a guitar pattern and adds note_events

    :param level: The current level of the nested pattern
    :type level: Dict[str, Union[str, Dict[str, Union[str, list]], int]]
    :param track: The guitar track to add note events to
    :type track: mido.MidiTrack
    :param sequences: The array of notes
    :type sequences: List[List[List[int]]]
    :param a: The current sequence
    :type a: int
    :param b: The current chord in the sequence
    :type b: int
    :param ticks_per_measure: how many ticks in a measure of this pattern
    :type ticks_per_measure: int
    :param ticks_per_beat: how many ticks per beat of this file
    :type ticks_per_beat: int
    """
    if "repeat_count" in level:
        for _ in range(0, cast(int, level["repeat_count"])):
            for c in cast(List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]], level["subpattern"]):
                guitar_pattern_repeat_recursion(c, track, sequences, a, b, ticks_per_measure, ticks_per_beat)
    else:
        if "pitchIndex" in level:
            track.append(Message(cast(str, level['note_event']), note=sequences[a][b][cast(int, level["pitchIndex"])] + C_VAL, channel=1, time=int(round(cast(int, level["time"]) * ticks_per_beat * 4 / ticks_per_measure))))
        else:
            track.append(Message(cast(str, level['note_event']), note=sequences[a][b][0] + cast(int, level["pitch"]), channel=1, time=int(round(cast(int, level["time"]) * ticks_per_beat * 4 / ticks_per_measure))))


def guitar(track: MidiTrack, pattern: Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]], a: int, b: int, sequences: List[List[List[int]]], ticks_per_beat: int):
    """Picks guitar patterns and adds them to the track

    :param track: The guitar track to add patterns to
    :type track: mido.MidiTrack
    :param progression_length: The number of chords in a single sequence
    :type progression_length: int
    :param sequences: The array of notes
    :type sequences: List[List[List[int]]]
    :param segments: The number of sequences
    :type segments: int
    :param ticks_per_beat: how many ticks per beat of this file
    :type ticks_per_beat: int
    """
    track.append(MetaMessage('text', text=cast(str, pattern['name'])))
    for c in cast(List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]], pattern['pattern']):
        guitar_pattern_repeat_recursion(c, track, sequences, a, b, cast(int, pattern['ticks_per_measure']), ticks_per_beat)


def create_track(progression_length: int, sequences: List[List[List[int]]], segments: int, chosen_patterns: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]], ticks_per_beat: int) -> MidiTrack:
    """Creates a guitar track given a specific length

    :param progression_length: The number of chords in a single sequence
    :type progression_length: int
    :param sequences: The array of notes
    :type sequences: List[List[List[int]]]
    :return: The generated guitar track
    :param segments: The number of sequences
    :type segments: int
    :param ticks_per_beat: how many ticks per beat of this file
    :type ticks_per_beat: int
    :return: The created guitar track
    :rtype: mido.MidiTrack
    """
    track: MidiTrack = MidiTrack()
    track.append(MetaMessage('instrument_name', name='Guitar'))
    track.append(Message('program_change', program=25, channel=1, time=0))
    for a in range(0, segments):
        for b in range(0, progression_length):
            guitar(track, chosen_patterns[a * progression_length + b], a, b, sequences, ticks_per_beat)
    track.append(MetaMessage('end_of_track'))
    return track


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
        i = randint(0, len(patterns) - 1)
        chosen_patterns.append(patterns[i])
        ticks_per_measure = lcm(ticks_per_measure, patterns[i]['ticks_per_measure'])
    return chosen_patterns, ticks_per_measure


def setup_patterns(path: str) -> int:
    """Initializes the entire set of guitar patterns

    :param path: The path to the pattern json files
    :type path: str
    :return: the lowest common multiple of ticks per measure from the files
    :rtype: int
    """
    read_patterns(path)
    return filter_patterns()
