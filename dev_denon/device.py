#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    from MD_Globals import *
    from MD_Device import MD_Device
    from MD_Command import MD_Command_ParseStr
else:
    from ..MD_Globals import *
    from ..MD_Device import MD_Device
    from ..MD_Command import MD_Command_ParseStr

import logging


class MD_Device(MD_Device):
    """ Device class for Denon AV.

    Most of the work is done by the base class, so we only set default parameters
    for the connection (to be overwritten by device attributes from the plugin
    configuration) and add a fixed terminator byte to outgoing datagrams.

    The know-how is in the commands.py (and some DT_ classes...)
    """

    def __init__(self, device_type, device_id, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-2]) + f'.{device_id}')

        # set parameter defaults
        self._params = {'command_class': MD_Command_ParseStr, 
                        PLUGIN_ATTR_NET_HOST: '', 
                        PLUGIN_ATTR_NET_PORT: 0, 
                        PLUGIN_ATTR_CONN_AUTO_CONN: True,
                        PLUGIN_ATTR_CONN_RETRIES: 5, 
                        PLUGIN_ATTR_CONN_CYCLE: 3, 
                        PLUGIN_ATTR_CONN_TIMEOUT: 3, 
                        PLUGIN_ATTR_CONN_TERMINATOR: b'\r',
                        'disconnected_callback': None}

        # set our own preferences concerning connections
        if PLUGIN_ATTR_NET_HOST in kwargs and kwargs[PLUGIN_ATTR_NET_HOST]:
            self._params[PLUGIN_ATTR_CONNECTION] = CONN_NET_TCP_CLI
        elif PLUGIN_ATTR_SERIAL_PORT in kwargs and kwargs[PLUGIN_ATTR_SERIAL_PORT]:
            self._params[PLUGIN_ATTR_CONNECTION] = CONN_SER_DIR

        super().__init__(device_type, device_id, **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'device initialized from {__spec__.name} with arguments {kwargs}')

    # we need to receive data via callback, as the "reply" can be unrelated to
    # the sent command. Getting it as return value would assign it to the wrong
    # command and discard it... so break the "return result"-chain
    def _send(self, data_dict):
        self._connection.send(data_dict)
        return None

    def _transform_send_data(self, data=None):
        if data:
            try:
                data['limit_response'] = self._params.get(PLUGIN_ATTR_CONN_TERMINATOR, b'\r')
                data['payload'] = f'{data.get("payload")}\r'
            except Exception as e:
                self.logger.error(f'ERROR {e}')
        return data
