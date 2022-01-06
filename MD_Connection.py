#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file aims to become part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  MD_Connection and derived classes for MultiDevice plugin
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import logging
from time import sleep, time
import requests
import serial
from threading import Lock

from lib.network import Tcp_client

if MD_standalone:
    from MD_Globals import *
else:
    from .MD_Globals import *


#############################################################################################################################################################################################################################################
#
# class MD_Connection and subclasses
#
#############################################################################################################################################################################################################################################

class MD_Connection(object):
    '''
    This class is the base class for further connection classes. It can - well,
    not much. Opening and closing of connections and writing and receiving data
    is something to implement in the interface-specific derived classes.

    :param device_type: device type as used in commands.py name
    :param device_id: device id for use in item configuration and logs
    :type device_type: str
    :type device_id: str
    '''
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger (if not already defined by derived class calling us via super().__init__())
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._data_received_callback = data_received_callback

        # set default parameters for the connection
        # as this base connection has no connection, we need no further parameters
        # when overloading, add defaults as needed
        self._params = {PLUGIN_ARG_CB_ON_DISCONNECT: None,
                        PLUGIN_ARG_CB_ON_CONNECT: None}
        self._params.update(kwargs)

        # convert params to protected properties (self._params['foo'] -> self._foo)
        self._set_connection_params()

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def open(self):
        ''' wrapper method provides stable interface and allows overloading '''
        self.logger.debug('open method called for connection')
        if self._open():
            self._is_connected = True
            self._send_init_on_open()

    def close(self):
        ''' wrapper method provides stable interface and allows overloading '''
        self.logger.debug('close method called for connection')
        self._close()
        self._is_connected = False

    def send(self, data_dict):
        '''
        Send data, possibly return response

        :param data: dict with raw data and possible additional parameters to send
        :type data_dict: dict
        :return: raw response data if applicable, None otherwise. Errors need to raise exceptions
        '''
        data = data_dict.get('payload', None)
        if not data:
            raise ValueError('send provided with empty data_dict["payload"], aborting')

        if self._send_init_on_send():
            response = self._send(data_dict)

        return response

    def on_data_received(self, by, data):
        ''' callback for on_data_received event '''
        if data:
            self.logger.debug(f'received raw data "{data}" from "{by}"')
            if self._data_received_callback:
                self._data_received_callback(by, data)

    def on_connect(self, by=None):
        ''' callback for on_connect event '''
        self._is_connected = True
        self.logger.info(f'on_connect called by {by}')
        if self._connected_callback:
            self._connected_callback(by)

    def on_disconnect(self, by=None):
        ''' callback for on_disconnect event '''
        self.logger.debug(f'on_disconnect called by {by}')
        self._is_connected = False
        if self._disconnected_callback:
            self._disconnected_callback()

    def connected(self):
        ''' getter for self._is_connected '''
        return self._is_connected

    #
    #
    # overloading needed for at least some of the following methods...
    #
    #

    def _open(self):
        '''
        Overload with opening of connection

        :return: True if successful
        :rtype: bool
        '''
        self.logger.debug(f'simulating opening connection as {__name__} with params {self._params}')
        return True

    def _close(self):
        '''
        Overload with closing of connection
        '''
        self.logger.debug(f'simulating closing connection as {__name__} with params {self._params}')

    def _send(self, data_dict):
        '''
        Overload with sending of data and - possibly - returning response data
        Return None if no response is received or expected.
        '''
        self.logger.debug(f'simulating to send data {data_dict}...')
        return None

    def _send_init_on_open(self):
        '''
        This class can be overloaded if anything special is needed to make the
        other side talk after opening the connection... ;)

        Using class properties instead of arguments makes overloading easy.

        It is routinely called by self.open()
        '''
        pass

    def _send_init_on_send(self):
        '''
        This class can be overloaded if anything special is needed to make the
        other side talk before sending commands... ;)

        Cancel sending if it returns False...

        It is routinely called by self.send()
        '''
        return True

    #
    #
    # private utility methods
    #
    #

    def _set_connection_params(self):
        '''
        Try to set some of the common parameters.
        Might need to be overloaded...
        '''
        for arg in PLUGIN_ARGS:
            if arg in self._params:
                setattr(self, '_' + arg, sanitize_param(self._params[arg]))

    def __str__(self):
        return self.__class__.__name__


class MD_Connection_Net_Tcp_Request(MD_Connection):
    '''
    This class implements TCP connections in the query-reply matter using
    the requests library, e.g. for HTTP communication.

    The data_dict['payload']-Data needs to be the full query URL. Additional
    parameter dicts can be added to be given to requests.request, as
    - method: get (default) or post
    - headers, data, cookies, files, params: passed thru to request()

    Response data is returned as text. Errors raise HTTPException
    '''
    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} "opening connection" as {__name__} with params {self._params}')
        return True

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} "closing connection" as {__name__} with params {self._params}')

    def _send(self, data_dict):
        url = data_dict.get('payload', None)
        if not url:
            self.logger.error(f'can not send without url parameter from data_dict {data_dict}, aborting')
            return False

        # default to get if not 'post' specified
        method = data_dict.get('method', 'get')

        # check for additional data
        par = {}
        for arg in ('headers', 'data', 'cookies', 'files', 'params'):
            par[arg] = data_dict.get(arg, {})

        # send data
        response = requests.request(method, url,
                                    params=par['params'],
                                    headers=par['headers'],
                                    data=par['data'],
                                    cookies=par['cookies'],
                                    files=par['files'])

        if 200 <= response.status_code < 400:
            return response.text
        else:
            try:
                err = ''
                response.raise_for_status()
            except requests.HTTPError as e:
                err = f' and error "{str(e)}"'
                self.logger.warning(f'TCP request returned code {response.status_code}{err}')
                raise e
        return None


class MD_Connection_Net_Tcp_Client(MD_Connection):
    '''
    This class implements a TCP connection using a single persistent connection
    to send data and an anynchronous listener with callback for receiving data.

    Data received is dispatched via callback, thus the send()-method does not
    return any response data.

    Callback syntax is:
        def disconnected_callback()
        def data_received_callback(command, message)
    If callbacks are class members, they need the additional first parameter 'self'
    '''
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._data_received_callback = data_received_callback

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ARG_NET_HOST: '',
                        PLUGIN_ARG_NET_PORT: 0,
                        PLUGIN_ARG_AUTORECONNECT: True,
                        PLUGIN_ARG_CONN_RETRIES: 1,
                        PLUGIN_ARG_CONN_CYCLE: 3,
                        PLUGIN_ARG_TIMEOUT: 3,
                        PLUGIN_ARG_TERMINATOR: None,
                        PLUGIN_ARG_CB_ON_DISCONNECT: None,
                        PLUGIN_ARG_CB_ON_CONNECT: None}
        self._params.update(kwargs)

        # convert params to protected properties (self._params['foo'] -> self._foo)
        self._set_connection_params()

        # initialize connection
        self._tcp = Tcp_client(host=self._host, port=self._port, name=f'{device_id}-TcpConnection',
                               autoreconnect=self._autoreconnect, connect_retries=self._connect_retries,
                               connect_cycle=self._connect_cycle, terminator=self._terminator)
        self._tcp.set_callbacks(data_received=self.on_data_received,
                                disconnected=self.on_disconnect,
                                connected=self.on_connect)

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} opening connection with params {self._params}')
        if not self._tcp.connected():
            self._tcp.connect()
            # give a moment to establish connection (threaded call). 
            # immediate return would always fail
            # "proper" control is executed by using on_connect callback
            sleep(2)
        return self._tcp.connected()

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} closing connection')
        self._tcp.close()

    def on_data_received(self, by, data):
        if isinstance(data, str):
            data = data.strip()
        super().on_data_received(by, data)

    def _send(self, data_dict):
        if not self._is_connected:
            self.open()

            if not self._is_connected:
                raise RuntimeError(f'trying to send {data_dict["payload"]}, but connection can\'t be opened.')

        self._tcp.send(data_dict['payload'])

        # we receive only via callback, so we return "no reply".
        return None


class MD_Connection_Net_Udp_Server(MD_Connection):
    # to be implemented
    pass


class MD_Connection_Serial(MD_Connection):
    '''
    This class implements a serial connection using a single persistent connection
    to send data and receive immediate answers.

    The data_dict provided to send() need the data to send in data_dict['payload']
    and the required response read mode in data_dict['data']['response']:


    If callbacks are provided, they are utilized; data_received_callback will be
    called in addition to returning the result to send() calls.

    Callback syntax is:
        def connected_callback(by=None)
        def disconnected_callback(by=None)
        def data_received_callback(by, message)
    If callbacks are class members, they need the additional first parameter 'self'
    '''
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._lock = Lock()
        self._lastbyte = b''
        self._lastbytetime = 0
        self._connection_attempts = 0

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ARG_SERIAL_PORT: '',
                        PLUGIN_ARG_SERIAL_BAUD: 9600,
                        PLUGIN_ARG_SERIAL_BSIZE: 8,
                        PLUGIN_ARG_SERIAL_PARITY: 'N',
                        PLUGIN_ARG_SERIAL_STOP: 1,
                        PLUGIN_ARG_PROTOCOL: None,
                        PLUGIN_ARG_TIMEOUT: 1,
                        PLUGIN_ARG_AUTORECONNECT: True,
                        PLUGIN_ARG_CONN_RETRIES: 1,
                        PLUGIN_ARG_CONN_CYCLE: 3,
                        PLUGIN_ARG_CB_ON_CONNECT: None,
                        PLUGIN_ARG_CB_ON_DISCONNECT: None}

        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()

        # initialize connection
        self._connection = serial.Serial()
        self._connection.baudrate = self._baudrate
        self._connection.parity = self._parity
        self._connection.bytesize = self._bytesize
        self._connection.stopbits = self._stopbits
        self._connection.port = self._serialport

        self._data_received_callback = data_received_callback

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} opening connection with params {self._params}')
        if self._is_connected:
            return True

        while not self._is_connected and self._connection_attempts <= self._connect_retries:

            self._connection_attempts += 1
            self._lock.acquire()
            try:
                self._connection.open()
                self._is_connected = True
                self.logger.info(f'connected to {self._serialport}')
                self._connection_attempts = 0
                if self._connected_callback:
                    self._connected_callback(f'serial_{self._serialport}')
                return True
            except (serial.SerialError, ValueError) as e:
                self.logger.error(f'error on connection to {self._serialport}. Error was: {e}')
                self._connection_attempts = 0
                return False
            finally:
                self._lock.release()

            if not self._is_connected:
                sleep(self._connect_cycle)

        self.logger.error(f'error on connection to {self._serialport}, max number of connection attempts reached')
        self._connection_attempts = 0
        return False

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} closing connection')
        self._is_connected = False
        try:
            self._connection.close()
        except Exception:
            pass
        self.logger.info(f'connection to {self._serialport} closed')
        if self._disconnected_callback:
            self._disconnected_callback(f'serial_{self._serialport}')

    def _send(self, data_dict):
        '''
        send data. data_dict needs to contain the following information:

        data_dict['payload']: data to send
        data_dict['data']['response']: number of bytes to read as response

        On errors, exceptions are raised

        :param data_dict: data_dict to send (used value is data_dict['payload'])
        :type data_dict: dict
        :return: response as bytes()
        data = data_dict.get('payload')
        '''
        data = data_dict['payload']
        if not type(data) in (bytes, bytearray, str):
            try:
                data = str(data)
            except Exception as e:
                raise ValueError(f'provided payload {data} could not be converted to string. Error was: {e}')
        if isinstance(data, str):
            data = data.encode('utf-8')

        if self._autoreconnect:
            self._open()

        if not self._is_connected:
            raise serial.SerialError(f'trying to send {data}, but connection can\'t be opened.')

        if not self._send_bytes(data):
            self.is_connected = False
            raise serial.SerialError(f'data {data} could not be sent')

        rlen = None
        if 'data' in data_dict:
            rlen = data_dict['data'].get('response', None)
        if rlen is None:
            return b''
        else:
            return self._read_bytes(rlen)

    def _send_bytes(self, packet):
        '''
        Send data to device

        :param packet: Data to be sent
        :type packet: bytearray|bytes
        :return: Returns False, if no connection is established or write failed; number of written bytes otherwise
        '''
        if not self._is_connected:
            return False

        try:
            numbytes = self._connection.write(packet)
        except serial.SerialTimeoutException:
            return False

        # self.logger.debug(f'_send_bytes: sent {packet} with {numbytes} bytes')
        return numbytes

    def _read_bytes(self, length):
        '''
        Try to read bytes from device, return read bytes
        if length is int > 0, try to read <length> bytes
        if length is bytes() or bytearray(), try to read till receiving <length>
        if length is 0, read until timeout (use with care...)

        :param length: Number of bytes to read, b'<terminator> for terminated read, 0 for unrestricted read (timeout)
        :return: read bytes
        :rtype: bytes
        '''
        if not self._is_connected:
            return b''

        totalreadbytes = bytes()
        # self.logger.debug('_read_bytes: start read')
        starttime = time()

        # don't wait for input indefinitely, stop after self._timeout seconds
        while time() <= starttime + self._timeout and self._is_connected:
            readbyte = self._connection.read()
            self._lastbyte = readbyte
            # self.logger.debug(f'_read_bytes: read {readbyte}')
            if readbyte != b'':
                self._lastbytetime = time.time()
            else:
                return totalreadbytes
            totalreadbytes += readbyte
            if isinstance(length, int) and length and len(totalreadbytes) >= length:
                return totalreadbytes
            elif isinstance(length, (bytes, bytearray)):
                if readbyte == length:
                    return totalreadbytes

        # timeout reached, did we read anything?
        if not totalreadbytes and not length:

            # just in case, force plugin to reconnect
            self._is_connected = False

        # return what we got so far, might be b''
        return totalreadbytes

    def reset_input_buffer(self):
        if self._connection:
            self._connection.reset_input_buffer()


class MD_Connection_Serial_Async(MD_Connection):
    # to be implemented
    pass
