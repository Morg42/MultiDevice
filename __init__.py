#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file is part of SmartHomeNG.
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
    ------------

    MultiDevice
    ^^^^^^^^^^^

    The 'MultiDevice'-class is derived from the SmartPlugin-class and provides
    the framework for handling item associations to the plugin, for storing
    item-command associations, for forwarding commands and the associated data
    to the device classes and receiving data from the device classes to update
    item values.
    This class will usually not need to be adjusted, but runs as the plugin itself.

    MD_Device
    ^^^^^^^^^

    The 'MD_Device'-class provides a framework for receiving (item) data values
    from the plugin and forward transformed data to the connection class and vice versa.
    A basic framework for transforming data by adjusting data type, possibly value
    byte length, json-formatting and numerical transformation (mult/div) are already
    implemented and can be used without code changed by device configuration.
    Special data tranformations and commands with complex actions will need to be
    implemented separately.

    MD_Connection
    ^^^^^^^^^^^^^
    This class and the derived classes provide frameworks for sending and receiving
    data to and from devices via serial or network connections. For both hardware
    layers implementation of persistent query-response-connections and listening
    servers with asynchronous push-to-callback are already available.
    If more complex communication setup is needed, this can be implemented on top
    of the existing classes.

    Configuration
    -------------

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
    -----------

    New device types can be implemented by providing the following:

    - a device configuration file defining commands and associated data formats
    - a specification of needed connection type
# TODO: decide if this is done in plugin.yaml or in device-commands.py
    - only if needed:
      * additional methods in the device class to handle special commands which
        do more than assign transformed item data to a single item or which need
        more complex item transformation
      * additional methods in the connection class to handle special forms of
        connection initialization (e.g. serial sync routines)
'''


from lib.model.smartplugin import SmartPlugin, SmartPluginWebIf
from lib.item import Items
from lib.utils import Utils

from collections import OrderedDict
import importlib
import logging
import re
import cherrypy
from ast import literal_eval

ITEM_ATTR_DEVICE    = 'md_device'
ITEM_ATTR_COMMAND   = 'md_command'
ITEM_ATTR_READ      = 'md_read'
ITEM_ATTR_CYCLE     = 'md_read_cycle'
ITEM_ATTR_READ_INIT = 'md_read_initial'
ITEM_ATTR_WRITE     = 'md_write'
ITEM_ATTR_READ_ALL  = 'md_read_all'

COMMAND_READ = True
COMMAND_WRITE = False


###############################################################################
#
# class MD_Device
#
###############################################################################

class MD_Device(object):
    '''
    This class is the base class for a simple device class. It can process commands
    by sending values to the device and collect data by parsing data received from
    the device.

    Configuration is done via devices/<device_id>_commands.py (see there for format)

    :param device_id: device type as used in commands.py name
    :param device_name: device name for use in item configuration and logs
    :type device_id: str
    :type device_name: str
    '''
    def __init__(self, device_id, device_name, **kwargs):

        # get MultiDevice logger (if not already defined by subclass)
        # NOTE: later on, decide if every device logs to its own logger?
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(__name__)

        # set class properties
        self.device = device_id
        self.name = device_name
        self.alive = False
        self._runtime_data_set = False

        self._data_received_callback = None
        self._commands_read = {}
        self._commands_initial = []
        self._commands_cyclic = {}

        # the following code should only be run if not called from subclass via super()
        # TODO - remove when done. say hello
        if self._is_base_device_class():
            self.logger.debug(f'Class {__name__} initialized for device {self.device} as {self.name} with arguments {kwargs}')

    def run(self):
        if self._runtime_data_set:
            self.logger.debug(f'Run method called for device {self.name}')
        else:
            self.logger.error(f'Run method called for device {self.name}, but runtime data not set, not starting device')
            return

        self.alive = True

    def stop(self):
        self.logger.debug(f'Stop method called for device {self.name}')
        self.alive = False

    def send_command(self, command, value=None):
        '''
        Sends the specified command to the device providing <value> as data

        :parameter command: the command to send
        :parameter value: the data to send, if applicable
        :type command: str
        '''
        pass

    def read_all_commands(self):
        '''
        Triggers all configured read commands
        '''
        pass

    def is_valid_command(self, command, read=None):
        '''
        Validate if 'command' is a valid command for this device
        Possible to check only for reading or writing

        :param command: the command to test
        :type command: str
        :param read: check for read (True) or write (False), or both (None)
        :type read: bool | NoneType
        :return: True if command is valid,
        '''
        # TODO: implement after reading and storing of commands is implemented
        return True

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
            self.logger.error(f'Error in runtime data: {e}. Stopping device.')

    def update_device_params(self, **kwargs):
        '''
        Updates configuration parametes for device. Needs device to not be running

        Overwrite as needed.
        '''
        if self.alive:
            self.logger.warning(f'Tried to update params for device {self.name} with {kwargs}, but device is still running. Ignoring request')

    def _is_base_device_class(self):
        '''
        Find out if this code is run as original MD_Device 'base' class of from
        subclass super() call

        This seems kind of clumsy. If anyone has a better idea...
        '''
        return str(type(self)).count('.') < 3


###############################################################################
#
# class MD_Connection
#
###############################################################################

class MD_Connection(object):
    '''
    This class is the base class for further connection classes. It can - well,
    not much. Opening and closing of connections and writing and receiving data
    is something to implement in the interface-specific derived classes.

    So, set up parameters, logging, and hope for a sunny day :)

    :param device_id: device type as used in commands.py name
    :param device_name: device name for use in item configuration and logs
    :type device_id: str
    :type device_name: str
    '''
    def __init__(self, device_id, device_name, **kwargs):

        # get MultiDevice logger
        self.logger = logging.getLogger(__name__)

        # set class properties
        self.device = device_id
        self.name = device_name

        # TODO - remove when done. say hello
        self.logger.debug(f'Class {__name__} initialized for device {self.device} as {self.name} with arguments {kwargs}')

    def start(self):
        self.logger.debug(f'Start method called for connection of {self._name}')

    def stop(self):
        self.logger.debug(f'Stop method called for connection of {self._name}')


###############################################################################
#
# class MultiDevice
#
###############################################################################

class MultiDevice(SmartPlugin):
    '''
    This class does the actual interface work between SmartHomeNG and the device
    classes. Mainly it parses plugin and item configuration data, sets up associations
    between devices and items and handles data exchange between SmartHomeNG and
    the device classes. Furthermore, it calls all devices' run() and stop() methods
    if so instructed by SmartHomeNG.

    It also looks good.
    '''

    PLUGIN_VERSION = '0.0.1'

    def __init__(self, sh):
        '''
        Initalizes the plugin. For this plugin, this means collecting all device
        modules and initializing them by instantiating the proper class.
        '''
        print('MD - ' + self.get_shortname())
        self._devices = {}              # contains all configured devices - <device_name>: {'id': <device_id>, 'device': <class-instance>, 'params': {'param1': val1, 'param2': val2...}}
        self._items_write = {}          # contains all items with write command - <item_id>: {'device_name': <device_name>, 'command': <command>}
        self._items_read = {}           # contains all items with read commands - <item_id>: {'device_name': <device_name>, 'command': <command>}
        self._items_readall = {}        # contains items which trigger 'read all' - <item_id>: <device_name>
        self._commands_read = {}        # contains all commands per device with read command - <device_name>: {<command>: <item_object>}
        self._commands_initial = {}     # contains all commands per device to be read after run() is called - <device_name>: ['command', 'command', ...]
        self._commands_cyclic = {}      # contains all commands per device to be read cyclically - device_name: {<command>: <cycle>}

        # Call init code of parent class (SmartPlugin)
        super().__init__()

        # get the parameters for the plugin (as defined in metadata plugin.yaml):
        devices = self.get_parameter_value('device')

        # iterate over all items in plugin configuration 'device' list
        for device in devices:
            device_id = None
            param = {}
            if type(device) is str:
                # got only the devic
                device_id = device_name = device
            elif type(device) is OrderedDict:
                # got at least device_id: device_name
                device_id, device_name = device.popitem()      # we only expect 1 pair per dict because of yaml parsing
                device_name, __, args = device_name.partition(',')
                if args:
                    # get all args in form of 'arg1=val1, arg2=val2, ...' into dict
                    res = re.match('\\s*([^ =,]+)\\s*=\\s*([^ =,]+)\\s*(?:,\\s*([^ =,]+)\\s*=\\s*([^ =,]+))*\\s*', args)
                    if res:
                        param = dict(zip(res.groups()[::2], res.groups()[1::2]))

                        # try to clean some parameter types
                        for p in param:
                            param[p] = self._sanitize_param(param[p])

            if device_name and device_name in self._devices:
                self.logger.warning(f'Duplicate device name {device_name} configured for device_ids {device_id} and {self._devices[device_name]["id"]}. Skipping processing of device id {device_id}')
                break

            # did we get a device id?
            if device_id:
                device_instance = None
                try:
                    # get module
                    device_module = importlib.import_module('.devices.' + device_id, __name__)
                    # get class name
                    device_class = getattr(device_module, 'MD_Device')
                    # get class instance
                    device_instance = device_class(device_id, device_name, **param)
                except AttributeError as e:
                    self.logger.error(f'Importing class MD_Device from external module {"devices/" + device_id + ".py"} failed. Skipping device {device_id}. Error was: {e}')
                except ImportError:
                    self.logger.warn(f'Importing external module {"devices/" + device_id + ".py"} failed, reverting to default MD_Device class')
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
        self._apply_on_all_devices('run')

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
                self.logger.warning(f'Item {item} requests device {device_name}, which is not configured, item is ignored')
                return

            device = self._get_device(device_name)
            self.logger.debug(f'parse item {item} for device {device_name}')

            if self.has_iattr(item.conf, ITEM_ATTR_COMMAND):

                command = self.get_iattr_value(item.conf, ITEM_ATTR_COMMAND)

                # command found, validate command for device
                if not device.is_valid_command(command):
                    self.logger.warning(f'Item {item} requests command {command} for device {device_name}, which is not configured, item is ignored')
                    return

                # command marked for reading
                if self.has_iattr(item.conf, ITEM_ATTR_READ) and self.get_iattr_value(item.conf, ITEM_ATTR_READ):
                    if device.is_valid_command(command, COMMAND_READ):
                        if command in self._commands_read[device_name]:
                            self.logger.warning(f'Item {item} requests command {command} for reading on device {device_name}, but this is already set with item {self._commands_read[device_name][command]}, item {item} is ignored')
                        else:
                            self._commands_read[device_name][command] = item
                            self._items_read[item.id()] = {'device_name': device_name, 'command': command}
                    else:
                        self.logger.warning(f'Item {item} requests command {command} for reading on device {device_name}, which is not allowed, read configuration is ignored')

                    # read on startup?
                    if self.has_iattr(item.conf, ITEM_ATTR_READ_INIT) and self.get_iattr_value(item.conf, ITEM_ATTR_READ_INIT):
                        if command not in self._commands_initial[device_name]:
                            self._commands_initial[device_name].append(command)

                    # read cyclically?
                    if self.has_iattr(item.conf, ITEM_ATTR_CYCLE):
                        cycle = self.get_iattr_value(item.conf, ITEM_ATTR_CYCLE)
                        # if cycle is already set for command, use the lower value of the two
                        self._commands_cyclic[device_name][command] = min(cycle, self._commands_cyclic[device_name].get(command, cycle))

                # command marked for writing
                if self.has_iattr(item.conf, ITEM_ATTR_WRITE) and self.get_iattr_value(item.conf, ITEM_ATTR_WRITE):
                    if device.is_valid_command(command, COMMAND_WRITE):
                        self._items_write[item.id()] = {'device_name': device_name, 'command': command}
                        return self.update_item

            # is read_all item?
            if self.has_iattr(item.conf, ITEM_ATTR_READ_ALL):
                self._items_readall[item.id()] = device_name
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

            self.logger.debug(f'update_item was called with item "{item}" from caller {caller}, source {source} and dest {dest}')
            if not self.has_iattr(item.conf, ITEM_ATTR_DEVICE) and not self.has_iattr(item.conf, ITEM_ATTR_COMMAND):
                self.logger.warning(f'update_item was called with item {item}, which is not configured for this plugin. This shouldn\'t happen...')
                return

            device_name = self.get_iattr_value(item.conf, ITEM_ATTR_DEVICE)

            # test if source of item change was not the item's device...
            if caller != self.get_shortname + '.' + device_name:

                # okay, go ahead
                self.logger.info(f'Update item: {item.id()}, item has been changed outside this plugin')

                # item in list of write-configured items?
                if item.id() in self._items_write:

                    # get data and send new value
                    device_name = self._items_write[item.id()]['device_name']
                    device = self._get_device(device_name)
                    command = self._items_write[item.id()]['command']
                    self.logger.debug(f'Writing value "{value}" to item {item.id()}')
                    device.send_command(command, item())

                elif item.id() in self._items_readall:

                    # get data and trigger read_all
                    device_name = self._items_readall[item.id()]
                    device = self._get_device(device_name)
                    self.logger.debug(f'Triggering read_all for device {device_name}')
                    device.read_all_commands()

    def received_data(self, device_name, command, value):
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
                self.logger.debug(f'Data update from device {device_name} with command {command} and value "{value}" for item {item.id()}')
                item(value)
            else:
                self.logger.warning(f'Data update from device {device_name} with command {command} and value "{value}" not assigned to any item, discarding data')

    def _update_device_params(self, device_name):
        '''
        hand over all device parameters to the device and tell it to do whatever
        is necessary to apply the new values.
        '''
        self.logger.debug(f'Updating device parameters for {device_name}')
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
            'callback': self.received_data
        }

    def _get_device_id(self, device_name):
        dev = self._devices.get(device_name, None)
        if dev:
            return dev['id']
        else:
            return None

    def _get_device(self, device_name):
        dev = self._devices.get(device_name, None)
        if dev:
            return dev['device']
        else:
            return None

    def _get_device_params(self, device_name):
        dev = self._devices.get(device_name, None)
        if dev:
            return dev['params']
        else:
            return None

    def _sanitize_param(self, val):
        '''
        Try to correct type of val:
        - return int(val) if val is integer
        - return float(val) if val is float
        - return bool(val) is val follows conventions for bool
        - try if string can be converted to list or dict; do so if possible
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
                if type(new) is list or type(new) is dict:
                    val = new
            except Exception:
                pass
        return val

    def __print_global_arrays(self):
        # for debugging only. console only. lame, so to say.
        print('******************************************************************************')
        print(f'_devices: {self._devices}')
        print('**************************')
        print(f'_items_write: {self._items_write}')
        print('**************************')
        print(f'_items_readall: {self._items_readall}')
        print('**************************')
        print(f'_commands_read: {self._commands_read}')
        print('**************************')
        print(f'_commands_initial: {self._commands_initial}')
        print('**************************')
        print(f'_commands_cyclic: {self._commands_cyclic}')
        print('******************************************************************************')


###############################################################################
#
# class WebInterface
#
###############################################################################


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
                           devices=self.plugin._devices)

    @cherrypy.expose
    def submit(self, button=None, param=None):
        '''
        Submit handler for Ajax
        '''
        if button is not None:

            if '#' in button:

                # run/stop command
                cmd, __, dev = button.partition('#')
                device = self.plugin._get_device(dev)
                if device:
                    if cmd == 'run':
                        self.logger.info(f'Webinterface starting device {dev}')
                        device.run()
                    elif cmd == 'stop':
                        self.logger.info(f'Webinterface stopping device {dev}')
                        device.stop()
            elif '.' in button:

                # set device arg - but only when stopped
                dev, __, arg = button.partition('.')
                if param is not None:
                    param = self.plugin._sanitize_param(param)
                    try:
                        self.logger.info(f'Webinterface setting param {arg} of device {dev} to {param}')
                        self.plugin._devices[dev]['params'][arg] = param
                        self.plugin._update_device_params(dev)
                    except Exception as e:
                        self.logger.info(f'Webinterface failed to set param {arg} of device {dev} to {param} with error {e}')

            # # possibly prepare data for returning
            # read_cmd = self.plugin._commandname_by_commandcode(button)
            # if read_cmd is not None:
            #     self._last_read[button] = {'addr': button, 'cmd': read_cmd, 'val': read_val}
            #     self._last_read['last'] = self._last_read[button]

        # # possibly return data to WebIf
        # cherrypy.response.headers['Content-Type'] = 'application/json'
        # return json.dumps(self._last_read).encode('utf-8')

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
            data = {}

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
