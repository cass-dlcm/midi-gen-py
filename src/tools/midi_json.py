import sys
import json


def read_header_chunk(out_dict, in_file):
    in_bytes = in_file.read(4)
    if (in_bytes[0] != 77 or in_bytes[1] != 84 or in_bytes[2] != 104 or in_bytes[3] != 100):
        quit()
    in_bytes = in_file.read(4)
    in_bytes = in_file.read(2)
    if (in_bytes[0] != 0 and in_bytes[1] != 1):
        quit()
    out_dict['format'] = 1
    in_bytes = in_file.read(2)
    if (in_bytes[0] == 0 and in_bytes[1] == 0):
        quit()
    out_dict['track_count'] = in_bytes[0] * 256 + in_bytes[1]
    in_bytes = in_file.read(2)
    if (in_bytes[0] == 0 and in_bytes[1] == 0):
        quit()
    out_dict['ticks_per_quarter_note'] = in_bytes[0] * 256 + in_bytes[1]


def read_track(out_dict, in_file, track_num):
    in_bytes = in_file.read(4)
    if (in_bytes[0] != 77 or in_bytes[1] != 84 or in_bytes[2] != 114 or in_bytes[3] != 107):
        quit()
    in_bytes = in_file.read(4)
    end_of_track = False
    most_recent_message = ''
    most_recent_channel = 0
    while (not end_of_track):
        temp_dict = {
            'message': ''
        }
        in_bytes = list(in_file.read(1))
        index = 0
        temp_dict['time'] = in_bytes[0]
        while (in_bytes[index] > 128):
            temp_dict['time'] -= 128
            in_bytes.append(int.from_bytes(in_file.read(1), 'big'))
            temp_dict['time'] *= 128
            index += 1
            temp_dict['time'] += in_bytes[index]
        in_bytes = in_file.read(1)
        if (in_bytes[0] == 0xff):
            temp_dict['message'] = 'meta_message'
            in_bytes = in_file.read(1)
            if (in_bytes[0] == 0x01):
                temp_dict['message'] += ' text'
                len = int.from_bytes(in_file.read(1), 'big')
                temp_dict['text'] = ''
                while (len > 0):
                    temp_dict['text'] += in_file.read(1).decode("utf-8")
                    len -= 1
            elif (in_bytes[0] == 0x02):
                temp_dict['message'] += ' copyright_notice'
                len = int.from_bytes(in_file.read(1), 'big')
                temp_dict['text'] = ''
                while (len > 0):
                    temp_dict['text'] += in_file.read(1).decode("utf-8")
                    len -= 1
            elif (in_bytes[0] == 0x03):
                temp_dict['message'] += ' sequence_name'
                len = int.from_bytes(in_file.read(1), 'big')
                temp_dict['text'] = ''
                while (len > 0):
                    temp_dict['text'] += in_file.read(1).decode("utf-8")
                    len -= 1
            elif (in_bytes[0] == 0x04):
                temp_dict['message'] += ' instrument_name'
                len = int.from_bytes(in_file.read(1), 'big')
                temp_dict['text'] = ''
                while (len > 0):
                    temp_dict['text'] += in_file.read(1).decode("utf-8")
                    len -= 1
            elif (in_bytes[0] == 0x05):
                temp_dict['message'] += ' lyric'
                len = int.from_bytes(in_file.read(1), 'big')
                temp_dict['text'] = ''
                while (len > 0):
                    temp_dict['text'] += in_file.read(1).decode("utf-8")
                    len -= 1
            elif (in_bytes[0] == 0x02):
                temp_dict['message'] += ' marker'
                len = int.from_bytes(in_file.read(1), 'big')
                temp_dict['text'] = ''
                while (len > 0):
                    temp_dict['text'] += in_file.read(1).decode("utf-8")
                    len -= 1
            elif (in_bytes[0] == 0x2f):
                in_file.read(1)
                temp_dict['message'] += ' end_of_track'
                end_of_track = True
            elif (in_bytes[0] == 0x51):
                in_file.read(1)
                in_bytes = in_file.read(3)
                temp_dict['message'] += ' tempo'
                temp_dict['tempo'] = int.from_bytes(in_bytes, 'little')
        elif (in_bytes[0] >= 0x80 and in_bytes[0] <= 0x8f):
            temp_dict['message'] = 'note_off'
            temp_dict['channel'] = in_bytes[0] - 0x80
            most_recent_channel = in_bytes[0] - 0x80
            temp_dict['pitch'] = int.from_bytes(in_file.read(1), 'big')
            temp_dict['velocity'] = int.from_bytes(in_file.read(1), 'big')
        elif (in_bytes[0] >= 0x90 and in_bytes[0] <= 0x9f):
            temp_dict['message'] = 'note_on'
            temp_dict['channel'] = in_bytes[0] - 0x90
            most_recent_channel = in_bytes[0] - 0x90
            temp_dict['pitch'] = int.from_bytes(in_file.read(1), 'big')
            temp_dict['velocity'] = int.from_bytes(in_file.read(1), 'big')
        elif (in_bytes[0] >= 0xc0 and in_bytes[0] <= 0xcf):
            temp_dict['message'] = 'program change'
            temp_dict['channel'] = in_bytes[0] - 0xc0
            temp_dict['patch'] = int.from_bytes(in_file.read(1), 'big')
        elif (in_bytes[0] == 0):
            pass
        elif (most_recent_message == 'note_off'):
            temp_dict['message'] = 'note_off'
            temp_dict['channel'] = most_recent_channel
            temp_dict['pitch'] = in_bytes[0]
            temp_dict['velocity'] = int.from_bytes(in_file.read(1), 'big')
        elif (most_recent_message == 'note_on'):
            temp_dict['message'] = 'note_on'
            temp_dict['channel'] = most_recent_channel
            temp_dict['pitch'] = in_bytes[0]
            temp_dict['velocity'] = int.from_bytes(in_file.read(1), 'big')
        out_dict['tracks'][track_num].append(temp_dict)
        most_recent_message = temp_dict['message']


for index in range(1, len(sys.argv)):
    in_file = open(sys.argv[index], 'rb')
    out_file = open(sys.argv[index] + '.json', 'w')
    out_dict = {}
    read_header_chunk(out_dict, in_file)
    out_dict['tracks'] = []
    out_dict['tracks'].append([])
    read_track(out_dict, in_file, 0)
    out_dict['tracks'].append([])
    read_track(out_dict, in_file, 1)
    out_dict['tracks'].append([])
    read_track(out_dict, in_file, 2)
    out_dict['tracks'].append([])
    read_track(out_dict, in_file, 3)
    json.dump(out_dict, out_file, indent=4)
