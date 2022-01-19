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
    'playercontrol': {
        'volume': {'read': True, 'write': True, 'read_cmd': 'mixer volume ?', 'item_type': 'num', 'write_cmd': ':prefset server volume {VAL}:', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'.*(?:mixer|prefset server) volume (\d{1,3})'}
    }
}
