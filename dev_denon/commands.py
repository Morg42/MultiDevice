#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev pioneer

commands = {
    'title': {
        'opcode': 'MD_VALUE',
        'read': True,
        'read_cmd': 'NSE',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'NSE1(.*)'
    },
    'album': {
        'opcode': 'MD_VALUE',
        'read': True,
        'read_cmd': 'NSE',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'NSE4(.*)'
    },
    'artist': {
        'opcode': 'MD_VALUE',
        'read': True,
        'read_cmd': 'NSE',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'NSE2(.*)'
    },
    'display': {
        'opcode': 'MD_VALUE',
        'read': True,
        'read_cmd': 'NSE',
        'item_type': 'str',
        'dev_datatype': 'DenonDisplay',
        'reply_token': 'REGEX',
        'reply_pattern': r'NSE(.*)'
    },
    'dialog': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSDIL ?',
        'write_cmd': ':PSDIL {VAL}:',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSDIL (ON|OFF)'
    },
    'tone': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSTONE CTRL ?',
        'write_cmd': ':PSTONE CTRL {VAL}:',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSTONE CTRL (ON|OFF)'
    },
    'treble': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSTRE ?',
        'item_type': 'num',
        'settings': {
                    'force_min': 44,
                    'force_max': 56
                    },
        'write_cmd': ':PSTRE {VAL}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSTRE (\d{2})'
    },
    'trebleup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSTRE UP',
        'dev_datatype': 'raw'
    },
    'trebledown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSTRE DOWN',
        'dev_datatype': 'raw'
    },
    'bass': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSBAS ?',
        'item_type': 'num',
        'settings': {
                    'force_min': 44,
                    'force_max': 56
                    },
        'write_cmd': ':PSBAS {VAL}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSBAS (\d{2})'
    },
    'bassup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSBAS UP',
        'dev_datatype': 'raw'
    },
    'bassdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSBAS DOWN',
        'dev_datatype': 'raw'
    },
    'level_front_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?L__CLV',
        'item_type': 'num',
        'write_cmd': ':L__{VAL:02}CLV:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'CLVL__(\d{2})'
    },
    'level_front_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?R__CLV',
        'item_type': 'num',
        'write_cmd': ':R__{VAL:02}CLV:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'CLVR__(\d{2})'
    },
    'level_front_center': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?C__CLV',
        'item_type': 'num',
        'write_cmd': ':C__{VAL:02}CLV:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'CLVC__(\d{2})'
    },
    'level_surround_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?SL_CLV',
        'item_type': 'num',
        'write_cmd': ':SL_{VAL:02}CLV:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'CLVSL_(\d{2})'
    },
    'level_surround_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?SR_CLV',
        'item_type': 'num',
        'write_cmd': ':SR_{VAL:02}CLV:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'CLVSR_(\d{2})'
    },
    'level_subwoofer': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?SW_CLV',
        'item_type': 'num',
        'write_cmd': ':SW_{VAL:02}CLV:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'CLVSW_(\d{2})'
    },
    'tunerpreset': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?PR',
        'item_type': 'num',
        'write_cmd': ':{VAL}PR:',
        'item_type': 'num',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'PR([A-Ga-g]\d{2})'
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
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PW?',
        'item_type': 'bool',
        'dev_datatype': 'DenonPwr',
        'reply_token': 'REGEX',
        'reply_pattern': r'PW(ON|STANDBY)'
    },
    'zone1_mute': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'MU?',
        'write_cmd': ':MU{VAL}:',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'MU(ON|OFF)'
    },
    'zone1_volume': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'MV?',
        'item_type': 'num',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'MV(\d{2,3})',
        'settings': {
                    'max': 98,
                    'force_min': 0
                    }
    },
    'zone1_volumeup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'MVUP',
        'dev_datatype': 'raw'
    },
    'zone1_volumedown': {
        'write_cmd': 'MVDOWN',
        'write': True,
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone1_source': {
        'opcode': 'MD_VALUE',
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
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?S',
        'item_type': 'num',
        'dev_datatype': 'PioListening',
        'reply_token': ['SR']
    },
    'zone1_playingmode': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': False,
        'read_cmd': '?L',
        'item_type': 'str',
        'dev_datatype': 'PioPlayingmode',
        'reply_token': ['LM']
    },
    'zone1_speakers': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list': [0, 1, 2, 3, 9]},
        'write_cmd': ':{VAL:01}SPK:',
        'read_cmd': '?SPK',
        'item_type': 'num',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'SPK(\d)'
    },
    'zone2_power': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?AP',
        'item_type': 'bool',
        'dev_datatype': 'PioPwr2',
        'reply_token': ['APR']
    },
    'zone2_mute': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': '?Z2M',
        'item_type': 'bool',
        'dev_datatype': 'PioMute2',
        'reply_token': ['Z2MUT']
    },
    'zone2_volume': {
        'opcode': "MD_VALUE",
        'read': True,
        'write': True,
        'read_cmd': '?ZV',
        'write_cmd': ':{VAL:02}ZV:',
        'item_type': 'num',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'ZV(\d{2})',
        'settings': {
                    'max': 82,
                    'force_min': 0
                    }
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
        'opcode': 'MD_VALUE',
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
