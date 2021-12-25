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

if MD_standalone:
    from MD_Globals import *
    import datatypes as DT
else:
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

    For attributes defined in commands.py, see explanation in the
    dev_example/commands.py file.

    This class serves as a base class for further format-specific command types.
    '''
    device = ''
    name = ''
    opcode = ''
    read = False
    write = False
    read_cmd = None
    write_cmd = None
    item_type = None
    reply_token = []
    reply_pattern = ''
    settings = None
    _DT = None

    def __init__(self, device_name, command, dt_class, **kwargs):

        # get MultiDevice.device logger (if not already defined by derived class calling us via super().__init__())
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_name}')

        if not device_name:
            self.logger.warning(f'building command {command} without a device, aborting')
        else:
            self.device = device_name

        if not command:
            self.logger.warning(f'building command without a name, aborting')
            return
        else:
            self.name = command

        kw = kwargs['cmd']
        self._plugin_params = kwargs['plugin']

        self._get_kwargs(COMMAND_PARAMS, **kw)

        try:
            self._DT = dt_class()
        except Exception as e:
            self.logger.error(f'building command {command} failed on instantiating datatype class {dt_class}. Error was: {e}')
            self._DT = DT.DT_raw()

        # only log if base class. Derived classes log their own messages
        if self.__class__ is MD_Command:
            self.logger.debug(f'learned command {command} with device datatype {dt_class}')

    def get_send_data(self, data):

        cmd = None

        data = self._check_value(data)

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

    def _check_min_max(self, data, key, min=True, force=False):
        ''' helper routine to check for min/max compliance and int/float type '''
        # if self.settings.get(key, None): this results in False if value is 0!
        if key in self.settings:
            bound = self.settings[key]
            if not isinstance(data, type(bound)):
                if type(data) is float and type(bound) is int:
                    data = int(data)
                elif type(data) is int and type(bound) is float:
                    data = float(data)
                else:
                    raise ValueError(f'Invalid data: type {type(data)} ({data}) given for {type(bound)} ({bound})')
            if (min and data >= bound) or (not min and data <= bound):
                return data
            if force:
                self.logger.debug(f'Value {data} changed to {bound} due to settings {self.settings}')
                return bound
            raise ValueError(f'Invalid data: value {data} not adhering to {"min" if min else "max"} value {bound}')
        return data

    def _check_value(self, data):
        '''
        check if value settings are defined and if so, if they are followed
        possibly adjust data in accordance with settings or do some magic ('read_val')

        non-compliance will raise ValueError

        This can be overloaded; make sure to (first?) call 
        data = super()._check_value(data)
        to run this code in addition to your own extension, if applicable

        :param data: data/value to send
        :return: adjusted data
        '''
        if data is not None:
            try:
    
                minmaxkeys = ['min', 'max', 'force_min', 'force_max']
                if self.settings:
                    if self.settings.get('read_val', None):
                        # if data == read_val, trigger force reading value from device by not providing data to command
                        if data == self.settings['read_val']:
                            return None
                    elif self.settings.get('valid_list', None):
                        if data not in self.settings['valid_list']:
                            raise ValueError(f'Invalid data: value {data} not in list {self.settings["valid_list"]}')
                    elif any(key in self.settings.keys() for key in minmaxkeys):
                        for key in minmaxkeys:
                            data = self._check_min_max(data, key, key[-3:] == 'min', key[:5] == 'force')

            except Exception as e:
                raise ValueError(f'Given value {data} for command {self.name} not valid according to settings {self.settings}. Error was: {e}')

        return data


class MD_Command_Str(MD_Command):
    '''
    This class represents a command which uses a string with arguments as payload,
    for example as query URL.

    Default behaviour is identical to MD_Command_Str.

    For sending, the read_cmd/write_cmd strings, opcode and data are parsed
    (recursively), to enable the following parameters:

    - 'MD_OPCODE' is replaced with the opcode,
    - 'MD_PARAM:attr:' is replaced with the value of the attr element from the plugin configuration,
    - 'MD_VALUE' is replaced with the given value (converted by DT-class)

    The returned data is only parsed by the DT_... classes.
    For the DT_json class, the read_data dict can be used to extract a specific
    element from a json response:

    ``read_data = {'dict': ['key1', 'key2', 'key3']}``

    would try to get

    ``json_response['key1']['key2']['key3']``

    and return it as the read value.

    This class is provided as a reference implementation for the Net-Connections.
    '''
    read_data = None

    def get_send_data(self, data):

        data = self._check_value(data)

        if data is None:
            # create read data
            if self.read_cmd:
                cmd_str = self._parse_str(self.read_cmd)
            else:
                cmd_str = self._parse_str(self.opcode, data)
        else:
            # create write data
            if self.write_cmd:
                cmd_str = self._parse_str(self.write_cmd, data)
            else:
                cmd_str = self._parse_str(self.opcode, data)

        data_dict = {}
        data_dict['payload'] = cmd_str
        for k in self._plugin_params.keys():
            data_dict[k] = self._parse_tree(self.params[k], data)

        return data_dict

    def _parse_str(self, string, data=None):
        '''
        parse string and replace
        - MD_OPCODE with the command opcode
        - MD_PARAM:<elem>: with the plugin parameter
        - MD_VALUE with the data value

        The replacement order ensures that $P-patterns from the opcode can be replaced
        as well as $V-pattern in any of the strings.
        '''
        def repl_func(matchobj):
            return str(self._plugin_params.get(matchobj.group(2), ''))

        string = string.replace('MD_OPCODE', self.opcode)

        regex = '(MD_PARAM:([^:]+):)'
        while re.match('.*' + regex + '.*', string):
            string = re.sub(regex, repl_func, string)

        if data is not None:
            string = string.replace('MD_VALUE', str(self._DT.get_send_data(data)))

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


class MD_Command_ParseStr(MD_Command_Str):
    '''
    With this class, you can simplify the creation of read and write commands
    containing data values. 

    Default behaviour is identical to MD_Command_Str.

    Giving write_cmd as ':<write expression>:' (note colons) will format the
    given string (without the colons), replacing 'VAL' with the value by using
    write_cmd.format(VAL=data_dict['payload']), so you can immediately embed 
    the value in the command string with configurable formatting conforming 
    to str.format() syntax.
    If you have to start and end the command string with colons, just use
    '::foo::' as write_cmd. If you absolutely HAVE to use a literal
    ':foo{VAL}bar:', you might need to write your own class...

    Giving reply_pattern as '<regex>' with one (1) match group will try and 
    capture the matched group into the received value.

    Giving reply_pattern as '<regex>' without capturing parentheses will return
    the reply value as is (can possibly be converted by the DT class).

    HINT: If you give reply_pattern as regex and reply_token as 'REGEX', the
    reply_pattern regex will be used to identify a reply as belonging to this
    command if a match is found.

    Both results can be achieved with customized DT_foo classes, but this
    might be an easier and cleaner solution. Please make sure to understand
    MRE by JF properly :)
    '''

    def get_send_data(self, data):

        data = self._check_value(data)

        if data is None:
            # create read data
            if self.read_cmd:
                cmd_str = self._parse_str(self.read_cmd)
            else:
                cmd_str = self._parse_str(self.opcode, data)
        else:
            # create write data
            if self.write_cmd:
                # test if write_cmd is ':foo:' to trigger formatting/substitution
                if self.write_cmd[0] == ':' and self.write_cmd[-1] == ':':
                    cmd_str = self._parse_str(self.write_cmd[1:-1].format(VAL=data))
                else:
                    cmd_str = self._parse_str(self.write_cmd, data)
            else:
                cmd_str = self._parse_str(self.opcode, data)

        return {'payload': cmd_str, 'data': None if data is None else self._DT.get_send_data(data)}

    def get_shng_data(self, data):
        '''
        Try to match data to reply_pattern if reply_pattern is set.

        If a match is found and a value is captured, it will be returned.

        If a match is found without a capturing group, the value will be
        returned as-is, possibly to be converted by the DT class.

        If no match can be achieved, it is not possible to return 
        a meaningful value. To signal the error, an exception will be raised.
        '''
        if self.reply_pattern:
            regex = re.compile(self.reply_pattern)
            match = regex.match(data)
            if match:
                if len(match.groups()) == 1:

                    # one captured group - ok
                    value = self._DT.get_shng_data(match.group(1))
                elif len(match.groups()) > 1:

                    # more than one captured group - error
                    raise ValueError(f'reply_pattern {self.reply_pattern} has more than one pair of capturing parentheses')
                else:

                    # no captured groups = no parentheses = no extraction of value, just do the "normal" thing
                    value = self._DT.get_shng_data(data)
            else:
                raise ValueError(f'reply_pattern {self.reply_pattern} could not get a match on {data}')
        else:
            value = self._DT.get_shng_data(data)
        return value
