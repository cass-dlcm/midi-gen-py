from src.main import main
from glob import glob
import os
from filecmp import cmp
from time import sleep


def test_main():
    main()
    list_of_files = glob('output/*.mid')
    file_a = max(list_of_files, key=os.path.getctime)
    sleep(1)
    main()
    list_of_files = glob('output/*.mid')
    file_b = max(list_of_files, key=os.path.getctime)
    assert not(cmp(file_a, file_b, shallow=False))
