import glob
from src.guitar_gen import read_guitar_patterns, filter_guitar_patterns, guitar, get_guitar_patterns
from mido import MidiTrack, MetaMessage, MidiFile, Message
from filecmp import cmp
from src.main import simple_pick_chords, simple_chord_order, progression_length, get_sequence


def test_guitar():
    file_list = glob.glob("data/guitar_patterns/*.json")
    for i in range(0, len(file_list)):
        mid = MidiFile()
        read_guitar_patterns()
        filter_guitar_patterns([i])
        guitar_track = MidiTrack()
        simple_pick_chords()
        simple_chord_order()
        guitar_track.append(Message(
            'program_change',
            program=25,
            channel=1,
            time=0))
        guitar(guitar_track, progression_length, get_sequence(), 1)
        guitar_track.append(MetaMessage('end_of_track'))
        mid.tracks.append(guitar_track)
        mid.save('tests\\output\\guitar\\' + get_guitar_patterns()[0]['name'] + '.mid')
        assert cmp('tests\\output\\guitar\\' + get_guitar_patterns()[0]['name'] + '.mid', 'tests\\data\\guitar\\' + get_guitar_patterns()[0]['name'] + '.mid', shallow=False)


test_guitar()
