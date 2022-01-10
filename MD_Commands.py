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
import re
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
    """ MD_Commands class for managing commands support

    This class represents a command list to save some error handling code on
    every access (in comparison to using a dict). Not much more functionality
    here, most calls check for errors and pass thru the request to the selected
    MD_Command-object

    Furthermore, this could be overloaded if so needed for special extensions.
    """
    def __init__(self, device_type, device_id, command_obj_class=MD_Command, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        self.logger.debug(f'commands initializing from {command_obj_class.__name__}')
        self._commands = None         # { 'cmd_x': MD_Command(params), ... }
        self._lookups = {}          # { 'name_x': {'fwd': {'K1': 'V1', ...}, 'rev': {'V1': 'K1', ...}, 'rci': {'v1': 'K1', ...}}}
        self._lookup_tables = []
        self.device_id = device_id
        self._device_type = device_type
        self._cmd_class = command_obj_class
        self._plugin_params = {}
        self._plugin_params.update(kwargs)

        self._model = self._plugin_params.get('model', None)

        self._dt = {}
        self._return_value = None
        self._read_dt_classes(device_type)
        if not self._read_commands(device_id):
            return None

        if self._commands is not None:
            self.logger.debug(f'{len(self._commands)} commands initialized')
        elif not MD_standalone:
            self.logger.error('commands could not be initialized')

    def is_valid_command(self, command, read=None):
        if command not in self._commands:
            return False

        if read is None:
            return True

        # if the corresponding attribute is not defined, assume False (fail safe)
        return getattr(self._commands[command], 'read' if read else 'write', False)

    def get_send_data(self, command, data=None, **kwargs):
        if command in self._commands:
            lu = self._get_cmd_lookup(command)
            if lu:
                data = self._lookup(data, lu, rev=True)
            return self._commands[command].get_send_data(data, **kwargs)

        raise Exception(f'command {command} not found in commands')

    def get_shng_data(self, command, data, **kwargs):
        if command in self._commands:
            result = self._commands[command].get_shng_data(data, **kwargs)
            lu = self._get_cmd_lookup(command)
            if lu:
                result = self._lookup(result, lu)
            return result

        raise Exception(f'command {command} not found in commands')

    def get_command_from_reply(self, data):
        if type(data) in (bytes, bytearray):
            data = str(data.decode('utf-8'))

        for command in self._commands:
            tokens = getattr(self._commands[command], 'reply_token', None)
            if tokens:
                if not isinstance(tokens, list):
                    tokens = [tokens]
                for token in tokens:
                    if token == 'REGEX' and getattr(self._commands[command], 'reply_pattern', None):

                        # token is "REGEX" - parse read_cmd as regex
                        try:
                            regex = re.compile(getattr(self._commands[command], 'reply_pattern'))
                            if regex.match(data) is not None:
                                self.logger.debug(f'matched reply_pattern {getattr(self._commands[command], "reply_pattern")} as regex against data {data}, found command {command}')
                                return command
                        except Exception as e:
                            self.logger.warning(f'parsing or matching reply_pattern {getattr(self._commands[command], "reply_pattern")} from command {command} as regex failed. Error was: {e}. Ignoring')
                    elif token != '' and token == data[:len(token)]:

                        # token ist just a string
                        return command
        return None

    def get_lookup(self, lookup, type='fwd'):
        """ returns the contents of the lookup table named <lookup>, None on error """
        if lookup in self._lookups and type in ('fwd', 'rev', 'rci'):
            return self._lookups[lookup][type]
        else:
            return None

    def _lookup(self, data, table, rev=False, ci=True):
        """
        try to lookup data from lookup dict <table>

        normal mode is device data -> shng data (rev=False, ci is ignored)
        reverse mode is shng data -> device data (rev=True, ci=False)
        ci mode is reverse mode, but case insensitive lookup (rev=True, ci=True, default for rev)

        As data is used as key in dict lookups, it must be a hashable type (num, int, float, str)

        Per definition, data can be None, e.g. for read commands. In this case, return None

        On success, lookup result is returned. On error, an exception is raised.

        :param data: data to look up
        :param table: name of lookup dict
        :param rev: reverse mode (see above)
        :param ci: case insensitive reverse mode (see above)
        :type table: str
        :type rev: bool
        :type ci: bool
        :return: lookup result
        """
        if data is None:
            return None

        mode = 'fwd'
        if rev:
            mode = 'rci' if ci else 'rev'

        lu = self.get_lookup(table, mode)
        if not lu:
            raise ValueError(f'Lookup table {table} not found.')

        if rev and ci and isinstance(data, str):
            data = data.lower()

        if data in lu:
            return lu[data]

        raise ValueError(f'Lookup of value {data} in table {table} failed, entry not found.')            

    def _get_cmd_lookup(self, command):
        """ returns lookup name for command or None """
        if command in self._commands:
            return self._commands[command].get_lookup()

        raise Exception(f'command {command} not found in commands')

    def _read_dt_classes(self, device_type):
        """
        This method enumerates all classes named 'DT_*' from the Datatypes module
        and tries to load custom 'DT_*' classes from the device's subdirectory
        datatypes.py file and collect all in the self._dt dict.
        Integrating custom classes into the DT module would change this for all
        loaded devices and name collisions could not be resolved.
        """
        def _enum_dt_cls(mod):
            classes = [cls for cls in dir(mod) if cls[:3] == 'DT_']
            for cls in classes:
                self._dt[cls] = getattr(mod, cls)

        self._dt['Datatype'] = DT.Datatype

        # enumerate 'DT_*' classes from DT
        _enum_dt_cls(DT)

        # try to load datatypes.py from device directory
        mod_str = 'dev_' + device_type + '.datatypes'
        if not MD_standalone:
            mod_str = '.'.join(self.__module__.split('.')[:-1]) + '.' + mod_str

        cust_mod = locate(mod_str)
        if cust_mod:
            _enum_dt_cls(cust_mod)

    def _read_commands(self, device_id):
        """
        This is the loader portion for the commands.py file.

        Errors preventing the device from working raise `Exception`
        """
        # did we get a device type?
        if not self._device_type:
            raise Exception('device_type not set, not reading commands')

        # try to load commands.py from device directory
        mod_str = 'dev_' + self._device_type + '.commands'
        if not MD_standalone:
            mod_str = '.'.join(self.__module__.split('.')[:-1]) + '.' + mod_str

        try:
            # get module
            cmd_module = locate(mod_str)
        except ImportError:
            raise CommandsError(f'importing external module {"dev_" + self._device_type + "/commands.py"} failed')
        except Exception as e:
            raise CommandsError(f'importing commands from external module {"dev_" + self._device_type + "/commands.py"} failed. Error was: "{e}"')
            return False

        if self._model == INDEX_GENERIC:
            self.logger.warning('configured model is identical to generic identifier, loading all commands.')
            self._model = None

        if self._model:
            if hasattr(cmd_module, 'models'):
                if isinstance(cmd_module.models, dict):
                    if self._model in cmd_module.models:
                        self.logger.info(f'model {self._model} identified')
                    else: 
                        raise CommandsError(f'configured model {self._model} not found in commands.py models {cmd_module.models.keys()}')
                else:
                    raise CommandsError(f'model configuration for device type {self._device_type} invalid, "models" is not a dict')
            else:
                self.logger.warning(f'plugin configuration wants model {self._model}, but device type {self._device_type} has no model configuration. Loading all commands...')
                self._model = None

        if hasattr(cmd_module, 'commands') and isinstance(cmd_module.commands, dict) and not MD_standalone:
            cmds = cmd_module.commands
            cmdlist = None
            if INDEX_GENERIC in cmds:
                if self._model in cmds[INDEX_GENERIC]:
                    cmds = cmds[INDEX_GENERIC][self._model]
                elif not self._model:
                    self.logger.debug('model set to empty string, not loading commands. You have been warned...')
                    cmds = {}
                else:
                    raise CommandsError(f'commands require configuration attribute "model", but model {self._model + " not set in commands dict" if self._model else "unknown"}.')

            if self._model:
                cmdlist = cmd_module.models.get(INDEX_GENERIC, []) + cmd_module.models.get(self._model, [])
                self.logger.debug(f'found {len(cmd_module.models.get(INDEX_GENERIC, []))} generic commands')
                if self._model:
                    self.logger.debug(f'found {len(cmd_module.models.get(self._model, []))} commands for model {self._model}')
            if cmdlist is None:
                cmdlist = cmds.keys()

            # remove command hierarchy
            cmdlist = self._flatten_commands(cmds, cmdlist)

            # actually import commands
            self._parse_commands(device_id, cmds, cmdlist)
        else:
            if not MD_standalone:
                self.logger.warning('no command definitions found. This device probably will not work...')

        if hasattr(cmd_module, 'lookups') and isinstance(cmd_module.lookups, dict):
            self._parse_lookups(device_id, cmd_module.lookups)
        else:
            self.logger.debug('no lookups found')

        return True

    def _flatten_commands(self, commands_dict, command_list):
        """ move nested command definitions to same level, adjust names """
        def walk(node, node_name, parent=None, func=None):
            for child in list(k for k in node.keys() if isinstance(node[k], dict)):
                walk(node[child], child, parent=node, func=func)
            if func:
                func(node, node_name, parent=parent)

        def moveItems(node, node_name, parent):
            # make sure we can move "upwards"
            if parent:
                # if node['opcode'] is not present, node is not a command
                if 'opcode' not in node:
                    for child in list(k for k in node.keys() if isinstance(node[k], dict)):
                        # node has dict elements node[child]
                        parent[node_name + "." + child] = node[child]
                        del node[child]

        def removeEmptyItems(node, node_name, parent):
            if len(node) == 0:
                del parent[node_name]

        # flatten cmds
        walk(commands_dict, '', None, moveItems)

        # remove empty dicts (old 'level names')
        walk(commands_dict, '', None, removeEmptyItems)

        new_cmdlist = []
        for cmd in commands_dict:
            if any(cmdspec == cmd[:len(cmdspec)] for cmdspec in command_list):
                new_cmdlist.append(cmd)

        return new_cmdlist

    def _parse_commands(self, device_id, commands, cmds=[]):
        """
        This is a reference implementation for parsing the commands dict imported
        from the commands.py file in the device subdirectory.
        For special purposes, this can be overloaded, if you want to use your
        own file format.
        """
        self._commands = {}

        for cmd in cmds:
            kw = {}
            for arg in COMMAND_PARAMS:
                if arg in commands[cmd]:
                    kw[arg] = commands[cmd][arg]

            # if valid_list_ci is present in settings, convert all str elements to lowercase only once
            if 'settings' in kw:
                if 'valid_list_ci' in kw['settings']:
                    kw['settings']['valid_list_ci'] = [entry.lower() if isinstance(entry, str) else entry for entry in kw['settings']['valid_list_ci']]

            dt_class = None
            dev_datatype = kw.get('dev_datatype', '')
            if dev_datatype:
                class_name = '' if dev_datatype[:2] == 'DT_' else 'DT_' + dev_datatype
                dt_class = self._dt.get(class_name)

            if kw.get('read', False) and kw.get('opcode', '') == '' and kw.get('read_cmd', '') == '':
                self.logger.info(f'command {cmd} will not create a command for reading values. Check commands.py configuration...')
            if kw.get('write', False) and kw.get('opcode', '') == '' and kw.get('write_cmd', '') == '':
                self.logger.info(f'command {cmd} will not create a command for writing values. Check commands.py configuration...')
            if not dt_class:
                self.logger.error(f'importing command {cmd} found invalid datatype "{dev_datatype}", replacing with DT_raw. Check function of device')
                dt_class = DT.DT_raw
            self._commands[cmd] = self._cmd_class(self.device_id, cmd, dt_class, **{'cmd': kw, 'plugin': self._plugin_params})

    def _parse_lookups(self, device_id, lookups):
        """
        This is a reference implementation for parsing the lookups dict imported
        from the commands.py file in the device subdirectory.
        For special purposes, this can be overloaded, if you want to use your
        own file format.
        """
        if INDEX_GENERIC in lookups:
            lu = lookups[INDEX_GENERIC]
            self.logger.debug(f'found {len(lu)} generic lookup table{"" if len(lu) == 1 else "s"}')

            if self._model and self._model in lookups:
                lu.update(lookups[self._model])
                self.logger.debug(f'found {len(lookups[self._model])} lookup table{"" if len(lookups[self._model]) == 1 else "s"} for model {self._model}')
        else:
            lu = lookups

        try:
            for table in lu:
                if isinstance(lu[table], dict):

                    self._lookups[table] = {}

                    # original dict
                    self._lookups[table]['fwd'] = lu[table]
                    # reversed dict
                    self._lookups[table]['rev'] = {v: k for (k, v) in lu[table].items()}
                    # reversed dict, keys are lowercase for case insensitive lookup
                    self._lookups[table]['rci'] = {v.lower() if isinstance(v, str) else v: k for (k, v) in lu[table].items()}

                    self._lookup_tables.append(table)
                    self.logger.debug(f'imported lookup table {table} with {len(lu[table])} items')
                else:
                    self.logger.warning(f'key {table} in lookups not in dict format, ignoring')
        except Exception as e:
            self.logger.error(f'importing lookup tables not possible, check syntax. Error was: {e}')
