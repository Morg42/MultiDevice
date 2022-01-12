#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab


""" commands for dev example

This section consists of a single dict which defines all the devices' commands.
The first example illustrates the generic syntax and the possible attributes and
the second example shows nested command definitions.

If models are defined and commands with the same name are identical on different
models, this definition syntax can be used. For specifying which commands are
present on which model, see below.
Alternatively, if commands with the same name are different on different models,
see the third example for commands definition.

In the first example, only one command is given to define possible keys and their
values' meaning.
"""

commands = {
    # name of the command as used in item attribute 'md_command'
    # provided values are defaults; dicts default to None, but are shown to
    # illustrate valid contents
    'cmd': {
        # can this command read = receive information from the device?
        'read': True,

        # can this command write = send item values to the device?
        'write': False,

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
        # - 'valid_min': minimum value, error if value is below
        # - 'valid_max': maximum value, error if value is above
        # - 'force_min': minimum value, set to this value if below (precedence over min)
        # - 'force_max': maximum value, set to this value is above (precedence over max)
        # - 'valid_list': list of allowed values, error if not in list
        'cmd_settings': {'valid_min': 0, 'valid_max': 255, 'force_min': 0, 'force_max': 255, 'valid_list': [1, 2, 3, 4, 5]},

        # optional, specifies lookup table to use (see below)
        # if a lookup table is defined, the value from SmartHomeNG is looked up
        # in the named table and the resulting value is processed by the device
        # instead; correspondingly, a converted value from the device is fed into
        # the lookup and the respective value is passed to SmartHomeNG as the value
        # for the item.
        # This makes it easy e.g. to convert numerical values into clear-text values
        # Note: setting this option ignores the ``settings`` parameters!
        'lookup': '<table_name>',

        # optional, specifies item attributes if struct file is generated by plugin
        'item_attrs': {

            # the following entries are directives for the struct.yaml generator

            # create md_read_initial: true entry
            # can also be specified for sections to trigger initial read group reading
            'initial': False,

            # create md_read_cycle entry with given cycle time
            # can also be specified for section to trigger cyclic read group reading
            'cycle': None,

            # create enforce_updates: true entry
            'enforce': False,

            # control autocreation of item read groups. None or key not present
            # means create all levels (default)
            # 0 means don't create read groups (not even from 'read_groups' dict!)
            # x (int > 0) means include the x lowest levels of read groups
            # e.g. if current item gets read groups 
            #      ['l1', 'l1.l2', 'l1.l2.l3', 'l1.l2.l3.l4'], setting
            #      read_group_levels': 2 will yield
            #      md_read_groups: ['l1.l2.l3', 'l1.l2.l3.l4']
            'read_group_levels': None,

            # create subitem 'lookup' containing lookup table
            # if lookup_item is True or 'list', the lookup will be type 'list'
            # otherwise specify 'lookup_item': 'fwd' / 'rev' / 'rci'
            'lookup_item': False,

            # attributes to add to the item definition verbatim
            # e.g. 'enforce_updates': 'true', 'md_initial_read': 'true'
            'attributes': {
                'attr1': 'value1',  
                'attr2': 'value2'
            },

            # additional read group configuration
            'read_groups': [
                {
                    # name of read group
                    'name': '<read group 1>',
                    # item path of trigger item to create
                    'trigger': 'path.to.item'
                },
                {
                    'name': '<read group 2>', 
                    'trigger': 'path.to.other.item'
                }
            ],
        }
    }
}

""" commands: nested definitions

If many commands are present, it might be beneficial to create a hierarchical
structure via nested dicts. This is simple as nesting can - more or less - be
used as you like. 
In the item definition, the combined command names from the following example
are:

* level1a.level2a.cmd1
* level1a.level2b.cmd1
* level1a.level2b.cmd2

Note that the two commands 'cmd1' are completely independent, as the internal
name includes the full path.
"""

commands = {
    'level1a': {
        'level2a': {
            'cmd1': {'contents': 'like first example'}
        },
        'level2b': {
            'cmd1': {'as': 'above'},
            'cmd2': {'still': 'unchanged'}
        }
    }
}

""" commands: model-specific definitions

The following commands example is for a scenario where different models are
configured and have overlapping command definitions with different contents.

The key on the first level specify the model or 'ALL' for commands common to
all models. 'ALL' needs to be present, even if it is an empty dict, as this
indicates the second definition syntax. Models not present on the first level
will load only the commands from the 'ALL' section.
Below the first level, commands are defined as in the first or second example,
nesting commands is supported.
There exist no dependencies between the different models.

In this case, the ``models`` dict (see next paragraph) is not necessary and
will be ignored.
"""

commands = {
    'ALL': {
        'cmd1': {'read': True, 'write': True, 'opcode': '1a', 'attrib': '...'}, 
        'cmd2': {'read': False, 'write': True, 'opcode': '2b', 'attrib': '...'}, 
    },
    'model1': {
        'cmd3': {'read': True, 'write': False, 'opcode': '3c', 'attrib': '...'}, 
        'cmd4': {'read': False, 'write': False, 'opcode': '4d', 'attrib': '...'}, 
    },
    'model3': {
        'cmd1': {'read': True, 'write': True, 'opcode': '3a', 'attrib': '...'},  # note different opcode
        'cmd3': {'read': True, 'write': False, 'opcode': '3z', 'attrib': '...'}, 
    },
    'model4': {
        'section1': {
            'cmd1': {'read': True, 'write': True, 'opcode': 'VI', 'attrib': '...'}, 
            'cmd2': {'read': False, 'write': True, 'opcode': 'VII', 'attrib': '...'}, 
        },
        'section2': {
            'cmd1': {'read': True, 'write': True, 'opcode': 'XX', 'attrib': '...'}, 
            'cmd2': {'read': False, 'write': True, 'opcode': 'YY', 'attrib': '...'},         
        }
    }
}

""" model: (optional) specifications for dev example

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

If the second variant (see example 3 above) of defining commands is chosen,
this dict will be ignored.

Hint: as this example only defines one command, the following example is purely
      fictional...
"""

models = {
    'ALL': ['cmd10', 'cmd11'],
    'model1': ['cmd1', 'cmd2', 'cmd3', 'cmd4'],
    'model2': ['cmd1', 'cmd2', 'cmd3', 'cmd5'],
    'model3': ['cmd1', 'cmd2', 'cmd4', 'cmd5', 'cmd6']
}


""" lookup: (optional) definition of lookup tables (see commands table)

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
"""

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

""" lookup: (optional) model-specific lookup tables
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
"""

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

""" structs: (optional) structs applicability for models

If the device supports models and provides structs, it may be that not
all struct apply to the specific device; e.g. a low-end AV receiver may
not have a second or third audio zone.

With this struct, you can define which structs apply to all devices and
which only to some devices. The syntax is identical to the ``models`` dict.

Even though the structs will be named multidevice.<device_id>.<struct_name>
in the item config, you must use the names from the ``structs.yaml`` file only.
"""

structs = {
    'ALL': ['general', 'control'],
    'model1': ['zone1'],
    'model2': ['zone1', 'zone2'],
    'model3': ['zone1', 'zone2', 'zone3', 'zonetwilight']
}
