#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev squeezebox


commands = {
    'server': {
        'playercount': {'read': True, 'write': False, 'opcode': 'slim.request', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_count', 'item_attrs': {'initial': True}, 'params': ["-", ["player", "count", "?"]]},
        'favoritescount': {'read': True, 'write': False, 'opcode': 'slim.request', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': 'count', 'item_attrs': {'initial': True}, 'params': ["-", ["favorites", "items"]]}
    },
    'database': {
        'totalgenres': {'read': True, 'write': False, 'opcode': 'slim.request', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_genres', 'item_attrs': {'initial': True}, 'params': ["-", ["info", "total", "genres", "?"]]},
        'totalduration': {'read': True, 'write': False, 'opcode': 'slim.request', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_duration', 'item_attrs': {'initial': True}, 'params': ["-",  ["info", "total", "duration", "?"]]},
        'totalartists': {'read': True, 'write': False, 'opcode': 'slim.request', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_artists', 'item_attrs': {'initial': True}, 'params': ["-", ["info", "total", "artists", "?"]]},
        'totalalbums': {'read': True, 'write': False, 'opcode': 'slim.request', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_albums', 'item_attrs': {'initial': True}, 'params': ["-", ["info", "total", "albums", "?"]]},
        'totalsongs': {'read': True, 'write': False, 'opcode': 'slim.request', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_songs', 'item_attrs': {'initial': True}, 'params': ["-", ["info", "total", "songs", "?"]]}
    }
}

lookups = {
    'REPEAT': {
        '0': 'OFF',
        '1': 'SONG',
        '2': 'PLAYLIST'
    },
    'SHUFFLE': {
        '0': 'OFF',
        '1': 'SONG',
        '2': 'ALBUM'
    }
}

item_templates = {
    'time': {
        'poll':
            {
                'type': 'bool',
                'eval': 'True if sh....playmode() == "play" else None',
                'enforce_updates': True,
                'cycle': '10 = True',
                'md_device': 'DEVICENAME',
                'md_read_group_trigger': 'player.control.time_poll'
            }
    }

}
