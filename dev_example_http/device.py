'''
Example class for TCP request connections.

This class reads arbitrary URLs or parametrized URLs using plugin configuration
for `host` and `port`.

See ``commands.py`` for command usage.
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

        super().__init__(device_id, device_name, command_class=MD_Command_Str, **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'device initialized from {__spec__.name} with arguments {kwargs}')
