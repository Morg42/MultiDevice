#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file aims to become part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  tool for creating structs from MultiDevice command definitions
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

""" tool for creating structs from MultiDevice command definitions

This tool takes the commands.py in the current folder and creates a struct.yaml
from it.

If the commands dict is in "generic/model" form (contains 'ALL' key), the tool
will create one struct for each model (with the commands from the 'ALL' key
combined); otherwise it will create a struct for each top-level key in the
commands dict.

It will create read groups and associated read trigger items on every nesting
level and assign each item to all ancestor read groups.

The structs will contain ``md_device: DEVICENAME`` for parsing by the
MultiDevice plugin on startup.

Usage: python3 /path/to/multidevice/tools/cmd2struct.py [<model>]

If a model is specified, the tool will create structs only for this model;
if model is not specified, it will process all models and commands.
"""

import sys
from commands import commands

# change if you feel like it...
INDENTWIDTH = 4


INDENT = ' ' * INDENTWIDTH
MODELINE = f'# vim: expandtab:ts={INDENTWIDTH}:sw={INDENTWIDTH}'


def walk(node, node_name, parent, func, path, indent, gpath, gpathlist, has_models):
    """ traverses a nested dict

    :param node: starting node
    :param node_name: name of the starting node on parent level ("key")
    :param parent: parent node
    :param func: function to call for each node
    :param path: path of the current node (pparent.parent.node)
    :param indent: indent level (indent is INDENT ** indent)
    :param gpath: path of "current" (next above) read group
    :param gpathlist: list of all current (above) read groups
    :param has_models: True is command dict has models ('ALL') -> then include top level = model name in read groups
    :type node: dict
    :type node_name: str
    :type parent: dict
    :type func: function
    :type path: str
    :type indent: int
    :type gpath: str
    :type gpathlist: list
    :type has_models: bool
    """

    # first call func -> print current node before descending
    if func is not None:
        func(node, node_name, parent, path, indent, gpath, gpathlist)

    # iterate over all children who are dicts
    for child in list(k for k in node.keys() if isinstance(node[k], dict)):

        # and recursively walk them. path and gpathlist is a bit messy...
        walk(node[child], child, node, func, (path if path else ('' if has_models else node_name)) + ('.' if path or not has_models else '') + child, indent + 1, path, gpathlist + ([path] if path else []), has_models)


def print_item(node, node_name, parent, path, indent, gpath, gpathlist):
    """ print item or read item for current node/command

    for params see walk() above, they are the same there
    """
    def _p_text(text, add=0):
        """ print indented text """
        print(f'{INDENT * (indent + 1 + add)}{text}')

    def _p_attr(key, val, add=0):
        """ print indented 'key: node[val]' """
        if val in node:
            print(f'{INDENT * (indent + 1 + add)}{key}: {node[val]}')

    # skip known command sub-dict nodes, but include command nodes
    if node_name not in ('settings', 'params', 'param_values') or 'item_type' in node:

        # item / level definition
        print(INDENT * indent + node_name + ':')

        # item -> print item attributes
        if 'item_type' in node:
            _p_attr('type', 'item_type')
            _p_text('md_device: DEVICENAME')
            _p_text(f'md_command: {path if path else node_name}')
            _p_attr('md_read', 'read')
            _p_attr('md_write', 'write')
            _p_text(f'md_read_group: {gpathlist}')
            print()

        # "level node" -> print read item
        elif node_name not in ('settings', 'params', 'param_values'):
            print()
            _p_text('read:')
            _p_text('type: bool', 1)
            _p_text('enforce_updates: true', 1)
            _p_text('md_device: DEVICENAME', 1)
            _p_text(f'md_read_group_trigger: {path if path else node_name}', 1)
            print()


if len(sys.argv) > 1:
    devices = [sys.argv[1]]
else:
    devices = list(commands.keys())

print('%YAML 1.1')
print('---')
print(MODELINE)

has_models = False

if 'ALL' in devices:
    has_models = True
    devices.remove('ALL')

for dev in devices:
    # get dict as ref
    c = {dev: commands[dev]}

    # add in 'ALL' commands if present
    # each key is only visited once, so we can risk changing the `commands` dict
    c[dev].update(commands.get('ALL', {}))

    # traverse from root node
    walk(c[dev], dev, commands, print_item, '', 0, dev, [dev], has_models)
