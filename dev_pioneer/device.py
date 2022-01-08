#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

'''
Device class for Pioneer AV function.

Most of the work is done by the base class, so we only set default parameters
for the connection (to be overwritten by device attributes from the plugin
configuration) and add a fixed terminator byte to outgoing datagrams.

The know-how is in the commands.py (and some DT_ classes...)
'''
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

    def __init__(self, device_type, device_id, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-2]) + f'.{device_id}')

        # set parameter defaults
        self._params = {'command_class': MD_Command_ParseStr, 
                        PLUGIN_ARG_NET_HOST: '', 
                        PLUGIN_ARG_NET_PORT: 8102, 
                        PLUGIN_ARG_AUTORECONNECT: True,
                        PLUGIN_ARG_CONN_RETRIES: 5, 
                        PLUGIN_ARG_CONN_CYCLE: 3, 
                        PLUGIN_ARG_TIMEOUT: 3, 
                        PLUGIN_ARG_TERMINATOR: b'\r',
                        'disconnected_callback': None}

        # set our own preferences concerning connections
        if PLUGIN_ARG_NET_HOST in kwargs and kwargs[PLUGIN_ARG_NET_HOST]:
            self._params[PLUGIN_ARG_CONNECTION] = CONN_NET_TCP_CLI
        elif PLUGIN_ARG_SERIAL_PORT in kwargs and kwargs[PLUGIN_ARG_SERIAL_PORT]:
            self._params[PLUGIN_ARG_CONNECTION] = CONN_SER_DIR

        super().__init__(device_type, device_id, **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'device initialized from {__spec__.name} with arguments {kwargs}')

    def _transform_send_data(self, data=None):
        if data:
            try:
                if 'data' in not data:
                    data['data'] = {}
                data['data']['limit_response'] = self._terminator
                data['payload'] = f'{data.get("payload")}\r'
            except Exception as e:
                self.logger.error(f'ERROR {e}')
        return data
