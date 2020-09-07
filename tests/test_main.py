from src.main import main, randomize_chord_order, pick_chords
from glob import glob
import os
from filecmp import cmp
from time import sleep
from typing import List, Dict, Union


def test_individuality():
    main()
    list_of_files: List[str] = glob('output/*.mid')
    file_a: str = max(list_of_files, key=os.path.getctime)
    sleep(1)
    main()
    list_of_files: List[str] = glob('output/*.mid')
    file_b: str = max(list_of_files, key=os.path.getctime)
    assert not(cmp(file_a, file_b, shallow=False))


def test_type_sequences():
    sequences: Dict[str, Union[List[List[List[int]]], List[str]]] = randomize_chord_order(pick_chords(4))
    assert isinstance(sequences, dict)
    assert 'values' in sequences
    assert isinstance(sequences['values'], list)
    for a in sequences['values']:
        assert isinstance(a, list)
        for b in a:
            assert isinstance(b, list)
            for c in b:
                assert isinstance(c, int)
                assert c >= 0
    assert 'strings' in sequences
    assert isinstance(sequences['strings'], list)
    for a in sequences['strings']:
        assert isinstance(a, str)
        assert len(a) > 0
