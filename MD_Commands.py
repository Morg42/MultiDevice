#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file aims to become part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  MD_Commands for MultiDevice plugin
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
from pydoc import locate

if MD_standalone:
    from MD_Globals import *
    from MD_Command import MD_Command
    import datatypes as DT
else:
    from .MD_Globals import *
    from .MD_Command import MD_Command
    from . import datatypes as DT


#############################################################################################################################################################################################################################################
#
# class MD_Commands
#
#############################################################################################################################################################################################################################################

class MD_Commands(object):
    '''
    This class represents a command list to save some error handling code on
    every access (in comparison to using a dict). Not much more functionality
    here, most calls check for errors and pass thru the request to the selected
    MD_Command-object

    Furthermore, this could be overloaded if so needed for special extensions.
    '''
    def __init__(self, device_id, device_name, command_obj_class=MD_Command, **kwargs):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(__name__)

        self.logger.debug(f'Device {device_name}: commands initializing from {command_obj_class.__name__}')
        self._commands = {}
        self.device = device_name
        self._device_id = device_id
        self._cmd_class = command_obj_class
        self._plugin_params = kwargs
        self._dt = {}
        self._read_dt_classes(device_id)
        self._read_commands(device_name)

        if self._commands:
            self.logger.debug(f'Device {self.device}: commands initialized')
        else:
            self.logger.error(f'Device {self.device}: commands could not be initialized')

    def is_valid_command(self, command, read=None):
        if command not in self._commands:
            return False

        if read is None:
            return True

        # if the corresponding attribute is not defined, assume False (fail safe)
        return getattr(self._commands[command], 'read' if read else 'write', False)

    def get_send_data(self, command, data=None):
        if command in self._commands:
            return self._commands[command].get_send_data(data)

        return None

    def get_shng_data(self, command, data):
        if command in self._commands:
            return self._commands[command].get_shng_data(data)

        return None

    def get_command_from_reply(self, data):
        for command in self._commands:
            tokens = getattr(self._commands[command], 'reply_token', None)
            if tokens:
                if not isinstance(tokens, list):
                    tokens = [tokens]
                for token in tokens:
                    # NOTE: if token == '', this would always match. Maybe make this a feature?
                    if token != '' and token == data[:len(token)]:
                        return command
        return None

    def _read_dt_classes(self, device_id):
        '''
        This method enumerates all classes named 'DT_*' from the Datatypes module
        and tries to load custom 'DT_*' classes from the device's subdirectory
        datatypes.py file and collect all in the self._dt dict.
        Integrating custom classes into the DT module would change this for all
        loaded devices and name collisions could not be resolved.
        '''
        def _enum_dt_cls(mod):
            classes = [cls for cls in dir(mod) if cls[:3] == 'DT_']
            for cls in classes:
                self._dt[cls] = getattr(mod, cls)

        self._dt['Datatype'] = DT.Datatype

        # enumerate 'DT_*' classes from DT
        _enum_dt_cls(DT)

        # try to load datatypes.py from device directory
        mod_str = 'dev_' + device_id + '.datatypes'
        if not MD_standalone:
            mod_str = '.'.join(self.__module__.split('.')[:-1]) + '.' + mod_str

        cust_mod = locate(mod_str)
        if cust_mod:
            _enum_dt_cls(cust_mod)

    def _read_commands(self, device_name):
        '''
        This is the loader portion for the commands.py file.
        '''
        # did we get a device id?
        if not self._device_id:
            return

        # try to load commands.py from device directory
        mod_str = 'dev_' + self._device_id + '.commands'
        if not MD_standalone:
            mod_str = '.'.join(self.__module__.split('.')[:-1]) + '.' + mod_str

        commands = {}
        try:
            # get module
            cmd_module = locate(mod_str)
            # get content
            commands = cmd_module.commands
        except ImportError:
            self.logger.error(f'Device {device_name}: importing external module {"dev_" + self._device_id + "/commands.py"} failed')
        except Exception as e:
            self.logger.error(f'Device {device_name}: importing commands from external module {"dev_" + self._device_id + "/commands.py"} failed. Error was: {e}')
        if commands and isinstance(commands, dict):
            self._parse_commands(device_name, commands)

    def _parse_commands(self, device_name, commands):
        '''
        This is a reference implementation for parsing the commands dict imported
        from the device subdirectory.
        For special purposes, this can be overloaded, if you want to use your
        own file format.
        '''
        for cmd in commands:
            kw = {}
            for arg in ('opcode', 'read', 'write', 'item_type', 'dev_datatype', 'read_cmd', 'write_cmd', 'read_data', 'reply_token'):
                if arg in commands[cmd]:
                    kw[arg] = commands[cmd][arg]

            dt_class = None
            dev_datatype = kw.get('dev_datatype', '')
            if dev_datatype:
                class_name = '' if dev_datatype[:2] == 'DT_' else 'DT_' + dev_datatype
                dt_class = self._dt.get(class_name)

            if kw.get('read', False) and kw.get('opcode', '') == '' and kw.get('read_cmd', '') == '':
                self.logger.info(f'Device {self.device}: command {cmd} will not create a command for reading values. Check commands.py configuration...')
            if kw.get('write', False) and kw.get('opcode', '') == '' and kw.get('write_cmd', '') == '':
                self.logger.info(f'Device {self.device}: command {cmd} will not create a command for writing values. Check commands.py configuration...')
            if not dt_class:
                self.logger.error(f'Device {device_name}: importing commands found invalid datatype {dev_datatype}, replacing with DT_raw. Check function of device')
                dt_class = DT.DT_raw
            self._commands[cmd] = self._cmd_class(self.device, cmd, dt_class, **{'cmd': kw, 'plugin': self._plugin_params})
