#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file aims to become part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  MultiDevice plugin for handling arbitrary devices via network or serial
#  connection.
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

'''
    The MultiDevice-Plugin (MD)
    ===========================

    This plugin aims to support a wide range of devices which work by sending
    commands to the device and reading data from it.
    By abstracting devices and connections, most devices will be able to be
    interfaced by this plugin.

    Base Classes
    ============

    MultiDevice
    -----------

    The ``MultiDevice``-class is derived from the SmartPlugin-class and provides
    the framework for handling item associations to the plugin, for storing
    item-command associations, for forwarding commands and the associated data
    to the device classes and receiving data from the device classes to update
    item values.
    This class will usually not need to be adjusted, but runs as the plugin itself.


    MD_Device
    ---------

    The ``MD_Device``-class provides a framework for receiving (item) data values
    from the plugin and forward it to the connection class and vice versa.
    A basic framework for managing the device, i.e. (re-)configuring, starting
    and stopping the device is already implemented and can be used without code
    changed by device configuration.

    ``MD_Device(device_id, device_name, **kwargs)``

    Public methods:

    - ``start()``
    - ``stop()``
    - ``send_command(command, value=None)``
    - ``read_all_commands()``
    - ``data_received(command, data)``
    - ``is_valid_command(command, read=None)``
    - ``set_runtime_data(**kwargs)``
    - ``update_device_params(**kwargs)``

    Methods possible to overload for inherited classes:

    - ``run_standalone()``
    - ``_set_device_params(**kwargs)``
    - ``_get_connection()``


    MD_Connection
    -------------

    This class and the derived classes provide frameworks for sending and receiving
    data to and from devices via serial or network connections. For both hardware
    layers implementation of query-response-connections and listening servers
    with asynchronous push-to-callback are already available.
    If more complex communication setup is needed, this can be implemented on top
    of the existing classes.

    Data is exchanged with ``MD_Device`` in a special dict format:

        data_dict = {
            'payload': raw data as needed by the connection}
            'kw1': additional 'keyword' args or data specific to the connection type
            'kw2': additional 'keyword' args or data specific to the connection type
            '...': additional 'keyword' args or data specific to the connection type
        }


    ``MD_Connection(device_id, device_name, data_received_callback, **kwargs)``

    Public methods:

    - ``open()``
    - ``close()``
    - ``send(data_dict)``

    Methods necessary to overload for inherited classes:

    - ``_open()``
    - ``_close()``
    - ``_send(data_dict)``


    Methods possible to overload for inherited classes:

    - ``_send_init_on_open()``
    - ``_send_init_on_send()``


    This class has subclasses defined for the following types of connection:

    - ``MD_Connection_Net_TCP_Client`` for query-reply TCP connections
    - ``MD_Connection_Net_TCP_Server`` for TCP listening server with async callback
    - ``MD_Connection_Net_UDP_Server`` for UDP listering server with async callback
    - ``MD_Connection_Serial_Client`` for query-reply serial connections
    - ``MD_Connection_Serial_Async`` for event-loop serial connection with async callback

    For detailed information and necessary configuration parameters, see the
    respective class definition docstring.


    MD_Commands
    -----------

    This class is a 'dict on steroids' of ``MD_Command``-objects with error checking as
    added value. In addition, it also loads command definitions from the file
    ``commands.py`` in the device folder and datatype sets and handles datatype association.

    No need to find out if ``command`` is defined, just call the method
    and the class will handle failure cases. Beware of NoneType-return values, though.

    ``MD_Commands(device_id, device_name, command_obj_class=MD_Command, **kwargs)``

    Public methods:

    - ``is_valid_command(command, read=None)``
    - ``get_send_data(command, data=None)``
    - ``get_shng_data(command, data)``

    Methods possible to overload:

    - ``_parse_commands(device_name, commands)``


    MD_Command
    ----------

    This class contains information concerning the command name, the opcode or
    URL needed to issue the command, and information about datatypes expected by
    SmartHomeNG and the device itself.

    Its contents will be initialized by the ``MD_Commands``-class while reading the
    command configuration.

    ``MD_Command(device_name, command_name, dt_class, **kwargs)``

    Public methods:

    - ``get_send_data(data)``
    - ``get_shng_data(data)``

    Methods possible to overload:

    - ``get_send_data(data)``
    - ``get_shng_data(data)``


    The class ``MD_Command_Str`` is an example for defining own commands according
    to your needs.

    This utilizes strings and dicts to build request URLs as payload data for the
    ``MD_Connection_Net_TCP_Client`` class.


    MD_Datatype
    -----------

    This is one of the most important classes. By declaration, it contains
    information about the data type and format needed by a device and methods
    to convert its value from selected Python data types used in items to the
    (possibly) special data formats required by devices and vice versa.

    Datatypes are specified in subclasses of Datatype with a nomenclature
    convention of `DT_<device data type of format>`.

    All default datatype classes are imported from ``datatypes.py`` into the 'DT' module.

    New devices can ship their own needed datatype classes in a file calles
    ``datatypes.py`` in the device's folder.

    For details concernin API and implementation, refer to the reference classes as
    examples.

    ``Datatype(fail_silent=True)``

    Public methods:

    - ``get_send_data(data)``
    - ``get_shng_data(data, type=None)``

    Methods necessary to overload:

    - ``get_send_data(data)``
    - ``get_shng_data(data, type=None)``


    Configuration
    =============

    The plugin class is capable of handling an arbitrary number of devices
    independently. Necessary configuration include the chosen devices respectively
    the device names and possibly device parameter in ``/etc/plugin.yaml``.

    The item configuration is supplemented by the attributes ``md_device`` and
    ``md_command``, which designate the device name from plugin configuration and
    the command name from the device configuration, respectively.

    The device class needs comprehensive configuration concerning available commands,
    the associated sent and received data formats, which will be supplied by way
    of configuration files in yaml format. Furthermore, the device-dependent
    type and configuration of connection should be set in ``/etc/plugin.yaml`` for
    each device used.

    The connection classes will be chosen and configured by the device classes.
    They should not need further configuration, as all data transformation is done
    by the device classes and the connection-specific attributes are provided
    from plugin configuration.


    New devices
    ===========

    A new device type ``gadget`` can be implemented by providing the following:

    - a device folder ``dev_gadget``
    - a device configuration file defining commands ``dev_gadget/commands.py``
    - specification of needed connection type in ``/etc/plugin.yaml`` ('conn_type')
    - only if needed:
        * a device class file with a derived class ``dev_gadget/device.py``
        * additional methods in the device class to handle special commands which
          do more than assign transformed item data to a single item or which need
          more complex item transformation
        * additional methods in the connection class to handle special forms of
          connection initialization (e.g. serial sync routines)
        * a data formats file defining data types ``dev_gadget/datatypes.py`` and
          additional data types in the datatype file
'''

import requests
import socket

from collections import OrderedDict
import importlib
import logging
import re
import sys
import cherrypy
import json
from time import sleep, time
from ast import literal_eval
from pydoc import locate


if __name__ == '__main__':
    # just needed for standalone mode

    class SmartPlugin():
        pass

    class SmartPluginWebIf():
        pass

    import os
    BASE = os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-3])
    sys.path.insert(0, BASE)
    import datatypes as DT
    MD_standalone = True

else:
    from lib.item import Items
    from lib.utils import Utils
    from lib.model.smartplugin import SmartPlugin, SmartPluginWebIf

    from . import datatypes as DT
    MD_standalone = False


#############################################################################################################################################################################################################################################
#
# global constants used to configure plugin, device, connection and items
#
#############################################################################################################################################################################################################################################

# plugin arguments, used in plugin config 'device'
PLUGIN_ARG_CONNECTION   = 'conn_type'
PLUGIN_ARG_NET_HOST     = 'host'
PLUGIN_ARG_NET_PORT     = 'port'
PLUGIN_ARG_SERIAL_PORT  = 'serial'

PLUGIN_ARGS = (PLUGIN_ARG_CONNECTION, PLUGIN_ARG_NET_HOST, PLUGIN_ARG_NET_PORT, PLUGIN_ARG_SERIAL_PORT)

# connection types for PLUGIN_ARG_CONNECTION
CONN_NET_TCP_REQ        = 'net_tcp_req'     # TCP client connection with URL-based requests
CONN_NET_TCP_SYN        = 'net_tcp_syn'     # persistent TCP client connection with immediate query-reply logic
CONN_NET_TCP_SRV        = 'net_tcp_srv'     # TCP server connection with async data callback
CONN_NET_UDP_SRV        = 'net_udp_srv'     # UDP server connection with async data callback
CONN_SER_CLI            = 'ser_cli'         # serial connection with query-reply logic
CONN_SER_ASYNC          = 'ser_async'       # serial connection with async data callback

CONNECTION_TYPES = (CONN_NET_TCP_REQ, CONN_NET_TCP_SYN, CONN_NET_TCP_SRV, CONN_NET_UDP_SRV, CONN_SER_CLI, CONN_SER_ASYNC)

# item attributes (as defines in plugin.yaml)
ITEM_ATTR_DEVICE        = 'md_device'
ITEM_ATTR_COMMAND       = 'md_command'
ITEM_ATTR_READ          = 'md_read'
ITEM_ATTR_CYCLE         = 'md_read_cycle'
ITEM_ATTR_READ_INIT     = 'md_read_initial'
ITEM_ATTR_WRITE         = 'md_write'
ITEM_ATTR_READ_ALL      = 'md_read_all'

ITEM_ATTRS = (ITEM_ATTR_DEVICE, ITEM_ATTR_COMMAND, ITEM_ATTR_READ, ITEM_ATTR_CYCLE, ITEM_ATTR_READ_INIT, ITEM_ATTR_WRITE, ITEM_ATTR_READ_ALL)

# command definition
COMMAND_READ            = True
COMMAND_WRITE           = False


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
            self.logger.warning(f'Device (unknown): building command {name} without a device, aborting')
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
            mod_str = self.__module__ + '.' + mod_str

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
            mod_str = self.__module__ + '.' + mod_str

        commands = {}
        try:
            # get module
            cmd_module = locate(mod_str)
            # get content
            commands = cmd_module.commands
        except AttributeError as e:
            self.logger.error(f'Device {device_name}: importing commands from external module {"dev_" + self._device_id + "/commands.py"} failed. Error was: {e}')
        except ImportError:
            self.logger.error(f'Device {device_name}: importing external module {"dev_" + self._device_id + "/commands.py"} failed')

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
            for arg in ('opcode', 'read', 'write', 'item_type', 'dev_type', 'read_cmd', 'write_cmd', 'read_data'):
                if arg in commands[cmd]:
                    kw[arg] = commands[cmd][arg]

            dt_class = None
            dev_type = kw.get('dev_type', '')
            if dev_type:
                dt_class = self._dt.get('DT_' + dev_type)

            if not dt_class:
                self.logger.error(f'Device {device_name}: importing commands found invalid datatype {dev_type}, replacing with DT_raw. Check function of device')
                dt_class = DT.DT_raw
            self._commands[cmd] = self._cmd_class(self.device, cmd, dt_class, **{'cmd': kw, 'plugin': self._plugin_params})


#############################################################################################################################################################################################################################################
#
# class MD_Device
#
#############################################################################################################################################################################################################################################

class MD_Device(object):
    '''
    This class is the base class for a simple device class. It can process commands
    by sending values to the device and collect data by parsing data received from
    the device.

    Configuration is done via dev_<device_id>/ commands.py (see there for format)

    :param device_id: device type as used in derived class names
    :param device_name: device name for use in item configuration and logs
    :type device_id: str
    :type device_name: str
    '''

    def __init__(self, device_id, device_name, **kwargs):
        '''
        This initializes the class object.

        As additional device classes are expected to be implemented as subclasses,
        most initialization steps are modularized as methods which can be overloaded
        as needed.
        As all pre-implemented methods are called in hopefully-logical sequence,
        this __init__ probably doesn't need to be changed.
        '''
        # get MultiDevice logger (if not already defined by subclass)
        # NOTE: later on, decide if every device logs to its own logger?
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(__name__)

        self.logger.debug(f'Device {device_name}: device initializing from {self.__class__.__name__} with arguments {kwargs}')

        # the connection object
        self._connection = None

        # the commands object
        self._commands = None

        # set class properties
        self._plugin_params = kwargs
        self.device_id = device_id
        self.device = device_name
        self.alive = False
        self._runtime_data_set = False

        self._data_received_callback = None
        self._commands_read = {}
        self._commands_initial = []
        self._commands_cyclic = {}

        # set device parameters, if any
        self._set_device_params()

        # try to read configuration files
        if not self._read_configuration():
            self.logger.error(f'Device {self.device}: configuration could not be read, device disabled')
            return

        # instantiate connection object
        self._connection = self._get_connection()
        if not self._connection:
            self.logger.error(f'Device {self.device}: could not setup connection with {kwargs}, device disabled')
            return

        # the following code should only be run if not called from subclass via super()
        if self.__class__ is MD_Device:
            self.logger.debug(f'Device {self.device}: device initialized from {self.__class__.__name__}')

    def start(self):
        if self.alive:
            return
        if self._runtime_data_set:
            self.logger.debug(f'Device {self.device}: start method called')
        else:
            self.logger.error(f'Device {self.device}: start method called, but runtime data not set, device disabled')
            return

        self.alive = True
        self._connection.open()

    def stop(self):
        self.logger.debug(f'Device {self.device}: stop method called')
        self.alive = False
        self._connection.close()

    # def run_standalone(self):
    #     '''
    #     If you want to provide a standalone function, you'll have to implement
    #     this function with the appropriate code. You can use all functions from
    #     the MultiDevice class, the devices, connections and commands.
    #     You do not have an sh object, items or web interfaces.
    #
    #     As this should not be present for the base class, the definition is
    #     commented out.
    #     '''
    #     pass

    def send_command(self, command, value=None):
        '''
        Sends the specified command to the device providing <value> as data

        :param command: the command to send
        :param value: the data to send, if applicable
        :type command: str
        :return: True if send was successful, False otherwise
        :rtype: bool
        '''
        if not self.alive:
            self.logger.warning(f'Device {self.device}: trying to send command {command} with value {value}, but device is not active.')
            return False

        if not self._connection:
            self.logger.warning(f'Device {self.device}: trying to send command {command} with value {value}, but connection is None. This shouldn\'t happen...')

        if not self._connection.connected:
            self._connection.open()
            if not self._connection.connected:
                self.logger.warning(f'Device {self.device}: trying to send command {command} with value {value}, but connection could not be established.')
                return False

        data_dict = self._commands.get_send_data(command, value)
        self.logger.debug(f'Device {self.device}: command {command} with value {value} yielded send data_dict {data_dict}')

        # if an error occurs on sending, an exception is thrown
        try:
            result = self._connection.send(data_dict)
        except Exception as e:
            self.logger.debug(f'Device {self.device}: error on sending command {command}, error was {e}')
            return False

        if result:
            self.logger.debug(f'Device {self.device}: command {command} received result of {result}')
            value = self._commands.get_shng_data(command, result)
            self.logger.debug(f'Device {self.device}: command {command} received result {result}, converted to value {value}')
            if self._data_received_callback:
                self._data_received_callback(self.device, command, value)
            else:
                self.logger.warning(f'Device {self.device}: received data {value} for command {command}, but _data_received_callback is not set. Discarding data.')
        return True

    def data_received(self, command, data):
        '''
        Callback function for received data e.g. from an event loop
        Processes data and dispatches value to plugin class

        :param command: the command in reply to which data was received
        :param data: received data in 'raw' connection format
        :type command: str
        '''
        self.logger.debug(f'Device {self.device}: data received for command {command}: {data}')
        value = self._commands.get_shng_data(command, data)
        self.logger.debug(f'Device {self.device}: data received for command {command}: {data} converted to value {value}')
        if self._data_received_callback:
            self._data_received_callback(command, value)
        else:
            self.logger.warning(f'Device {self.device}: received data {value} for command {command}, but _data_received_callback is not set. Discarding data.')

    def read_all_commands(self):
        '''
        Triggers all configured read commands
        '''
        for cmd in self._commands_read:
            self.send_command(cmd)

    def is_valid_command(self, command, read=None):
        '''
        Validate if 'command' is a valid command for this device
        Possible to check only for reading or writing

        :param command: the command to test
        :type command: str
        :param read: check for read (True) or write (False), or both (None)
        :type read: bool | NoneType
        :return: True if command is valid, False otherwise
        :rtype: bool
        '''
        if self._commands:
            return self._commands.is_valid_command(command, read)
        else:
            return False

    def set_runtime_data(self, **kwargs):
        '''
        Sets runtime data received from the plugin class
        '''
        try:
            self._commands_read = kwargs['read_commands']
            self._commands_cyclic = kwargs['cycle_commands']
            self._commands_initial = kwargs['initial_commands']
            self._data_received_callback = kwargs['callback']
            self._runtime_data_set = True
        except KeyError as e:
            self.logger.error(f'Device {self.device}: error in runtime data: {e}. Stopping device.')

    def update_device_params(self, **kwargs):
        '''
        Updates configuration parametes for device. Needs device to not be running

        overload as needed.
        '''
        if self.alive:
            self.logger.warning(f'Device {self.device}: tried to update params with {kwargs}, but device is still running. Ignoring request')
            return

        if not kwargs:
            self.logger.warning(f'Device {self.device}: update_device_params called without new parameters. Don\'t know what to update.')
            return

        # merge new params with self._plugin_params, overwrite old values if necessary
        self._plugin_params = {**self._plugin_params, **kwargs}

        # update this class' settings
        self._set_device_params()

        # update = recreate the connection with new parameters
        self._connection = self._get_connection()

    #
    #
    # check if overloading needed
    #
    #

    def _set_device_params(self, **kwargs):
        '''
        This method parses self._parameters for parameters it needs itself and does the
        necessary initialization.
        Needs to be overloaded for maximum effect
        '''
        pass

    def _get_connection(self):
        '''
        return connection object. Try to identify the wanted connection  and return
        the proper subclass instead. If no decision is possible, just return an
        instance of MD_Connection.

        If you need to use other connection types for your device, implement it
        and preselect with PLUGIN_ARG_CONNECTION in /etc/plugin.yaml, so this
        class will never be used.
        Otherwise, just parse them in after calling super()._set_connection_params()

        HINT: If you need to modify this, just write something new.
        The "autodetect"-code will probably only be used with unaltered connection
        classes. Just return the wanted connection object and ride into the light.
        '''
        conn_type = None
        params = self._plugin_params

        # try to find out what kind of connection is wanted
        if PLUGIN_ARG_CONNECTION in self._plugin_params and self._plugin_params[PLUGIN_ARG_CONNECTION] in CONNECTION_TYPES:
            conn_type = self._plugin_params[PLUGIN_ARG_CONNECTION]
        else:

            if PLUGIN_ARG_NET_PORT in self._plugin_params:

                # no further information on network specifics, use basic HTTP TCP client
                conn_type = CONN_NET_TCP_REQ

            elif PLUGIN_ARG_SERIAL_PORT in self._plugin_params:

                # this seems to be a serial killer application
                conn_type = CONN_SER_CLI

            if conn_type:
                params[PLUGIN_ARG_CONNECTION] = conn_type

        if conn_type == CONN_NET_TCP_REQ:

            return MD_Connection_Net_TCP_Request(self.device_id, self.device, self._data_received_callback, **self._plugin_params)
        elif conn_type == CONN_NET_TCP_SYN:

            return MD_Connection_Net_TCP_Reply(self.device_id, self.device, self._data_received_callback, **self._plugin_params)
        elif conn_type == CONN_NET_TCP_SRV:

            return MD_Connection_Net_TCP_Server(self.device_id, self.device, self._data_received_callback, **self._plugin_params)
        elif conn_type == CONN_NET_UDP_SRV:

            return MD_Connection_Net_UDP_Server(self.device_id, self.device, self._data_received_callback, **self._plugin_params)
        elif conn_type == CONN_SER_CLI:

            return MD_Connection_Serial_Client(self.device_id, self.device, self._data_received_callback, **self._plugin_params)
        elif conn_type == CONN_SER_ASYNC:

            return MD_Connection_Serial_Async(self.device_id, self.device, self._data_received_callback, **self._plugin_params)
        else:
            return MD_Connection(self.device_id, self.device, self._data_received_callback, **self._plugin_params)

        # Please go on. There is nothing to see here. You shouldn't be here anyway...
        self.logger.error(f'Device {self.device}: could not setup connection with {params}, device disabled')

    #
    #
    # private utility methods
    #
    #

    def _read_configuration(self):
        '''
        This initiates reading of configuration.
        Basically, this calls the MD_Commands object to fill itselt; but if needed,
        this can be overloaded to do something else.
        '''
        self._commands = MD_Commands(self.device_id, self.device, MD_Command, **self._plugin_params)
        return True


#############################################################################################################################################################################################################################################
#
# class MD_Connection and subclasses
#
#############################################################################################################################################################################################################################################

class MD_Connection(object):
    '''
    This class is the base class for further connection classes. It can - well,
    not much. Opening and closing of connections and writing and receiving data
    is something to implement in the interface-specific derived classes.

    :param device_id: device type as used in commands.py name
    :param device_name: device name for use in item configuration and logs
    :type device_id: str
    :type device_name: str
    '''
    def __init__(self, device_id, device_name, data_received_callback, **kwargs):

        # get MultiDevice logger
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f'Device {device_name}: connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_id = device_id
        self.device = device_name
        self.connected = False

        self._params = kwargs
        self._data_received_callback = data_received_callback

        # check if some of the arguments are usable
        self._set_connection_params()

        # tell someone about our actual class
        self.logger.debug(f'Device {self.device}: connection initialized from {self.__class__.__name__}')

    def open(self):
        self.logger.debug(f'Device {self.device}: open method called for connection')
        if self._open():
            self.connected = True
        self._send_init_on_open()

    def close(self):
        self.logger.debug(f'Device {self.device}: close method called for connection')
        self._close()
        self.connected = False

    def send(self, data_dict):
        '''
        Send data, possibly return response

        :param data: dict with raw data and possible additional parameters to send
        :type data_dict: dict
        :return: raw response data if applicable, None otherwise. Errors need to raise exceptions
        '''
        self._send_init_on_send()
        response = self._send(data_dict)

        return response

    #
    #
    # overloading needed for at least some of the following methods...
    #
    #

    def _open(self):
        '''
        Overload with opening of connection

        :return: True if successful
        :rtype: bool
        '''
        self.logger.debug(f'Device {self.device}: opening connection as {__name__} for device {self.device} with params {self._params}')
        return True

    def _close(self):
        '''
        Overload with closing of connection
        '''
        self.logger.debug(f'Device {self.device}: closing connection as {__name__} for device {self.device} with params {self._params}')

    def _send(self, data_dict):
        '''
        Overload with sending of data and - possibly - returning response data
        Return None if no response is received or expected.
        '''
        self.logger.debug(f'Device {self.device}: device {self.device} simulating to send data {data_dict}...')
        return None

    def _send_init_on_open(self):
        '''
        This class can be overloaded if anything special is needed to make the
        other side talk after opening the connection... ;)

        Using class properties instead of arguments makes overloading easy.

        It is routinely called by self.open()
        '''
        pass

    def _send_init_on_send(self):
        '''
        This class can be overloaded if anything special is needed to make the
        other side talk before sending commands... ;)

        It is routinely called by self.send()
        '''
        pass

    #
    #
    # private utility methods
    #
    #

    def _set_connection_params(self):
        '''
        Try to set some of the common parameters.
        Might need to be overloaded...
        '''
        for arg in PLUGIN_ARGS:
            if arg in self._params:
                setattr(self, arg, sanitize_param(self._params[arg]))


class MD_Connection_Net_TCP_Request(MD_Connection):
    '''
    This class implements a TCP connection in the query-reply matter using
    the requests library.

    The data_dict['payload']-Data needs to be the full query URL. Additional
    parameter dicts can be added to be given to requests.request, as
    - method: get (default) or post
    - headers, data, cookies, files, params: passed thru to request()

    Response data is returned as text. Errors raise HTTPException
    '''
    def _open(self):
        self.logger.debug(f'Device {self.device}: {self.__class__.__name__} "opening connection" as {__name__} for device {self.device} with params {self._params}')
        return True

    def _close(self):
        self.logger.debug(f'Device {self.device}: {self.__class__.__name__} "closing connection" as {__name__} for device {self.device} with params {self._params}')

    def _send(self, data_dict):
        url = data_dict.get('payload', None)
        if not url:
            self.logger.error(f'Device {self.device}: can not send without url parameter from data_dict {data_dict}, aborting')
            return False

        # default to get if not 'post' specified
        method = data_dict.get('method', 'get')

        # check for additional data
        par = {}
        for arg in ('headers', 'data', 'cookies', 'files', 'params'):
            par[arg] = data_dict.get(arg, {})

        # send data
        response = requests.request(method, url,
                                    params=par['params'],
                                    headers=par['headers'],
                                    data=par['data'],
                                    cookies=par['cookies'],
                                    files=par['files'])

        if 200 <= response.status_code < 400:
            return response.text
        else:
            try:
                err = ''
                response.raise_for_status()
            except requests.HTTPError as e:
                err = f' and error "{str(e)}"'
                self.logger.warning(f'Device {self.device}: TCP request returned code {response.status_code}{err}')
                raise e
        return None


class MD_Connection_Net_TCP_Reply(MD_Connection):
    '''
    This class implements a persistent TCP connection via sockets

    The data_dict['payload'] is sent as string 1:1; the remainder of data_dict is ignored.

    Response data is returned as text, or None in case of error
    '''

    def __init__(self, device_id, device_name, data_received_callback, **kwargs):

        # get MultiDevice logger
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f'Device {device_name}: connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_id = device_id
        self.device = device_name
        self.connected = False
        self._tcp = None
        self._buffer = b''

        self._params = {PLUGIN_ARG_NET_HOST: '', PLUGIN_ARG_NET_PORT: 0, 'autoreconnect': True, 'connect_retries': 5, 'connect_cycle': 30, 'timeout': 3, 'terminator': b'\x0a'}
        self._params.update(kwargs)
        self._data_received_callback = data_received_callback

        # check if some of the arguments are usable
        self._set_connection_params()

        self._autoreconnect = self._params['autoreconnect']
        self._connect_retries = self._params['connect_retries']
        self._connect_cycle = self._params['connect_cycle']
        self._timeout = self._params['timeout']
        self._terminator = self._params['terminator']

        if not (self.host != '' and self.port > 0):
            self.logger.error(f'Device {self.device}: insufficient configuration data (TCP {self.host}:{self.port}), not initializing connection') 
            return False

        # tell someone about our actual class
        self.logger.debug(f'Device {self.device}: connection initialized from {self.__class__.__name__}')

    def _open(self):
        if not self.connected:
            self.logger.debug(f'Device {self.device}: {self.__class__.__name__} "opening connection" as {__name__} for device {self.device} with params {self._params}')
            self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._tcp.setblocking(False)
            self._tcp.settimeout(5)
            try:
                self._tcp.connect((f'{self.host}', int(self.port)))
                self._tcp.settimeout(self._timeout)
                self.connected = True
                self.logger.debug(f'Device {self.device}: connection established to {self.host}:{self.port}')
            except Exception:
                self.logger.warning(f'Device {self.device}: could not establish a connection to {self.host}:{self.port}')

        return self.connected

    def _close(self):
        self.logger.debug(f'Device {self.device}: {self.__class__.__name__} "closing connection" as {__name__} for device {self.device} with params {self._params}')
        if self.connected:
            self._tcp.close()
            self.connected = False

    def _reconnect(self):
        if not self.connected and self._autoreconnect:
            attempt = 0
            while attempt < self._connect_retries and not self.connected:
                attempt += 1
                self.logger.info(f'Device {self.device}: autoreconnecting, attempt {attempt}/{self._connect_retries}')
                if self._open():
                    break
                sleep(self._connect_cycle)

            if not self.connected:
                self.logger.warning(f'Device {self.device}: autoreconnect failed after {self._connect_retries} attempts')
                return False

    def _send(self, data_dict):
        # extract payload
        data = data_dict.get('payload', None)
        if not data:
            self.logger.error(f'Device {self.device}: refusing to send empty payload from data_dict {data_dict}, aborting')
            return None

        if not self.connected and not self._reconnect():
            self.logger.error(f'Device {self.device}: not connected and reconnect not requested or failed, aborting')
            return None

        # convert payload
        if not isinstance(data, (bytes, bytearray)):
            try:
                data = str(data)
            except Exception:
                pass
            try:
                data = data.encode('utf-8')
            except Exception as e:
                self.logger.warning(f'Device {self.device}: error {e} while encoding data {data} for remote {self.host}:{self.port}')
                return None

        # just send data, watch for closed socket (BrokenPipeError)
        # raise on unknown error, don't know what else to do
        try:
            self.logger.debug(f'Device {self.device}: sending data {data} to {self.host}:{self.port}')
            self._tcp.send(data)
            self.logger.debug(f'Device {self.device}: data sent')
        except BrokenPipeError:
            self.logger.warning(f'Device {self.device}: detected disconnect from {self.host}, send failed.')
            self.connected = False
            if self._autoreconnect:
                self.logger.debug(f'Autoreconnect enabled for {self._host}')
                self._reconnect()
            return None
        except Exception as e:  # log errors we are not prepared to handle and raise exception for further debugging
            self.logger.warning(f'Device {self.device}: unhandleded error on sending to {self.host}, cannot send data {data}. Error: {e}')
            raise

        # receive buffer data until
        # - connection is gone
        # - terminator is found
        # - timeout is hit
        self.logger.debug(f'Device {self.device}: reading response from {self.host}:{self.port}')
        buffer = b''
        begin = time()

        # TODO: remove
        self.logger.debug(f'Device {self.device}: starting read at {begin} from {self.host}:{self.port}')        
        while self.connected and self._terminator not in buffer and time() - begin > self._timeout:
            try:
                sdata = b''
                sdata = self._tcp.recv(8192)
                # TODO: remove
                self.logger.debug(f'Device {self.device}: reading response part {sdata} from {self.host}:{self.port}')
                if sdata:
                    buffer.append(sdata)
                else:
                    sleep(0.1)
            except BrokenPipeError:
                self.logger.warning(f'Device {self.device}: detected disconnect from {self.host} while receiving.')
                self.connected = False
                if self._autoreconnect:
                    self.logger.debug(f'Autoreconnect enabled for {self._host}')
                    self._reconnect()
                return None
            except Exception as e:
                # TODO: remove
                self.logger.debug(f'Device {self.device}: reading response, ignoring exception {e} from {self.host}:{self.port}')
                pass

        # TODO: remove
        self.logger.debug(f'Device {self.device}: quit read at {time()} from {self.host}:{self.port}')        

        # I'll be back...
        if buffer and self._terminator in buffer:

            # TODO: remove
            self.logger.debug(f'Device {self.device}: checking result {buffer} for terminator {self._terminator} from {self.host}:{self.port}')        
            # return data up to first terminator
            tpos = buffer.find(self._terminator)
            # TODO: remove
            self.logger.debug(f'Device {self.device}: found terminator at {tpos} from {self.host}:{self.port}')        
            result = buffer[:tpos].decode('utf-8').strip()
            # TODO: store remainder in class member and use for next receive...? implement locking
            self.logger.debug(f'Device {self.device}: received response {result} from {self.host}:{self.port}')
            return result
        elif time() - begin > self._timeout:
            self.logger.info(f'Device {self.device}: timeout while reading response from {self.host}.')
        elif not self.connected:
            self.logger.warning(f'Device {self.device}: disconnect detected while reading response from {self.host}.')
        else:
            self.logger.warning(f'Device {self.device}: received no reply from from {self.host}.')

        return None


class MD_Connection_Net_TCP_Server(MD_Connection):
    '''
    This class implements a TCP connection using a listener with asynchronous
    callback for receiving data. Callbacks for incoming connections and disconnect
    events can be provided, they are not utilized by this class as of now.

    The callbacks return a `ConnectionClient` from `lib.network`. For receiving
    data this is handled internally;

    Data received independently from clients is dispatched via callback.
    '''
    def __init__(self, device_id, device_name, data_received_callback, incoming_connection_callback, disconnected_callback, **kwargs):

        # get MultiDevice logger
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f'Device {device_name}: connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_id = device_id
        self.device = device_name
        self.connected = False

        self._params = kwargs
        self._data_received_callback = data_received_callback
        self._incoming_connection_callback = incoming_connection_callback
        self._disconnected_callback = disconnected_callback

        # check if some of the arguments are usable
        self._set_connection_params()

        # tell someone about our actual class
        self.logger.debug(f'Device {self.device}: connection initialized from {self.__class__.__name__}')


class MD_Connection_Net_UDP_Server(MD_Connection):
    pass


class MD_Connection_Serial_Client(MD_Connection):
    pass


class MD_Connection_Serial_Async(MD_Connection):
    pass


#############################################################################################################################################################################################################################################
#
# class MultiDevice
#
#############################################################################################################################################################################################################################################

class MultiDevice(SmartPlugin):
    '''
    This class does the actual interface work between SmartHomeNG and the device
    classes. Mainly it parses plugin and item configuration data, sets up associations
    between devices and items and handles data exchange between SmartHomeNG and
    the device classes. Furthermore, it calls all devices' run() and stop() methods
    if so instructed by SmartHomeNG.

    It also looks good.
    '''

    PLUGIN_VERSION = '0.0.2'

    def __init__(self, sh, standalone_device='', logger=None, **kwargs):
        '''
        Initalizes the plugin. For this plugin, this means collecting all device
        modules and initializing them by instantiating the proper class.
        '''

        if not sh:
            self.logger = logger

        self.logger.debug(f'Initializung MultiDevice-Plugin as {__name__}')

        self._devices = {}              # contains all configured devices - <device_name>: {'id': <device_id>, 'device': <class-instance>, 'params': {'param1': val1, 'param2': val2...}}
        self._items_write = {}          # contains all items with write command - <item_id>: {'device_name': <device_name>, 'command': <command>}
        self._items_readall = {}        # contains items which trigger 'read all' - <item_id>: <device_name>
        self._commands_read = {}        # contains all commands per device with read command - <device_name>: {<command>: <item_object>}
        self._commands_initial = {}     # contains all commands per device to be read after run() is called - <device_name>: ['command', 'command', ...]
        self._commands_cyclic = {}      # contains all commands per device to be read cyclically - device_name: {<command>: <cycle>}

        # Call init code of parent class (SmartPlugin)
        super().__init__()

        if sh:
            # get the parameters for the plugin (as defined in metadata plugin.yaml):
            devices = self.get_parameter_value('device')
        else:
            # set devices to "only device, kwargs set as config"
            devices = {standalone_device: kwargs}

        # iterate over all items in plugin configuration 'device' list
        #
        # example:
        #
        # multidevice:
        #     plugin_name: multidevice
        #     device:
        #         - dev1                    # -> case 1, name=dev1, id=dev1
        #         - mydev: dev2             # -> case 2, name=mydev, id=dev2
        #         - my2dev:                 # -> case 3, name=my2dev, id=dev3
        #             - device: dev3
        #             - host: somehost
        #         - dev4:
        #             - host: someotherhost # -> case 4, name=dev4, id=dev4,
        #                                   #    handled implicitly by case 3

        for device in devices:
            device_id = None
            param = {}
            if type(device) is str:
                # case 1, device configuration is only string
                device_id = device_name = device

            elif type(device) is OrderedDict:

                # either we have devname: devid or devname: (list of arg: value)
                device_name, conf = device.popitem()      # we only expect 1 pair per dict because of yaml parsing

                if type(conf) is str:
                    # case 2, device_name: device_id
                    device_id = conf
                # dev_id: (list of OrderedDict(arg: value))?
                elif type(conf) is list and all(type(arg) is OrderedDict for arg in conf):
                    # case 3, get device_id from parsing conf
                    device_id = device_name
                    for odict in conf:
                        for arg in odict.keys():

                            # store parameters
                            if arg == 'device':
                                device_id = odict[arg]
                            else:
                                param[arg] = sanitize_param(odict[arg])

                else:
                    self.logger.warning(f'Configuration for device {device_id} has unknown format, skipping {device_id}')
                    device_id = device_name = None

            if device_name and device_name in self._devices:
                self.logger.warning(f'Device {self.device}: duplicate device name {device_name} configured for device_ids {device_id} and {self._devices[device_name]["id"]}. Skipping processing of device id {device_id}')
                break

            # did we get a device id?
            if device_id:
                device_instance = None
                try:
                    # get module
                    device_module = importlib.import_module('.dev_' + device_id + '.device', __name__)
                    # get class name
                    device_class = getattr(device_module, 'MD_Device')
                    # get class instance
                    device_instance = device_class(device_id, device_name, **param)
                except AttributeError as e:
                    self.logger.error(f'Device {device_name}: importing class MD_Device from external module {"dev_" + device_id + "/device.py"} failed. Skipping device {device_name}. Error was: {e}')
                except (ImportError):
                    self.logger.warning(f'Device {device_name}: importing external module {"dev_" + device_id + "/device.py"} failed, reverting to default MD_Device class')
                    device_instance = MD_Device(device_id, device_name, **param)

                if device_instance:
                    # fill class dicts
                    self._devices[device_name] = {'id': device_id, 'device': device_instance, 'params': param}
                    self._commands_read[device_name] = {}
                    self._commands_initial[device_name] = []
                    self._commands_cyclic[device_name] = {}

        if not self._devices:
            self._init_complete = False
            return

        # if plugin should start even without web interface
        if sh:
            self.init_webinterface(WebInterface)

    def run(self):
        '''
        Run method for the plugin
        '''
        self.logger.debug('Run method called')

        # self.__print_global_arrays()

        # hand over relevant assigned commands and runtime-generated data
        self._apply_on_all_devices('set_runtime_data', self._generate_runtime_data)

        # start the devices
        self.alive = True
        self._apply_on_all_devices('start')

    def stop(self):
        '''
        Stop method for the plugin
        '''
        self.logger.debug('Stop method called')
        # self.scheduler_remove('poll_device')
        self.alive = False

        self._apply_on_all_devices('stop')

    def parse_item(self, item):
        '''
        Default plugin parse_item method. Is called when the plugin is initialized.
        The plugin can, corresponding to its attribute keywords, decide what to do with
        the item in future, like adding it to an internal array for future reference
        :param item:    The item to process.
        :return:        If the plugin needs to be informed of an items change you should return a call back function
                        like the function update_item down below. An example when this is needed is the knx plugin
                        where parse_item returns the update_item function when the attribute knx_send is found.
                        This means that when the items value is about to be updated, the call back function is called
                        with the item, caller, source and dest as arguments and in case of the knx plugin the value
                        can be sent to the knx with a knx write function within the knx plugin.
        '''
        if self.has_iattr(item.conf, ITEM_ATTR_DEVICE):

            # item is marked for plugin handling.
            device_name = self.get_iattr_value(item.conf, ITEM_ATTR_DEVICE)

            # is device_name known?
            if device_name and device_name not in self._devices:
                self.logger.warning(f'Item {item} requests device {device_name}, which is not configured, ignoring item')
                return

            device = self._get_device(device_name)
            self.logger.debug(f'Item {item}: parse for device {device_name}')

            if self.has_iattr(item.conf, ITEM_ATTR_COMMAND):

                command = self.get_iattr_value(item.conf, ITEM_ATTR_COMMAND)

                # command found, validate command for device
                if not device.is_valid_command(command):
                    self.logger.warning(f'Item {item} requests undefined command {command} for device {device_name}, ignoring item')
                    return

                # command marked for reading
                if self.has_iattr(item.conf, ITEM_ATTR_READ) and self.get_iattr_value(item.conf, ITEM_ATTR_READ):
                    if device.is_valid_command(command, COMMAND_READ):
                        if command in self._commands_read[device_name]:
                            self.logger.warning(f'Item {item} requests command {command} for reading on device {device_name}, but this is already set with item {self._commands_read[device_name][command]}, ignoring item')
                        else:
                            self._commands_read[device_name][command] = item
                            self.logger.debug(f'Item {item} saved for reading command {command} on device {device_name}')
                    else:
                        self.logger.warning(f'Item {item} requests command {command} for reading on device {device_name}, which is not allowed, read configuration is ignored')

                    # read on startup?
                    if self.has_iattr(item.conf, ITEM_ATTR_READ_INIT) and self.get_iattr_value(item.conf, ITEM_ATTR_READ_INIT):
                        if command not in self._commands_initial[device_name]:
                            self._commands_initial[device_name].append(command)
                            self.logger.debug(f'Item {item} saved for startup reading command {command} on device {device_name}')

                    # read cyclically?
                    if self.has_iattr(item.conf, ITEM_ATTR_CYCLE):
                        cycle = self.get_iattr_value(item.conf, ITEM_ATTR_CYCLE)
                        # if cycle is already set for command, use the lower value of the two
                        self._commands_cyclic[device_name][command] = min(cycle, self._commands_cyclic[device_name].get(command, cycle))
                        self.logger.debug(f'Item {item} saved for cyclic reading command {command} on device {device_name}')

                # command marked for writing
                if self.has_iattr(item.conf, ITEM_ATTR_WRITE) and self.get_iattr_value(item.conf, ITEM_ATTR_WRITE):
                    if device.is_valid_command(command, COMMAND_WRITE):
                        self._items_write[item.id()] = {'device_name': device_name, 'command': command}
                        self.logger.debug(f'Item {item} saved for writing command {command} on device {device_name}')
                        return self.update_item

            # is read_all item?
            if self.has_iattr(item.conf, ITEM_ATTR_READ_ALL):
                self._items_readall[item.id()] = device_name
                self.logger.debug(f'Item {item} saved for read_all on device {device_name}')
                return self.update_item

    # def parse_logic(self, logic):
    #     '''
    #     Default plugin parse_logic method
    #     '''
    #     if 'xxx' in logic.conf:
    #         # self.function(logic['name'])
    #         pass

    def update_item(self, item, caller=None, source=None, dest=None):
        '''
        Item has been updated

        This method is called, if the value of an item has been updated by SmartHomeNG.
        It should write the changed value out to the device (hardware/interface) that
        is managed by this plugin.

        :param item: item to be updated towards the plugin
        :param caller: if given it represents the callers name
        :param source: if given it represents the source
        :param dest: if given it represents the dest
        '''
        if self.alive:

            self.logger.debug(f'Update_item was called with item "{item}" from caller {caller}, source {source} and dest {dest}')
            if not self.has_iattr(item.conf, ITEM_ATTR_DEVICE) and not self.has_iattr(item.conf, ITEM_ATTR_COMMAND):
                self.logger.warning(f'Update_item was called with item {item}, which is not configured for this plugin. This shouldn\'t happen...')
                return

            device_name = self.get_iattr_value(item.conf, ITEM_ATTR_DEVICE)

            # test if source of item change was not the item's device...
            if caller != self.get_shortname() + '.' + device_name:

                # okay, go ahead
                self.logger.info(f'Update item: {item.id()} for device {device_name}: item has been changed outside this plugin')

                # item in list of write-configured items?
                if item.id() in self._items_write:

                    # get data and send new value
                    device_name = self._items_write[item.id()]['device_name']
                    device = self._get_device(device_name)
                    command = self._items_write[item.id()]['command']
                    self.logger.debug(f'Writing value "{item()}" from item {item.id()} with command “{command}“ for device {device_name}')
                    device.send_command(command, item())

                elif item.id() in self._items_readall:

                    # get data and trigger read_all
                    device_name = self._items_readall[item.id()]
                    device = self._get_device(device_name)
                    self.logger.debug(f'Triggering read_all for device {device_name}')
                    device.read_all_commands()

    def data_received(self, device_name, command, value):
        '''
        Callback function - new data has been received from device.
        Value is already in item-compatible format, so find appropriate item
        and update value

        :param device_name: name of the originating device
        :param command: command for or in reply to which data was received
        :param value: data
        :type device_name: str
        :type command: str
        '''
        if self.alive:

            # check if combination of device_name and command is configured for read access
            if device_name in self._commands_read and command in self._commands_read[device_name]:
                item = self._commands_read[device_name][command]
                self.logger.debug(f'Device {device_name}: data update with command {command} and value {value} for item {item.id()}')
                item(value)
            else:
                self.logger.warning(f'Device {device_name}: data update with command {command} and value {value} not assigned to any item, discarding data')

    def _update_device_params(self, device_name):
        '''
        hand over all device parameters to the device and tell it to do whatever
        is necessary to apply the new values.
        The device _will_ ignore this while it is running. To avoid accidental
        service interruption, device.stop() is not called automatically.
        Do. this. yourself.

        :param device_name: device name (surprise!)
        :type device:name: string
        '''
        self.logger.debug(f'Device {device_name}: updating device parameters')
        device = self._get_device(device_name)
        if device:
            device.update_device_params(**self._get_device_params(device_name))

    def _apply_on_all_devices(self, method, args_function=None):
        '''
        Call <method> on all devices stored in self._devices. If supplied,
        call args_function(device_name) for each device and hand over its
        returned dict as **kwargs.

        :param method: name of method to run
        :param args_function: function to build arguments dict
        :type method: str
        :type args_function: function
        '''
        for device in self._devices:

            kwargs = {}
            if args_function:
                kwargs = args_function(device)
            getattr(self._get_device(device), method)(**kwargs)

    def _generate_runtime_data(self, device_name):
        '''
        generate dict with device-specific data needed to run, which is
        - list of all 'read'-configured commands
        - list of all cyclic commands with cycle times
        - list of all initial read commands
        - callback for returning data to the plugin
        '''
        return {
            'read_commands': self._commands_read[device_name].keys(),
            'cycle_commands': self._commands_cyclic[device_name],
            'initial_commands': self._commands_initial[device_name],
            'callback': self.data_received
        }

    def _get_device_id(self, device_name):
        ''' getter method. Really most unused. '''
        dev = self._devices.get(device_name, None)
        if dev:
            return dev['id']
        else:
            return None

    def _get_device(self, device_name):
        ''' getter method for device object '''
        dev = self._devices.get(device_name, None)
        if dev:
            return dev['device']
        else:
            return None

    def _get_device_params(self, device_name):
        ''' getter method '''
        dev = self._devices.get(device_name, None)
        if dev:
            return dev['params']
        else:
            return None


#############################################################################################################################################################################################################################################
#
# class WebInterface
#
#############################################################################################################################################################################################################################################

class WebInterface(SmartPluginWebIf):

    def __init__(self, webif_dir, plugin):
        """
        Initialization of instance of class WebInterface

        :param webif_dir: directory where the webinterface of the plugin resides
        :param plugin: instance of the plugin
        :type webif_dir: str
        :type plugin: object
        """
        self.logger = plugin.logger
        self.webif_dir = webif_dir
        self.plugin = plugin
        self.items = Items.get_instance()

        self.tplenv = self.init_template_environment()

    @cherrypy.expose
    def index(self, reload=None):
        """
        Build index.html for cherrypy

        Render the template and return the html file to be delivered to the browser

        :return: contents of the template after beeing rendered
        """
        tmpl = self.tplenv.get_template('index.html')
        # add values to be passed to the Jinja2 template eg: tmpl.render(p=self.plugin, interface=interface, ...)

        plgitems = []
        for item in self.items.return_items():
            if any(elem in item.property.attributes for elem in [ITEM_ATTR_DEVICE, ITEM_ATTR_COMMAND, ITEM_ATTR_READ, ITEM_ATTR_CYCLE, ITEM_ATTR_READ_INIT, ITEM_ATTR_WRITE, ITEM_ATTR_READ_ALL]):
                plgitems.append(item)

        return tmpl.render(p=self.plugin,
                           items=sorted(self.items.return_items(), key=lambda k: str.lower(k['_path'])),
                           item_count=0,
                           plgitems=plgitems,
                           running={dev: self.plugin._devices[dev]['device'].alive for dev in self.plugin._devices},
                           devices=self.plugin._devices)

    @cherrypy.expose
    def submit(self, button=None, param=None):
        '''
        Submit handler for Ajax
        '''
        if button is not None:

            notify = None

            if '#' in button:

                # run/stop command
                cmd, __, dev = button.partition('#')
                device = self.plugin._get_device(dev)
                if device:
                    if cmd == 'run':
                        self.logger.info(f'Webinterface starting device {dev}')
                        device.start()
                    elif cmd == 'stop':
                        self.logger.info(f'Webinterface stopping device {dev}')
                        device.stop()
            elif '.' in button:

                # set device arg - but only when stopped
                dev, __, arg = button.partition('.')
                if param is not None:
                    param = sanitize_param(param)
                    try:
                        self.logger.info(f'Webinterface setting param {arg} of device {dev} to {param}')
                        self.plugin._devices[dev]['params'][arg] = param
                        self.plugin._update_device_params(dev)
                        notify = dev + '-' + arg + '-notify'
                    except Exception as e:
                        self.logger.info(f'Webinterface failed to set param {arg} of device {dev} to {param} with error {e}')

            # # possibly prepare data for returning
            # read_cmd = self.plugin._commandname_by_commandcode(button)
            # if read_cmd is not None:
            #     self._last_read[button] = {'addr': button, 'cmd': read_cmd, 'val': read_val}
            #     self._last_read['last'] = self._last_read[button]

            data = {'running': {dev: self.plugin._devices[dev]['device'].alive for dev in self.plugin._devices}, 'notify': notify}

        # # possibly return data to WebIf
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(data).encode('utf-8')

    @cherrypy.expose
    def get_data_html(self, dataSet=None):
        """
        Return data to update the webpage

        For the standard update mechanism of the web interface, the dataSet to return the data for is None

        :param dataSet: Dataset for which the data should be returned (standard: None)
        :return: dict with the data needed to update the web page.
        """
        if dataSet is None:
            # get the new data
            # data = {}
            pass

            # data['item'] = {}
            # for i in self.plugin.items:
            #     data['item'][i]['value'] = self.plugin.getitemvalue(i)
            #
            # return it as json the the web page
            # try:
            #     return json.dumps(data)
            # except Exception as e:
            #     self.logger.error("get_data_html exception: {}".format(e))
        return {}


#############################################################################################################################################################################################################################################
#
# non-class functions
#
#############################################################################################################################################################################################################################################

def sanitize_param(val):
    '''
    Try to correct type of val:
    - return int(val) if val is integer
    - return float(val) if val is float
    - return bool(val) is val follows conventions for bool
    - try if string can be converted to list, tuple or dict; do so if possible
    - return val unchanged otherwise

    :param val: value to sanitize
    :return: sanitized (or unchanged) value
    '''
    if Utils.is_int(val):
        val = int(val)
    elif Utils.is_float(val):
        val = float(val)
    elif val.lower() in ('true', 'false', 'on', 'off', 'yes', 'no'):
        val = Utils.to_bool(val)
    else:
        try:
            new = literal_eval(val)
            if type(new) in (list, dict, tuple):
                val = new
        except Exception:
            pass
    return val


if __name__ == '__main__':

    usage = '''
    Usage:
    ----------------------------------------------------------------------------------

    This plugin is meant to be used inside SmartHomeNG.

    Is is generally possible to run this plugin in standalone mode, usually for
    diagnostic purposes - IF the specified device supports this mode.
    As devices are modular extensions, it is not possible to print a list of supported
    devices.

    You need to call this plugin with the device name as the first parameter, any
    necessary configuration options either as arg=value pairs or as a python dict
    (this needs to be enclosed in quotes).
    Be aware that later parameters, be they dict or pair type, overwrite earlier
    parameters of the same name.

    ./__init__.py MD_Device host=www.smarthomeng.de port=80

    or

    ./__init__.py MD_Device '{"host": "www.smarthomeng.de", "port": 80}'

    If you call it with -v as a parameter after the device name, you get additional
    debug information:

    ./__init__.py MD_Device -v

    '''

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.CRITICAL)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(message)s  @ %(lineno)d')
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)

    device = ""

    if len(sys.argv) > 1:
        device = sys.argv[1]

    if device:

        # check for further command line arguments
        params = {}
        for arg in range(2, len(sys.argv)):

            arg_str = sys.argv[arg]
            if arg_str == '-v':
                print('Debug logging enabled')
                logger.setLevel(logging.DEBUG)

            else:
                try:
                    # convertible to dict?
                    params.update(literal_eval(arg_str))
                except Exception:
                    # if not: try to parse as 'name=value'
                    match = re.match('([^= \n]+)=([^= ˜n])', arg_str)
                    if match:
                        name, value = match.groups(0)
                        params[name] = value

    else:
        print(usage)
        exit()

    print("This is MultiDevice plugin running in standalone mode")
    print("=====================================================")

    md = MultiDevice(None, standalone_device=device, logger=logger, **params)

    if md._devices:
        dev = md._devices[list(md._devices.keys())[0]]
        print(f'Device loaded: {device} --- ', end='')

        if getattr(dev['device'], 'run_standalone', ''):
            print('running standalone method...')

            dev['device'].run_standalone()
        else:
            print('device doesn\'t have a standalone function.')
    else:
        print(f'Device {device} could not be loaded.')

    print('Done.')
