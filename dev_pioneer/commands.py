#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev pioneer

commands = {
    'power': {
        # send (transformed) data value as command
        'opcode': '$V',
        'read': True,
        'write': True,
        # zum Auslesen des Power-Status (cmd: read!) '?P' senden
        'read_cmd': '?P',
        # shng item type should be bool for this command
        'item_type': 'bool',
        # device type / data conversion is DT_PioPwr
        'dev_type': 'PioPwr',
        # reply token(s) identifying this command
        'reply_token': ['PWR']
    }
}
