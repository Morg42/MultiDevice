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
from threading import Lock, Thread
from contextlib import contextmanager

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
    """ MD_Connection class to provide actual connection support

    This class is the base class for further connection classes. It can - well,
    not much. Opening and closing of connections and writing and receiving data
    is something to implement in the interface-specific derived classes.

    :param device_type: device type as used in commands.py name
    :param device_id: device id for use in item configuration and logs
    :type device_type: str
    :type device_id: str
    """
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger (if not already defined by derived class calling us via super().__init__())
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        if MD_standalone:
            self.logger = logging.getLogger('__main__')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._data_received_callback = data_received_callback

        # set default parameters for the connection
        # as this base connection has no connection, we need no further parameters
        # when overwriting, add defaults as needed
        self._params = {PLUGIN_ATTR_CB_ON_DISCONNECT: None,
                        PLUGIN_ATTR_CB_ON_CONNECT: None}
        self._params.update(kwargs)

        # convert params to protected properties (self._params['foo'] -> self._foo)
        self._set_connection_params()

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def open(self):
        """ wrapper method provides stable interface and allows overwriting """
        self.logger.debug('open method called for connection')
        if self._open():
            self._is_connected = True
            self._send_init_on_open()

        return self._is_connected        

    def close(self):
        """ wrapper method provides stable interface and allows overwriting """
        self.logger.debug('close method called for connection')
        self._close()
        self._is_connected = False

    def send(self, data_dict):
        """
        Send data, possibly return response

        :param data: dict with raw data and possible additional parameters to send
        :type data_dict: dict
        :return: raw response data if applicable, None otherwise. Errors need to raise exceptions
        """
        if not self._is_connected:
            if self._autoreconnect:
                self._open()
            if not self._is_connected:
                raise RuntimeError(f'trying to send, but not connected')

        data = data_dict.get('payload', None)
        if not data:
            raise ValueError('send provided with empty data_dict["payload"], aborting')

        response = None
        
        if self._send_init_on_send():
            response = self._send(data_dict)

        return response

    def on_data_received(self, by, data):
        """ callback for on_data_received event """
        if data:
            self.logger.debug(f'received raw data "{data}" from "{by}"')
            if self._data_received_callback:
                self._data_received_callback(by, data)

    def on_connect(self, by=None):
        """ callback for on_connect event """
        self._is_connected = True
        self.logger.info(f'on_connect called by {by}')
        if self._connected_callback:
            self._connected_callback(by)

    def on_disconnect(self, by=None):
        """ callback for on_disconnect event """
        self.logger.debug(f'on_disconnect called by {by}')
        self._is_connected = False
        if self._disconnected_callback:
            self._disconnected_callback()

    def connected(self):
        """ getter for self._is_connected """
        return self._is_connected

    #
    #
    # overwriting needed for at least some of the following methods...
    #
    #

    def _open(self):
        """
        overwrite with opening of connection

        :return: True if successful
        :rtype: bool
        """
        self.logger.debug(f'simulating opening connection as {__name__} with params {self._params}')
        return True

    def _close(self):
        """
        overwrite with closing of connection
        """
        self.logger.debug(f'simulating closing connection as {__name__} with params {self._params}')

    def _send(self, data_dict):
        """
        overwrite with sending of data and - possibly - returning response data
        Return None if no response is received or expected.
        """
        self.logger.debug(f'simulating to send data {data_dict}...')
        return None

    def _send_init_on_open(self):
        """
        This class can be overwritten if anything special is needed to make the
        other side talk after opening the connection... ;)

        Using class properties instead of arguments makes overwriting easy.

        It is routinely called by self.open()
        """
        pass

    def _send_init_on_send(self):
        """
        This class can be overwritten if anything special is needed to make the
        other side talk before sending commands... ;)

        Cancel sending if it returns False...

        It is routinely called by self.send()
        """
        return True

    #
    #
    # private utility methods
    #
    #

    def _set_connection_params(self):
        """
        Try to set some of the common parameters.
        Might need to be overwritten...
        """
        for arg in PLUGIN_ATTRS:
            if arg in self._params:
                setattr(self, '_' + arg, sanitize_param(self._params[arg]))

    def __str__(self):
        return self.__class__.__name__


class MD_Connection_Net_Tcp_Request(MD_Connection):
    """ Connection via TCP / HTTP requests

    This class implements TCP connections in the query-reply matter using
    the requests library, e.g. for HTTP communication.

    The data_dict['payload']-Data needs to be the full query URL. Additional
    parameter dicts can be added to be given to requests.request, as
    - method: get (default) or post
    - headers, data, cookies, files, params: passed thru to request()

    Response data is returned as text. Errors raise HTTPException
    """
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
    """ Connection via direct TCP connection with listener

    This class implements a TCP connection using a single persistent connection
    to send data and an anynchronous listener with callback for receiving data.

    Data received is dispatched via callback, thus the send()-method does not
    return any response data.

    Callback syntax is:
        def disconnected_callback()
        def data_received_callback(command, message)
    If callbacks are class members, they need the additional first parameter 'self'
    """
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        if MD_standalone:
            self.logger = logging.getLogger('__main__')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._data_received_callback = data_received_callback

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ATTR_NET_HOST: '',
                        PLUGIN_ATTR_NET_PORT: 0,
                        PLUGIN_ATTR_CONN_AUTO_CONN: True,
                        PLUGIN_ATTR_CONN_RETRIES: 1,
                        PLUGIN_ATTR_CONN_CYCLE: 3,
                        PLUGIN_ATTR_CONN_TIMEOUT: 3,
                        PLUGIN_ATTR_CONN_TERMINATOR: None,
                        PLUGIN_ATTR_CB_ON_DISCONNECT: None,
                        PLUGIN_ATTR_CB_ON_CONNECT: None}
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

    def _send(self, data_dict):
        self._tcp.send(data_dict['payload'])

        # we receive only via callback, so we return "no reply".
        return None


class MD_Connection_Net_Udp_Server(MD_Connection):
    # to be implemented
    pass


class MD_Connection_Serial(MD_Connection):
    """ Connection for serial connectivity

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
    """
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        class TimeoutLock(object):
            def __init__(self):
                self._lock = Lock()

            def acquire(self, blocking=True, timeout=-1):
                return self._lock.acquire(blocking, timeout)

            @contextmanager
            def acquire_timeout(self, timeout):
                result = self._lock.acquire(timeout=timeout)
                yield result
                if result:
                    self._lock.release()

            def release(self):
                self._lock.release()

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        if MD_standalone:
            self.logger = logging.getLogger('__main__')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._lock = TimeoutLock()
        self.__lock_timeout = 2         # TODO: validate this is a sensible value
        self._timeout_mult = 3
        self._lastbyte = b''
        self._lastbytetime = 0
        self._connection_attempts = 0
        self._read_buffer = b''
        self.__use_read_buffer = True
        self.__running = False

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ATTR_SERIAL_PORT: '',
                        PLUGIN_ATTR_SERIAL_BAUD: 9600,
                        PLUGIN_ATTR_SERIAL_BSIZE: 8,
                        PLUGIN_ATTR_SERIAL_PARITY: 'N',
                        PLUGIN_ATTR_SERIAL_STOP: 1,
                        PLUGIN_ATTR_PROTOCOL: None,
                        PLUGIN_ATTR_CONN_BINARY: False,
                        PLUGIN_ATTR_CONN_TIMEOUT: 1.0,
                        PLUGIN_ATTR_CONN_AUTO_CONN: True,
                        PLUGIN_ATTR_CONN_RETRIES: 1,
                        PLUGIN_ATTR_CONN_CYCLE: 3,
                        PLUGIN_ATTR_CB_ON_CONNECT: None,
                        PLUGIN_ATTR_CB_ON_DISCONNECT: None}

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
        self._connection.timeout = self._timeout

        self._data_received_callback = data_received_callback

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} _open called with params {self._params}')
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
                    self._connected_callback(self)
                self._setup_listener()
                return True
            except (serial.SerialException, ValueError) as e:
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
        self.logger.debug(f'{self.__class__.__name__} _close called')
        self._is_connected = False
        try:
            self._connection.close()
        except Exception:
            pass
        self.logger.info(f'connection to {self._serialport} closed')
        if self._disconnected_callback:
            self._disconnected_callback(self)

    def _send(self, data_dict):
        """
        send data. data_dict needs to contain the following information:

        data_dict['payload']: data to send
        data_dict['limit_response']: expected response type/length:
                                     - number of bytes to read as response
                                     - terminator to recognize end of reply
                                     - 0 to read till timeout

        On errors, exceptions are raised

        :param data_dict: data_dict to send (used value is data_dict['payload'])
        :type data_dict: dict
        :return: response as bytes() or None if no response is received or limit_response is None
        """
        self.logger.debug(f'{self.__class__.__name__} _send called with {data_dict}')

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
            raise serial.SerialException(f'trying to send {data}, but connection can\'t be opened.')

        if not self._send_bytes(data):
            self.is_connected = False
            raise serial.SerialException(f'data {data} could not be sent')

        # don't try to read response if listener is active
        if self.__running:
            return None

        rlen = data_dict.get('limit_response', None)
        if rlen is None:
            return None
        else:
            res = self._read_bytes(rlen)
            if not self._binary:
                res = str(res, 'utf-8').strip()

            if self._data_received_callback:
                self._data_received_callback(self, res, None)

            return res

    def _send_bytes(self, packet):
        """
        Send data to device

        :param packet: Data to be sent
        :type packet: bytearray|bytes
        :return: Returns False, if no connection is established or write failed; number of written bytes otherwise
        """
        # self.logger.debug(f'{self.__class__.__name__} _send_bytes called with {packet}')

        if not self._is_connected:
            self.logger.debug('_send_bytes not connected, aborting')
            return False

        try:
            numbytes = self._connection.write(packet)
        except serial.SerialTimeoutException:
            return False

        # self.logger.debug(f'_send_bytes: sent {packet} with {numbytes} bytes')
        return numbytes

    def _read_bytes(self, limit_response, clear_buffer=False):
        """
        Try to read bytes from device, return read bytes
        if limit_response is int > 0, try to read at least <limit_response> bytes
        if limit_response is bytes() or bytearray(), try to read till receiving <limit_response>
        if limit_response is 0, read until timeout (use with care...)

        :param limit_response: Number of bytes to read, b'<terminator> for terminated read, 0 for unrestricted read (timeout)
        :return: read bytes
        :rtype: bytes
        """
        self.logger.debug(f'{self.__class__.__name__} _read_bytes called with limit {limit_response}')

        if not self._is_connected:
            return 0

        maxlen = 0
        term_bytes = None
        if isinstance(limit_response, int):
            maxlen = limit_response
        elif isinstance(limit_response, (bytes, bytearray, str)):
            term_bytes = bytes(limit_response)

        # take care of "overflow" from last read
        if clear_buffer:
            totalreadbytes = b''
        else:
            totalreadbytes = self._read_buffer
        self._read_buffer = b''

        # self.logger.debug('_read_bytes: start read')
        starttime = time()

        # prevent concurrent read attempts; 
        with self._lock.acquire_timeout(self.__lock_timeout) as locked:

            if locked:
                # don't wait for input indefinitely, stop after 3 * self._timeout seconds
                while time() <= starttime + self._timeout_mult * self._timeout:
                    readbyte = self._connection.read()
                    self._lastbyte = readbyte
                    # self.logger.debug(f'_read_bytes: read {readbyte}')
                    if readbyte != b'':
                        self._lastbytetime = time()
                    else:
                        return totalreadbytes
                    totalreadbytes += readbyte

                    # limit_response reached?
                    if maxlen and len(totalreadbytes) >= maxlen:
                        return totalreadbytes

                    if term_bytes and term_bytes in totalreadbytes:
                        if self.__use_read_buffer:
                            pos = totalreadbytes.find(term_bytes)
                            self._read_buffer += totalreadbytes[pos + len(term_bytes):]
                            return totalreadbytes[:pos + len(term_bytes)]
                        else:
                            return totalreadbytes
            else:
                self.logger.warning('read_bytes couldn\'t get lock on serial. Ths is unintended...')

        # timeout reached, did we read anything?
        if not totalreadbytes and not self.__running:

            # just in case, force plugin to reconnect
            self._is_connected = False

        # return what we got so far, might be b''
        return totalreadbytes

    def reset_input_buffer(self):
        if self._connection:
            self._connection.reset_input_buffer()

    def _setup_listener(self):
        """ empty, for subclass use """
        pass


class MD_Connection_Serial_Async(MD_Connection_Serial):
    """ Connection for serial connectivity with async listener

    This class implements a serial connection for call-based sending and a
    threaded listener for async reading with callbacks.

    As this is derived from ``MD_Connection_Serial``, most of the documentation
    is identical.

    The timeout needs to be set small enough not to block reading for too long.
    Recommended times are between 0.2 and 0.8 seconds.

    The ``data_received_callback`` needs to be set or you won't get data.

    Callback syntax is:
        def connected_callback(by=None)
        def disconnected_callback(by=None)
        def data_received_callback(by, message)
    If callbacks are class members, they need the additional first parameter 'self'
    """
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):
        # set additional class members
        self.__receive_thread = None
        super().__init__(device_type, device_id, data_received_callback, **kwargs)
        # self._timeout_mult = 1.5

    def _setup_listener(self):
        if not self._is_connected:
            return

        self.__running = True
        self.__receive_thread = Thread(target=self.__receive_thread_worker, name=f'{self.device_id}_Serial')
        self.__receive_thread.daemon = True
        self.__receive_thread.start()

    def _close(self):
        self.logger.debug(f'stopping receive thread {self.__receive_thread.name}')
        self.__running = False
        try:
            self.__receive_thread.join()
        except Exception:
            pass

    def __receive_thread_worker(self):
        """ thread worker to handle receiving """
        __buffer = b''

        self._is_receiving = True
        # try to find possible "hidden" errors
        try:
            while self._is_connected and self.__running:
                try:
                    msg = self._read_bytes(0)
                except serial.SerialTimeoutException:
                    pass

                if msg:

                    # If we work in line mode (with a terminator) slice buffer into single chunks based on terminator
                    if self._terminator:
                        __buffer += msg
                        while True:
                            # terminator = int means fixed size chunks
                            if isinstance(self._terminator, int):
                                i = self._terminator
                                if i > len(__buffer):
                                    break
                            # terminator is str or bytes means search for it
                            else:
                                i = __buffer.find(self._terminator)
                                if i == -1:
                                    break
                                i += len(self._terminator)
                            line = __buffer[:i]
                            __buffer = __buffer[i:]
                            if self._data_received_callback:
                                self._data_received_callback(self, line if self._binary else str(line, 'utf-8').strip())
                    # If not in terminator mode just forward what we received

                if not self.__running:
                    # socket shut down by self.close, no error
                    self.logger.debug('serial connection shut down by call to close method')
                    return

        except Exception as e:
            if not self.__running:
                self.logger.debug(f'serial receive thread {self.__receive_thread.name} shutting down')
                return
            else:
                self.logger.error(f'serial receive thread {self.__receive_thread.name} died with unexpected error: {e}')
