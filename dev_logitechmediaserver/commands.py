#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev squeezebox


commands = {
    'server': {
        'playercount': {'read': True, 'write': False, 'opcode': 'server.playercount', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_count', 'item_attrs': {'initial': True, 'attributes': {'md_custom1': '"-"'}}, 'params': ["-", ["player", "count", "?"]]},
        'favoritescount': {'read': True, 'write': False, 'opcode': 'server.favoritescount', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': 'count', 'item_attrs': {'initial': True, 'attributes': {'md_custom1': '"-"'}}, 'params': ["-", ["favorites", "items"]]},
        'version': {'read': True, 'write': False, 'opcode': 'server.version', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '_version', 'item_attrs': {'initial': True, 'attributes': {'md_custom1': '"-"'}}, 'params': ["-", ["version", "?"]]}
    },
    'database': {
        'totalgenres': {'read': True, 'write': False, 'opcode': 'database.totalgenres', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_genres', 'item_attrs': {'initial': True, 'attributes': {'md_custom1': '"-"'}}, 'params': ["-", ["info", "total", "genres", "?"]]},
        'totalduration': {'read': True, 'write': False, 'opcode': 'database.totalduration', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_duration', 'item_attrs': {'initial': True, 'attributes': {'md_custom1': '"-"'}}, 'params': ["-",  ["info", "total", "duration", "?"]]},
        'totalartists': {'read': True, 'write': False, 'opcode': 'database.totalartists', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_artists', 'item_attrs': {'initial': True, 'attributes': {'md_custom1': '"-"'}}, 'params': ["-", ["info", "total", "artists", "?"]]},
        'totalalbums': {'read': True, 'write': False, 'opcode': 'database.totalalbums', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_albums', 'item_attrs': {'initial': True, 'attributes': {'md_custom1': '"-"'}}, 'params': ["-", ["info", "total", "albums", "?"]]},
        'totalsongs': {'read': True, 'write': False, 'opcode': 'database.totalsongs', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '_songs', 'item_attrs': {'initial': True, 'attributes': {'md_custom1': '"-"'}}, 'params': ["-", ["info", "total", "songs", "?"]]}
    },
    'player': {
        'control': {
            'power': {'read': True, 'write': True, 'opcode': 'player.control.power', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_pattern': r'{CUSTOM_PATTERN1} (?:prefset server\s)?power (\d)', 'item_attrs': {'initial': True}, 'params': ["{CUSTOM_ATTR1}", ["power", "{RAW_VALUE:01}"]]},
            'playpause': {'read': True, 'write': True, 'opcode': 'player.control.playpause', 'item_type': 'bool', 'dev_datatype': 'SqueezePlay', 'reply_pattern': r'{CUSTOM_PATTERN1} (?:playlist\s)?(play|pause)(?:\s3)?$', 'params': ["{CUSTOM_ATTR1}", ["{VALUE}"]]},
            'volume': {'read': True, 'write': True, 'opcode': 'player.control.volume', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '', 'params': ["{CUSTOM_ATTR1}", ["mixer", "volume", "{VALUE}"]]},
            'sleep': {'read': True, 'write': True, 'opcode': 'player.control.sleep', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '{CUSTOM_PATTERN1} sleep (.*)', 'params': ["{CUSTOM_ATTR1}", ["sleep", "{VALUE}"]]}
        },
        'info': {
            'status': {'read': True, 'write': False, 'opcode': 'player.info.status', 'item_type': 'dict', 'dev_datatype': 'str', 'reply_pattern': '(.*)', 'params': ["{CUSTOM_ATTR1}", ["status", "-"]]},
            'connected': {'read': True, 'write': False, 'opcode': 'player.info.connected', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'name': {'read': True, 'write': False, 'opcode': 'player.info.name', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'signalstrength': {'read': True, 'write': False, 'opcode': 'player.info.signalstrength', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'playmode': {'read': True, 'write': False, 'cmd_settings': {'valid_list_ci': ['PLAY', 'PAUSE', 'STOP']}, 'opcode': 'player.info.playmode', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '{VALID_LIST_CI}'},
            'time': {'read': True, 'write': False, 'opcode': 'player.info.time', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'duration': {'read': True, 'write': False, 'opcode': 'player.info.duration', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'title': {'read': True, 'write': False, 'opcode': 'player.info.title', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '(.*)'}
        },
        'playlist': {
            'mode': {'read': True, 'write': False, 'opcode': 'player.playlist.mode', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'seq_no': {'read': True, 'write': False, 'opcode': 'player.playlist.seq_no', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'index': {'read': True, 'write': False, 'opcode': 'player.playlist.index', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'timestamp': {'read': True, 'write': False, 'opcode': 'player.playlist.timestamp', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'tracks': {'read': True, 'write': False, 'opcode': 'player.playlist.tracks', 'item_type': 'num', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'nextsong1': {'read': True, 'write': False, 'opcode': 'player.playlist.nextsong1', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'nextsong2': {'read': True, 'write': False, 'opcode': 'player.playlist.nextsong2', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'nextsong3': {'read': True, 'write': False, 'opcode': 'player.playlist.nextsong3', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'nextsong4': {'read': True, 'write': False, 'opcode': 'player.playlist.nextsong4', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'nextsong5': {'read': True, 'write': False, 'opcode': 'player.playlist.nextsong5', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': '(.*)'},
            'repeat': {'read': True, 'write': True, 'opcode': 'player.playlist.repeat', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': r'{CUSTOM_PATTERN1} playlist repeat (\d)', 'lookup': 'REPEAT', 'item_attrs': {'attributes': {'remark': '0 = Off, 1 = Song, 2 = Playlist'}, 'lookup_item': True}, 'params': ["{CUSTOM_ATTR1}", ["playlist", "repeat", "{VALUE}"]]},
            'shuffle': {'read': True, 'write': True, 'opcode': 'player.playlist.shuffle', 'item_type': 'str', 'dev_datatype': 'str', 'reply_pattern': r'{CUSTOM_PATTERN1} playlist shuffle (\d)', 'lookup': 'SHUFFLE', 'item_attrs': {'attributes': {'remark': '0 = Off, 1 = Song, 2 = Album'}, 'lookup_item': True}, 'params': ["{CUSTOM_ATTR1}", ["playlist", "shuffle", "{VALUE}"]]},
        }
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
