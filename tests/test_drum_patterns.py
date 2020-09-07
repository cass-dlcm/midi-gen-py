import glob
from src.drum_gen import read_patterns, filterDrumPatterns, drum
from src.drum_gen import get_patterns
from src.main import create_simple_meta_track
from mido import MidiTrack, MetaMessage, MidiFile
from filecmp import cmp
from os import mkdir
from typing import List


def test_drums():
    file_list: List[str] = glob.glob("data/drum_patterns/*.json")
    for i in range(0, len(file_list)):
        mid: MidiFile = MidiFile()
        create_simple_meta_track(mid)
        read_patterns()
        filterDrumPatterns([i])
        drumTrack: MidiTrack = MidiTrack()
        drumTrack.append(MetaMessage('instrument_name', name='Drum set'))
        drum(drumTrack)
        drumTrack.append(MetaMessage('end_of_track'))
        mid.tracks.append(drumTrack)
        try:
            mkdir("tests/output")
            print("Created tests/output directory.")
        except FileExistsError:
            pass
        try:
            mkdir("tests/output/drums")
            print("Created tests/output/drums directory.")
        except FileExistsError:
            pass
        file_name: str = get_patterns()[0]['name'] + '.mid'
        mid.save('tests/output/drums/' + file_name)
        assert abs(mid.length - 2) < .001
        assert cmp('tests/output/drums/' + file_name,
                   'tests/data/drums/' + file_name, shallow=False)
