from ..MD_Device import MD_Device
import logging


class MD_Device(MD_Device):

    def __init__(self, device_id, device_name, standalone=False, **kwargs):

        # get MultiDevice logger
# NOTE: later on, decide if every device logs to its own logger?
        s, __, __ = __name__.rpartition('.')
        s, __, __ = s.rpartition('.')
        self.logger = logging.getLogger(s)

        super().__init__(device_id, device_name, standalone=standalone, **kwargs)

        # TODO - remove when done. say hello
        self.logger.debug(f'Device {device_name}: device initialized from {__spec__.name} with arguments {kwargs}')
