import json
import mido
import glob
import random

# "Crash Cymbal 1" is Crash Cymbal 1
# "Ride Cymbal 1" is Ride Cymbal 1
# "Claves" is Claves

drumTypes = {
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

file_list = glob.glob("./drum_patterns/*.json")
data = []
for file_path in file_list:
    with open(file_path) as json_file:
        data.append(json.load(json_file))

# Format: (note event, drum type, time (in 1/480 of a quarter note))
drumPatterns = (
)


def drum_pattern_repeat_recursion(level, drumTrack):
    if "repeat_count" in level:
        for a in range(0, level["repeat_count"]):
            for b in level["subpattern"]:
                drum_pattern_repeat_recursion(b, drumTrack)
    else:
        if (level["noteEvent"] == "on"):
            drumTrack.append(mido.Message('note_on', note=drumTypes[level["drumType"]], channel=9, time=level["time"]))
        elif (level["noteEvent"] == "off"):
            drumTrack.append(mido.Message('note_off', note=drumTypes[level["drumType"]], channel=9, time=level["time"]))
        else:
            print("whoops")


def drum(drumTrack):
    pattern = random.choice(data)["pattern"]
    for i in pattern:
        drum_pattern_repeat_recursion(i, drumTrack)


def createPatternFile():
    patternFile = open('drum_patterns.json', 'w')
    a = []
    for pattern in drumPatterns:
        b = {}
        c = []
        for note in pattern:
            print(note)
            d = {
                'noteEvent': note[0],
                'drumType': note[1],
                'time': note[2]
            }
            c.append(d)
        b['name'] = ''
        b['pattern'] = c
        a.append(b)
    patternFile.write(json.dumps(a, indent=2))


# createPatternFile()
