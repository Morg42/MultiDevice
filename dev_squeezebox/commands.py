#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev squeezebox


commands = {
    'server': {
        'listenmode': {'read': True, 'write': True, 'write_cmd': ':listen {VAL:01}:', 'item_type': 'bool', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'.*listen (\d)'}
    },
    'playercontrol': {
        'volume': {'read': True, 'write': True, 'read_cmd': 'mixer volume ?', 'item_type': 'num', 'write_cmd': ':mixer volume {VAL}:', 'item_type': 'num', 'dev_datatype': 'str', 'reply_token': 'REGEX', 'reply_pattern': r'.*mixer volume (\d)'}
    }
}
