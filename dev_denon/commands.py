#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
""" commands for dev pioneer

Most commands send a string (fixed for reading, attached data for writing)
while parsing the response works by extracting the needed string part by
regex. Some commands translate the device data into readable values via
lookups.
"""

models = {
    'ALL': ['general.power', 'general.inputname_DVD', 'general.inputname_BD', 'general.inputname_TV', 'general.inputname_SAT', 'general.inputname_MPLAY', 'general.inputname_GAME', 'general.inputname_AUX1', 'general.inputname_CD', 'general.inputname_AUX2', 'general.inputname_PHONO', 'general.setupmenu', 'general.display', 'general.soundmode', 'general.inputsignal', 'general.inputrate', 'general.inputformat', 'general.inputresolution', 'general.outputresolution',
            'tuner.tunerpreset', 'tuner.tunerpresetup', 'tuner.tunerpresetdown',
            'zone1.power', 'zone1.mute', 'zone1.volume', 'zone1.volumemax', 'zone1.volumeup', 'zone1.volumedown', 'zone1.input', 'zone1.listeningmode', 'zone1.sleep', 'zone1.standby',
            'zone1.cinema_eq', 'zone1.hdmiaudioout', 'zone1.dynamicrange', 'zone1.pictureenhance', 'zone1.subwoofertoggle', 'zone1.subwoofer', 'zone1.subwooferup', 'zone1.subwooferdown', 'zone1.lfe', 'zone1.lfeup', 'zone1.lfedown', 'zone1.tone', 'zone1.audioinput', 'zone1.videoinput', 'zone1.ecomode', 'zone1.treble', 'zone1.trebleup', 'zone1.trebledown', 'zone1.bass', 'zone1.bassup', 'zone1.bassdown',
            'zone1.levels.front_left', 'zone1.levels.front_right', 'zone1.levels.front_height_left', 'zone1.levels.front_height_right', 'zone1.levels.front_center', 'zone1.levels.surround_left', 'zone1.levels.surround_right', 'zone1.levels.surroundback_left', 'zone1.levels.surroundback_right', 'zone1.levels.rear_height_left', 'zone1.levels.rear_height_right', 'zone1.levels.subwoofer',
            'zone2.power', 'zone2.mute', 'zone2.volume', 'zone2.volumeup', 'zone2.volumedown', 'zone2.sleep', 'zone2.standby', 'zone2.hdmiout', 'zone2.input'],
    'AVR-X6300H': ['zone1.levels.subwoofer2', 'zone1.aspectratio', 'zone1.hdmimonitor', 'zone1.videoresolution', 'zone1.videoprocessingmode', 'zone1.speakersetup', 'zone1.dialogenhance', 'zone2.treble', 'zone2.trebleup', 'zone2.trebledown', 'zone2.bass', 'zone2.bassup', 'zone2.bassdown', 'zone2.level_front', 'zone2.level_front', 'zone2.HPF', 'zone2.level_front_left', 'zone2.level_front_right', 'zone3.power', 'zone3.mute', 'zone3.volume', 'zone3.volumeup', 'zone3.volumedown', 'zone3.input', 'zone3.sleep', 'zone3.standby', 'zone3.treble', 'zone3.trebleup', 'zone3.trebledown', 'zone3.bass', 'zone3.bassup', 'zone3.bassdown', 'zone3.level_front_left', 'zone3.level_front_right', 'zone3.HPF'],
    'AVR-X4300H': ['zone1.levels.subwoofer2', 'zone1.aspectratio', 'zone1.hdmimonitor', 'zone1.videoresolution', 'zone1.videoprocessingmode', 'zone1.dialogtoggle', 'zone1.dialog', 'zone1.dialogup', 'zone1.dialogdown', 'zone1.speakersetup', 'zone2.treble', 'zone2.trebleup', 'zone2.trebledown', 'zone2.bass', 'zone2.bassup', 'zone2.bassdown', 'zone2.level_front', 'zone2.level_front', 'zone2.HPF', 'zone2.level_front_left', 'zone2.level_front_right', 'zone3.power', 'zone3.mute', 'zone3.volume', 'zone3.volumeup', 'zone3.volumedown', 'zone3.input', 'zone3.sleep', 'zone3.standby', 'zone3.treble', 'zone3.trebleup', 'zone3.trebledown', 'zone3.bass', 'zone3.bassup', 'zone3.bassdown', 'zone3.level_front_left', 'zone3.level_front_right', 'zone3.HPF'],
    'AVR-X3300W': ['zone1.levels.subwoofer2', 'zone1.aspectratio', 'zone1.videoresolution', 'zone1.videoprocessingmode', 'zone1.dialogtoggle', 'zone1.dialog', 'zone1.dialogup', 'zone1.dialogdown', 'zone2.treble', 'zone2.trebleup', 'zone2.trebledown', 'zone2.bass', 'zone2.bassup', 'zone2.bassdown', 'zone2.level_front', 'zone2.level_front', 'zone2.HPF', 'zone2.level_front_left', 'zone2.level_front_right', 'tuner.title', 'tuner.genre', 'tuner.artist', 'general.display'],
    'AVR-X2300W': ['zone1.aspectratio', 'zone1.hdmimonitor', 'zone1.videoresolution', 'zone1.videoprocessingmode', 'zone1.dialogtoggle', 'zone1.dialog', 'zone1.dialogup', 'zone1.dialogdown', 'zone2.level_front_left', 'zone2.level_front_right', 'tuner.title', 'tuner.genre', 'tuner.artist', 'general.display'],
    'AVR-X1300W': ['zone1.dialogtoggle', 'zone1.dialog', 'zone1.dialogup', 'zone1.dialogdown', 'tuner.title', 'tuner.genre', 'tuner.artist', 'general.display']
}

commands = {
    'general': {
        'power': {'read': True, 'write': True, 'read_cmd': 'PW?', 'write_cmd': 'PW{VALUE}', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_pattern': 'PW(ON|STANDBY)', 'lookup': 'POWER'},
        'setupmenu': {'read': True, 'write': True, 'read_cmd': 'MNMEN?', 'write_cmd': 'MNMEN {VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'MNMEN (ON|OFF)'},
        'display': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'NSE', 'item_type': 'str', 'dev_datatype': 'DenonDisplay', 'reply_pattern': 'NSE(.*)'},
        'soundmode': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'SSSMG ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': r'SSSMG ([A-Z]{3})', 'lookup': 'SOUNDMODE'},
        'inputsignal': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'SSINFAISSIG ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': r'SSINFAISSIG (\d{2})', 'lookup': 'INPUTSIGNAL'},
        'inputrate': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'SSINFAISFSV ?', 'item_type': 'num', 'dev_datatype': 'convert0', 'reply_pattern': r'SSINFAISFSV (\d{2,3}|NON)'},
        'inputformat': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'SSINFAISFOR ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'SSINFAISFOR (.*)'},
        'inputresolution': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'SSINFSIGRES ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'SSINFSIGRES I(.*)'},
        'outputresolution': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'SSINFSIGRES ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'SSINFSIGRES O(.*)'},
    },
    'tuner': {
        'title': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'NSE', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'NSE1(.*)'},
        'album': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'NSE', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'NSE4(.*)'},
        'artist': {'opcode': '{VALUE}', 'read': True, 'write': True, 'read_cmd': 'NSE', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'NSE2(.*)'},
        'tunerpreset': {'read': True, 'write': True, 'read_cmd': 'TPAN?', 'item_type': 'num', 'write_cmd': 'TPAN{RAW_VALUE:02}', 'dev_datatype': 'str', 'reply_pattern': r'TPAN(\d{2})'},
        'tunerpresetup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'TPANUP', 'dev_datatype': 'raw'},
        'tunerpresetdown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'TPANDOWN', 'dev_datatype': 'raw'},
    },
    'zone1': {
        'custom_inputnames': {'read': True, 'write': False, 'read_cmd': 'SSFUN ?', 'item_type': 'dict', 'dev_datatype': 'str', 'reply_pattern': 'SSFUN(.*)', 'item_attrs': {'initial': True, 'item_template': 'custom_inputnames'}},
        'power': {'read': True, 'write': True, 'read_cmd': 'ZM?', 'write_cmd': 'ZM{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'ZM(ON|OFF)'},
        'mute': {'read': True, 'write': True, 'read_cmd': 'MU?', 'write_cmd': 'MU{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'MU(ON|OFF)'},
        'volume': {'read': True, 'write': True, 'read_cmd': 'MV?', 'write_cmd': 'MV{VALUE}', 'item_type': 'num', 'dev_datatype': 'DenonVol', 'reply_pattern': r'MV(\d{2,3})', 'cmd_settings': {'force_min': 0.0, 'valid_max': 98.0}},
        'volumemax': {'opcode': '{VALUE}', 'read': True, 'write': False, 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': r'MVMAX (\d{2,3})'},
        'volumeup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'MVUP', 'dev_datatype': 'raw'},
        'volumedown': {'read': False, 'write_cmd': 'MVDOWN', 'write': True, 'item_type': 'bool', 'dev_datatype': 'raw'},
        'input': {'read': True, 'write': True, 'read_cmd': 'SI?', 'write_cmd': 'SI{VALUE}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'SI(.*)', 'lookup': 'INPUT', 'item_attrs': {'attributes': {'on_change': '.custom_name = sh...custom_inputnames()[value]', 'custom_name': {'type': 'str', 'on_change': '.. = sh....custom_inputnames.reverse()[value]'}}}},
        'listeningmode': {'read': True, 'write': True, 'cmd_settings': {'valid_list_ci': ['MOVIE', 'MUSIC', 'GAME', 'DIRECT', 'PURE DIRECT', 'STEREO', 'AUTO', 'DOLBY DIGITAL', 'DTS SURROUND', 'AURO3D', 'AURO2DSURR', 'MCH STEREO', 'ROCK ARENA', 'JAZZ CLUB', 'MONO MOVIE', 'MATRIX', 'VIDEO GAME', 'VIRTUAL', 'LEFT', 'RIGHT']}, 'read_cmd': 'MS?', 'write_cmd': 'MS{RAW_VALUE_UPPER}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'MS{VALID_LIST_CI}'},
        'sleep': {'read': True, 'write': True, 'item_type': 'num', 'read_cmd': 'SLP?', 'write_cmd': 'SLP{VALUE}', 'dev_datatype': 'convert0', 'reply_pattern': r'SLP(\d{3}|OFF)', 'cmd_settings': {'force_min': 0, 'force_max': 120}},
        'standby': {'read': True, 'write': True, 'item_type': 'num', 'read_cmd': 'STBY?', 'write_cmd': 'STBY{VALUE}', 'dev_datatype': 'DenonStandby1', 'reply_pattern': r'STBY(\d{2}M|OFF)', 'cmd_settings': {'valid_list_ci': [0, 15, 30, 60]}},
        'cinema_eq': {'read': True, 'write': True, 'read_cmd': 'PSCINEMA EQ. ?', 'write_cmd': 'PSCINEMA EQ.{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'PSCINEMA EQ.(ON|OFF)'},
        'speakersetup': {'opcode': '{VALUE}', 'read': True, 'write': True, 'cmd_settings': {'valid_list_ci': ['FL', 'HF']}, 'read_cmd': 'PSSP: ?', 'write_cmd': 'PSSP:{RAW_VALUE_UPPER}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'PSSP:(FL|HF|FR)'},
        'aspectratio': {'read': True, 'write': True, 'read_cmd': 'VSASP ?', 'write_cmd': 'VSASP{VALUE}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'VSASP(.*)', 'lookup': 'ASPECT'},
        'hdmimonitor': {'read': True, 'write': True, 'cmd_settings': {'force_min': 0, 'force_max': 2}, 'read_cmd': 'VSMONI ?', 'write_cmd': 'VSMONI{VALUE}', 'item_type': 'num', 'dev_datatype': 'convertAuto', 'reply_pattern': 'VSMONI(AUTO|1|2)'},
        'hdmiresolution': {'read': True, 'write': True, 'read_cmd': 'VSSCH ?', 'write_cmd': 'VSSCH{VALUE}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'VSSCH(.*)', 'lookup': 'RESOLUTION'},
        'hdmiaudioout': {'read': True, 'write': True, 'item_type': 'str', 'read_cmd': 'VSAUDIO ?', 'write_cmd': 'VSAUDIO {RAW_VALUE_UPPER}', 'dev_datatype': 'str', 'reply_pattern': 'VSAUDIO (TV|AMP)', 'cmd_settings': {'valid_list_ci': ['TV', 'AMP']}},
        'videoprocessingmode': {'read': True, 'write': True, 'item_type': 'str', 'read_cmd': 'VSVPM ?', 'write_cmd': 'VSVPM{VALUE}', 'dev_datatype': 'str', 'reply_pattern': 'VSVPM(AUTO|GAME|BYP|MOVI)', 'lookup': 'VIDEOPROCESS'},
        'videoresolution': {'read': True, 'write': True, 'read_cmd': 'VSSC ?', 'write_cmd': 'VSSC{VALUE}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'VSSC(.*)', 'lookup': 'RESOLUTION'},
        'dynamicrange': {'read': True, 'write': True, 'read_cmd': 'PSDRC ?', 'item_type': 'num', 'write_cmd': 'PSDRC {VALUE}', 'dev_datatype': 'str', 'reply_pattern': 'PSDRC ([A-Z]{2,4})', 'lookup': 'DYNAM'},
        'dialogtoggle': {'read': True, 'write': True, 'read_cmd': 'PSDIL ?', 'write_cmd': 'PSDIL {VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'PSDIL (ON|OFF)'},
        'dialog': {'read': True, 'write': True, 'read_cmd': 'PSDIL ?', 'item_type': 'num', 'cmd_settings': {'force_min': -12, 'force_max': 12}, 'write_cmd': 'PSDIL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'PSDIL (\d{2})'},
        'dialogup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSDIL UP', 'dev_datatype': 'raw'},
        'dialogdown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSDIL DOWN', 'dev_datatype': 'raw'},
        'dialogenhance': {'read': True, 'write': True, 'read_cmd': 'PSDEH ?', 'write_cmd': 'PSDEH {VALUE}', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': 'PSDEH ([A-Z]{3,4})', 'lookup': 'DIALOG'},
        'pictureenhancer': {'read': True, 'write': True, 'read_cmd': 'PVENH ?', 'item_type': 'num', 'cmd_settings': {'force_min': 0, 'force_max': 12}, 'write_cmd': 'PVENH {RAW_VALUE:02}', 'dev_datatype': 'int', 'reply_pattern': r'PVENH (\d{2})'},
        'subwoofertoggle': {'read': True, 'write': True, 'read_cmd': 'PSSWL ?', 'write_cmd': 'PSSWL {VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'PSSWL (ON|OFF)'},
        'subwoofer': {'read': True, 'write': True, 'read_cmd': 'PSSWL ?', 'item_type': 'num', 'cmd_settings': {'force_min': -12, 'valid_max': 12}, 'write_cmd': 'PSSWL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'PSSWL (\d{2})'},
        'subwooferup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSSWL UP', 'dev_datatype': 'raw'},
        'subwooferdown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSSWL DOWN', 'dev_datatype': 'raw'},
        'lfe': {'read': True, 'write': True, 'read_cmd': 'PSLFE ?', 'item_type': 'num', 'cmd_settings': {'force_min': -10, 'valid_max': 3}, 'write_cmd': 'PSLFE {RAW_VALUE:02}', 'dev_datatype': 'int', 'reply_pattern': r'PSLFE (\d{2})'},
        'lfeup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSLFE UP', 'dev_datatype': 'raw'},
        'lfedown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSLFE DOWN', 'dev_datatype': 'raw'},
        'tone': {'read': True, 'write': True, 'read_cmd': 'PSTONE CTRL ?', 'write_cmd': 'PSTONE CTRL {VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'PSTONE CTRL (ON|OFF)'},
        'audioinput': {'read': True, 'write': True, 'cmd_settings': {'valid_list_ci': ['AUTO', 'HDMI', 'DIGITAL', 'ANALOG']}, 'read_cmd': 'SD?', 'write_cmd': 'SD{RAW_VALUE_UPPER}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'SD(.*)'},
        'videoinput': {'read': True, 'write': True, 'cmd_settings': {'valid_list_ci': ['DVD', 'BD', 'TV', 'SAT/CBL', 'MPLAY', 'GAME' 'AUX1', 'AUX2', 'CD', 'ON', 'OFF']}, 'read_cmd': 'SV?', 'write_cmd': 'SV{RAW_VALUE_UPPER}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'SV(.*)'},
        'ecomode': {'opcode': '{VALUE}', 'read': True, 'write': True, 'cmd_settings': {'valid_list_ci': ['ON', 'OFF', 'AUTO']}, 'read_cmd': 'ECO?', 'write_cmd': 'ECO{RAW_VALUE_UPPER}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'ECO(ON|OFF|AUTO)'},
        'treble': {'read': True, 'write': True, 'read_cmd': 'PSTRE ?', 'item_type': 'num', 'cmd_settings': {'force_min': -6, 'force_max': 6}, 'write_cmd': 'PSTRE {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'PSTRE (\d{2})'},
        'trebleup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSTRE UP', 'dev_datatype': 'raw'},
        'trebledown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSTRE DOWN', 'dev_datatype': 'raw'},
        'bass': {'read': True, 'write': True, 'read_cmd': 'PSBAS ?', 'item_type': 'num', 'cmd_settings': {'force_min': -6, 'force_max': 6}, 'write_cmd': 'PSBAS {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'PSBAS (\d{2})'},
        'bassup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSBAS UP', 'dev_datatype': 'raw'},
        'bassdown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'PSBAS DOWN', 'dev_datatype': 'raw'},
        'levels': {
            'front_left': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVFL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVFL (\d{2,3})'},
            'front_right': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVFR {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVFR (\d{2,3})'},
            'front_height_left': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVFHL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVFHL (\d{2,3})'},
            'front_height_right': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVFHR {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVFHR (\d{2,3})'},
            'front_center': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVC {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVC (\d{2,3})'},
            'surround_left': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVSL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVSL (\d{2,3})'},
            'surround_right': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVSR {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVSR (\d{2,3})'},
            'surroundback_left': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVSBL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVSBL (\d{2,3})'},
            'surroundback_right': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVSBR {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVSBR (\d{2,3})'},
            'rear_height_left': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVRHL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVRHL (\d{2,3})'},
            'rear_height_right': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVRHR {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVRHR (\d{2,3})'},
            'subwoofer': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVSW {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVSW (\d{2,3})'},
            'subwoofer2': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12.0, 'valid_max': 12.0}, 'read_cmd': 'CV?', 'item_type': 'num', 'write_cmd': 'CVSW2 {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'CVSW2 (\d{2,3})'},
        }
    },
    'zone2': {
        'power': {'read': True, 'write': True, 'read_cmd': 'Z2?', 'write_cmd': 'Z2{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'Z2(ON|OFF)'},
        'mute': {'read': True, 'write': True, 'read_cmd': 'Z2MU?', 'write_cmd': 'Z2MU{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'Z2MU(ON|OFF)'},
        'volume': {'read': True, 'write': True, 'read_cmd': 'Z2?', 'write_cmd': 'Z2{VALUE}', 'item_type': 'num', 'dev_datatype': 'DenonVol', 'reply_pattern': r'Z2(\d{2,3})', 'cmd_settings': {'force_min': 0.0, 'valid_max': 98.0}},
        'volumeup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z2UP', 'dev_datatype': 'raw'},
        'volumedown': {'read': False, 'write_cmd': 'Z2DOWN', 'write': True, 'item_type': 'bool', 'dev_datatype': 'raw'},
        'sleep': {'read': True, 'write': True, 'item_type': 'num', 'read_cmd': 'Z2SLP?', 'write_cmd': 'Z2SLP{VALUE}', 'dev_datatype': 'convert0', 'reply_pattern': r'Z2SLP(\d{3}|OFF)', 'cmd_settings': {'force_min': 0, 'force_max': 120}},
        'standby': {'read': True, 'write': True, 'item_type': 'num', 'read_cmd': 'Z2STBY?', 'write_cmd': 'Z2STBY{VALUE}', 'dev_datatype': 'DenonStandby', 'reply_pattern': r'Z2STBY(\dH|OFF)', 'cmd_settings': {'valid_list_ci': [0, 2, 4, 8]}},
        'hdmiout': {'read': True, 'write': True, 'item_type': 'str', 'read_cmd': 'Z2HDA?', 'write_cmd': 'Z2HDA {RAW_VALUE_UPPER}', 'dev_datatype': 'str', 'reply_pattern': 'Z2HDA (THR|PCM)', 'cmd_settings': {'valid_list_ci': ['THR', 'PCM']}},
        'treble': {'read': True, 'write': True, 'read_cmd': 'Z2PSTRE ?', 'item_type': 'num', 'cmd_settings': {'force_min': -10, 'force_max': 10}, 'write_cmd': 'Z2PSTRE {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'Z2PSTRE (\d{2})'},
        'trebleup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z2PSTRE UP', 'dev_datatype': 'raw'},
        'trebledown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z2PSTRE DOWN', 'dev_datatype': 'raw'},
        'bass': {'read': True, 'write': True, 'read_cmd': 'Z2PSBAS ?', 'item_type': 'num', 'cmd_settings': {'force_min': -10, 'force_max': 10}, 'write_cmd': 'Z2PSBAS {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'Z2PSBAS (\d{2})'},
        'bassup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z2PSBAS UP', 'dev_datatype': 'raw'},
        'bassdown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z2PSBAS DOWN', 'dev_datatype': 'raw'},
        'level_front_left': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12, 'valid_max': 12}, 'read_cmd': 'Z2CV?', 'item_type': 'num', 'write_cmd': 'Z2CVFL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'Z2CVFL (\d{2})'},
        'level_front_right': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12, 'valid_max': 12}, 'read_cmd': 'Z2CV?', 'item_type': 'num', 'write_cmd': 'Z2CVFR {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'Z2CVFR (\d{2})'},
        'HPF': {'read': True, 'write': True, 'read_cmd': 'Z2HPF?', 'write_cmd': 'Z2HPF{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'Z2HPF(ON|OFF)'},
        'input': {'read': True, 'write': True, 'read_cmd': 'Z2?', 'write_cmd': 'Z2{VALUE}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'Z2(.*)', 'lookup': 'INPUT'}
    },
    'zone3': {
        'power': {'read': True, 'write': True, 'read_cmd': 'Z3?', 'write_cmd': 'Z3{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'Z3(ON|OFF)'},
        'mute': {'read': True, 'write': True, 'read_cmd': 'Z3MU?', 'write_cmd': 'Z3MU{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'Z3MU(ON|OFF)'},
        'volume': {'read': True, 'write': True, 'read_cmd': 'Z3?', 'item_type': 'num', 'dev_datatype': 'DenonVol', 'reply_pattern': r'Z3(\d{2,3})', 'cmd_settings': {'force_min': 0.0, 'valid_max': 98.0}},
        'volumeup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z3UP', 'dev_datatype': 'raw'},
        'volumedown': {'read': False, 'write_cmd': 'Z3DOWN', 'write': True, 'item_type': 'bool', 'dev_datatype': 'raw'},
        'sleep': {'read': True, 'write': True, 'item_type': 'num', 'read_cmd': 'Z3SLP?', 'write_cmd': 'Z3SLP{VALUE}', 'dev_datatype': 'convert0', 'reply_pattern': r'Z3SLP(\d{3}|OFF)', 'cmd_settings': {'force_min': 0, 'valid_max': 120}},
        'standby': {'read': True, 'write': True, 'item_type': 'num', 'read_cmd': 'Z3STBY?', 'write_cmd': 'Z3STBY{VALUE}', 'dev_datatype': 'DenonStandby', 'reply_pattern': r'Z3STBY(\dH|OFF)', 'cmd_settings': {'valid_list_ci': [0, 2, 4, 8]}},
        'treble': {'read': True, 'write': True, 'read_cmd': 'Z3PSTRE ?', 'item_type': 'num', 'cmd_settings': {'force_min': -10, 'force_max': 10}, 'write_cmd': 'Z3PSTRE {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'Z3PSTRE (\d{2})'},
        'trebleup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z3PSTRE UP', 'dev_datatype': 'raw'},
        'trebledown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z3PSTRE DOWN', 'dev_datatype': 'raw'},
        'bass': {'read': True, 'write': True, 'read_cmd': 'Z3PSBAS ?', 'item_type': 'num', 'cmd_settings': {'force_min': -10, 'force_max': 10}, 'write_cmd': 'Z3PSBAS {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'Z3PSBAS (\d{2})'},
        'bassup': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z3PSBAS UP', 'dev_datatype': 'raw'},
        'bassdown': {'read': False, 'write': True, 'item_type': 'bool', 'write_cmd': 'Z3PSBAS DOWN', 'dev_datatype': 'raw'},
        'level_front_left': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12, 'valid_max': 12}, 'read_cmd': 'Z3CV?', 'item_type': 'num', 'write_cmd': 'Z3CVFL {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'Z3CVFL (\d{2})'},
        'level_front_right': {'read': True, 'write': True, 'cmd_settings': {'force_min': -12, 'valid_max': 12}, 'read_cmd': 'Z3CV?', 'item_type': 'num', 'write_cmd': 'Z3CVFR {VALUE}', 'dev_datatype': 'remap50to0', 'reply_pattern': r'Z3CVFR (\d{2})'},
        'HPF': {'read': True, 'write': True, 'read_cmd': 'Z3HPF?', 'write_cmd': 'Z3HPF{VALUE}', 'item_type': 'bool', 'dev_datatype': 'onoff', 'reply_pattern': 'Z3HPF(ON|OFF)'},
        'input': {'read': True, 'write': True, 'read_cmd': 'Z3?', 'write_cmd': 'Z3{RAW_VALUE_UPPER}', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': 'Z3(.*)', 'lookup': 'INPUT3'}
    }
}

lookups = {
    'ALL': {
        'INPUTSIGNAL': {
            '01': 'Analog',
            '02': 'PCM',
            '03': 'Dolby Digital',
            '04': 'Dolby TrueHD',
            '05': 'Dolby Atmos',
            '06': 'DTS',
            '07': '07',
            '08': 'DTS-HD Hi Res',
            '09': 'DTS-HD MSTR',
            '10': '10',
            '11': '11',
            '12': 'Unknown',
            '13': 'PCM Zero',
            '14': '14',
            '15': 'MP3',
            '16': '16',
            '17': 'AAC',
            '18': 'FLAC',
        },
        'RESOLUTION': {
            '48P': '480p/576p',
            '10I': '1080i',
            '72P': '720p',
            '10P': '1080p',
            '10P24': '1080p:24Hz',
            '4K': '4K',
            '4KF': '4K(60/50)',
            'AUTO': 'Auto'
        },
        'ASPECT': {
            'NRM': '4:3',
            'FUL': '16:9'
        },
        'POWER': {
            'ON': True,
            'STANDBY': False
        },
        'SOUNDMODE': {
            'MUS': 'MUSIC',
            'MOV': 'MOVIE',
            'GAM': 'GAME',
            'PUR': 'PURE DIRECT'
        },
        'DYNAM': {
            'OFF': 0,
            'LOW': 1,
            'MID': 2,
            'HI': 3,
            'AUTO': 4
        },
        'DIALOG': {
            'OFF': 0,
            'LOW': 1,
            'MED': 2,
            'HIGH': 3,
            'AUTO': 4
        },
        'VIDEOPROCESS': {
            'MOVI': 'Movie',
            'BYP': 'Bypass',
            'GAME': 'Game',
            'AUTO': 'Auto'
        },
        'INPUT': {
            'SOURCE': 'SOURCE',
            'TUNER': 'TUNER',
            'DVD': 'DVD',
            'BD': 'BD',
            'TV': 'TV',
            'SAT/CBL': 'SAT/CBL',
            'MPLAY': 'MPLAY',
            'GAME': 'GAME',
            'HDRADIO': 'HDRADIO',
            'NET': 'NET',
            'AUX1': 'AUX1',
            'BT': 'BT'
        },
        'INPUT3': {
            'SOURCE': 'SOURCE',
            'TUNER': 'TUNER',
            'PHONO': 'PHONO',
            'CD': 'CD',
            'DVD': 'DVD',
            'BD': 'BD',
            'TV': 'TV',
            'SAT/CBL': 'SAT/CBL',
            'MPLAY': 'MPLAY',
            'GAME': 'GAME',
            'NET': 'NET',
            'AUX1': 'AUX1',
            'AUX2': 'AUX2',
            'BT': 'BT',
            'QUICK1': 'QUICK1',
            'QUICK2': 'QUICK2',
            'QUICK3': 'QUICK3',
            'QUICK4': 'QUICK4',
            'QUICK5': 'QUICK5',
            'QUICK1 MEMORY': 'QUICK1 MEMORY',
            'QUICK2 MEMORY': 'QUICK2 MEMORY',
            'QUICK3 MEMORY': 'QUICK3 MEMORY',
            'QUICK4 MEMORY': 'QUICK4 MEMORY',
            'QUICK5 MEMORY': 'QUICK5 MEMORY'
        }
    },
    'AVR-X6300H': {
        'INPUT': {
            'PHONO': 'PHONO',
            'CD': 'CD',
            'AUX2': 'AUX2'
        }
    },
    'AVR-X4300H': {
        'INPUT': {
            'PHONO': 'PHONO',
            'CD': 'CD',
            'AUX2': 'AUX2'
        }
    },
    'AVR-X3300W': {
        'INPUT': {
            'CD': 'CD',
            'AUX2': 'AUX2',
            'IRADIO': 'IRADIO',
            'SERVER': 'SERVER',
            'FAVORITES': 'FAVORITES',
            'USB/IPOD': 'USB/IPOD',
            'USB': 'USB',
            'IPD': 'IPD',
            'IRP': 'IRP',
            'FVP': 'FVP'
        }
    },
    'AVR-X2300W': {
        'INPUT': {
            'CD': 'CD',
            'AUX2': 'AUX2',
            'IRADIO': 'IRADIO',
            'SERVER': 'SERVER',
            'FAVORITES': 'FAVORITES',
            'USB/IPOD': 'USB/IPOD',
            'USB': 'USB',
            'IPD': 'IPD',
            'IRP': 'IRP',
            'FVP': 'FVP'
        }
    },
    'AVR-X1300W': {
        'INPUT': {
            'IRADIO': 'IRADIO',
            'SERVER': 'SERVER',
            'FAVORITES': 'FAVORITES',
            'USB/IPOD': 'USB/IPOD',
            'USB': 'USB',
            'IPD': 'IPD',
            'IRP': 'IRP',
            'FVP': 'FVP'
        }
    }
}

item_templates = {
    'custom_inputnames': {
        'reverse': {
            'type': 'dict',
            'eval': '"{v: k for (k, v) in sh...().items()}"',
            'update': {
                'type': 'bool',
                'eval': 'sh...timer(2, {})',
                'eval_trigger': '...'
            }
        }
    }
}
