from .. import MD_Device, MD_Commands, MD_Command_Str
import logging


class MD_Device(MD_Device):

    def __init__(self, device_id, device_name, **kwargs):

        # get MultiDevice logger
# NOTE: later on, decide if every device logs to its own logger?
        s, __, __ = __name__.rpartition('.')
        s, __, __ = s.rpartition('.')
        self.logger = logging.getLogger(s)

        super().__init__(device_id, device_name, **kwargs)

        # TODO - remove when done. say hello
        self.logger.debug(f'Device {device_name}: device initialized from {__spec__.name} with arguments {kwargs}')

    def _read_configuration(self):
        self._commands = MD_Commands(self.device_id, self.device, MD_Command_Str, **self._plugin_params)
        return True
