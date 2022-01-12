#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

""" commands for dev kodi """

commands = {
    'update':           {'read': True, 'write': True,  'opcode': 'update',                      'reply_token': 'update',                      'item_type': 'bool', 'dev_datatype': 'raw', 'params': None},
    'player':           {'read': True, 'write': False, 'opcode': 'player',                      'reply_token': 'player',                      'item_type': 'int',  'dev_datatype': 'raw', 'params': None},
    'state':            {'read': True, 'write': False, 'opcode': 'media',                       'reply_token': 'media',                       'item_type': 'str',  'dev_datatype': 'raw', 'params': None},
    'media':            {'read': True, 'write': False, 'opcode': 'media',                       'reply_token': 'media',                       'item_type': 'str',  'dev_datatype': 'raw', 'params': None},
    'title':            {'read': True, 'write': False, 'opcode': 'title',                       'reply_token': 'title',                       'item_type': 'str',  'dev_datatype': 'raw', 'params': None},
    'streams':          {'read': True, 'write': False, 'opcode': 'streams',                     'reply_token': 'streams',                     'item_type': 'dict', 'dev_datatype': 'raw', 'params': None},
    'subtitles':        {'read': True, 'write': False, 'opcode': 'subtitles',                   'reply_token': 'subtitles',                   'item_type': 'dict', 'dev_datatype': 'raw', 'params': None},
    'macro':            {'read': True, 'write': True,  'opcode': 'macro',                       'reply_token': 'macro',                       'item_type': 'bool', 'dev_datatype': 'raw', 'params': None},

    'ping':             {'read': True, 'write': False, 'opcode': 'JSONRPC.Ping',                'reply_token': 'JSONRPC.Ping',                'item_type': 'bool', 'dev_datatype': 'raw', 'params': None},
    'get_status_au':    {'read': True, 'write': False, 'opcode': 'Application.GetProperties',   'reply_token': 'Application.GetProperties',   'item_type': 'bool', 'dev_datatype': 'raw', 'params': ['properties'], 'param_values': [['volume', 'muted']]},

    'get_players':      {'read': True, 'write': False, 'opcode': 'Player.GetPlayers',           'reply_token': 'Player.GetPlayers',           'item_type': 'bool', 'dev_datatype': 'raw', 'params': None},
    'get_actplayer':    {'read': True, 'write': False, 'opcode': 'Player.GetActivePlayers',     'reply_token': 'Player.GetActivePlayers',     'item_type': 'bool', 'dev_datatype': 'raw', 'params': None},
    'get_status_play':  {'read': True, 'write': False, 'opcode': 'Player.GetProperties',        'reply_token': 'Player.GetProperties',        'item_type': 'bool', 'dev_datatype': 'raw', 'params': ['playerid', 'properties'], 'param_values': ['ID', ['type', 'speed', 'time', 'percentage', 'totaltime', 'position', 'currentaudiostream', 'audiostreams', 'subtitleenabled', 'currentsubtitle', 'subtitles', 'currentvideostream', 'videostreams']]},
    'get_item':         {'read': True, 'write': False, 'opcode': 'Player.GetItem',              'reply_token': 'Player.GetItem',              'item_type': 'bool', 'dev_datatype': 'raw', 'params': ['playerid', 'properties'], 'param_values': ['ID', ['title', 'artist']]},
    'get_favourites':   {'read': True, 'write': False, 'opcode': 'Favourites.GetFavourites',    'reply_token': 'Favourites.GetFavourites',    'item_type': 'bool', 'dev_datatype': 'raw', 'params': ['properties'], 'param_values': [['window', 'path', 'thumbnail', 'windowparameter']]},

    'playpause':        {'read': True, 'write': True,  'opcode': 'Player.PlayPause',            'reply_token': 'Player.PlayPause',            'item_type': 'bool', 'dev_datatype': 'raw', 'params': ['playerid', 'play'], 'param_values': ['ID', 'toggle']},
    'seek':             {'read': True, 'write': True,  'opcode': 'Player.Seek',                 'reply_token': 'Player.Seek',                 'item_type': 'num',  'dev_datatype': 'raw', 'params': ['playerid', 'value'], 'param_values': ['ID', 'VAL'], 'cmd_settings': {'force_min': 0.0, 'force_max': 100.0}},
    'audio':            {'read': True, 'write': True,  'opcode': 'Player.SetAudioStream',       'reply_token': 'Player.SetAudioStream',       'item_type': 'str',  'dev_datatype': 'raw', 'params': ['playerid', 'stream'], 'param_values': ['ID', 'VAL']},
    'speed':            {'read': True, 'write': True,  'opcode': 'Player.SetSpeed',             'reply_token': 'Player.SetSpeed',             'item_type': 'int',  'dev_datatype': 'raw', 'params': ['playerid', 'speed'], 'param_values': ['ID', 'VAL'], 'cmd_settings': {'valid_list': [-32,-16,-8,-4,-2,-1,1,2,4,8,16,32]}},
    'subtitle':         {'read': True, 'write': True,  'opcode': 'Player.SetSubtitle',          'reply_token': 'Player.SetSubtitle',          'item_type': 'str',  'dev_datatype': 'raw', 'params': ['playerid', 'subtitle', 'enable'], 'param_values': ['ID', 'VAL', ('False if "VAL"=="off" else True',)]},
    'stop':             {'read': True, 'write': True,  'opcode': 'Player.Stop',                 'reply_token': 'Player.Stop',                 'item_type': 'bool', 'dev_datatype': 'raw', 'params': ['playerid'], 'param_values': ['ID']},
    'goto':             {'read': True, 'write': True,  'opcode': 'Player.GoTo',                 'reply_token': 'Player.GoTo',                 'item_type': 'str',  'dev_datatype': 'raw', 'params': ['playerid', 'to'], 'param_values': ['ID', 'VAL'], 'cmd_settings': {'valid_list': ['previous','next']}},
    'power':            {'read': True, 'write': True,  'opcode': 'System.Shutdown',             'reply_token': 'System.Shutdown',             'item_type': 'bool', 'dev_datatype': 'raw', 'params': None},
    'quit':             {'read': True, 'write': True,  'opcode': 'Application.Quit',            'reply_token': 'Application.Quit',            'item_type': 'bool', 'dev_datatype': 'raw', 'params': None},
    'mute':             {'read': True, 'write': True,  'opcode': 'Application.SetMute',         'reply_token': 'Application.SetMute',         'item_type': 'bool', 'dev_datatype': 'raw', 'params': ['mute'],   'param_values': ['VAL']},
    'volume':           {'read': True, 'write': True,  'opcode': 'Application.SetVolume',       'reply_token': 'Application.SetVolume',       'item_type': 'int',  'dev_datatype': 'raw', 'params': ['volume'], 'param_values': ['VAL'], 'cmd_settings': {'force_min': 0, 'force_max': 100}},
    'action':           {'read': True, 'write': True,  'opcode': 'Input.ExecuteAction',         'reply_token': 'Input.ExecuteAction',         'item_type': 'str',  'dev_datatype': 'raw', 'params': ['action'], 'param_values': ['VAL'], 'cmd_settings': {'valid_list': ['left','right','up','down','select','back','menu','info','pause','stop','skipnext','skipprevious','fullscreen','aspectratio','stepforward','stepback','osd','showsubtitles','nextsubtitle','cyclesubtitle','audionextlanguage','number1','number2','number3','number4','number5','number6','number7','number8','number9','fastforward','rewind','play','playpause','volumeup','volumedown','mute','enter']}}

}
