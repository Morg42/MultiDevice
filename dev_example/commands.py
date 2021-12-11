#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

# commands for dev example

commands = {
    # name of the command as used in item attribute 'md_command'
    'cmd': {
        # general / fallback command sequence/string/..., HTTP URL for MD_Connection_Net_Tcp_Request
        'opcode': '',
        # can this command read = receive information from the device?
        'read': True,
        # can this command write = send item values to the device?
        'write': True,
        # optional, specific command to read value from device (if not defined, use opcode)
        'read_cmd': '',
        # optional, specific command to write item value to device (if not defined, use opcode)
        'write_cmd': '',
        # expected SmartHomeNG item type of associated item
        'item_type': 'bool',
        # datatype (DT_xyz) class used to talk to the device (see ../datatypes.py)
        'dev_datatype': 'raw',
        # optional, start sequence/beginning of reply to indicate reply belongs to this command
        'reply_token': ['']
    }
}
