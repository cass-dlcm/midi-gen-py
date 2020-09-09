from json import load
from mido import MetaMessage, MidiTrack, Message
from glob import glob
from random import choice
from typing import List, Dict, Union, cast
from numpy import lcm

C_VAL: int = 48
patterns: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]] = []
file_list = glob("data/guitar_patterns/*.json")

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


def read_patterns():
    """Reads the guitar patterns in from a folder"""
    global patterns
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


def filter_patterns(chosen: List[int]) -> int:
    """Filters the guitar patterns only to the ones chosen

    :param chosen: A list of numbers of the chosen guitar patterns
    :type chosen: List[int]
    """
    global patterns
    ticks_per_measure: int = 4
    temp: List[Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]]] = []
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
    """
    if "repeat_count" in level:
        for _ in range(0, cast(int, level["repeat_count"])):
            for c in cast(List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]], level["subpattern"]):
                guitar_pattern_repeat_recursion(c, track, sequences, a, b, ticks_per_measure, ticks_per_beat)
    else:
        if "pitchIndex" in level:
            track.append(Message(cast(str, level['note_event']), note=sequences[a][b][cast(int, level["pitchIndex"])] + C_VAL, channel=1, time=int(cast(int, level["time"]) * ticks_per_beat * 4 / ticks_per_measure)))
        else:
            track.append(Message(cast(str, level['note_event']), note=sequences[a][b][0] + cast(int, level["pitch"]), channel=1, time=int(cast(int, level["time"]) * ticks_per_beat * 4 / ticks_per_measure)))


def guitar(track: MidiTrack, progression_length: int, sequences: List[List[List[int]]], segments: int, ticks_per_beat: int):
    """Picks guitar patterns and adds them to the track

    :param track: The guitar track to add patterns to
    :type track: mido.MidiTrack
    :param progression_length: The number of chords in a single sequence
    :type progression_length: int
    :param sequences: The array of notes
    :type sequences: List[List[List[int]]]
    :param segments: The number of sequences
    :type segments: int
    """
    for a in range(0, segments):
        for b in range(0, progression_length):
            pickPattern: Dict[str, Union[str, int, List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]]]] = choice(patterns)
            track.append(MetaMessage('text', text=cast(str, pickPattern['name'])))
            for c in cast(List[Dict[str, Union[str, int, Dict[str, Union[str, list]]]]], pickPattern['pattern']):
                guitar_pattern_repeat_recursion(c, track, sequences, a, b, cast(int, pickPattern['ticks_per_measure']), ticks_per_beat)


def create_track(progression_length: int, sequences: List[List[List[int]]], segments: int, ticks_per_beat: int) -> MidiTrack:
    """Creates a guitar track given a specific length

    :param progression_length: The number of chords in a single sequence
    :type progression_length: int
    :param sequences: The array of notes
    :type sequences: List[List[List[int]]]
    :return: The generated guitar track
    :param segments: The number of sequences
    :type segments: int
    :return: The created guitar track
    :rtype: mido.MidiTrack
    """
    track: MidiTrack = MidiTrack()
    track.append(MetaMessage('instrument_name', name='Guitar'))
    track.append(Message('program_change', program=25, channel=1, time=0))
    guitar(track, progression_length, sequences, segments, ticks_per_beat)
    track.append(MetaMessage('end_of_track'))
    return track


def setup_patterns() -> int:
    """Initializes the entire set of guitar patterns

    Todo: ask user for specific patterns
    """
    read_patterns()
    total_patterns: int = len(get_patterns())
    a: List[int] = []
    for i in range(0, total_patterns):
        a.append(i)
    return filter_patterns(a)
