#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab


'''
    commands for dev example

    This section consists of a single dict which defines all the devices' commands.
    Alternatively, if models are supported and required, see second example for
    commands definition.

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
        'settings': {'min': 0, 'max': 255, 'force_min': 0, 'force_max': 255, 'valid_list': [1, 2, 3, 4, 5]},
        # optional, specifies lookup table to use (see below)
        # if a lookup table is defined, the value from SmartHomeNG is looked up
        # in the named table and the resulting value is processed by the device
        # instead; correspondingly, a converted value from the device is fed into
        # the lookup and the respective value is passed to SmartHomeNG as the value
        # for the item.
        # This makes it easy e.g. to convert numerical values into clear-text values
        # Note: setting this option ignores the ``settings`` parameters!
        'lookup': 'table_name'
    }
}

'''
    The following commands example is for a scenario where different models are
    configured and have overlapping command definitions with different contents.

    The only key on the first level is an underscore, this signals the model-variant.
    The keys on the second level are the model names.
    Below the model names, commands are defined as in the first example. There
    exist no common or dependent command definitions between the different
    models.

    In this case, a model _must_ be specified in the device configuration; the
    ``models`` dict (see next paragraph) is not necessary and will be ignored.
'''

commands = {
    'ALL': {
        'model1': {
            'cmd1': {'read': True, 'write': True, 'opcode': '1a', ... }, 
            'cmd2': {'read': False, 'write': True, 'opcode': '2b', ... }, 
            'cmd3': {'read': True, 'write': False, 'opcode': '3c', ... }, 
            'cmd4': {'read': False, 'write': False, 'opcode': '4d', ... }, 
        },
        'model2': {
            'cmd1': {'read': True, 'write': True, 'opcode': '1c', ... }, 
            'cmd2': {'read': False, 'write': True, 'opcode': '2d', ... }, 
        },
        'model3': {
            'cmd1': {'read': True, 'write': True, 'opcode': '1x', ... }, 
            'cmd2': {'read': False, 'write': True, 'opcode': '2y', ... }, 
            'cmd3': {'read': True, 'write': False, 'opcode': '3z', ... }, 
        },
        ...
    }
}

'''
    (optional) model specifications for dev example

    Different models of a type (eg. different heating models of the same manufacturer
    or different AV receivers of the same series) might require different command
    sets.

    This - optional - dict allows to specify sets of commands which are supported
    by different models. The keys are the model names and the values are lists of
    all commands supported by the respective model. Commands listed under the
    special - optional - key `ALL` are added to all models.

    If the device is configured without a model name, all commands will be available.
    If the device is configured with a model name not listed here (but the ``models``
    dict is present), the device will not load.
    If the device is configured with a model name, but the ``models`` dict is not
    present, the device will have all commands available.

    If the second variant of defining commands is chosen, this dict will be ignored.

    Hint: as this example only defines one command, the following example is purely
          fictional...
'''

models = {
    'ALL': ['cmd10', 'cmd11']
    'model1': ['cmd1', 'cmd2', 'cmd3', 'cmd4'],
    'model2': ['cmd1', 'cmd2', 'cmd3', 'cmd5'],
    'model3': ['cmd1', 'cmd2', 'cmd4', 'cmd5', 'cmd6']
}


'''
    (optional) definition of lookup tables (see commands table)

    Each table is a plain dict containing device values as keys and corresponding
    SmartHomeNG item values as values. Lookup tables are used both for forward
    (device -> shng) and reverse (shng -> device) lookups. By default, reverse
    lookups are case insensitive to allow for typos.

    The lookups dict can have two forms:

    a) without the ability to contain model specific data
    b) with the ability to contain model specific data

    Case a) is the easier one: each key is a lookup table name and each value is
    a plain dict with ``<device value>: <shng item value>`` dict entries.

    Example:
'''

lookups = {
    'table1': {
        1: 'foo',
        2: 'bar',
        3: 'baz'
    },
    'table2': {
        'a': 'lorem',
        'b': 'ipsum',
        'c': 'dolor'
    }
}

'''
    Case b) is basically the same, but with an additional first level inserted.
    The first level MUST contain a key named 'ALL' (duh), which specifies
    "generic" lookup tables valid for all models. The value to this key is a dict
    like the one in case a).
    The first level CAN (and should, why would you do it otherwise?) have
    additional entries named for the supported models. Its value again is a dict
    like the one in case a). These entries are ADDED to the generic entries,
    while tables existent in both are taken from the model-specific dict.

    In the following example, all models will use ``table1`` and ``table2``;
    both model1 and model2 will have the additional ``table3``, while only
    model1 has a modified ``table1``.

    Example:
'''

lookups = {
    'ALL': {
        'table1': {
            1: 'foo',
            2: 'bar',
            3: 'baz'
        },
        'table2': {
            'a': 'lorem',
            'b': 'ipsum',
            'c': 'dolor'
        }
    },
    'model1': {
        'table1': {
            1: 'boo',
            2: 'far',
            3: 'faz'
        },
        'table3': {
            1.0: 'one',
            2.0: 'two',
            3.0: 'three',
            3.14: 'pi'
        }
    },
    'model2': {
        'table3': {
            1.0: 'one',
            2.0: 'two',
            3.0: 'three',
            3.14: 'pi'
        }
    }
}
