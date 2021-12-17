#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev pioneer

commands = {
    'zone1_power': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?P',
        'item_type': 'bool',
        'dev_datatype': 'PioPwr',
        'reply_token': ['PWR']
    },
    'zone1_mute': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?M',
        'item_type': 'bool',
        'dev_datatype': 'PioMute',
        'reply_token': ['MUT']
    },
    'zone1_volume': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?V',
        'item_type': 'num',
        'dev_datatype': 'PioVol',
        'reply_token': ['VOL']
    },
    'zone1_volume+': {
        'write': True,
        'write_cmd': 'VU',
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone1_volume-': {
        'write': True,
        'write_cmd': 'VD',
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone1_source': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?F',
        'item_type': 'num',
        'dev_datatype': 'PioSource',
        'reply_token': ['FN']
    }
}
