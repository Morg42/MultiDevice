#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

'''
Device class for Viessmann heating systems.
'''

if MD_standalone:
    from MD_Globals import *
    from MD_Device import MD_Device
    from MD_Command import MD_Command_Viessmann
    from MD_Protocol import MD_Protocol_Viessmann
else:
    from ..MD_Globals import *
    from ..MD_Device import MD_Device
    from ..MD_Command import MD_Command_Viessmann
    from ..MD_Protocol import MD_Protocol_Viessmann

import logging


class MD_Device(MD_Device):

    def __init__(self, device_type, device_id, **kwargs):
        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-2]) + f'.{device_id}')

        # set parameter defaults
        self._params = {'command_class': MD_Command_Viessmann, 
                        PLUGIN_ARG_PROTOCOL: PROTO_VIESSMANN}

        super().__init__(device_type, device_id, **kwargs)

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'device initialized from {__spec__.name} with arguments {kwargs}')

    def run_standalone(self):
        '''
        try to identify device
        '''
        self.get_device_type('P300')

    def read_addr(self, addr):
        '''
        Tries to read a data point indepently of item config

        :param addr: data point addr (2 byte hex address)
        :type addr: str
        :return: Value if read is successful, None otherwise
        '''
        addr = addr.lower()

        commandname = self._commands.get_command_from_reply(addr)
        if commandname is None:
            self.logger.debug(f'Address {addr} not defined in commandset, aborting')
            return None

        self.logger.debug(f'Attempting to read address {addr} for command {commandname}')

        return self.send_command(commandname)

    def read_temp_addr(self, addr, length=1, mult=0, signed=False):
        '''
        Tries to read an arbitrary supplied data point indepently of device config

        :param addr: data point addr (2 byte hex address)
        :type addr: str
        :param len: Length (in byte) expected from address read
        :type len: num
        :param mult: value multiplicator
        :type mult: num
        :param signed: specifies signed or unsigned value
        :type signed: bool
        :return: Value if read is successful, None otherwise
        '''
        # as we have no reference whatever concerning the supplied data, we do a few sanity checks...

        addr = addr.lower()

        if len(addr) != 4:              # addresses are 2 bytes
            self.logger.warning(f'temp address: address not 4 digits long: {addr}')
            return None

        for c in addr:                  # addresses are hex strings
            if c not in '0123456789abcdef':
                self.logger.warning(f'temp address: address digit "{c}" is not hex char')
                return None

        if length < 1 or length > 32:          # empiritistical choice
            self.logger.warning(f'temp address: len is not > 0 and < 33: {len}')
            return None

        # addr already known?
        cmd = self._commands.get_command_from_reply(addr)
        if cmd:
            self.logger.info(f'temp address {addr} already known for command {cmd}')
        else:
            # create temp commandset
            cmd = 'temp_cmd'
            cmdconf = {'read': True, 'write': False, 'opcode': addr, 'reply_token': addr, 'item_type': 'num', 'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', mult, signed, length]}
            self.logger.debug(f'Adding temporary command config {cmdconf} for command temp_cmd')
            self._commands._parse_commands(self.device_id, {cmd: cmdconf}, [cmd])

        res = self.read_addr(addr)

        if cmd == 'temp_cmd':
            del self._commands._commands['temp_cmd']

        return res

    def write_addr(self, addr, value):
        '''
        Tries to write a data point indepently of item config

        :param addr: data point addr (2 byte hex address)
        :type addr: str
        :param value: value to write
        :return: Value if read is successful, None otherwise
        '''
        addr = addr.lower()

        commandname = self._commands.get_command_from_reply(addr)
        if commandname is None:
            self.logger.debug(f'Address {addr} not defined in commandset, aborting')
            return None

        self.logger.debug(f'Attempting to write address {addr} with value {value} for command {commandname}')

        return self.send_command(commandname, value)

    def get_device_type(self, protocol):

        serialport = self._params.get('serialport', None)

        # try to connect and read device type info from 0x00f8
        self.logger.info(f'Trying protocol {protocol} on device {serialport}')

        # first, initialize Viessmann object for use
        self.alive = True
        self._params['viess_proto'] = protocol
        self._get_connection()
        self.set_runtime_data(read_commands=[], read_commands_grp=[], cycle_commands=[], initial_commands=[], callback=None)
        res = self._connection.open()

        if not res:
            self.logger.critical(f'Connection to {serialport} failed. Please check connection.')
            return None

        val = self.read_temp_addr('00f8', 2, 0, False)

        if val is None:
            raise ValueError('Error on communicating with the device, no response received. Unknown error.')

        # let it go...
        self._connection.close()

        if val is not None:
            return val
        else:
            return None
