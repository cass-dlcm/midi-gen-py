from json import load
from mido import MetaMessage, MidiTrack, Message, MidiFile
from glob import glob
from random import choice
from typing import List, Dict

C_VAL: int = 48
guitar_patterns: List[Dict[str, List[dict]]] = []
file_list = glob("data/guitar_patterns/*.json")

# Format as json:
# {
#     "name": a unique name,
#     "pattern": [
#         {
#             "noteEvent": either "note_on" or "note_off",
#             "pitchIndex": which pitch in the given chord,
#             "time": measured in 1/480 of a quarter note
#         },
#         {
#             "repeat_count": a number of times to repeat the subpattern,
#             "subpattern": {
#                 {
#                     "noteEvent": either "note_on" or "note_off",
#                     "pitchIndex": which pitch in the given chord,
#                     "time": measured in 1/480 of a quarter note
#                 }
#             }
#         }
#     ]
# }


def read_patterns():
    global guitar_patterns
    guitar_patterns = []
    for file in file_list:
        with open(file) as json_file:
            guitar_patterns.append(load(json_file))


def get_patterns() -> List[Dict[str, List[dict]]]:
    return guitar_patterns


def filter_patterns(chosen: List[int]):
    global guitar_patterns
    temp: List[Dict[str, List[dict]]] = []
    for i in chosen:
        temp.append(guitar_patterns[i])
    guitar_patterns = temp


def guitar_pattern_repeat_recursion(level: dict, guitar_track: MidiTrack,
                                    sequences: List[List[List[int]]], a: int,
                                    b: int):
    if "repeat_count" in level:
        for a in range(0, level["repeat_count"]):
            for c in level["subpattern"]:
                guitar_pattern_repeat_recursion(c, guitar_track, sequences, a,
                                                b)
    else:
        guitar_track.append(Message(level['noteEvent'],
                            note=sequences[a][b][level["pitchIndex"]] + C_VAL,
                            channel=1, time=level["time"]))


def guitar(guitar_track: MidiTrack, progression_length: int,
           sequences: List[List[List[int]]], segments: int):
    for a in range(0, segments):
        for b in range(0, progression_length):
            pickPattern: dict = choice(guitar_patterns)
            guitar_track.append(MetaMessage('text', text=pickPattern['name']))
            for c in pickPattern['pattern']:
                guitar_pattern_repeat_recursion(c, guitar_track, sequences, a,
                                                b)


def create_guitar_track(mid: MidiFile, progression_length: int,
                        sequences: List[List[List[int]]], segments: int):
    read_patterns()
    totalPatterns: int = len(get_patterns())
    a: List[int] = []
    for i in range(0, totalPatterns):
        a.append(i)
    filter_patterns(a)
    guitar_track: MidiTrack = MidiTrack()
    guitar_track.append(MetaMessage('instrument_name', name='Guitar'))
    mid.tracks.append(guitar_track)
    guitar_track.append(Message(
        'program_change',
        program=25,
        channel=1,
        time=0))
    guitar(guitar_track, progression_length, sequences, segments)
    guitar_track.append(MetaMessage('end_of_track'))
