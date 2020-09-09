from json import load
from os import system, mkdir
from time import sleep
from typing import TextIO, List, Dict, Union, cast

config: Dict[str, Union[str, int]] = {}


def load_config(file_loc: str):
    global config
    with open(file_loc) as json_file:
        config = load(json_file)


hues: List[int] = []


def add_value_to_hues(value: int):
    """Adds values passed in to the array of hues emitted

    :param value: The hue value to add
    :type value: int
    """
    hues.append(value)


def write_file(timestamp: str, bpm: int, progressionLength: int, segments: int):
    """Writes Ardiuno program to file and optionally executes it

    :param timestamp: A timestamp, formatted as '%Y-%m-%d_%H_%M_%S'
    :type timestamp: str
    :param bpm: The beats per minute of the song
    :type bpm: int
    :param progression_length: The number of chords in a single sequence
    :type progression_length: int
    :param segments: The number of sequences
    :type segments: int
    """
    d = 800000 / 24 / cast(int, config['LED_COUNT']) / (bpm / 240) * .9
    arduinoStr: str = '#include <Adafruit_NeoPixel.h>\n#define LED_PIN    '
    arduinoStr += str(cast(int, config['LED_PIN']))
    arduinoStr += '\n#define LED_COUNT '
    arduinoStr += str(cast(int, config['LED_COUNT']))
    arduinoStr += '\nAdafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO'
    arduinoStr += '_KHZ800);\nint a = 0;\nint b = 0;\nconst int hues[] = {'
    for i in range(0, len(hues) - 1):
        arduinoStr += str(hues[i]) + ', '
    arduinoStr += str(hues[len(hues) - 1])
    arduinoStr += '};\nvoid setup() {\n  strip.begin();\n  strip.show();\n}\ni'
    arduinoStr += 'nt getColor() {\n  return (int)(65536.0 * ((hues[a] * ('
    arduinoStr += str(int(d))
    arduinoStr += ' - b)) * '
    arduinoStr += str(float.hex(1 / int(d)))
    arduinoStr += ' + (hues[a + 1] * b) * '
    arduinoStr += str(float.hex(1 / int(d)))
    arduinoStr += ') * 0.0833333333333333);\n}\nvoid loop() {\n  if (a < '
    arduinoStr += str(progressionLength * segments)
    arduinoStr += ') {\n    strip.fill(strip.ColorHSV(getColor()));\n  }\n  b+'
    arduinoStr += '+;\n  strip.show();\n  if (b == '
    arduinoStr += str(int(d))
    arduinoStr += ') {\n    a++;\n    b = 0;\n  }\n}'
    try:
        mkdir('output/' + timestamp)
    except FileExistsError:
        pass
    file_name: str = 'output/' + timestamp + '/' + timestamp + '.ino'
    ardFile: TextIO = open(file_name, 'w')
    ardFile.write(arduinoStr)
    ardFile.close()
    if config['execute'] and __name__ == "lights":
        exe_path: str = cast(str, config['path_to_ide'])
        main_flag: str = ' --upload -v'
        board_flag: str = ' --board ' + cast(str, config['board'])
        port_flag: str = ' --port ' + cast(str, config['port'])
        system(exe_path + main_flag + board_flag + port_flag + ' ' + file_name)
        sleep(11)
