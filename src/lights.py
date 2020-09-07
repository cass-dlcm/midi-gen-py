from json import load
from os import system, mkdir
from time import sleep
from typing import TextIO, List

with open('arduino_config.json') as json_file:
    config = load(json_file)

hues: List[int] = []


def addValueToHues(value: int):
    hues.append(value)


def writeToFile(timestamp: str, bpm: int, progressionLength: int):
    d = 800000 / 24 / config['LED_COUNT'] / (bpm / 240) * .9
    arduinoStr: str = '#include <Adafruit_NeoPixel.h>\n#define LED_PIN    '
    arduinoStr += str(config['LED_PIN'])
    arduinoStr += '\n#define LED_COUNT '
    arduinoStr += str(config['LED_COUNT'])
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
    arduinoStr += str(progressionLength * 8)
    arduinoStr += ') {\n    strip.fill(strip.ColorHSV(getColor()));\n  }\n  b+'
    arduinoStr += '+;\n  strip.show();\n  if (b == '
    arduinoStr += str(int(d))
    arduinoStr += ') {\n    a++;\n    b = 0;\n  }\n}'
    try:
        mkdir('output\\' + timestamp)
    except FileExistsError:
        pass
    file_name: str = 'output\\' + timestamp + '\\' + timestamp + '.ino'
    ardFile: TextIO = open(file_name, 'w')
    ardFile.write(arduinoStr)
    ardFile.close()
    if config['execute'] and __name__ == "lights":
        exe_path: str = config['path_to_ide']
        main_flag: str = ' --upload -v'
        board_flag: str = ' --board ' + config['board']
        port_flag: str = ' --port ' + config['port']
        system(exe_path + main_flag + board_flag + port_flag + ' ' + file_name)
        sleep(11)
