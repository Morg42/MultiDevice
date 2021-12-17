#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev pioneer

commands = {
    'error': {
        'opcode': '',
        'read': True,
        'item_type': 'str',
        'dev_datatype': 'PioError',
        'reply_token': ['E0', 'E02', 'E04']
    },
    'title': {
        'opcode': '',
        'read': True,
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': ['GEH01020']
    },
    'genre': {
        'opcode': '$V',
        'read': True,
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': ['GEH05024']
    },
    'station': {
        'opcode': '',
        'read': True,
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': ['GEH04022']
    },
    'display': {
        'opcode': '',
        'read': True,
        'read_cmd': '?FL',
        'item_type': 'str',
        'dev_datatype': 'PioDisplay',
        'reply_token': ['FL']
    },
    'tone': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?TO',
        'item_type': 'bool',
        'dev_datatype': 'PioTone',
        'reply_token': ['TO']
    },
    'treble': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?TR',
        'item_type': 'num',
        'dev_datatype': 'PioTreble',
        'reply_token': ['TR']
    },
    'trebleup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'TI',
        'dev_datatype': 'raw'
    },
    'trebledown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'TD',
        'dev_datatype': 'raw'
    },
    'bass': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?BA',
        'item_type': 'num',
        'dev_datatype': 'PioBass',
        'reply_token': ['BA']
    },
    'bassup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'BI',
        'dev_datatype': 'raw'
    },
    'bassdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'BD',
        'dev_datatype': 'raw'
    },
    'tunerpreset': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?PR',
        'item_type': 'num',
        'dev_datatype': 'PioTunerpreset',
        'reply_token': ['PR']
    },
    'tunerpresetup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'TPI',
        'dev_datatype': 'raw'
    },
    'tunerpresetdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'TPD',
        'dev_datatype': 'raw'
    },
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
        'write_cmd': ':{VAL:03}VL:',
        'item_type': 'num',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'VOL(\d{3})'
    },
    'zone1_volumeup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'VU',
        'dev_datatype': 'raw'
    },
    'zone1_volumedown': {
        'write_cmd': 'VD',
        'write': True,
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone1_source': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?F',
        'item_type': 'str',
        'dev_datatype': 'PioSource',
        'reply_token': ['FN']
    },
    'zone1_sourceup': {
        'write_cmd': 'FU',
        'write': True,
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone1_sourcedown': {
        'write_cmd': 'FD',
        'write': True,
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone1_listeningmode': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?S',
        'item_type': 'num',
        'dev_datatype': 'PioListening',
        'reply_token': ['SR']
    },
    'zone1_playingmode': {
        'opcode': '$V',
        'read': True,
        'write': False,
        'read_cmd': '?L',
        'item_type': 'str',
        'dev_datatype': 'PioPlayingmode',
        'reply_token': ['LM']
    },
    'zone1_speakers': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?SPK',
        'item_type': 'num',
        'dev_datatype': 'PioSpeakers',
        'reply_token': ['SPK']
    },
    'zone2_power': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?AP',
        'item_type': 'bool',
        'dev_datatype': 'PioPwr2',
        'reply_token': ['APR']
    },
    'zone2_mute': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?Z2M',
        'item_type': 'bool',
        'dev_datatype': 'PioMute2',
        'reply_token': ['Z2MUT']
    },
    'zone2_volume': {
        'opcode': "$V",
        'read': True,
        'write': True,
        'read_cmd': '?ZV',
        'write_cmd': ':{VAL:02}ZV:',
        'item_type': 'num',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'ZV(\d{2})'
    },
    'zone2_volumeup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'ZU',
        'dev_datatype': 'raw'
    },
    'zone2_volumedown': {
        'write_cmd': 'ZD',
        'write': True,
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone2_source': {
        'opcode': '$V',
        'read': True,
        'write': True,
        'read_cmd': '?ZS',
        'item_type': 'str',
        'dev_datatype': 'PioSource2',
        'reply_token': ['Z2F']
    },
    'zone2_sourceup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'ZSFU',
        'dev_datatype': 'raw'
    },
    'zone2_sourcedown': {
        'write_cmd': 'ZSFD',
        'write': True,
        'item_type': 'bool',
        'dev_datatype': 'raw'
    }
}
