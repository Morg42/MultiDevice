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
    commands to a device and reading data from it.
    By abstracting devices and connections, most devices will be able to be
    interfaced by this plugin.

    General description
    ===================

    The whole MultiDevice-plugin is organized and abstracted into multiple levels
    of (reference) base classes and derived classes handling special implementations.

    The plugin manages item association and updates. For each device it handles,
    it creates an object based on MD_Device or derived classes.

    The device object handles starting and stopping the device and its configuration.
    
    Possible commands are bundled by the MD_Commands class which handles loading, 
    validating and calling the separate MD_Command or derived objects. 
    
    Each MD_Command object handles one command and is responsible for creating  
    command tokens/strings to/from the real device. 

    Each command is assigned a data type, which is represented by a Datatype-
    derived class and transforms values between the real device and the command object.
    
    To actually talk to the real device, that is, send commands/values and receive
    replies, it uses a standardized interface via one of the MD_Connection or 
    derived classes. 

    Thus, the plugin, devices and commands are ignorant of physical connection
    details, the connection implementation is transparent regarding actual data
    structures or content, and only the datatype classes need to concern itself
    with validity of data sent or received.

    (New) devices each reside in their respective subfolder of the plugin folder,
    providing a derived device class, a command definition and - if applicable -
    additional necessary datatypes. These are automatically loaded by the plugin
    if the respective device has a configuration entry in ``/etc/plugin.yaml``.


    This concept is meant to
    - minimize the amount of (repeating) code needed to implement a new device,
    - make it easy to adjust functionality by deriving base classes, overriding
      methods without needing to adjust the remaining code,
    - reduce implementing a new device (mostly) to properly defining the
      command API and datatypes,
    - keeping individual devices separated and independent as each is loaded into
      its own module / namespace.

    This comes at the cost of needing to understand the architecture of the plugin
    to be able to decide what to change/extend and what to keep.

    My hope is that with proper documentation and examples, this last part is
    easier to achieve than having to rewrite the whole handling code for items,
    network, serial interfaces and commands every time.

    Thanks to OnkelAndy for kicking my backside repeatedly; otherwise the
    development of this plugin might have stalled before being able to run ;)



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

    In addition, the plugin has a - limited - capability to run as a standalone
    program, for example to initiate a device discovery or diagnostic functions.
    To this end, it must be run from the plugin folder by issuing

    ``python3 __init__.py <devicename>``

    Be advised that any functionality to provide in this mode must absolutely
    by implemented by you :)


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
    - ``on_data_received(command, data)``
    - ``is_valid_command(command, read=None)``
    - ``set_runtime_data(**kwargs)``
    - ``update_device_params(**kwargs)``
    - ``get_lookup(lookup)``

    Methods possibly needed to overload for inherited classes:

    - ``run_standalone()``
    - ``_transform_send_data(data_dict)``
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

    Methods necessary to overload for derived classes:

    - ``_open()``
    - ``_close()``
    - ``_send(data_dict)``


    Methods possible to overload for derived classes:

    - ``_send_init_on_open()``
    - ``_send_init_on_send()``


    This class has subclasses defined for the following types of connection:

    - ``MD_Connection_Net_TCP_Request`` for query-reply TCP connections
    - ``MD_Connection_Net_Tcp_Client``  for persistent TCP connections with async replies
    - ``MD_Connection_Net_UDP_Server``  for UDP listering server with async callback
    - ``MD_Connection_Serial_Client``   for query-reply serial connections
    - ``MD_Connection_Serial_Async``    for event-loop serial connection with async callback

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
    - ``get_command_from_reply(data)``
    - ``get_lookup(lookup)``

    Methods possible to overload:

    - ``_parse_commands(device_name, commands)``


    MD_Command
    ----------

    This class contains information concerning the command name, the opcode or
    URL needed to issue the command, and information about datatypes expected by
    SmartHomeNG items and the device itself.

    Its contents will be initialized by the ``MD_Commands``-class while reading the
    command configuration.

    ``MD_Command(device_name, command_name, dt_class, **kwargs)``

    Public methods:

    - ``get_send_data(data)``
    - ``get_shng_data(data)``

    Methods possible to overload:

    - ``get_send_data(data)``
    - ``get_shng_data(data)``
    - ``_check_value(data)``


    The classes ``MD_Command_Str`` and ``MD_Command_ParseStr`` are examples for 
    defining own command classes according to your needs.
    These examples utilize strings and dicts to build request URLs as payload data
    for the ``MD_Connection_Net_TCP_Request`` or ``MD_Connection_Net_Tcp_Client`` classes.
    They also demonstrate parameter substitution in command definitions on different
    levels of complexity.


    MD_Datatype
    -----------

    This is one of the most important classes. By declaration, it contains
    information about the data type and format needed by a device and methods
    to convert its value from selected Python data types used in items to the
    (possibly) special data formats required by devices and vice versa.

    Datatypes are specified in subclasses of Datatype with a nomenclature
    convention of `DT_<device data type of format>`.

    All default datatype classes are imported from ``datatypes.py`` into the 'DT' module.

    New devices can ship their own needed datatype classes in a file called
    ``datatypes.py`` in the devices' folder.

    For details concerning API and implementation, refer to the reference classes as
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
    the device names and possibly device parameter in ``etc/plugin.yaml``.

    The item configuration is supplemented by the attributes ``md_device`` and
    ``md_command``, which designate the device name from plugin configuration and
    the command name from the device configuration, respectively.

    The device class needs comprehensive configuration concerning available commands,
    the associated sent and received data formats, which will be supplied by way
    of configuration files in python format. Furthermore, the device-dependent
    type and configuration of connection should be set in ``etc/plugin.yaml`` for
    each device used.

    The connection classes will be chosen and configured by the device classes.
    They should not need further configuration, as all data transformation is done
    by the device classes and the connection-specific attributes are provided
    from plugin configuration.

    Example:

    ```
    multidevice:
        plugin_name: multidevice
        device:
            - <type>                    # id = <type>, type = <type>, folder = dev_<type>
                - param1: <value1>      #   optional
            - <id>:                     # id = <id>, type = <type>, folder = dev_<type>
                - device: <type>
                - param1: <value1>      #   optional
                - param2: <value2>      #   optional
            - dev1                      # id = dev1, type = dev1, folder = dev_dev1
            - mydev: dev2               # id = mydev, type = dev2, folder = dev_dev2
            - my2dev:                   # id = my2dev, type = dev3, folder = dev_dev3
                - device: dev3
                - host: somehost        #   optional
            - dev4:                     # id = dev4, type = dev4, folder = dev_dev4
                - host: someotherhost   #   optional
    ```


    New devices
    ===========

    A new device type ``gadget`` can be implemented by providing the following:

    - a device folder ``dev_gadget``
    - a device configuration file defining commands ``dev_gadget/commands.py``
    - specification of needed connection type in ``etc/plugin.yaml`` ('conn_type')
    - only if needed:
        * a device class file with a derived class ``dev_gadget/device.py``
        * additional methods in the device class to handle special commands which
          do more than assign transformed item data to a single item or which need
          more complex item transformation
        * additional methods in the connection class to handle special forms of
          connection initialization (e.g. serial sync routines)
        * a data formats file defining data types ``dev_gadget/datatypes.py`` and
          additional data types in the datatype file

    For examples on how to implement this, take a look at the dev_example folder
    which contains simple examples as well as the reference documentation for the
    commands.py file structure.
    Also, take a look into the different existing device classes to get a feeling
    for the needed effort to implement a new device.
'''

from collections import OrderedDict
import importlib
import builtins
import logging
import re
import os
import sys
import cherrypy
import json
from ast import literal_eval


if __name__ == '__main__':
    # just needed for standalone mode
    builtins.MD_standalone = True

    class SmartPlugin():
        pass

    class SmartPluginWebIf():
        pass

    import os
    BASE = os.path.sep.join(os.path.realpath(__file__).split(os.path.sep)[:-3])
    sys.path.insert(0, BASE)

    from MD_Globals import *
    from MD_Device import MD_Device

else:
    builtins.MD_standalone = False

    from lib.item import Items
    from lib.model.smartplugin import SmartPlugin, SmartPluginWebIf
    import lib.shyaml as shyaml

    from .MD_Globals import *
    from .MD_Device import MD_Device


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

    PLUGIN_VERSION = '0.1.0'

    def __init__(self, sh, standalone_device='', logger=None, **kwargs):
        '''
        Initalizes the plugin. For this plugin, this means collecting all device
        modules and initializing them by instantiating the proper class.
        '''

        if not sh:
            self.logger = logger

        self.logger.debug(f'Initializung MultiDevice-Plugin as {__name__}')

        self._devices = {}              # contains all configured devices - <device_name>: {'id': <device_id>, 'device': <class-instance>, 'logger': <logger-instance>, 'params': {'param1': val1, 'param2': val2...}}
        self._items_write = {}          # contains all items with write command - <item_id>: {'device_name': <device_name>, 'command': <command>}
        self._items_readall = {}        # contains items which trigger 'read all' - <item_id>: <device_name>
        self._commands_read = {}        # contains all commands per device with read command - <device_name>: {<command>: <item_object>}
        self._commands_initial = {}     # contains all commands per device to be read after run() is called - <device_name>: ['command', 'command', ...]
        self._commands_cyclic = {}      # contains all commands per device to be read cyclically - device_name: {<command>: {'cycle': <cycle>, 'next': <next>}}

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
                self.logger.warning(f'Duplicate device name {device_name} configured for device_ids {device_id} and {self._devices[device_name]["id"]}. Skipping processing of device id {device_id}')
                break

            # did we get a device id?
            if device_id:
                device_instance = None
                try:
                    # get module
                    mod_str = 'dev_' + device_id + '.device'
                    if not MD_standalone:
                        mod_str = '.' + mod_str
                    device_module = importlib.import_module(mod_str, __name__)
                    # get class name
                    device_class = getattr(device_module, 'MD_Device')
                    # get class instance
                    device_instance = device_class(device_id, device_name, plugin=self, **param)
                except AttributeError as e:
                    self.logger.error(f'Importing class MD_Device from external module {"dev_" + device_id + "/device.py"} failed. Skipping device {device_name}. Error was: {e}')
                except (ImportError):
                    self.logger.warning(f'Importing external module {"dev_" + device_id + "/device.py"} for device {device_name} failed, reverting to default MD_Device class')
                    device_instance = MD_Device(device_id, device_name, plugin=self, **param)

                if device_instance:

                    # create logger for device identity to use in update_item() and store in _devices dict
                    dev_logger = logging.getLogger(f'{__name__}.{device_name}')

                    # fill class dicts
                    self._devices[device_name] = {'id': device_id, 'device': device_instance, 'logger': dev_logger, 'params': param}
                    self._commands_read[device_name] = {}
                    self._commands_initial[device_name] = []
                    self._commands_cyclic[device_name] = {}
                    dev_logger = None

                    # check for and load struct definitions
                    if not MD_standalone:
                        self.logger.debug(f'trying to load struct definitions for device {device_name} from folder dev_{device_id}')
                        struct_file = os.path.join(self._plugin_dir, 'dev_' + device_id, 'struct.yaml')
                        raw_struct = shyaml.yaml_load(struct_file, ordered=True, ignore_notfound=True)

                        # if valid struct definition is found
                        if raw_struct is not None:

                            self.logger.debug(f'loaded {len(raw_struct.keys())} structs for processing')
                            # replace all mentions of "DEVICE" with the plugin/device's name
                            try:
                                mod_struct = eval(str(raw_struct).replace('DEVICENAME', device_name))
                            except Exception as e:
                                self.logger.warning(f'importing structs for device {device_name} failed, check struct definitions. Error was: {e}')
                            else:
                                for struct_name in mod_struct:
                                    self.logger.debug(f'adding struct {self.get_shortname()}.{device_name}.{struct_name}')
                                    self._sh.items.add_struct_definition(self.get_shortname() + '.' + device_name, struct_name, mod_struct[struct_name])

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
                        self._commands_cyclic[device_name][command] = { 'cycle': min(cycle, self._commands_cyclic[device_name].get(command, cycle)), 'next': 0 }
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

            # is lookup table item?
            if self.has_iattr(item.conf, ITEM_ATTR_LOOKUP):
                table = self.get_iattr_value(item.conf, ITEM_ATTR_LOOKUP)
                if table:
                    lu = device.get_lookup(table)
                    item.set(lu, 'MultiDevice.' + device_name, source='Init')
                    if lu:
                        self.logger.debug(f'Item {item} assigned lookup {table} from device {device_name} with contents {device.get_lookup(table)}')
                    else:
                        self.logger.info(f'Item {item} requested lookup {table} from device {device_name}, which was empty or non-existent')
                else:
                    self.logger.warning(f'Item {item} has attribute {ITEM_ATTR_LOOKUP} without a value set. Ignoring.')

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

                # from here on, use device's logger so messages are displayed for the device
                dev_log = self._get_device_logger(device_name)

                # okay, go ahead
                dev_log.info(f'Update item: {item.id()}: item has been changed outside this plugin')

                # item in list of write-configured items?
                if item.id() in self._items_write:

                    # get data and send new value
                    device_name = self._items_write[item.id()]['device_name']
                    device = self._get_device(device_name)
                    command = self._items_write[item.id()]['command']
                    dev_log.debug(f'Writing value "{item()}" from item {item.id()} with command "{command}"')
                    if not device.send_command(command, item()):
                        dev_log.debug(f'Writing value "{item()}" from item {item.id()} with command “{command}“ failed, resetting item value')
                        item(item.property.last_value, self.get_shortname() + '.' + device_name)
                        return None

                elif item.id() in self._items_readall:

                    # get data and trigger read_all
                    device_name = self._items_readall[item.id()]
                    device = self._get_device(device_name)
                    dev_log.debug('Triggering read_all')
                    device.read_all_commands()

    def on_data_received(self, device_name, command, value):
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

            # from here on, use device's logger so messages are displayed for the device
            dev_log = self._get_device_logger(device_name)

            # check if combination of device_name and command is configured for reading
            if device_name in self._commands_read and command in self._commands_read[device_name]:
                item = self._commands_read[device_name][command]
                dev_log.debug(f'Command {command} updated item {item.id()} with value {value}')
                item(value, self.get_shortname() + "." + device_name)
            else:
                dev_log.warning(f'Command {command} yielded value {value}, not assigned to any item, discarding data')

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
        self.logger.debug(f'updating parameters for device {device_name}')
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
            'callback': self.on_data_received
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

    def _get_device_logger(self, device_name):
        ''' getter for device logger, return plugin logger on error '''
        log = self.logger
        dev = self._devices.get(device_name, None)
        if dev:
            log = dev.get('logger', self.logger)
        return log


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
