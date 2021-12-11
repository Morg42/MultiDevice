#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

'''
Example class for Pioneer AV Power On function.
'''
if MD_standalone:
    from MD_Device import MD_Device
    from MD_Command import MD_Command_Str
else:
    from ..MD_Device import MD_Device
    from ..MD_Command import MD_Command_Str

import logging


class MD_Device(MD_Device):

    def __init__(self, device_id, device_name, **kwargs):

        # get MultiDevice logger
        s, __, __ = __name__.rpartition('.')
        s, __, __ = s.rpartition('.')
        self.logger = logging.getLogger(s)

        # call base class init, request 'net_tcp_client' connection and MD_Command_Str command class
        super().__init__(device_id, device_name, conn_type='net_tcp_client', command_class=MD_Command_Str, **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'Device {device_name}: device initialized from {__spec__.name} with arguments {kwargs}')
