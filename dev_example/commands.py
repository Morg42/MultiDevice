#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

'''
    commands for dev example

    This file consists of a single dict which defines all the devices' commands.

    In this example, only one command is given to define possible keys and their
    values' meaning.
'''

commands = {
    # name of the command as used in item attribute 'md_command'
    'cmd': {
        # can this command read = receive information from the device?
        'read': True,
        # can this command write = send item values to the device?
        'write': True,
        # general / fallback command sequence/string/..., HTTP URL for MD_Connection_Net_Tcp_Request
        'opcode': '',
        # optional, specific command to read value from device (if not defined, use opcode)
        'read_cmd': '',
        # optional, specific command to write item value to device (if not defined, use opcode)
        'write_cmd': '',
        # expected SmartHomeNG item type of associated item == default item type into which to convert replies
        'item_type': 'bool',
        # datatype used to talk to the device (see ../datatypes.py). For DT_xyz class, use 'xyz'
        'dev_datatype': 'raw',
        # optional, start sequence/beginning of reply to indicate reply belongs to this command
        # this can be a string or a list of strings
        # only in MD_Command_ParseStr, this can be 'REGEX' to enable the next parameter...
        'reply_token': [''],
        # optional, regex with one capturing group to automatically extract reply values from the reply
        # implemented only in MD_Command_ParseStr as of now
        'reply_pattern': '',
        # optional, this dict defines limits for value validity for sending data to the device.
        # - 'min': minimum value, error if value is below
        # - 'max': maximum value, error if value is above
        # - 'force_min': minimum value, set to this value if below (precedence over min)
        # - 'force_max': maximum value, set to this value is above (precedence over max)
        # - 'valid_list': list of allowed values, error if not in list
        # - 'read_val': value to trigger (forced) reading of value from device
        #               (e.g. -1, can be combined with min=0)
        'settings': {'min': 0, 'max': 255, 'force_min': 0, 'force_max': 255, 'valid_list': [1, 2, 3, 4, 5], 'read_val': -1}
    }
}
