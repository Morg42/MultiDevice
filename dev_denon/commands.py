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
        'reply_pattern': 'PW(ON|STANDBY)'
    },
    'setupmenu': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'MNMEN?',
        'write_cmd': 'MNMEN MD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': 'MNMEN (ON|OFF)'
    },
    'title': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'read_val': '-111'},
        'read_cmd': 'NSE',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'NSE1(.*)'
    },
    'album': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'read_val': '-111'},
        'read_cmd': 'NSE',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'NSE4(.*)'
    },
    'artist': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'read_val': '-111'},
        'read_cmd': 'NSE',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'NSE2(.*)'
    },
    'display': {
        # The display command is only working with receivers without HEOS
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'read_val': '-111'},
        'read_cmd': 'NSE',
        'item_type': 'str',
        'dev_datatype': 'DenonDisplay',
        'reply_token': 'REGEX',
        'reply_pattern': 'NSE(.*)'
    },
    'inputsignal': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'read_val': '-111'},
        'read_cmd': 'SSINFAISSIG ?',
        'item_type': 'str',
        'dev_datatype': 'DenonInputsignal',
        'reply_token': 'REGEX',
        'reply_pattern': r'SSINFAISSIG (\d{2})'
    },
    'inputrate': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'read_val': -111},
        'read_cmd': 'SSINFAISFSV ?',
        'item_type': 'num',
        'dev_datatype': 'convert0',
        'reply_token': 'REGEX',
        'reply_pattern': r'SSINFAISFSV (\d{2,3}|NON)'
    },
    'inputformat': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'read_val': '-111'},
        'read_cmd': 'SSINFAISFOR ?',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'SSINFAISFOR (.*)'
    },
    'inputresolution': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'read_val': '-111'},
        'read_cmd': 'SSINFSIGRES ?',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'SSINFSIGRES (.*)'
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
        'reply_pattern': 'PSDIL (ON|OFF)'
    },
    'cinema_eq': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSCINEMA EQ. ?',
        'write_cmd': 'PSCINEMA EQ.MD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': 'PSCINEMA EQ.(ON|OFF)'
    },
    'speakersetup': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['FL', 'HF', 'FR'], 'read_val': '-111'},
        'read_cmd': 'PSSP: ?',
        'write_cmd': ':PSSP:{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'PSSP:(FL|HF|FR)'
    },
    'aspectratio': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list': ['4:3', '16:9'], 'read_val': '-111'},
        'read_cmd': 'VSASP ?',
        'write_cmd': 'VSASPMD_VALUE',
        'item_type': 'str',
        'dev_datatype': 'DenonAspect',
        'reply_token': 'REGEX',
        'reply_pattern': 'VSASP(NRM|FUL)'
    },
    'hdmimonitor': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 0, 'force_max': 2, 'read_val': -111},
        'read_cmd': 'VSMONI ?',
        'write_cmd': 'VSMONIMD_VALUE',
        'item_type': 'num',
        'dev_datatype': 'convertAuto',
        'reply_token': 'REGEX',
        'reply_pattern': 'VSMONI(AUTO|1|2)'
    },
    'hdmiresolution': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['480p/576p', '480p', '576p', '1080i',
                     '720p', '1080p', '1080p:24Hz', '4K', '4K(60/50)', 'AUTO'], 'read_val': '-111'},
        'read_cmd': 'VSSCH ?',
        'write_cmd': 'VSSCHMD_VALUE',
        'item_type': 'str',
        'dev_datatype': 'DenonResolution',
        'reply_token': 'REGEX',
        'reply_pattern': 'VSSCH(48P|10I|72P|10P|10P24|4K|4KF|AUTO)'
    },
    'hdmiaudioout': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'str',
        'read_cmd': 'VSAUDIO ?',
        'write_cmd': ':VSAUDIO {VAL_UPPER}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'VSAUDIO (TV|AMP)',
        'settings': {'valid_list_ci': ['TV', 'AMP'], 'read_val': '-111'}
    },
    'videoprocessingmode': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'str',
        'read_cmd': 'VSVPM ?',
        'write_cmd': 'VSVPMMD_VALUE',
        'dev_datatype': 'DenonVideoproc',
        'reply_token': 'REGEX',
        'reply_pattern': 'VSVPM(AUTO|GAME|BYP|MOVI)',
        'settings': {'valid_list_ci': ['AUTO', 'GAME', 'BYPASS', 'MOVIE'], 'read_val': '-111'}
    },
    'videoresolution': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['480p/576p', '480p', '576p', '1080i',
                     '720p', '1080p', '1080p:24Hz', '4K', '4K(60/50)', 'AUTO'], 'read_val': '-111'},
        'read_cmd': 'VSSC ?',
        'write_cmd': 'VSSCMD_VALUE',
        'item_type': 'str',
        'dev_datatype': 'DenonResolution',
        'reply_token': 'REGEX',
        'reply_pattern': 'VSSC(48P|10I|72P|10P|10P24|4K|4KF|AUTO)'
    },
    'dynamicrange': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSDRC ?',
        'item_type': 'num',
        'settings': {'force_min': 0, 'force_max': 4, 'read_val': -111},
        'write_cmd': 'PSDRC MD_VALUE',
        'dev_datatype': 'DenonDynam',
        'reply_token': 'REGEX',
        'reply_pattern': 'PSDRC ([A-Z]{2,4})'
    },
    'dialog': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSDIL ?',
        'item_type': 'num',
        'settings': {'force_min': -12, 'force_max': 12, 'read_val': -111},
        'write_cmd': 'PSDIL MD_VALUE',
        'dev_datatype': 'remap50to0',
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
    'dialogenhance': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': 0, 'force_max': 4, 'read_val': -111},
        'read_cmd': 'PSDEH ?',
        'write_cmd': 'PSDEH MD_VALUE',
        'item_type': 'num',
        'dev_datatype': 'DenonDialog',
        'reply_token': 'REGEX',
        'reply_pattern': 'PSDEH ([A-Z]{3,4})'
    },
    'pictureenhancer': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PVENH ?',
        'item_type': 'num',
        'settings': {'force_min': 0, 'force_max': 12, 'read_val': -111},
        'write_cmd': ':PVENH {VAL:02}:',
        'dev_datatype': 'num',
        'reply_token': 'REGEX',
        'reply_pattern': r'PVENH (\d{2})'
    },
    'subwoofertoggle': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSSWL ?',
        'write_cmd': 'PSSWL MD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': 'PSSWL (ON|OFF)'
    },
    'subwoofer': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSSWL ?',
        'item_type': 'num',
        'settings': {'force_min': -12, 'force_max': 12, 'read_val': -1113},
        'write_cmd': 'PSSWL MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSSWL (\d{2})'
    },
    'subwooferup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSSWL UP',
        'dev_datatype': 'raw'
    },
    'subwooferdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSSWL DOWN',
        'dev_datatype': 'raw'
    },
    'lfe': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSLFE ?',
        'item_type': 'num',
        'settings': {'force_min': -10, 'force_max': 0, 'read_val': -1113},
        'write_cmd': ':PSLFE {VAL:02}:',
        'dev_datatype': 'num',
        'reply_token': 'REGEX',
        'reply_pattern': r'PSLFE (\d{2})'
    },
    'lfeup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSLFE UP',
        'dev_datatype': 'raw'
    },
    'lfedown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'PSLFE DOWN',
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
        'reply_pattern': 'PSTONE CTRL (ON|OFF)'
    },
    'zone1_audioinput': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['AUTO', 'HDMI', 'DIGITAL', 'ANALOG', '7.1IN', 'NO'], 'read_val': '-111'},
        'read_cmd': 'SD?',
        'write_cmd': ':SD{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'SD(.*)'
    },
    'zone1_digitalinput': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['AUTO', 'PCM', 'DTS'], 'read_val': '-111'},
        'read_cmd': 'DC?',
        'write_cmd': ':DC{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'DC(.*)'
    },
    'zone1_videoinput': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['DVD', 'BD', 'TV', 'SAT/CBL', 'MPLAY', 'GAME'
                                       'AUX1', 'AUX2', 'AUX3', 'AUX4', 'AUX5',
                                       'AUX6', 'AUX7', 'CD', 'ON', 'OFF'], 'read_val': '-111'},
        'read_cmd': 'SV?',
        'write_cmd': ':SV{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'SV(.*)'
    },
    'zone1_ecomode': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['ON', 'OFF', 'AUTO'], 'read_val': '-111'},
        'read_cmd': 'ECO?',
        'write_cmd': ':ECO{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'ECO(ON|OFF|AUTO)'
    },
    'zone1_treble': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'PSTRE ?',
        'item_type': 'num',
        'settings': {'force_min': -6, 'force_max': 6, 'read_val': -111},
        'write_cmd': 'PSTRE MD_VALUE',
        'dev_datatype': 'remap50to0',
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
        'settings': {'force_min': -6, 'force_max': 6, 'read_val': -111},
        'write_cmd': 'PSBAS MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': 'PSBAS (\d{2})'
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
        'settings': {'force_min': -10, 'force_max': 10, 'read_val': -111},
        'write_cmd': 'Z2PSTRE MD_VALUE',
        'dev_datatype': 'remap50to0',
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
        'settings': {'force_min': -10, 'force_max': 10, 'read_val': -111},
        'write_cmd': 'Z2PSBAS MD_VALUE',
        'dev_datatype': 'remap50to0',
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
    'zone3_treble': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z3PSTRE ?',
        'item_type': 'num',
        'settings': {'force_min': -10, 'force_max': 10, 'read_val': -111},
        'write_cmd': 'Z3PSTRE MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3PSTRE (\d{2})'
    },
    'zone3_trebleup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z3PSTRE UP',
        'dev_datatype': 'raw'
    },
    'zone3_trebledown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z3PSTRE DOWN',
        'dev_datatype': 'raw'
    },
    'zone3_bass': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z3PSBAS ?',
        'item_type': 'num',
        'settings': {'force_min': -10, 'force_max': 10, 'read_val': -111},
        'write_cmd': 'Z3PSBAS MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3PSBAS (\d{2})'
    },
    'zone3_bassup': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z3PSBAS UP',
        'dev_datatype': 'raw'
    },
    'zone3_bassdown': {
        'write': True,
        'item_type': 'bool',
        'write_cmd': 'Z3PSBAS DOWN',
        'dev_datatype': 'raw'
    },
    'zone1_level_front_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVFL MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVFL (\d{2,3})'
    },
    'zone1_level_front_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVFR MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVFR (\d{2,3})'
    },
    'zone1_level_front_height_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVFHL MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVFHL (\d{2,3})'
    },
    'zone1_level_front_height_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVFHR MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVFHR (\d{2,3})'
    },
    'zone1_level_front_center': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVC MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVC (\d{2,3})'
    },
    'zone1_level_surround_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVSL MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVSL (\d{2,3})'
    },
    'zone1_level_surround_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVSR MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVSR (\d{2,3})'
    },
    'zone1_level_rear_height_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVRHL MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVRHL (\d{2,3})'
    },
    'zone1_level_rear_height_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVRHR MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVRHR (\d{2,3})'
    },
    'zone1_level_subwoofer': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12.0, 'max': 12.0, 'read_val': -111},
        'read_cmd': 'CV?',
        'item_type': 'num',
        'write_cmd': 'CVSW MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'CVSW (\d{2,3})'
    },
    'zone2_level_front_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12, 'max': 12, 'read_val': -111},
        'read_cmd': 'Z2CV?',
        'item_type': 'num',
        'write_cmd': 'Z2CVFL MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2CVFL (\d{2})'
    },
    'zone2_level_front_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12, 'max': 12, 'read_val': -111},
        'read_cmd': 'Z2CV?',
        'item_type': 'num',
        'write_cmd': 'Z2CVFR MD_VALUE',
        'dev_datatype': 'remap50to0',
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
        'reply_pattern': 'Z2HPF(ON|OFF)'
    },
    'zone3_level_front_left': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12, 'max': 12, 'read_val': -111},
        'read_cmd': 'Z3CV?',
        'item_type': 'num',
        'write_cmd': 'Z3CVFL MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3CVFL (\d{2})'
    },
    'zone3_level_front_right': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'force_min': -12, 'max': 12, 'read_val': -111},
        'read_cmd': 'Z3CV?',
        'item_type': 'num',
        'write_cmd': 'Z3CVFR MD_VALUE',
        'dev_datatype': 'remap50to0',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3CVFR (\d{2})'
    },
    'zone3_HPF': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'read_cmd': 'Z3HPF?',
        'write_cmd': 'Z3HPFMD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': 'Z3HPF(ON|OFF)'
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
        'write_cmd': 'ZMMD_VALUE',
        'item_type': 'bool',
        'dev_datatype': 'onoff',
        'reply_token': 'REGEX',
        'reply_pattern': 'ZM(ON|OFF)'
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
        'reply_pattern': 'MU(ON|OFF)'
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
        'settings': {'force_min': 0.0, 'max': 98.0, 'read_val': -111}
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
        'settings': {'valid_list_ci': ['PHONO', 'CD', 'TUNER', 'DVD', 'BD', 'TV',
                                       'SAT/CBL', 'MPLAY', 'GAME', 'HDRADIO', 'NET',
                                       'PANDORA', 'SIRIUSXM', 'IRADIO', 'SERVER',
                                       'FAVORITES', 'AUX1', 'AUX2', 'AUX3', 'AUX4',
                                       'AUX5', 'AUX6', 'AUX7', 'BT', 'USB/IPOD',
                                       'USB', 'IPD', 'IRP', 'FVP'], 'read_val': '-111'},
        'read_cmd': 'SI?',
        'write_cmd': ':SI{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'SI(.*)'
    },
    'zone1_listeningmode': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['MOVIE', 'MUSIC', 'GAME', 'DIRECT', 'PURE DIRECT',
                                       'STEREO', 'AUTO', 'DOLBY DIGITAL', 'DTS SURROUND',
                                       'AURO3D', 'AURO2DSURR', 'MCH STEREO', 'WIDE SCREEN',
                                       'SUPER STADIUM', 'ROCK ARENA', 'JAZZ CLUB',
                                       'CLASSIC CONCERT', 'MONO MOVIE', 'MATRIX',
                                       'VIDEO GAME', 'VIRTUAL', 'LEFT', 'RIGHT'], 'read_val': '-111'},
        'read_cmd': 'MS?',
        'write_cmd': ':MS{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'MS(.*)'
    },
    'zone1_sleep': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'num',
        'read_cmd': 'SLP?',
        'write_cmd': 'SLPMD_VALUE',
        'dev_datatype': 'convert0',
        'reply_token': 'REGEX',
        'reply_pattern': r'SLP(\d{3}|OFF)',
        'settings': {'force_min': 0, 'force_max': 120, 'read_val': -111}
    },
    'zone1_standby': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'num',
        'read_cmd': 'STBY?',
        'write_cmd': 'STBYMD_VALUE',
        'dev_datatype': 'DenonStandby1',
        'reply_token': 'REGEX',
        'reply_pattern': r'STBY(\d{2}M|OFF)',
        'settings': {'valid_list_ci': [0, 15, 30, 60], 'read_val': -111}
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
        'reply_pattern': 'Z2(ON|OFF)'
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
        'reply_pattern': 'Z2MU(ON|OFF)'
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
        'settings': {'force_min': 0.0, 'valid_max': 98.0, 'read_val': -111}
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
        'settings': {'force_min': 0, 'force_max': 120, 'read_val': -111}
    },
    'zone2_standby': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'num',
        'read_cmd': 'Z2STBY?',
        'write_cmd': 'Z2STBYMD_VALUE',
        'dev_datatype': 'DenonStandby',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z2STBY(\dH|OFF)',
        'settings': {'valid_list_ci': [0, 2, 4, 8], 'read_val': -111}
    },
    'zone2_hdmiout': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'str',
        'read_cmd': 'Z2HDA?',
        'write_cmd': ':Z2HDA {VAL_UPPER}:',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'Z2HDA (THR|PCM)',
        'settings': {'valid_list_ci': ['THR', 'PCM'], 'read_val': '-111'}
    },
    'zone2_source': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'settings': {'valid_list_ci': ['SOURCE', 'PHONO', 'CD', 'TUNER', 'DVD', 'BD',
                                       'TV', 'SAT/CBL', 'MPLAY', 'GAME', 'HDRADIO',
                                       'NET', 'PANDORA', 'SIRIUSXM', 'IRADIO', 'SERVER',
                                       'FAVORITES', 'AUX1', 'AUX2', 'AUX3', 'AUX4',
                                       'AUX5', 'AUX6', 'AUX7', 'BT', 'USB/IPOD',
                                       'USB', 'IPD', 'IRP', 'FVP'], 'read_val': '-111'},
        'read_cmd': 'Z2?',
        'write_cmd': ':Z2{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'Z2(SOURCE|PHONO|CD|TUNER|DVD|BD|TV|SAT/CBL|MPLAY|GAME|HDRADIO|NET|PANDORA|SIRIUSXM|IRADIO|SERVER|FAVORITES|AUX1|AUX2|AUX3|AUX4|AUX5|AUX6|AUX7|BT|USB/IPOD|USB|IPD|IRP|FVP)'
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
        'reply_pattern': 'Z3(ON|OFF)'
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
        'reply_pattern': 'Z3MU(ON|OFF)'
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
        'settings': {'force_min': 0.0, 'valid_max': 98.0, 'read_val': -111}
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
        'settings': {'valid_list_ci': ['SOURCE', 'PHONO', 'CD', 'TUNER', 'DVD', 'BD',
                                       'TV', 'SAT/CBL', 'MPLAY', 'GAME', 'HDRADIO',
                                       'NET', 'PANDORA', 'SIRIUSXM', 'IRADIO', 'SERVER',
                                       'FAVORITES', 'AUX1', 'AUX2', 'AUX3', 'AUX4',
                                       'AUX5', 'AUX6', 'AUX7', 'BT', 'USB/IPOD',
                                       'USB', 'IPD', 'IRP', 'FVP'], 'read_val': '-111'},
        'read_cmd': 'Z3?',
        'write_cmd': ':Z3{VAL_UPPER}:',
        'item_type': 'str',
        'dev_datatype': 'str',
        'reply_token': 'REGEX',
        'reply_pattern': 'Z3(SOURCE|PHONO|CD|TUNER|DVD|BD|TV|SAT/CBL|MPLAY|GAME|HDRADIO|NET|PANDORA|SIRIUSXM|IRADIO|SERVER|FAVORITES|AUX1|AUX2|AUX3|AUX4|AUX5|AUX6|AUX7|BT|USB/IPOD|USB|IPD|IRP|FVP)'
    },
    'zone3_sleep': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'num',
        'read_cmd': 'Z3SLP?',
        'write_cmd': 'Z3SLPMD_VALUE',
        'dev_datatype': 'convert0',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3SLP(\d{3}|OFF)',
        'settings': {'force_min': 0, 'valid_max': 120, 'read_val': -111}
    },
    'zone3_standby': {
        'opcode': 'MD_VALUE',
        'read': True,
        'write': True,
        'item_type': 'num',
        'read_cmd': 'Z3STBY?',
        'write_cmd': 'Z3STBYMD_VALUE',
        'dev_datatype': 'DenonStandby',
        'reply_token': 'REGEX',
        'reply_pattern': r'Z3STBY(\dH|OFF)',
        'settings': {'valid_list_ci': [0, 2, 4, 8], 'read_val': -111}
    }
}
