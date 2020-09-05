import glob
from src.drum_gen import readDrumPatterns, filterDrumPatterns, drum, getDrumPatterns
from mido import MidiTrack, MetaMessage, MidiFile
from filecmp import cmp


def test_drums():
    file_list = glob.glob("data/drum_patterns/*.json")
    for i in range(0, len(file_list)):
        mid = MidiFile()
        readDrumPatterns()
        filterDrumPatterns([i])
        drumTrack = MidiTrack()
        drum(drumTrack)
        drumTrack.append(MetaMessage('end_of_track'))
        mid.tracks.append(drumTrack)
        mid.save('tests/output/drums/' + getDrumPatterns()[0]['name'] + '.mid')
        assert cmp('tests/output/drums/' + getDrumPatterns()[0]['name'] + '.mid', 'tests/data/drums/' + getDrumPatterns()[0]['name'] + '.mid', shallow=False)


test_drums()
