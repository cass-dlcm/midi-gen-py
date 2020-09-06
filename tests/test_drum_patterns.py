import glob
from src.drum_gen import readDrumPatterns, filterDrumPatterns, drum, getDrumPatterns
from src.main import create_simple_meta_track
from mido import MidiTrack, MetaMessage, MidiFile
from filecmp import cmp
from os import mkdir


def test_drums():
    file_list = glob.glob("data/drum_patterns/*.json")
    for i in range(0, len(file_list)):
        mid = MidiFile()
        create_simple_meta_track(mid)
        readDrumPatterns()
        filterDrumPatterns([i])
        drumTrack = MidiTrack()
        drumTrack.append(MetaMessage('instrument_name', name='Drum set'))
        drum(drumTrack)
        drumTrack.append(MetaMessage('end_of_track'))
        mid.tracks.append(drumTrack)
        try:
            mkdir("tests/output")
            print("Created output directory.")
        except FileExistsError:
            pass
        try:
            mkdir("tests/output/drums")
            print("Created output directory.")
        except FileExistsError:
            pass
        mid.save('tests/output/drums/' + getDrumPatterns()[0]['name'] + '.mid')
        print(getDrumPatterns()[0]['name'])
        assert abs(mid.length - 2) < .001
        assert cmp('tests/output/drums/' + getDrumPatterns()[0]['name'] + '.mid', 'tests/data/drums/' + getDrumPatterns()[0]['name'] + '.mid', shallow=False)
