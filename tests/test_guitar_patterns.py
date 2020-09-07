import glob
from src.guitar_gen import read_patterns, filter_patterns, guitar, get_patterns
from mido import MidiTrack, MetaMessage, MidiFile, Message
from filecmp import cmp
from src.main import simple_pick_chords, simple_chord_order
from src.main import create_simple_meta_track
from os import mkdir
from typing import List, Dict


def test_guitar():
    file_list: List[str] = glob.glob("data/guitar_patterns/*.json")
    for i in range(0, len(file_list)):
        progression_length: int = 4
        mid: MidiFile = MidiFile()
        create_simple_meta_track(mid)
        read_patterns()
        filter_patterns([i])
        guitar_track: MidiTrack = MidiTrack()
        guitar_track.append(MetaMessage('instrument_name', name='Guitar'))
        sequences: Dict[str, list] = simple_chord_order(simple_pick_chords(
            progression_length))
        guitar_track.append(Message('program_change', program=25, channel=1,
                                    time=0))
        guitar(guitar_track, progression_length, sequences['values'], 1)
        guitar_track.append(MetaMessage('end_of_track'))
        mid.tracks.append(guitar_track)
        try:
            mkdir("tests/output")
            print("Created tests/output directory.")
        except FileExistsError:
            pass
        try:
            mkdir("tests/output/guitar")
            print("Created tests/output/guitar directory.")
        except FileExistsError:
            pass
        file_name: str = get_patterns()[0]['name'] + '.mid'
        mid.save('tests/output/guitar/' + file_name)
        assert abs(mid.length - 8) < .001
        assert cmp('tests/output/guitar/' + file_name,
                   'tests/data/guitar/' + file_name, shallow=False)
