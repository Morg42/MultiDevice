#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

'''
Example class for Pioneer AV Power On function.
'''

from ..MD_Device import MD_Device
from ..MD_Commands import MD_Commands
from ..MD_Command import MD_Command_Str
import logging


class MD_Device(MD_Device):

    def __init__(self, device_id, device_name, standalone=False, **kwargs):

        # get MultiDevice logger
        s, __, __ = __name__.rpartition('.')
        s, __, __ = s.rpartition('.')
        self.logger = logging.getLogger(s)

        super().__init__(device_id, device_name, standalone=standalone, conn_type='net_tcp_cli', **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'Device {device_name}: device initialized from {__spec__.name} with arguments {kwargs}')

    def _read_configuration(self):
        self._commands = MD_Commands(self.device_id, self.device, MD_Command_Str, standalone=self._standalone, **self._plugin_params)
        return True
