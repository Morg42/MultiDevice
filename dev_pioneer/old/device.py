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

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-2]) + f'.{device_name}')

        super().__init__(device_id, device_name, conn_type='net_tcp_client', command_class=MD_Command_Str, **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'device initialized from {__spec__.name} with arguments {kwargs}')

    def _transform_send_data(self, data=None):
        if data:
            try:
                data['payload'] = f'{data.get("payload")}\r'
            except Exception as e:
                self.logger.error(f'ERROR {e}')
        return data
