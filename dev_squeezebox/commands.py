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
        'totalsongs': {'read': True, 'write': False, 'read_cmd': 'info total songs ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'info total songs (\d+)'}
    },
    'player': {
        'control': {
            'power': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 power ?', 'item_type': 'bool', 'write_cmd': ':MD_CUSTOM1 power {VAL:01}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 (?:prefset server\s)?power (\d)'},
            'playmode': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 mode ?', 'item_type': 'str', 'write_cmd': ':MD_CUSTOM1 mode {VAL}:', 'dev_datatype': 'SqueezePlayMode', 'cmd_settings': {'valid_list_ci': ['PLAY', 'PAUSE', 'STOP']}, 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 (?:mode|playlist) (play|pause\s?\d?|stop)'},
            'playpause': {'read': True, 'write': True, 'item_type': 'bool', 'write_cmd': 'MD_CUSTOM1 MD_VALUE', 'dev_datatype': 'SqueezePlay', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 (?:playlist\s)?(play|pause)(?:\s3)?$'},
            'stop': {'read': True, 'write': True, 'item_type': 'bool', 'write_cmd': 'MD_CUSTOM1 MD_VALUE', 'dev_datatype': 'SqueezeStop', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 (?:playlist\s)?(stop)$'},
            'mute': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 mixer muting ?', 'item_type': 'bool', 'write_cmd': ':MD_CUSTOM1 mixer muting {VAL:01}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 (?:mixer muting|prefset server mute) (\d)'},
            'volume': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 mixer volume ?', 'item_type': 'num', 'write_cmd': ':MD_CUSTOM1 mixer volume {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 prefset server volume (-?\d{1,3})'},
            'volume_low': {'read': False, 'write': True, 'item_type': 'num', 'write_cmd': ':MD_CUSTOM1 mixer volume {VAL}:', 'dev_datatype': 'str', 'item_attrs': {'attributes': {'cache': True, 'enforce_updates': True, 'initial_value': 60}}},
            'volume_high': {'read': False, 'write': True, 'item_type': 'num', 'write_cmd': ':MD_CUSTOM1 mixer volume {VAL}:', 'dev_datatype': 'str', 'item_attrs': {'attributes': {'cache': True, 'enforce_updates': True, 'initial_value': 80}}},
            'volumeup': {'read': False, 'write': True, 'item_type': 'num', 'write_cmd': ':MD_CUSTOM1 mixer volume +{VAL}:', 'dev_datatype': 'str', 'item_attrs': {'attributes': {'cache': True, 'enforce_updates': True, 'initial_value': 1}}},
            'volumedown': {'read': False, 'write': True, 'item_type': 'num', 'write_cmd': ':MD_CUSTOM1 mixer volume -{VAL}:', 'dev_datatype': 'str', 'item_attrs': {'attributes': {'cache': True, 'enforce_updates': True, 'initial_value': 1}}},
            'alarm': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 alarm ?', 'item_type': 'str', 'write_cmd': ':MD_CUSTOM1 alarm {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 alarm (.*)'},
            'sync': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 sync ?', 'write_cmd': ':MD_CUSTOM1 sync {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 sync (.*)'},
            'unsync': {'read': False, 'write': True, 'write_cmd': 'MD_CUSTOM1 sync -', 'item_type': 'bool', 'dev_datatype': 'str'},
            'display': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 display ? ?', 'item_type': 'str', 'write_cmd': ':MD_CUSTOM1 display {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 display\s?(.*)'},
            'connect': {'read': True, 'write': True, 'item_type': 'str', 'write_cmd': ':MD_CUSTOM1 connect {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 connect (.*)'},
            'disconnect': {'read': True, 'write': True, 'item_type': 'str', 'write_cmd': ':disconnect MD_CUSTOM1 {VAL}:', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'disconnect CUSTOM_PATTERN1 (.*)'},
            'time': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 time ?', 'write_cmd': ':MD_CUSTOM1 time {VAL}:', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 time (\d+(?:\.\d{2})?)', 'item_attrs': {'item_template': 'time', 'enforce': True, 'read_groups': [{'name': 'player.control.time_poll', 'trigger': 'poll'}]}},
            'forward': {'read': False, 'write': True, 'write_cmd': ':MD_CUSTOM1 time +{VAL}:', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 time \+(\d+(?:\.\d{2})?)', 'item_attrs': {'enforce': True, 'attributes': {'initial_value': 10}}},
            'rewind': {'read': False, 'write': True, 'write_cmd': ':MD_CUSTOM1 time -{VAL}:', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 time \-(\d+(?:\.\d{2})?)', 'item_attrs': {'enforce': True, 'attributes': {'initial_value': 10}}}
        },
        'playlist': {
            'repeat': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 playlist repeat ?', 'item_type': 'num', 'write_cmd': 'MD_CUSTOM1 playlist repeat MD_VALUE', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 playlist repeat (\d)', 'lookup': 'REPEAT', 'item_attrs': {'attributes': {'remark': '0 = Off, 1 = Song, 2 = Playlist'}, 'lookup_item': True}},
            'shuffle': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 playlist shuffle ?', 'item_type': 'num', 'write_cmd': 'MD_CUSTOM1 playlist shuffle MD_VALUE', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 playlist shuffle (\d)', 'lookup': 'SHUFFLE', 'item_attrs': {'attributes': {'remark': '0 = Off, 1 = Song, 2 = Album'}, 'lookup_item': True}},
            'index': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 playlist index ?', 'write_cmd': ':MD_CUSTOM1 playlist index {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 playlist index (\d+)'},
            'name': {'read': True, 'write': True, 'read_cmd': 'MD_CUSTOM1 playlist name ?', 'write_cmd': ':MD_CUSTOM1 playlist name {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist name (.*)'},
            'id': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlistcontrol cmd:load playlist_id:{VAL}:', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 playlistcontrol cmd:load playlist_id:(\d+)'},
            'save': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist save {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist save (.*)'},
            'load': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist resume {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist resume (.*)'},
            'loadalbum': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist loadalbum {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist loadalbum (.*)'},
            'loadtracks': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist loadtracks {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist loadtracks (.*)'},
            'add': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist add {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist add (.*)'},
            'addalbum': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist addalbum {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist addalbum (.*)'},
            'addtracks': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist addtracks {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist addtracks (.*)'},
            'insertalbum': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist insertalbum {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist insertalbum (.*)'},
            'inserttracks': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist insert {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist insert (.*)'},
            'tracks': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 playlist tracks ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist tracks (.*)'},
            'clear': {'read': True, 'write': True, 'write_cmd': 'MD_CUSTOM1 playlist clear', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist clear$', 'item_attrs': {'enforce': True, 'attributes': {'eval': 'True if value else None'}}},
            'delete': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist delete {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist delete (.*)'},
            'deleteitem': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist deleteitem {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist deleteitem (.*)'},
            'deletealbum': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist deletealbum {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist deletealbum (.*)'},
            'preview': {'read': True, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist preview {VAL}:', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 playlist preview (.*)'},
            'next': {'read': False, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist index +{VAL}:', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'item_attrs': {'enforce': True, 'attributes': {'initial_value': 1}}},
            'previous': {'read': False, 'write': True, 'write_cmd': ':MD_CUSTOM1 playlist index -{VAL}:', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'item_attrs': {'enforce': True, 'attributes': {'initial_value': 1}}},
            'customskip': {'read': False, 'write': True, 'item_type': 'str', 'write_cmd': ':MD_CUSTOM1 customskip setfilter filter{VAL}.cs.xml:', 'dev_datatype': 'str', 'item_attrs': {'attributes': {'cache': True}}}
        },
        'info': {
            'connected': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 connected ?', 'item_type': 'bool', 'dev_datatype': 'SqueezeConnection', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 (?:connected|client) (\d|disconnect|reconnect)'},
            'name': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 name ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 name (.*)'},
            'sleep': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 sleep ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 sleep (.*)'},
            'alarms': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 alarms ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 alarms (.*)'},
            'syncgroups': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 syncgroups ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 syncgroups (\d+)'},
            'signalstrength': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 signalstrength ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 signalstrength (\d+)'},
            'genre': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 genre ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 genre (.*)'},
            'artist': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 artist ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 artist (.*)'},
            'album': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 album ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 album (.*)', 'item_attrs': {'initial': True}},
            'title': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 current_title ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 (?:current_title|playlist newsong) (.*?)(?:\s\d+)?$'},
            'path': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 path ?', 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': 'CUSTOM_PATTERN1 path (.*)'},
            'duration': {'read': True, 'write': False, 'read_cmd': 'MD_CUSTOM1 duration ?', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'CUSTOM_PATTERN1 duration (\d+)'},
            'albumarturl': {'read': True, 'write': False, 'item_type': 'str', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': '(http://.*)'}
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
