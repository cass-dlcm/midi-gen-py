import mido
import random

# 0x24 is Bass Drum 1
# 0x25 is Side Stick
# 0x26 is Acoustic Snare
# 0x2a is Closed Hi Hat
# 0x2c is Pedal Hi Hat
# 0x31 is Crash Cymbal 1
# 0x33 is Ride Cymbal 1
# 0x4b is Claves

# Format: [note event, pitch, time]
drumPatterns = [
# 12-8 equals 4-4 drum pattern
[[0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x24, 160], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x26, 160], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x24, 160], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x26, 160], [0x89, 0x2a, 0]],

# 3 4 popular music rhythm
[[0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x2a, 320], [0x99, 0x2a, 0], [0x89, 0x24, 320], [0x89, 0x2a, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x26, 320], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 320], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x26, 320], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 320]],

# 3-2 rumba clave
[[0x99, 0x4b, 0], [0x89, 0x4b, 240], [0x99, 0x4b, 120], [0x89, 0x4b, 120], [0x99, 0x4b, 360], [0x89, 0x4b, 120], [0x99, 0x4b, 240], [0x89, 0x4b, 240], [0x99, 0x4b, 0], [0x89, 0x4b, 240], [0x89, 0x4b, 240]],

# 6-8 clave
[[0x99, 0x4b, 0], [0x89, 0x4b, 320], [0x99, 0x4b, 0], [0x89, 0x4b, 160], [0x99, 0x4b, 320], [0x89, 0x4b, 160], [0x99, 0x4b, 160], [0x89, 0x4b, 320], [0x99, 0x4b, 0], [0x89, 0x4b, 480]],

# Backbeat pattern snare drum
[[0x99, 0x26, 480], [0x89, 0x26, 240], [0x99, 0x26, 0], [0x89, 0x26, 240], [0x99, 0x26, 480], [0x89, 0x26, 480]],

# Basic drum pattern with 128th note ride
[[0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x99, 0x33, 0], [0x89, 0x33, 15], [0x89, 0x26, 0]],

# Basic drum pattern with 16th note ride
[[0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x89, 0x26, 0]],

# Basic drum pattern with 32nd note ride
[[0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x99, 0x33, 0], [0x89, 0x33, 60], [0x89, 0x26, 0]],

# Basic drum pattern with 64th note ride
[[0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x99, 0x33, 0], [0x89, 0x33, 30], [0x89, 0x26, 0]],

# Basic drum pattern with 8th note ride
[[0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 240], [0x99, 0x33, 0], [0x89, 0x33, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 240], [0x99, 0x33, 0], [0x89, 0x33, 240], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 240], [0x99, 0x33, 0], [0x89, 0x33, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 240], [0x99, 0x33, 0], [0x89, 0x33, 240], [0x89, 0x26, 0]],

# Basic drum pattern with half note ride
[[0x99, 0x33, 0], [0x99, 0x24, 0], [0x89, 0x24, 480], [0x99, 0x26, 0], [0x89, 0x26, 480], [0x89, 0x33, 0], [0x99, 0x33, 0], [0x99, 0x24, 0], [0x89, 0x24, 480], [0x99, 0x26, 0], [0x89, 0x26, 480], [0x89, 0x33, 0]],

# Basic drum pattern with quarter note ride
[[0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 480], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 480], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x33, 480], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x33, 0], [0x89, 0x33, 480], [0x89, 0x26, 0]],

# Basic drum pattern with whole note ride
[[0x99, 0x33, 0], [0x99, 0x24, 0], [0x89, 0x24, 480], [0x99, 0x26, 0], [0x89, 0x26, 480], [0x99, 0x24, 0], [0x89, 0x24, 480], [0x99, 0x26, 0], [0x89, 0x26, 480], [0x89, 0x33, 0]],

# Big four Buddy Bolden
[[0x99, 0x24, 0], [0x89, 0x24, 240], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x24, 0], [0x89, 0x24, 240], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x24, 0], [0x89, 0x24, 240], [0x99, 0x2a, 0], [0x89, 0x2a, 180], [0x99, 0x24, 0], [0x89, 0x24, 60], [0x99, 0x24, 0], [0x89, 0x24, 240], [0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x2a, 0]],

# Blast beat drum pattern 2
[[0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0]],

# Blast beat drum pattern 4
[[0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x24, 120], [0x89, 0x26, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x24, 120], [0x89, 0x26, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x24, 120], [0x89, 0x26, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x24, 120], [0x89, 0x26, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x24, 120], [0x89, 0x26, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x24, 120], [0x89, 0x26, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x24, 120], [0x89, 0x26, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x24, 120], [0x89, 0x26, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0]],

# Blast beat drum pattern most common and simple
[[0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x26, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x26, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x26, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x26, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x26, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x26, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x26, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x26, 0], [0x89, 0x26, 120]],

# Blast beat drum pattern
[[0x99, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x26, 0], [0x89, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x26, 0], [0x89, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x26, 0], [0x89, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x26, 0], [0x89, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x26, 0], [0x89, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x26, 0], [0x89, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x26, 0], [0x89, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x24, 240], [0x89, 0x26, 0], [0x89, 0x2a, 0]],

# Characteristic disco drum pattern
[[0x99, 0x33, 0], [0x99, 0x24, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x33, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x89, 0x26, 0],[0x99, 0x33, 0], [0x99, 0x24, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x99, 0x33, 0], [0x99, 0x24, 0], [0x99, 0x26, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x33, 120], [0x99, 0x33, 0], [0x89, 0x24, 120], [0x89, 0x33, 0], [0x89, 0x26, 0]],

# Characteristic rock drum pattern rimshot
[[0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x2a, 232], [0x89, 0x2a, 8], [0x99, 0x2a, 225], [0x99, 0x25, 0], [0x89, 0x24, 15], [0x89, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x2a, 0], [0x89, 0x25, 240], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x2a, 232], [0x99, 0x24, 0], [0x89, 0x2a, 8], [0x89, 0x24, 0], [0x99, 0x2a, 225], [0x99, 0x25, 0], [0x89, 0x24, 15], [0x89, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x2a, 0], [0x89, 0x25, 240], [0x89, 0x2a, 0]],

# Characteristic rock drum pattern
[[0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x89, 0x26, 0]],

# Characteristic rock hi-hat pattern
[[0x99, 0x2c, 0], [0x89, 0x2c, 240], [0x99, 0x2c, 0], [0x89, 0x2c, 240], [0x99, 0x2c, 0], [0x89, 0x2c, 240], [0x99, 0x2c, 0], [0x89, 0x2c, 240], [0x99, 0x2c, 0], [0x89, 0x2c, 240], [0x99, 0x2c, 0], [0x89, 0x2c, 240], [0x99, 0x2c, 0], [0x89, 0x2c, 240], [0x99, 0x2c, 0], [0x89, 0x2c, 240]],

# Compound duple drum pattern
[[0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 320], [0x99, 0x2a, 0], [0x89, 0x2a, 320], [0x99, 0x2a, 0], [0x89, 0x2a, 320], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 320], [0x99, 0x2a, 0], [0x89, 0x2a, 320], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 320]],

# Compound quadruple drum pattern
[[0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x99, 0x2a, 0], [0x89, 0x2a, 160], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 160]],

# Compund triple drum pattern
[[0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 214], [0x99, 0x2a, 0], [0x89, 0x2a, 213], [0x99, 0x2a, 0], [0x89, 0x2a, 213], [0x89, 0x24, 0],
[0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 214], [0x99, 0x2a, 0], [0x89, 0x2a, 213], [0x99, 0x2a, 0], [0x89, 0x2a, 213], [0x89, 0x26, 0],
[0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 214], [0x99, 0x2a, 0], [0x89, 0x2a, 213], [0x99, 0x2a, 0], [0x89, 0x2a, 213], [0x89, 0x26, 0]],

# D-beat drum pattern 0
[[0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x24, 549], [0x89, 0x2a, 0],
[0x99, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 137], [0x89, 0x26, 0], [0x89, 0x2a, 274], [0x99, 0x2a, 0], [0x89, 0x24, 137], [0x99, 0x24, 0], [0x89, 0x2a, 274], [0x89, 0x24, 0],
[0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x26, 549], [0x89, 0x2a, 0]],

# D-beat drum pattern 1
[[0x99, 0x24, 0], [0x99, 0x31, 0], [0x89, 0x24, 240], [0x99, 0x26, 0], [0x89, 0x31, 120], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x31, 0], [0x89, 0x24, 120], [0x89, 0x31, 0], [0x99, 0x31, 120], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x26, 240], [0x89, 0x31, 0], [0x99, 0x24, 0], [0x99, 0x31, 0], [0x89, 0x24, 240], [0x99, 0x26, 0], [0x89, 0x31, 120], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x31, 0], [0x89, 0x24, 120], [0x89, 0x31, 0], [0x99, 0x31, 120], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x26, 0], [0x89, 0x26, 240], [0x89, 0x31, 0]],

# D-beat drum pattern 2a
[[0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x24, 120], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x89, 0x2a, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x26, 240], [0x89, 0x2a, 0], [0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x24, 120], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x89, 0x2a, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x26, 240], [0x89, 0x2a, 0]],

# D-beat drum pattern 2b
[[0x99, 0x24, 0], [0x99, 0x31, 0], [0x89, 0x31, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x31, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x89, 0x31, 120], [0x99, 0x31, 0], [0x89, 0x24, 120], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x89, 0x31, 0], [0x99, 0x26, 0], [0x99, 0x31, 0], [0x89, 0x26, 240], [0x89, 0x31, 0], [0x99, 0x24, 0], [0x99, 0x31, 0], [0x89, 0x31, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x31, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x89, 0x31, 120], [0x99, 0x31, 0], [0x89, 0x24, 120], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x89, 0x31, 0], [0x99, 0x26, 0], [0x99, 0x31, 0], [0x89, 0x26, 240], [0x89, 0x31, 0]],

# D-beat drum pattern 3
[[0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x99, 0x2a, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x89, 0x24, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 240], [0x89, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x2a, 240], [0x89, 0x24, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x26, 120], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x24, 120], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 240], [0x89, 0x26, 0]],

# Delayed backbeat
[[0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 120], [0x89, 0x24, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x26, 60], [0x99, 0x24, 0], [0x89, 0x2a, 60], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 120], [0x89, 0x24, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x26, 60], [0x99, 0x24, 0], [0x89, 0x2a, 60], [0x99, 0x2a, 0], [0x89, 0x24, 60], [0x99, 0x24, 0], [0x89, 0x2a, 60], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 120], [0x89, 0x24, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x26, 60], [0x99, 0x24, 0], [0x89, 0x2a, 60], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0], [0x99, 0x24, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 120], [0x89, 0x24, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x26, 60], [0x99, 0x24, 0], [0x89, 0x2a, 60], [0x99, 0x2a, 0], [0x89, 0x24, 60], [0x99, 0x24, 0], [0x89, 0x2a, 60], [0x89, 0x24, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x89, 0x2a, 120], [0x89, 0x26, 0]],

# Double bass drum beat
[[0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x23, 0], [0x89, 0x2a, 120], [0x89, 0x23, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x23, 0], [0x89, 0x2a, 120], [0x89, 0x23, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x23, 0], [0x89, 0x26, 120], [0x89, 0x2a, 0], [0x89, 0x23, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x23, 0], [0x89, 0x2a, 120], [0x89, 0x23, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x23, 0], [0x89, 0x2a, 120], [0x89, 0x23, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x23, 0], [0x89, 0x2a, 120], [0x89, 0x23, 0], [0x99, 0x26, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x24, 120], [0x99, 0x23, 0], [0x89, 0x26, 120], [0x89, 0x2a, 0], [0x89, 0x23, 0]],

# Double-time rock pattern
[[0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x24, 120], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x26, 120], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x24, 120], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x26, 120], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x24, 120], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x26, 120], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x24, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x24, 120], [0x89, 0x2a, 0], [0x99, 0x2a, 0], [0x99, 0x26, 0], [0x89, 0x2a, 120], [0x99, 0x2a, 0], [0x89, 0x26, 120], [0x89, 0x2a, 0]],

# Eighth-note ride pattern with triplet swing
[[0x99, 0x33, 0], [0x89, 0x33, 320], [0x99, 0x33, 0], [0x89, 0x33, 160], [0x99, 0x33, 0], [0x89, 0x33, 320], [0x99, 0x33, 0], [0x89, 0x33, 160], [0x99, 0x33, 0], [0x89, 0x33, 320], [0x99, 0x33, 0], [0x89, 0x33, 160], [0x99, 0x33, 0], [0x89, 0x33, 320], [0x99, 0x33, 0], [0x89, 0x33, 160]]
]

def drum(drumTrack):
    pattern = random.choice(drumPatterns)
    for i in pattern:
        if (i[0] == 0x99):
            drumTrack.append(mido.Message('note_on', note=i[1], channel=9, time=i[2]))
        elif (i[0] == 0x89):
            drumTrack.append(mido.Message('note_off', note=i[1], channel=9, time=i[2]))
        else:
            print("whoops")
