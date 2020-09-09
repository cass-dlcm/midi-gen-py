from mido import MidiTrack, Message, MetaMessage, MidiFile
from typing import Dict
if __name__ == "piano_gen":
    from lights import addValueToHues
else:
    from src.lights import addValueToHues

C_VAL: int = 48


def create_piano_track(mid: MidiFile, progressionLength: int, sequences: Dict[str, list], ticks_per_beat: int):
    chordTrack: MidiTrack = MidiTrack()
    mid.tracks.append(chordTrack)
    chordTrack.append(MetaMessage('instrument_name', name='Piano'))
    chordTrack.append(Message(
        'program_change',
        program=0,
        time=0))
    for a in range(0, 8):
        for b in range(0, progressionLength):
            addValueToHues(sequences['values'][a][b][0])
            chordTrack.append(MetaMessage(
                'text', text=sequences['strings'][a * progressionLength + b]))
            for c in range(0, 4):
                chordTrack.append(Message(
                    'note_on',
                    note=sequences['values'][a][b][c] + C_VAL,
                    channel=0))
            chordTrack.append(Message(
                'note_on',
                velocity=0,
                note=0,
                channel=0,
                time=int(ticks_per_beat * 4)))
            for c in range(0, 4):
                chordTrack.append(Message(
                    'note_off',
                    note=sequences['values'][a][b][c] + C_VAL,
                    channel=0))
    chordTrack.append(MetaMessage('end_of_track'))
