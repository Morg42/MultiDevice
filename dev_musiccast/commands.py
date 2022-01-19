#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

""" commands for dev musiccast """

commands = {
    'basic': {
        'power':     {'read': True, 'write': True,  'opcode': ':v1/main/setPower?power={VAL}:', 'item_type': 'bool', 'dev_datatype': 'none', 'lookup': 'power', 'item_attrs': {'enforce': True}},
        'input':     {'read': True, 'write': True,  'opcode': ':v1/main/setInput?input={VAL}:', 'item_type': 'num',  'dev_datatype': 'none', 'item_attrs': {'enforce': True}},
        'mute':      {'read': True, 'write': True,  'opcode': ':v1/main/setMute?enable={VAL}:', 'item_type': 'bool', 'dev_datatype': 'none', 'lookup': 'bool', 'item_attrs': {'enforce': True}},
        'volume':    {'read': True, 'write': True,  'opcode': ':v1/main/setVolume?volume={VAL}:', 'item_type': 'str',  'dev_datatype': 'none', 'item_attrs': {'enforce': True}},
        'status':    {'read': True, 'write': False, 'opcode': 'v1/main/getStatus', 'item_type': 'bool', 'dev_datatype': 'none', 'item_attrs': {'enforce': True}},
        'playinfo':  {'read': True, 'write': False, 'opcode': 'v1/main/getPlayInfo', 'item_type': 'bool', 'dev_datatype': 'none', 'item_attrs': {'enforce': True}},
        'preset':    {'read': True, 'write': True,  'opcode': ':v1/netusb/recallPreset?zone=main&num={VAL}:', 'item_type': 'num', 'dev_datatype': 'none', 'item_attrs': {'enforce': True}},
        'sleep':     {'read': True, 'write': True,  'opcode': ':v1/main/setSleep?sleep={VAL}:', 'item_type': 'num', 'dev_datatype': 'none', 'item_attrs': {'enforce': True}},
        'playback':  {'read': True, 'write': True,  'opcode': ':v1/netusb/setPlayback?playback={VAL}:', 'item_type': 'str', 'dev_datatype': 'none', 'cmd_settings': {'valid_list': ['play', 'stop', 'pause', 'play_pause', 'previous', 'next', 'fast_reverse_start', 'fast_reverse_stop', 'fast_forward_start', 'fast_forward_stop']}, 'item_attrs': {'enforce': True}},
        'passthru':  {'read': True, 'write': True,  'opcode': ':{VAL}:', 'item_type': 'str', 'dev_datatype': 'none', 'item_attrs': {'enforce': True}},
        'track':     {'read': True, 'write': False, 'opcode': '', 'item_type': 'str', 'dev_datatype': 'none'},
        'albumart':  {'read': True, 'write': False, 'opcode': '', 'item_type': 'str', 'dev_datatype': 'none'},
        'artist':    {'read': True, 'write': False, 'opcode': '', 'item_type': 'str', 'dev_datatype': 'none'},
        'curtime':   {'read': True, 'write': False, 'opcode': '', 'item_type': 'num', 'dev_datatype': 'none'},
        'totaltime': {'read': True, 'write': False, 'opcode': '', 'item_type': 'num', 'dev_datatype': 'none'},
    },
    'alarm': {
        'enable':        {'read': True, 'write': True,  'opcode': 'v1/clock/setAlarmSettings', 'item_type': 'bool', 'dev_datatype': 'al_on', 'lookup': 'bool', 'item_attrs': {'enforce': True}},
        'time':      {'read': True, 'write': True,  'opcode': 'v1/clock/setAlarmSettings', 'item_type': 'str',  'dev_datatype': 'al_time', 'item_attrs': {'enforce': True}},
        'beep':      {'read': True, 'write': True,  'opcode': 'v1/clock/setAlarmSettings', 'item_type': 'bool', 'dev_datatype': 'al_beep', 'lookup': 'bool', 'item_attrs': {'enforce': True}},
    }
}

lookups = {
    'bool': {
        'true': True,
        'false': False
    },
    'power': {
        'on': True,
        'standby': False
    }
}
