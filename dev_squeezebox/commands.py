#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev squeezebox


commands = {
    'server': {
        'listenmode': {'read': True, 'write': True, 'write_cmd': ':listen {VAL:01}:', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'listen (\d)'},
        'playercount': {'read': True, 'write': False, 'read_cmd': 'player count ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'player count (\d+)'},
        'favoritescount': {'read': True, 'write': False, 'read_cmd': 'favorites items', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'favorites items\s+ count:(\d+)'},
    },
    'database': {
        'rescan': {
            'start': {'read': False, 'write': True, 'write_cmd': ':rescan {VAL}:', 'item_type': 'str', 'dev_datatype': 'str'},
            'running': {'read': True, 'write': False, 'read_cmd': 'rescan ?', 'item_type': 'bool', 'dev_datatype': 'SqueezeRescan', 'reply_token': 'REGEX', 'reply_pattern': 'rescan (.*)'},
            'progress': {'read': True, 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'scanner notify progress:(.*)'},
            'runningtime': {'read': True, 'read_cmd': 'rescanprogress totaltime', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'rescanprogress totaltime .* totaltime:([0-9]{2}:[0-9]{2}:[0-9]{2})'},
            'fail': {'read': True, 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'rescanprogress totaltime rescan:0 lastscanfailed:(.*)'},
            'abortscan': {'read': True, 'write': True, 'write_cmd': 'abortscan', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_token': 'abortscan'},
            'wipecache': {'read': False, 'write': True, 'write_cmd': 'wipecache', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_token': 'wipecache'}
        },
        'totalgenres': {'read': True, 'write': False, 'read_cmd': 'info total genres ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'info total genres (\d+)'},
        'totalduration': {'read': True, 'write': False, 'read_cmd': 'info total duration ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'info total duration ([0-9.]*)'},
        'totalartists': {'read': True, 'write': False, 'read_cmd': 'info total artists ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'info total artists (\d+)'},
        'totalalbums': {'read': True, 'write': False, 'read_cmd': 'info total albums ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'info total albums (\d+)'},
        'totalsongs': {'read': True, 'write': False, 'read_cmd': 'info total songs ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'info total songs (\d+)'},
        'totalalbums': {'read': True, 'write': False, 'read_cmd': 'info total albums ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'info total albums (\d+)'},
    },
    'player': {
        'control': {
            'power': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 power ?', 'item_type': 'bool', 'write_cmd': ':MD_CUSTOM1 power {VAL:01}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 prefset server power (\d)'},
            'volume': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 mixer volume ?', 'item_type': 'num', 'write_cmd': ':MD_CUSTOM1 prefset server volume {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 (?:mixer|prefset server) volume (\d{1,3})'},
            'alarm': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 alarm ?', 'item_type': 'str', 'write_cmd': ':MD_CUSTOM1 alarm {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 alarm (.*)'},
            'sync': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 sync ?', 'write_cmd': ':MD_CUSTOM1 sync {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 sync (.*)'},
            'unsync': {'read': False, 'write': True, 'write_cmd': 'MD_CUSTOM1 sync -', 'item_type': 'bool', 'dev_datatype': 'str'},
            'display': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 display ?', 'item_type': 'str', 'write_cmd': ':MD_CUSTOM1 display {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 display (.*)'},
            'connect': {'read': True, 'write': True, 'item_type': 'str', 'write_cmd': ':MD_CUSTOM1 connect {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 connect (.*)'},
            'disconnect': {'read': True, 'write': True, 'item_type': 'str', 'write_cmd': ':disconnect MD_CUSTOM1 {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'disconnect CUSTOM_PATTERN1 (.*)'},
        },
        'info': {
            'connected': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 connected ?', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 connected (\d)'},
            'playername': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 playername ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playername (.*)'},
            'sleep': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 sleep ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 sleep (.*)'},
            'alarms': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 alarms ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 alarms (.*)'},
            'syncgroups': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 syncgroups ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 syncgroups (\d+)'},
            'signalstrength': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 signalstrength ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 signalstrength (\d+)'},
            'genre': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 genre ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 genre (.*)'},
            'artist': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 artist ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 artist (.*)'},
            'album': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 album ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 album (.*)', 'item_attrs': {'item_template': 'albumart'}},
            'title': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 title ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 title (.*)'},
            'title': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 title ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 title (.*)'},
        }

    }
}

item_templates = {
    'albumart': {
        'md_albumart': '',

        'currentalbumarturl': {
            'type': 'str',
            'visu_acl': 'ro',
            'cache': True,
            'remark': 'Will get set to http://<SERVER IP>:<WEB_PORT>/music/current/cover.jpg?player=<PLAYER MAC> automatically on plugin start'
        }
    }
}
