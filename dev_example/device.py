#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

'''
Example class for TCP client (async receiving) connection.
'''
if MD_standalone:
    from MD_Globals import *
    from MD_Device import MD_Device
    from MD_Command import MD_Command_Str
else:
    from ..MD_Globals import *
    from ..MD_Device import MD_Device
    from ..MD_Command import MD_Command_Str

import logging


class MD_Device(MD_Device):

    def __init__(self, device_type, device_id, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-2]) + f'.{device_id}')

        # set parameter defaults
        # TODO: adapt these to actual requirements!
        self._params = {'command_class': MD_Command_Str,            # remember to import the needed class!
                        PLUGIN_ARG_CONNECTION: CONN_NET_TCP_CLI,    # check MD_Globals.py for constants
                        PLUGIN_ARG_NET_HOST: '', 
                        PLUGIN_ARG_NET_PORT: 0, 
                        PLUGIN_ARG_AUTORECONNECT: True,
                        PLUGIN_ARG_CONN_RETRIES: 5, 
                        PLUGIN_ARG_CONN_CYCLE: 3, 
                        PLUGIN_ARG_TIMEOUT: 3, 
                        PLUGIN_ARG_TERMINATOR: b'\r',
                        'disconnected_callback': None}

        super().__init__(device_type, device_id, **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'device initialized from {__spec__.name} with arguments {kwargs}')
