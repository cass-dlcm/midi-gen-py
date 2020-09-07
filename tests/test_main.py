from src.main import main
from glob import glob
import os
from filecmp import cmp
from time import sleep
from typing import List


def test_main():
    main()
    list_of_files: List[str] = glob('output/*.mid')
    file_a: str = max(list_of_files, key=os.path.getctime)
    sleep(1)
    main()
    list_of_files: List[str] = glob('output/*.mid')
    file_b: str = max(list_of_files, key=os.path.getctime)
    assert not(cmp(file_a, file_b, shallow=False))
