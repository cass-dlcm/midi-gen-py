from json import load
from mido import MetaMessage, MidiTrack, Message
from glob import glob
from random import choice

c_val = 48
guitar_patterns = []
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


def read_guitar_patterns():
    global guitar_patterns
    guitar_patterns = []
    for file in file_list:
        with open(file) as json_file:
            guitar_patterns.append(load(json_file))


def get_guitar_patterns():
    return guitar_patterns


def filter_guitar_patterns(chosen):
    global guitar_patterns
    temp = []
    for i in chosen:
        temp.append(guitar_patterns[i])
    guitar_patterns = temp


def guitar_pattern_repeat_recursion(level, guitar_track, sequences, a, b):
    if "repeat_count" in level:
        for a in range(0, level["repeat_count"]):
            for b in level["subpattern"]:
                guitar_pattern_repeat_recursion(b, guitar_track)
    else:
        guitar_track.append(Message(level['noteEvent'], note=sequences[a][b][level["pitchIndex"]] + c_val, channel=1, time=level["time"]))


def guitar(guitar_track, progression_length, sequences, segments):
    for a in range(0, segments):
        for b in range(0, progression_length):
            pickPattern = choice(guitar_patterns)
            guitar_track.append(MetaMessage('text', text=pickPattern['name']))
            for c in pickPattern['pattern']:
                guitar_pattern_repeat_recursion(c, guitar_track, sequences, a, b)


def create_guitar_track(mid, progression_length, sequences, segments):
    read_guitar_patterns()
    guitar_track = MidiTrack()
    guitar_track.append(MetaMessage('instrument_name', name='Guitar'))
    mid.tracks.append(guitar_track)
    guitar_track.append(Message(
        'program_change',
        program=25,
        channel=1,
        time=0))
    guitar(guitar_track, progression_length, sequences, segments)
    guitar_track.append(MetaMessage('end_of_track'))
