#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev pioneer

commands = {
    'power': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PW?',
        'item_type': 'bool',
        'dev_datatype': 'DenonPwr',
        'reply_token': 'REGEX',
        'reply_pattern': r'PW(ON|STANDBY)'
    },
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
    'dialogtoggle': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSDIL ?',
        'write_cmd': 'PSDIL MD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSDIL (ON|OFF)'
    },
    'dialog': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 38, 'force_max': 62},
        'read_cmd': 'PSDIL ?',
        'write_cmd': ':PSDIL {VAL}:',
        'item_type': 'num',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSDIL (\d{2})'
    },
    'dialogup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSDIL UP',
        'dev_datatype': 'raw'
    },
    'dialogdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSDIL DOWN',
        'dev_datatype': 'raw'
    },
    'tone': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSTONE CTRL ?',
        'write_cmd': 'PSTONE CTRL MD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSTONE CTRL (ON|OFF)'
    },
    'zone1_treble': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSTRE ?',
        'item_type': 'num',
        'settings': {
                    'force_min': 44,
                    'force_max': 56
                    },
        'write_cmd': ':PSTRE {VAL:02}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSTRE (\d{2})'
    },
    'zone1_trebleup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSTRE UP',
        'dev_datatype': 'raw'
    },
    'zone1_trebledown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSTRE DOWN',
        'dev_datatype': 'raw'
    },
    'zone1_bass': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSBAS ?',
        'item_type': 'num',
        'settings': {
                    'force_min': 44,
                    'force_max': 56
                    },
        'write_cmd': ':PSBAS {VAL:02}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSBAS (\d{2})'
    },
    'zone1_bassup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSBAS UP',
        'dev_datatype': 'raw'
    },
    'zone1_bassdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSBAS DOWN',
        'dev_datatype': 'raw'
    },
    'zone2_treble': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z2PSTRE ?',
        'item_type': 'num',
        'settings': {
                    'force_min': 40,
                    'force_max': 60
                    },
        'write_cmd': ':Z2PSTRE {VAL:02}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2PSTRE (\d{2})'
    },
    'zone2_trebleup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z2PSTRE UP',
        'dev_datatype': 'raw'
    },
    'zone2_trebledown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z2PSTRE DOWN',
        'dev_datatype': 'raw'
    },
    'zone2_bass': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z2PSBAS ?',
        'item_type': 'num',
        'settings': {
                    'force_min': 40,
                    'force_max': 60
                    },
        'write_cmd': ':Z2PSBAS {VAL:02}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2PSBAS (\d{2})'
    },
    'zone2_bassup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z2PSBAS UP',
        'dev_datatype': 'raw'
    },
    'zone2_bassdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z2PSBAS DOWN',
        'dev_datatype': 'raw'
    },
    'zone1_level_front_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 38.0, 'max': 62.0},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVFL MD_VALUE',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVFL (\d{2,3})'
    },
    'zone1_level_front_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 38.0, 'max': 62.0},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVFR MD_VALUE',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVFR (\d{2,3})'
    },
    'zone1_level_front_center': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 38.0, 'max': 62.0},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVC MD_VALUE',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVC (\d{2,3})'
    },
    'zone1_level_surround_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 38.0, 'max': 62.0},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVSL MD_VALUE',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVSL (\d{2,3})'
    },
    'zone1_level_surround_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 38.0, 'max': 62.0},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVSR MD_VALUE',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVSR (\d{2,3})'
    },
    'zone1_level_subwoofer': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 38.0, 'max': 62.0},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVSW MD_VALUE',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVSW (\d{2,3})'
    },
    'zone2_level_front_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {
                    'force_min': 38,
                    'max': 62
                    },
        'read_cmd': 'Z2CV?',
        'item_type': 'num',
        'write_cmd': 'Z2CVFL MD_VALUE',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2CVFL (\d{2})'
    },
    'zone2_level_front_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {
                    'force_min': 38,
                    'max': 62
                    },
        'read_cmd': 'Z2CV?',
        'item_type': 'num',
        'write_cmd': 'Z2CVFR MD_VALUE',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2CVFR (\d{2})'
    },
    'zone2_HPF': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z2HPF?',
        'write_cmd': 'Z2HPFMD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2HPF(ON|OFF)'
    },
    'tunerpreset': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'TPAN?',
        'item_type': 'num',
        'write_cmd': ':TPAN{VAL:02}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'TPAN(\d{2})'
    },
    'tunerpresetup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'TPANUP',
        'dev_datatype': 'raw'
    },
    'tunerpresetdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'TPANDOWN',
        'dev_datatype': 'raw'
    },
    'zone1_power': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'ZM?',
        'write_cmd': 'ZM MD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'ZM(ON|OFF)'
    },
    'zone1_mute': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'MU?',
        'write_cmd': 'MUMD_VALUE',
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
        'write_cmd': 'MVMD_VALUE',
        'item_type': 'num',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'MV(\d{2,3})',
        'settings': {'force_min': 0.0, 'max': 98.0}
    },
    'zone1_volumemax': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': False,
        'item_type': 'num',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'MVMAX (\d{2,3})'
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
        'settings': {'valid_list': ['PHONO', 'CD', 'TUNER', 'DVD', 'BD', 'TV', 
                                    'SAT/CBL', 'MPLAY', 'GAME', 'HDRADIO', 'NET', 
                                    'PANDORA', 'SIRIUSXM', 'IRADIO', 'SERVER', 
                                    'FAVORITES', 'AUX1', 'AUX2', 'AUX3', 'AUX4', 
                                    'AUX5', 'AUX6', 'AUX7', 'BT', 'USB/IPOD', 
                                    'USB', 'IPD', 'IRP', 'FVP']},
        'read_cmd': 'SI?',
        'write_cmd': ':SI{VAL}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'SI(.*)'
    },
    'zone1_listeningmode': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list': ['MOVIE', 'MUSIC', 'GAME', 'DIRECT', 'PURE DIRECT', 
                                    'STEREO', 'AUTO', 'DOLBY DIGITAL', 'DTS SURROUND', 
                                    'AURO3D', 'AURO2DSURR', 'MCH STEREO', 'WIDE SCREEN', 
                                    'SUPER STADIUM', 'ROCK ARENA', 'JAZZ CLUB', 
                                    'CLASSIC CONCERT', 'MONO MOVIE', 'MATRIX', 
                                    'VIDEO GAME', 'VIRTUAL', 'LEFT', 'RIGHT']},
        'read_cmd': 'MS?',
        'write_cmd': ':MS{VAL}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r'MS(.*)'
    },
    'zone2_power': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z2?',
        'write_cmd': 'Z2MD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2(ON|OFF)'
    },
    'zone2_mute': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z2MU?',
        'write_cmd': 'Z2MUMD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2MU(ON|OFF)'
    },
    'zone2_volume': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z2?',
        'item_type': 'num',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2(\d{2,3})',
        'settings': {'force_min': 0.0, 'max': 98.0}
    },
    'zone2_volumeup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z2UP',
        'dev_datatype': 'raw'
    },
    'zone2_volumedown': {
        'write_cmd': 'Z2DOWN',
        'write': True,
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone2_sleep': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'num',
        'read_cmd': 'Z2SLP?',
        'write_cmd': 'Z2SLPMD_VALUE',
        'dev_datatype': 'convert0',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2SLP(\d{3}|OFF)',
        'settings': {
                    'force_max': 120,
                    'force_min': 0
                    }
    },
    'zone2_standby': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'num',
        'read_cmd': 'Z2STBY?',
        'dev_datatype': 'DenonStandby',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2STBY(\dH|OFF)',
        'settings': {
                    'valid_list': [0, 2, 4, 8]
                    }
    },
    'zone2_source': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list': ['SOURCE', 'PHONO', 'CD', 'TUNER', 'DVD', 'BD', 
                                    'TV', 'SAT/CBL', 'MPLAY', 'GAME', 'HDRADIO', 
                                    'NET', 'PANDORA', 'SIRIUSXM', 'IRADIO', 'SERVER', 
                                    'FAVORITES', 'AUX1', 'AUX2', 'AUX3', 'AUX4', 
                                    'AUX5', 'AUX6', 'AUX7', 'BT', 'USB/IPOD', 
                                    'USB', 'IPD', 'IRP', 'FVP']},
        'read_cmd': 'Z2?',
        'write_cmd': ':Z2{VAL}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r"Z2(SOURCE|PHONO|CD|TUNER|DVD|BD|TV|SAT/CBL|MPLAY|GAME|HDRADIO|NET|PANDORA|SIRIUSXM|IRADIO|SERVER|FAVORITES|AUX1|AUX2|AUX3|AUX4|AUX5|AUX6|AUX7|BT|USB/IPOD|USB|IPD|IRP|FVP)"
    },
    'zone3_power': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z3?',
        'write_cmd': 'Z3MD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3(ON|OFF)'
    },
    'zone3_mute': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z3MU?',
        'write_cmd': 'Z3MUMD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3MU(ON|OFF)'
    },
    'zone3_volume': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z3?',
        'item_type': 'num',
        'dev_datatype': 'DenonVol',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3(\d{2,3})',
        'settings': {'force_min': 0.0, 'max': 98.0}
    },
    'zone3_volumeup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z3UP',
        'dev_datatype': 'raw'
    },
    'zone3_volumedown': {
        'write_cmd': 'Z3DOWN',
        'write': True,
        'item_type': 'bool',
        'dev_datatype': 'raw'
    },
    'zone3_source': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list': ['SOURCE', 'PHONO', 'CD', 'TUNER', 'DVD', 'BD', 
                                    'TV', 'SAT/CBL', 'MPLAY', 'GAME', 'HDRADIO', 
                                    'NET', 'PANDORA', 'SIRIUSXM', 'IRADIO', 'SERVER', 
                                    'FAVORITES', 'AUX1', 'AUX2', 'AUX3', 'AUX4', 
                                    'AUX5', 'AUX6', 'AUX7', 'BT', 'USB/IPOD', 
                                    'USB', 'IPD', 'IRP', 'FVP']},
        'read_cmd': 'Z3?',
        'write_cmd': ':Z3{VAL}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': r"Z3(SOURCE|PHONO|CD|TUNER|DVD|BD|TV|SAT/CBL|MPLAY|GAME|HDRADIO|NET|PANDORA|SIRIUSXM|IRADIO|SERVER|FAVORITES|AUX1|AUX2|AUX3|AUX4|AUX5|AUX6|AUX7|BT|USB/IPOD|USB|IPD|IRP|FVP)"
    }

}
