# This file is part of midi-gen-py.
# midi-gen-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# midi-gen-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with midi-gen-py.  If not, see <https://www.gnu.org/licenses/>.

from mido import MidiTrack, Message, MetaMessage
from typing import Dict, List, Union, cast
if __name__ == "piano_gen":
    from lights import add_value_to_hues
else:
    from src.lights import add_value_to_hues

C_VAL: int = 48


def create_track(progression_length: int, sequences: Dict[str, Union[List[str], List[List[List[int]]]]], ticks_per_beat: int) -> MidiTrack:
    """Generates a track of piano chords

    :param progression_length: How long an individual chord progression is
    :type progression_length: int
    :param sequences: A dictionary containing chord values and names
    :type sequences: Dict[str, Union[List[str], List[List[List[int]]]]]
    :param ticks_per_beat: The amount of ticks in a quarter note for the file
    :type int:
    :return: The created track
    :rtype: mido.MidiTrack
    """
    track: MidiTrack = MidiTrack()
    track.append(MetaMessage('instrument_name', name='Piano'))
    track.append(Message(
        'program_change',
        program=0,
        time=0))
    for a in range(0, 8):
        for b in range(0, progression_length):
            add_value_to_hues(sequences['values'][a][b][0])
            track.append(MetaMessage(
                'text', text=sequences['strings'][a * progression_length + b]))
            for c in range(0, 4):
                track.append(Message(
                    'note_on',
                    note=cast(int, sequences['values'][a][b][c]) + C_VAL,
                    channel=0))
            track.append(Message(
                'note_off',
                note=cast(int, sequences['values'][a][b][c]) + C_VAL,
                channel=0,
                time=int(ticks_per_beat * 4)))
            for c in range(1, 4):
                track.append(Message(
                    'note_off',
                    note=cast(int, sequences['values'][a][b][c]) + C_VAL,
                    channel=0))
    track.append(MetaMessage('end_of_track'))
    return track
