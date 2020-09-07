import glob
from src.guitar_gen import read_guitar_patterns, filter_guitar_patterns, guitar, get_guitar_patterns
from mido import MidiTrack, MetaMessage, MidiFile, Message
from filecmp import cmp
from src.main import simple_pick_chords, simple_chord_order, create_simple_meta_track
from os import mkdir


def test_guitar():
    file_list = glob.glob("data/guitar_patterns/*.json")
    for i in range(0, len(file_list)):
        progression_length = 4
        mid = MidiFile()
        create_simple_meta_track(mid)
        read_guitar_patterns()
        filter_guitar_patterns([i])
        guitar_track = MidiTrack()
        guitar_track.append(MetaMessage('instrument_name', name='Guitar'))
        sequences = simple_chord_order(simple_pick_chords(progression_length))
        guitar_track.append(Message(
            'program_change',
            program=25,
            channel=1,
            time=0))
        guitar(guitar_track, progression_length, sequences['values'], 1)
        guitar_track.append(MetaMessage('end_of_track'))
        mid.tracks.append(guitar_track)
        try:
            mkdir("tests/output")
            print("Created output directory.")
        except FileExistsError:
            pass
        try:
            mkdir("tests/output/guitar")
            print("Created output directory.")
        except FileExistsError:
            pass
        mid.save('tests/output/guitar/' + get_guitar_patterns()[0]['name'] + '.mid')
        print(get_guitar_patterns()[0]['name'])
        assert abs(mid.length - 8) < .001
        assert cmp('tests/output/guitar/' + get_guitar_patterns()[0]['name'] + '.mid', 'tests/data/guitar/' + get_guitar_patterns()[0]['name'] + '.mid', shallow=False)
