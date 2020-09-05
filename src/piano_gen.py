from mido import MidiTrack, Message, MetaMessage
if __name__ == "piano_gen":
    from lights import addValueToHues
else:
    from src.lights import addValueToHues

c_val = 48


def create_piano_track(mid, progressionLength, sequences):
    chordTrack = MidiTrack()
    mid.tracks.append(chordTrack)
    chordTrack.append(Message(
        'program_change',
        program=0,
        time=0))
    for a in range(0, 8):
        for b in range(0, progressionLength):
            addValueToHues(sequences[a][b][0])
            for c in range(0, 4):
                chordTrack.append(Message(
                    'note_on',
                    note=sequences[a][b][c] + c_val,
                    channel=0))
            chordTrack.append(Message(
                'note_on',
                velocity=0,
                note=0,
                channel=0,
                time=1920))
            for c in range(0, 4):
                chordTrack.append(Message(
                    'note_off',
                    note=sequences[a][b][c] + c_val,
                    channel=0))
    chordTrack.append(MetaMessage('end_of_track'))
