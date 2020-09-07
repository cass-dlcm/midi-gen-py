import json
from mido import MetaMessage, MidiTrack, Message, MidiFile
from glob import glob
from random import choice

# "Crash Cymbal 1" is Crash Cymbal 1
# "Ride Cymbal 1" is Ride Cymbal 1
# "Claves" is Claves

drumTypes: dict = {
    "Acoustic Bass Drum": 0x23,
    "Bass Drum 1": 0x24,
    "Side Stick": 0x25,
    "Acoustic Snare": 0x26,
    "Closed Hi Hat": 0x2a,
    "Pedal Hi Hat": 0x2c,
    "Open Hi Hat": 0x2e,
    "Crash Cymbal 1": 0x31,
    "Ride Cymbal 1": 0x33,
    "Claves": 0x4b
}

file_list: list = glob("data/drum_patterns/*.json")

# Format as json:
# {
#     "name": a unique name,
#     "pattern": [
#         {
#             "noteEvent": either "on" or "off",
#             "drumType": any drum type listed in drum_gen.drumTypes,
#             "time": measured in 1/480 of a quarter note
#         },
#         {
#             "repeat_count": a number of times to repeat the subpattern,
#             "subpattern": {
#                 {
#                     "noteEvent": either "on" or "off",
#                     "drumType": any drum type listed in drum_gen.drumTypes,
#                     "time": measured in 1/480 of a quarter note
#                 }
#             }
#         }
#     ]
# }
drumPatterns: list = []


def readDrumPatterns():
    global drumPatterns
    drumPatterns = []
    for file_path in file_list:
        with open(file_path) as json_file:
            drumPatterns.append(json.load(json_file))


def getDrumPatterns() -> list:
    return drumPatterns


def filterDrumPatterns(chosen: list):
    global drumPatterns
    temp: list = []
    for i in chosen:
        temp.append(drumPatterns[i])
    drumPatterns = temp


def drum_pattern_repeat_recursion(level: dict, drumTrack: MidiTrack):
    if "repeat_count" in level:
        for a in range(0, level["repeat_count"]):
            for b in level["subpattern"]:
                drum_pattern_repeat_recursion(b, drumTrack)
    else:
        if (level["noteEvent"] == "on"):
            drumTrack.append(Message('note_on', note=drumTypes[level["drumType"]], channel=9, time=level["time"]))
        elif (level["noteEvent"] == "off"):
            drumTrack.append(Message('note_off', note=drumTypes[level["drumType"]], channel=9, time=level["time"]))
        else:
            print("whoops")


def drum(drumTrack: MidiTrack):
    pattern: dict = choice(drumPatterns)
    drumTrack.append(MetaMessage('text', text=pattern['name']))
    for i in pattern['pattern']:
        drum_pattern_repeat_recursion(i, drumTrack)


def create_drum_track(mid: MidiFile, progressionLength: int):
    readDrumPatterns()
    totalPatterns: int = len(getDrumPatterns())
    a: list = []
    for i in range(0, totalPatterns):
        a.append(i)
    filterDrumPatterns(a)
    drumTrack: MidiTrack = MidiTrack()
    drumTrack.append(MetaMessage('instrument_name', name='Drum set'))
    mid.tracks.append(drumTrack)
    for _ in range(0, 8 * progressionLength):
        drum(drumTrack)
    drumTrack.append(MetaMessage('end_of_track'))
