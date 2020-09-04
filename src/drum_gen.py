import json
import mido
# import random

# "Crash Cymbal 1" is Crash Cymbal 1
# "Ride Cymbal 1" is Ride Cymbal 1
# "Claves" is Claves

drumTypes = {
    "Bass Drum 1": 0x24,
    "Side Stick": 0x25,
    "Acoustic Snare": 0x26,
    "Closed Hi Hat": 0x2a,
    "Pedal Hi Hat": 0x2c,
    "Crash Cymbal 1": 0x31,
    "Ride Cymbal 1": 0x33,
    "Claves": 0x4b
}

with open('drum_patterns/D-beat drum pattern 2b.json') as json_file:
    data = json.load(json_file)

# Format: (note event, drum type, time (in 1/480 of a quarter note))
drumPatterns = (
    # D-beat drum pattern 3
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 240), ("off", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 240), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Acoustic Snare", 0)),

    # Delayed backbeat
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0)),

    # Double bass drum beat
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("off", 0x23, 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("off", 0x23, 0)),

    # Double-time rock pattern
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0)),

    # Eighth-note ride pattern with triplet swing
    (("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 320), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 160), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 320), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 160), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 320), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 160), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 320), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 160)),

    # Fill with groove number 2 and crash
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0),
        ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0),
        ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 60),
        ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 60), ("on", "Crash Cymbal 1", 0), ("on", "Bass Drum 1", 0),
        ("off", "Crash Cymbal 1", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0),
        ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120),
        ("off", "Closed Hi Hat", 0)),

    # Fill with groove number 2 and sixteenth notes
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0),
        ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0),
        ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 60),
        ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 60), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0),
        ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120),
        ("off", "Closed Hi Hat", 0)),

    # Four to the floor bass drum pattern
    (("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 480), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 480),
        ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 480), ("on", "Bass Drum 1", 0),
        ("off", "Bass Drum 1", 480)),

    # Four to the floor beat
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0),
        ("off", "Bass Drum 1", 240), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240),
        ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 240),
        ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0)),

    # Four-four pattern with open and closed hi-hats
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Closed Hi Hat", 120), ("on", 0x2e, 0), ("off", "Bass Drum 1", 240), ("off", 0x2e, 0),
        ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Closed Hi Hat", 120), ("on", 0x2e, 0), ("off", "Bass Drum 1", 240), ("off", 0x2e, 0),
        ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Closed Hi Hat", 120), ("on", 0x2e, 0), ("off", "Bass Drum 1", 240), ("off", 0x2e, 0),
        ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0),
        ("off", "Closed Hi Hat", 120), ("on", 0x2e, 0), ("off", "Bass Drum 1", 240),
        ("off", 0x2e, 0)),

    # Gallop drum pattern
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 240), ("on", "Bass Drum 1", 0),
        ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0),
        ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 240),
        ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0), ("off", "Acoustic Snare", 120),
        ("off", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Bass Drum 1", 240), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0),
        ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0),
        ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 240), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120),
        ("on", "Bass Drum 1", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 0)),

    # Ghost note drumming
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 116), ("off", "Closed Hi Hat", 4),
        ("on", "Closed Hi Hat", 112), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 8), ("off", "Acoustic Snare", 0),
        ("on", "Acoustic Snare", 225), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 15), ("off", "Bass Drum 1", 0),
        ("off", "Acoustic Snare", 240), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Closed Hi Hat", 120), ("on", "Acoustic Snare", 0), ("off", "Bass Drum 1", 120), ("off", "Acoustic Snare", 0),
        ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 116), ("off", "Closed Hi Hat", 4),
        ("on", "Closed Hi Hat", 112), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 8), ("off", "Acoustic Snare", 0),
        ("on", "Acoustic Snare", 225), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 15), ("off", "Bass Drum 1", 0),
        ("off", "Acoustic Snare", 240), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0),
        ("off", "Closed Hi Hat", 120), ("on", "Acoustic Snare", 0), ("off", "Bass Drum 1", 120),
        ("off", "Acoustic Snare", 0)),

    # Half time rock pattern
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0),
        ("off", "Bass Drum 1", 240), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0),
        ("off", "Acoustic Snare", 240), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 120),
        ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120),
        ("on", "Closed Hi Hat", 120), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120),
        ("off", "Closed Hi Hat", 120),
        ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), (0xff01, 120)),

    # Half time shuffle
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 180), ("on", "Closed Hi Hat", 180),
        ("off", "Bass Drum 1", 180), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 180),
        ("on", "Closed Hi Hat", 180), ("off", "Closed Hi Hat", 180),
        ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 180), ("on", "Closed Hi Hat", 180),
        ("off", "Acoustic Snare", 180), ("off", "Closed Hi Hat", 0),
        ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 180),
        ("on", "Closed Hi Hat", 180), ("off", "Closed Hi Hat", 180))
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
    # pattern = random.choice(data)["pattern"]
    pattern = data["pattern"]
    for i in pattern:
        drum_pattern_repeat_recursion(i, drumTrack)
