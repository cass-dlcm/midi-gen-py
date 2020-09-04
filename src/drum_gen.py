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

with open('drum_patterns/Blast beat drum pattern most common and simple.json') as json_file:
    data = json.load(json_file)

# Format: (note event, drum type, time (in 1/480 of a quarter note))
drumPatterns = (
    # Blast beat drum pattern
    (("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 240), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 0)),

    # Characteristic disco drum pattern
    (("on", "Ride Cymbal 1", 0), ("on", "Bass Drum 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Bass Drum 1", 120), ("off", "Ride Cymbal 1", 0), ("on", "Ride Cymbal 1", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Bass Drum 1", 120), ("off", "Ride Cymbal 1", 0), ("off", "Acoustic Snare", 0), ("on", "Ride Cymbal 1", 0), ("on", "Bass Drum 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Bass Drum 1", 120), ("off", "Ride Cymbal 1", 0), ("on", "Ride Cymbal 1", 0), ("on", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 120), ("on", "Ride Cymbal 1", 0), ("off", "Bass Drum 1", 120), ("off", "Ride Cymbal 1", 0), ("off", "Acoustic Snare", 0)),

    # Characteristic rock drum pattern rimshot
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 232), ("off", "Closed Hi Hat", 8), ("on", "Closed Hi Hat", 225), ("on", "Side Stick", 0), ("off", "Bass Drum 1", 15), ("off", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Side Stick", 240), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 232), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 8), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 225), ("on", "Side Stick", 0), ("off", "Bass Drum 1", 15), ("off", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Side Stick", 240), ("off", "Closed Hi Hat", 0)),

    # Characteristic rock drum pattern
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Acoustic Snare", 0)),

    # Characteristic rock hi-hat pattern
    (("on", "Pedal Hi Hat", 0), ("off", "Pedal Hi Hat", 240), ("on", "Pedal Hi Hat", 0), ("off", "Pedal Hi Hat", 240), ("on", "Pedal Hi Hat", 0), ("off", "Pedal Hi Hat", 240), ("on", "Pedal Hi Hat", 0), ("off", "Pedal Hi Hat", 240), ("on", "Pedal Hi Hat", 0), ("off", "Pedal Hi Hat", 240), ("on", "Pedal Hi Hat", 0), ("off", "Pedal Hi Hat", 240), ("on", "Pedal Hi Hat", 0), ("off", "Pedal Hi Hat", 240), ("on", "Pedal Hi Hat", 0), ("off", "Pedal Hi Hat", 240)),

    # Compound duple drum pattern
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 320), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 320), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 320), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 320), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 320), ("off", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 320)),

    # Compound quadruple drum pattern
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("off", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160), ("off", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 160)),

    # Compund triple drum pattern
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 214), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 213), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 213), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 214), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 213), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 213), ("off", "Acoustic Snare", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 214), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 213), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 213), ("off", "Acoustic Snare", 0)),

    # D-beat drum pattern 0
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 549), ("off", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 137), ("off", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 274), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 137), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 274), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 549), ("off", "Closed Hi Hat", 0)),

    # D-beat drum pattern 1
    (("on", "Bass Drum 1", 0), ("on", "Crash Cymbal 1", 0), ("off", "Bass Drum 1", 240), ("on", "Acoustic Snare", 0), ("off", "Crash Cymbal 1", 120), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Crash Cymbal 1", 0), ("off", "Bass Drum 1", 120), ("off", "Crash Cymbal 1", 0), ("on", "Crash Cymbal 1", 120), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 240), ("off", "Crash Cymbal 1", 0), ("on", "Bass Drum 1", 0), ("on", "Crash Cymbal 1", 0), ("off", "Bass Drum 1", 240), ("on", "Acoustic Snare", 0), ("off", "Crash Cymbal 1", 120), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Crash Cymbal 1", 0), ("off", "Bass Drum 1", 120), ("off", "Crash Cymbal 1", 0), ("on", "Crash Cymbal 1", 120), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 240), ("off", "Crash Cymbal 1", 0)),

    # D-beat drum pattern 2a
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 240), ("off", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 240), ("off", "Closed Hi Hat", 0)),

    # D-beat drum pattern 2b
    (("on", "Bass Drum 1", 0), ("on", "Crash Cymbal 1", 0), ("off", "Crash Cymbal 1", 240), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Crash Cymbal 1", 0), ("off", "Acoustic Snare", 120), ("on", "Bass Drum 1", 0), ("off", "Crash Cymbal 1", 120), ("on", "Crash Cymbal 1", 0), ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("off", "Crash Cymbal 1", 0), ("on", "Acoustic Snare", 0), ("on", "Crash Cymbal 1", 0), ("off", "Acoustic Snare", 240), ("off", "Crash Cymbal 1", 0), ("on", "Bass Drum 1", 0), ("on", "Crash Cymbal 1", 0), ("off", "Crash Cymbal 1", 240), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Crash Cymbal 1", 0), ("off", "Acoustic Snare", 120), ("on", "Bass Drum 1", 0), ("off", "Crash Cymbal 1", 120), ("on", "Crash Cymbal 1", 0), ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("off", "Crash Cymbal 1", 0), ("on", "Acoustic Snare", 0), ("on", "Crash Cymbal 1", 0), ("off", "Acoustic Snare", 240), ("off", "Crash Cymbal 1", 0)),

    # D-beat drum pattern 3
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 240), ("off", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 240), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 240), ("off", "Acoustic Snare", 0)),

    # Delayed backbeat
    (("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0), ("on", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Bass Drum 1", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Acoustic Snare", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 60), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 60), ("off", "Bass Drum 1", 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("off", "Closed Hi Hat", 120), ("off", "Acoustic Snare", 0)),

    # Double bass drum beat
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("off", 0x23, 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Closed Hi Hat", 120), ("off", 0x23, 0), ("on", "Acoustic Snare", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Bass Drum 1", 120), ("on", 0x23, 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("off", 0x23, 0)),

    # Double-time rock pattern
    (("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Bass Drum 1", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Bass Drum 1", 120), ("off", "Closed Hi Hat", 0), ("on", "Closed Hi Hat", 0), ("on", "Acoustic Snare", 0), ("off", "Closed Hi Hat", 120), ("on", "Closed Hi Hat", 0), ("off", "Acoustic Snare", 120), ("off", "Closed Hi Hat", 0)),

    # Eighth-note ride pattern with triplet swing
    (("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 320), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 160), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 320), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 160), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 320), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 160), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 320), ("on", "Ride Cymbal 1", 0), ("off", "Ride Cymbal 1", 160))

    # Fill with groove number 2 and crash
    ((0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x24, 120), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x26, 0),
        (0x89, 0x2a, 120), (0x99, 0x2a, 0), (0x89, 0x26, 120), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x24, 120), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x26, 0),
        (0x89, 0x2a, 120), (0x89, 0x26, 0), (0x99, 0x26, 0), (0x89, 0x26, 60),
        (0x99, 0x26, 0), (0x89, 0x26, 60), (0x99, 0x31, 0), (0x99, 0x24, 0),
        (0x89, 0x31, 120), (0x99, 0x2a, 0), (0x89, 0x24, 120), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x99, 0x26, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x26, 120), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x2a, 120), (0x89, 0x24, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x2a, 120), (0x89, 0x24, 0), (0x99, 0x2a, 0), (0x99, 0x26, 0),
        (0x89, 0x2a, 120), (0x99, 0x2a, 0), (0x89, 0x26, 120),
        (0x89, 0x2a, 0)),

    # Fill with groove number 2 and sixteenth notes
    ((0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x24, 120), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x26, 0),
        (0x89, 0x2a, 120), (0x99, 0x2a, 0), (0x89, 0x26, 120), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x24, 120), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x26, 0),
        (0x89, 0x26, 120), (0x89, 0x2a, 0), (0x99, 0x26, 0), (0x89, 0x26, 60),
        (0x99, 0x26, 0), (0x89, 0x26, 60), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x2a, 120), (0x99, 0x2a, 0), (0x89, 0x24, 120), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x99, 0x26, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x26, 120), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x24, 120), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x24, 120), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x26, 0),
        (0x89, 0x2a, 120), (0x99, 0x2a, 0), (0x89, 0x26, 120),
        (0x89, 0x2a, 0)),

    # Four to the floor bass drum pattern
    ((0x99, 0x24, 0), (0x89, 0x24, 480), (0x99, 0x24, 0), (0x89, 0x24, 480),
        (0x99, 0x24, 0), (0x89, 0x24, 480), (0x99, 0x24, 0),
        (0x89, 0x24, 480)),

    # Four to the floor beat
    ((0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 240), (0x99, 0x2a, 0),
        (0x89, 0x24, 240), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x99, 0x26, 0), (0x89, 0x2a, 240), (0x99, 0x2a, 0), (0x89, 0x24, 240),
        (0x89, 0x26, 0), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x2a, 240), (0x99, 0x2a, 0), (0x89, 0x24, 240), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x99, 0x24, 0), (0x99, 0x26, 0), (0x89, 0x2a, 240),
        (0x99, 0x2a, 0), (0x89, 0x24, 240), (0x89, 0x26, 0), (0x89, 0x2a, 0)),

    # Four-four pattern with open and closed hi-hats
    ((0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x2a, 120), (0x99, 0x2e, 0), (0x89, 0x24, 240), (0x89, 0x2e, 0),
        (0x99, 0x2a, 0), (0x99, 0x26, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x2a, 120), (0x99, 0x2e, 0), (0x89, 0x24, 240), (0x89, 0x2e, 0),
        (0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x2a, 120), (0x99, 0x2e, 0), (0x89, 0x24, 240), (0x89, 0x2e, 0),
        (0x99, 0x2a, 0), (0x99, 0x26, 0), (0x89, 0x2a, 120), (0x99, 0x2a, 0),
        (0x89, 0x2a, 120), (0x99, 0x2e, 0), (0x89, 0x24, 240),
        (0x89, 0x2e, 0)),

    # Gallop drum pattern
    ((0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x24, 240), (0x99, 0x24, 0),
        (0x89, 0x24, 120), (0x99, 0x24, 0), (0x89, 0x2a, 120), (0x89, 0x24, 0),
        (0x99, 0x26, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x24, 240),
        (0x99, 0x24, 0), (0x89, 0x24, 120), (0x99, 0x24, 0), (0x89, 0x26, 120),
        (0x89, 0x2a, 0), (0x89, 0x24, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x24, 240), (0x99, 0x24, 0), (0x89, 0x24, 120), (0x99, 0x24, 0),
        (0x89, 0x2a, 120), (0x89, 0x24, 0), (0x99, 0x26, 0), (0x99, 0x2a, 0),
        (0x99, 0x24, 0), (0x89, 0x24, 240), (0x99, 0x24, 0), (0x89, 0x24, 120),
        (0x99, 0x24, 0), (0x89, 0x26, 120), (0x89, 0x2a, 0), (0x89, 0x24, 0)),

    # Ghost note drumming
    ((0x99, 0x2a, 0), (0x99, 0x24, 0), (0x99, 0x26, 116), (0x89, 0x2a, 4),
        (0x99, 0x2a, 112), (0x99, 0x24, 0), (0x89, 0x24, 8), (0x89, 0x26, 0),
        (0x99, 0x26, 225), (0x99, 0x2a, 0), (0x89, 0x2a, 15), (0x89, 0x24, 0),
        (0x89, 0x26, 240), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x2a, 120), (0x99, 0x26, 0), (0x89, 0x24, 120), (0x89, 0x26, 0),
        (0x99, 0x2a, 0), (0x99, 0x24, 0), (0x99, 0x26, 116), (0x89, 0x2a, 4),
        (0x99, 0x2a, 112), (0x99, 0x24, 0), (0x89, 0x24, 8), (0x89, 0x26, 0),
        (0x99, 0x26, 225), (0x99, 0x2a, 0), (0x89, 0x2a, 15), (0x89, 0x24, 0),
        (0x89, 0x26, 240), (0x89, 0x2a, 0), (0x99, 0x2a, 0), (0x99, 0x24, 0),
        (0x89, 0x2a, 120), (0x99, 0x26, 0), (0x89, 0x24, 120),
        (0x89, 0x26, 0)),

    # Half time rock pattern
    ((0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 240), (0x99, 0x2a, 0),
        (0x89, 0x24, 240), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x99, 0x26, 0), (0x89, 0x2a, 240), (0x99, 0x2a, 0),
        (0x89, 0x26, 240), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 120), (0x89, 0x24, 120),
        (0x99, 0x2a, 0), (0x89, 0x2a, 120),
        (0x99, 0x2a, 120), (0x99, 0x26, 0), (0x89, 0x2a, 120),
        (0x89, 0x2a, 120),
        (0x99, 0x2a, 0), (0x89, 0x2a, 120), (0xff01, 120)),

    # Half time shuffle
    ((0x99, 0x2a, 0), (0x99, 0x24, 0), (0x89, 0x2a, 180), (0x99, 0x2a, 180),
        (0x89, 0x24, 180), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x89, 0x2a, 180),
        (0x99, 0x2a, 180), (0x89, 0x2a, 180),
        (0x99, 0x2a, 0), (0x99, 0x26, 0), (0x89, 0x2a, 180), (0x99, 0x2a, 180),
        (0x89, 0x26, 180), (0x89, 0x2a, 0),
        (0x99, 0x2a, 0), (0x89, 0x2a, 180),
        (0x99, 0x2a, 180), (0x89, 0x2a, 180))
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
