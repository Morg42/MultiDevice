#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

'''
Device class for Pioneer AV function.
'''
if MD_standalone:
    from MD_Device import MD_Device
    from MD_Command import MD_Command, MD_Command_ParseStr
    from MD_Commands import MD_Commands
else:
    from ..MD_Device import MD_Device
    from ..MD_Command import MD_Command, MD_Command_ParseStr
    from ..MD_Commands import MD_Commands

import logging


class MD_Device(MD_Device):

    def __init__(self, device_id, device_name, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-2]) + f'.{device_name}')

        super().__init__(device_id, device_name, conn_type='net_tcp_client', command_class=MD_Command_ParseStr, **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'device initialized from {__spec__.name} with arguments {kwargs}')

    def _transform_send_data(self, data=None):
        if data:
            try:
                data['payload'] = f'{data.get("payload")}\r'
            except Exception as e:
                self.logger.error(f'ERROR {e}')
        return data

    def _read_configuration(self):
        '''
        This initiates reading of configuration.
        Basically, this calls the MD_Commands object to fill itselt; but if needed,
        this can be overloaded to do something else.
        '''
        cls = self._command_class
        if cls is None:
            cls = MD_Command
        self._commands = MD_Commands(self.device_id, self.device, cls, **self._plugin_params)
        return True
