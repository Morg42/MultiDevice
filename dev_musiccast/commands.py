#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

""" commands for dev musiccast """

commands = {
    'special': {
        # special?
        'wakeup':    {'read': True, 'write': True,  'opcode': '', 'reply_token': '', 'item_type': 'bool', 'dev_datatype': 'raw', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
    }, 
    'basic': {
        'power':     {'read': True, 'write': True,  'opcode': ':v1/MD_PARAM:zone:/setPower?power=VAL:', 'reply_token': '', 'item_type': 'bool', 'dev_datatype': 'none', 'lookup': 'power', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'input':     {'read': True, 'write': True,  'opcode': ':v1/MD_PARAM:zone:/setInput?input=VAL:', 'reply_token': '', 'item_type': 'num',  'dev_datatype': 'none', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'mute':      {'read': True, 'write': True,  'opcode': ':v1/MD_PARAM:zone:/setMute?enable=VAL:', 'reply_token': '', 'item_type': 'bool', 'dev_datatype': 'none', 'lookup': 'bool', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True},
        'volume':    {'read': True, 'write': True,  'opcode': ':v1/MD_PARAM:zone:/setVolume?volume=VAL:', 'reply_token': '', 'item_type': 'str',  'dev_datatype': 'none', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'status':    {'read': True, 'write': False, 'opcode': 'v1/MD_PARAM:zone:/getStatus', 'reply_token': '', 'item_type': 'bool', 'dev_datatype': 'none', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'playinfo':  {'read': True, 'write': False, 'opcode': 'v1/MD_PARAM:zone:/getPlayInfo', 'reply_token': '', 'item_type': 'bool', 'dev_datatype': 'none', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'preset':    {'read': True, 'write': True,  'opcode': ':v1/MD_PARAM:source:/recallPreset?zone=MD_PARAM:zone:&num=VAL:', 'reply_token': '', 'item_type': 'num', 'dev_datatype': 'none', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'sleep':     {'read': True, 'write': True,  'opcode': ':v1/MD_PARAM:zone:/setSleep?sleep=VAL:', 'reply_token': '', 'item_type': 'num', 'dev_datatype': 'none', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'playback':  {'read': True, 'write': True,  'opcode': ':v1/MD_PARAM:source:/setPlayback?playback=VAL:', 'reply_token': '', 'item_type': 'str', 'dev_datatype': 'none', 'lookup': 'playback', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'passthru':  {'read': True, 'write': True,  'opcode': ':VAL:', 'reply_token': '', 'item_type': 'str', 'dev_datatype': 'none', 'params': [], 'param_values': [], 'item_attrs': {'enforce': True}},
        'track':     {'read': True, 'write': False, 'opcode': '', 'reply_token': '', 'item_type': 'str', 'dev_datatype': 'none', 'params': [], 'param_values': []},
        'albumart':  {'read': True, 'write': False, 'opcode': '', 'reply_token': '', 'item_type': 'str', 'dev_datatype': 'none', 'params': [], 'param_values': []},
        'artist':    {'read': True, 'write': False, 'opcode': '', 'reply_token': '', 'item_type': 'str', 'dev_datatype': 'none', 'params': [], 'param_values': []},
        'curtime':   {'read': True, 'write': False, 'opcode': '', 'reply_token': '', 'item_type': 'num', 'dev_datatype': 'none', 'params': [], 'param_values': []},
        'totaltime': {'read': True, 'write': False, 'opcode': '', 'reply_token': '', 'item_type': 'num', 'dev_datatype': 'none', 'params': [], 'param_values': []},
    },
    'alarm': {
        'on':        {'read': True, 'write': True,  'opcode': 'v1/clock/setAlarmSettings', 'reply_token': '', 'item_type': 'bool', 'dev_datatype': 'al_on', 'lookup': 'bool', 'item_attrs': {'enforce': True}},
        'time':      {'read': True, 'write': True,  'opcode': 'v1/clock/setAlarmSettings', 'reply_token': '', 'item_type': 'str',  'dev_datatype': 'al_time', 'item_attrs': {'enforce': True}},
        'beep':      {'read': True, 'write': True,  'opcode': 'v1/clock/setAlarmSettings', 'reply_token': '', 'item_type': 'bool', 'dev_datatype': 'al_beep', 'lookup': 'bool', 'item_attrs': {'enforce': True}},
    }
}
