#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file aims to become part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  MD_Command and derived classes for MultiDevice plugin
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

import logging
import re

from .MD_Globals import *
from . import datatypes as DT


#############################################################################################################################################################################################################################################
#
# class MD_Command
#
#############################################################################################################################################################################################################################################

class MD_Command(object):
    '''
    This class represents a general command that uses read_cmd/write_cmd or, if
    not present, opcode as payload for the connection. Data is supplied in the
    'data'-key values in the data_dict. DT type conversion is applied with default
    values.
    This class serves as a base class for further format-specific command types.
    '''
    device = ''
    name = ''
    opcode = ''
    read = False
    write = False
    item_type = None
    _DT = None

    def __init__(self, device_name, command, dt_class, **kwargs):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(__name__)

        if not device_name:
            self.logger.warning(f'Device (unknown): building command {command} without a device, aborting')
        else:
            self.device = device_name

        if not command:
            self.logger.warning(f'Device {self.device}: building command without a name, aborting')
            return
        else:
            self.name = command

        kw = kwargs['cmd']
        self._plugin_params = kwargs['plugin']

        self._get_kwargs(('opcode', 'read', 'write', 'item_type'), **kw)

        try:
            self._DT = dt_class()
        except Exception as e:
            self.logger.error(f'Device {device_name}: building command {command} failed on instantiating datatype class {dt_class}. Error was {e}')
            self._DT = DT.DT_raw()

        # only log if base class. Derived classes log their own messages
        if self.__class__ is MD_Command:
            self.logger.debug(f'Device {self.device}: learned command {command} with device data type {dt_class}')

    def get_send_data(self, data):
        # create read data
        if data is None:
            if self.read_cmd:
                cmd = self.read_cmd
            else:
                cmd = self.opcode
        else:
            if self.write_cmd:
                cmd = self.write_cmd
            else:
                cmd = self.opcode

        return {'payload': cmd, 'data': self._DT.get_send_data(data)}

    def get_shng_data(self, data):
        value = self._DT.get_shng_data(data)
        return value

    def _get_kwargs(self, args, **kwargs):
        '''
        check if any items from args is present in kwargs and set the class property
        of the same name to its value.

        :param args: list or tuple of parameter names
        :type args: list | tuple
        '''
        for arg in args:
            if kwargs.get(arg, None):
                setattr(self, arg, kwargs[arg])


class MD_Command_Str(MD_Command):
    '''
    This class represents a command which uses a string with arguments as payload,
    for example as query URL.

    For sending, the read_cmd/write_cmd strings, opcode and data are parsed
    (recursively), to enable the following parameters:

    - '$C' is replaced with the opcode,
    - '$P:attr:' is replaced with the value of the attr element from the plugin configuration,
    - '$V' is replaced with the given value

    The returned data is only parsed by the DT_... classes.
    For the DT_json class, the read_data dict can be used to extract a specific
    element from a json response:

    ``read_data = {'dict': ['key1', 'key2', 'key3']}``

    would try to get

    ``json_response['key1']['key2']['key3']``

    and return it as the read value.

    This class is provided as a reference implementation for the Net-Connections.
    '''
    read_cmd = None
    write_cmd = None
    read_data = None
    params = {}
    values = {}
    bounds = {} 
    _DT = None

    def __init__(self, device_name, name, dt_class, **kwargs):

        super().__init__(device_name, name, dt_class, **kwargs)

        kw = kwargs['cmd']
        self._plugin_params = kwargs['plugin']

        self._get_kwargs(('read_cmd', 'write_cmd', 'read_data', 'params', 'values', 'bounds'), **kw)

        self.logger.debug(f'Device {self.device}: learned command {self.name} with device data type {dt_class.__name__}')

    def get_send_data(self, data):
        # create read data
        if data is None:
            if self.read_cmd:
                cmd_str = self._parse_str(self.read_cmd)
            else:
                cmd_str = self._parse_str(self.opcode, data)
        else:
            if self.write_cmd:
                cmd_str = self._parse_str(self.write_cmd, data)
            else:
                cmd_str = self._parse_str(self.opcode, data)

        data_dict = {}
        data_dict['payload'] = cmd_str
        for k in self.params.keys():
            data_dict[k] = self._parse_tree(self.params[k], data)

        return data_dict

    def _parse_str(self, string, data=None):
        '''
        parse string and replace
        - $C with the command opcode
        - $P:<elem>: with the plugin parameter
        - $V with the data value

        The replacement order ensures that $P-patterns from the opcode can be replaced
        as well as $V-pattern in any of the strings.
        '''
        def repl_func(matchobj):
            return str(self._plugin_params.get(matchobj.group(2), ''))

        string = string.replace('$C', self.opcode)

        regex = '(\\$P:([^:]+):)'
        while re.match('.*' + regex + '.*', string):
            string = re.sub(regex, repl_func, string)

        if data is not None:
            string = string.replace('$V', str(self._DT.get_send_data(data)))

        return string

    def _parse_tree(self, node, data):
        '''
        traverse node and
        - apply _parse_str to strings
        - recursively _parse_tree for all elements of iterables or
        - return unknown or unparseable elements unchanged
        '''
        if issubclass(node, str):
            return self._parse_str(node, data)
        elif issubclass(node, list):
            return [self._parse_tree(k, data) for k in node]
        elif issubclass(node, tuple):
            return (self._parse_tree(k, data) for k in node)
        elif issubclass(node, dict):
            new_dict = {}
            for k in node.keys():
                new_dict[k] = self._parse_tree(node[k], data)
            return new_dict
        else:
            return node
