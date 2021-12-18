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
import socket
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

    :param device_id: device type as used in commands.py name
    :param device_name: device name for use in item configuration and logs
    :type device_id: str
    :type device_name: str
    '''
    def __init__(self, device_id, device_name, data_received_callback, **kwargs):

        # get MultiDevice.device logger (if not already defined by derived class calling us via super().__init__())
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_name}')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_id = device_id
        self.device = device_name
        self.connected = False

        self._params = kwargs
        self._data_received_callback = data_received_callback

        # check if some of the arguments are usable
        self._set_connection_params()

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def open(self):
        self.logger.debug('open method called for connection')
        if self._open():
            self.connected = True
        self._send_init_on_open()

    def close(self):
        self.logger.debug('close method called for connection')
        self._close()
        self.connected = False

    def send(self, data_dict):
        '''
        Send data, possibly return response

        :param data: dict with raw data and possible additional parameters to send
        :type data_dict: dict
        :return: raw response data if applicable, None otherwise. Errors need to raise exceptions
        '''
        self._send_init_on_send()
        response = self._send(data_dict)

        return response

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
        self.logger.debug(f'opening connection as {__name__} for device {self.device} with params {self._params}')
        return True

    def _close(self):
        '''
        Overload with closing of connection
        '''
        self.logger.debug(f'closing connection as {__name__} for device {self.device} with params {self._params}')

    def _send(self, data_dict):
        '''
        Overload with sending of data and - possibly - returning response data
        Return None if no response is received or expected.
        '''
        self.logger.debug(f'device {self.device} simulating to send data {data_dict}...')
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

        It is routinely called by self.send()
        '''
        pass

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
                setattr(self, arg, sanitize_param(self._params[arg]))


class MD_Connection_Net_Tcp_Request(MD_Connection):
    '''
    This class implements a TCP connection in the query-reply matter using
    the requests library.

    The data_dict['payload']-Data needs to be the full query URL. Additional
    parameter dicts can be added to be given to requests.request, as
    - method: get (default) or post
    - headers, data, cookies, files, params: passed thru to request()

    Response data is returned as text. Errors raise HTTPException
    '''
    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} "opening connection" as {__name__} for device {self.device} with params {self._params}')
        return True

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} "closing connection" as {__name__} for device {self.device} with params {self._params}')

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


class MD_Connection_Net_Tcp_Reply(MD_Connection):
    '''
    This class implements a persistent TCP connection via sockets

    The data_dict['payload'] is sent as string 1:1; the remainder of data_dict is ignored.

    Response data is returned as text, or None in case of error

    NOTE: this is - as of now - not a good implementation, especially the "receive" part leaves quite some things to be desired. Use for testing only
    '''

    def __init__(self, device_id, device_name, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_name}')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_id = device_id
        self.device = device_name
        self.connected = False
        self._tcp = None
        self._buffer = b''

        self._params = {PLUGIN_ARG_NET_HOST: '', PLUGIN_ARG_NET_PORT: 0, 'autoreconnect': True, 'connect_retries': 5, 'connect_cycle': 30, 'timeout': 3, 'terminator': b'\x0a'}
        self._params.update(kwargs)
        self._data_received_callback = data_received_callback

        # check if some of the arguments are usable
        self._set_connection_params()

        self._autoreconnect = self._params['autoreconnect']
        self._connect_retries = self._params['connect_retries']
        self._connect_cycle = self._params['connect_cycle']
        self._terminator = self._params['terminator']

        if not (self.host != '' and self.port > 0):
            self.logger.error(f'insufficient configuration data (TCP {self.host}:{self.port}), not initializing connection') 
            return False

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def _open(self):
        if not self.connected:
            self.logger.debug(f'{self.__class__.__name__} "opening connection" as {__name__} for device {self.device} with params {self._params}')
            self._tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._tcp.setblocking(False)
            self._tcp.settimeout(5)
            try:
                self._tcp.settimeout(self.timeout)
                self._tcp.connect((f'{self.host}', int(self.port)))
                self.connected = True
                self.logger.debug(f'connection established to {self.host}:{self.port}')
            except Exception:
                self.logger.warning(f'could not establish a connection to {self.host}:{self.port}')

        return self.connected

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} "closing connection" as {__name__} for device {self.device} with params {self._params}')
        if self.connected:
            self._tcp.close()
            self.connected = False

    def _reconnect(self):
        if not self.connected and self._autoreconnect:
            attempt = 0
            while attempt < self._connect_retries and not self.connected:
                attempt += 1
                self.logger.info(f'autoreconnecting, attempt {attempt}/{self._connect_retries}')
                if self._open():
                    break
                sleep(self._connect_cycle)

            if not self.connected:
                self.logger.warning(f'Autoreconnect failed after {self._connect_retries} attempts')
                return False

    def _send(self, data_dict):
        # extract payload
        data = data_dict.get('payload', None)
        if not data:
            self.logger.error(f'Refusing to send empty payload from data_dict {data_dict}, aborting')
            return None

        if not self.connected and not self._reconnect():
            self.logger.error('Not connected and reconnect not requested or failed, aborting')
            return None

        # convert payload
        if not isinstance(data, (bytes, bytearray)):
            try:
                data = str(data)
            except Exception:
                pass
            try:
                data = data.encode('utf-8')
            except Exception as e:
                self.logger.warning(f'Error while encoding data {data} for remote {self.host}:{self.port}. Error was: {e}')
                return None

        # just send data, watch for closed socket (BrokenPipeError)
        # raise on unknown error, don't know what else to do
        try:
            self.logger.debug(f'Sending data {data} to {self.host}:{self.port}')
            self._tcp.send(data)
            self.logger.debug('Data sent')
        except BrokenPipeError:
            self.logger.warning(f'Detected disconnect from {self.host}, send failed.')
            self.connected = False
            if self._autoreconnect:
                self.logger.debug(f'Autoreconnect enabled for {self._host}')
                self._reconnect()
            return None
        except Exception as e:  # log errors we are not prepared to handle and raise exception for further debugging
            self.logger.warning(f'Unhandleded error on sending to {self.host}, cannot send data {data}. Error was: {e}')
            raise

        # receive buffer data until
        # - connection is gone
        # - terminator is found
        # - timeout is hit
        self.logger.debug(f'Reading response from {self.host}:{self.port}')
        buffer = bytearray()
        begin = time()

        # TODO: remove
        # self.logger.debug(f'starting read at {begin} from {self.host}:{self.port}')        
        while self.connected and self._terminator not in buffer and time() - begin <= self.timeout:
            try:
                sdata = bytearray()
                sdata = self._tcp.recv(8192)
                # TODO: remove
                # self.logger.debug(f'reading response part {sdata} from {self.host}:{self.port}')
                if sdata:
                    buffer += sdata
                else:
                    sleep(0.1)
            except BrokenPipeError:
                self.logger.warning(f'detected disconnect from {self.host} while receiving.')
                self.connected = False
                if self._autoreconnect:
                    self.logger.debug(f'Autoreconnect enabled for {self._host}')
                    self._reconnect()
                return None
            except Exception as e:
                # TODO: remove
                # self.logger.debug(f'reading response, ignoring exception {e} from {self.host}:{self.port}')
                pass

        # TODO: remove
        # self.logger.debug(f'quit read at {time()} from {self.host}:{self.port}')        

        # I'll be back...
        if buffer and self._terminator in buffer:

            # TODO: remove
            # self.logger.debug(f'checking result {buffer} for terminator {self._terminator} from {self.host}:{self.port}')        
            # return data up to first terminator
            tpos = buffer.find(self._terminator)
            # TODO: remove
            # self.logger.debug(f'found terminator at {tpos} from {self.host}:{self.port}')        
            result = buffer[:tpos].decode('utf-8').strip()
            # TODO: store remainder in class member and use for next receive...? implement locking
            self.logger.debug(f'received response {result} from {self.host}:{self.port}')
            return result
        elif time() - begin > self.timeout:
            self.logger.info(f'timeout while reading response from {self.host}.')
        elif not self.connected:
            self.logger.warning(f'disconnect detected while reading response from {self.host}.')
        else:
            self.logger.warning(f'received no reply from from {self.host}.')

        return None


class MD_Connection_Net_Tcp_Client(MD_Connection):
    '''
    This class implements a TCP connection using a single persistent connection
    to send data and an anynchronous listener with callback for receiving data.

    Data received is dispatched via callback, then send()-method does not
    return any response data.
    '''
    def __init__(self, device_id, device_name, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_name}')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_id = device_id
        self.device = device_name
        self.connected = False

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ARG_NET_HOST: '', PLUGIN_ARG_NET_PORT: 0, 'autoreconnect': True, 'connect_retries': 1, 'connect_cycle': 3, 'disconnected_callback': None, 'timeout': 3, 'terminator': b'\r\n'}
        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()
        self._autoreconnect = self._params['autoreconnect']
        self._connect_retries = self._params['connect_retries']
        self._connect_cycle = self._params['connect_cycle']
        self._terminator = self._params['terminator']

        self._data_received_callback = data_received_callback
        self._disconnected_callback = self._params['disconnected_callback']

        # initialize connection
        self._tcp = Tcp_client(host=self.host, port=self.port, name=f'{device_id}TcpConnection',
                               autoreconnect=self._autoreconnect, connect_retries=self._connect_retries,
                               connect_cycle=self._connect_cycle, terminator=self._terminator)
        self._tcp.set_callbacks(data_received=self.on_data_received,
                                disconnected=self.on_disconnect)

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} "opening connection" as {__name__} for device {self.device} with params {self._params}')
        if not self._tcp.connected():
            self._tcp.connect()
            sleep(2)
        return self._tcp.connected()

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} "closing connection" as {__name__} for device {self.device}')
        self._tcp.close()

    def on_disconnect(self):
        self.logger.debug('connection was closed')
        self.connected = False
        if self._disconnected_callback:
            self._disconnected_callback()

    def on_data_received(self, tcp_cli, data):
        data = data.strip()
        if data:
            self.logger.debug(f'received raw data "{data}" from "{tcp_cli.name}"')

            # as we don't know the command for which the reply was issued, we return None as command
            # the device class has to handle this in conjunction with the commands and datatypes
            if self._data_received_callback:
                self._data_received_callback(None, data)

    def _send(self, data_dict):
        data = data_dict.get('payload', None)
        if not data:
            self.logger.error(f'can not send without payload data from data_dict {data_dict}, aborting')
            return False

        if not self.connected:
            self.open()

            if not self.connected:
                self.logger.error(f'trying to send {data}, but connection can\'t be opened.')
                return False

        self._tcp.send(data)

        # we receive only via callback, so we return "no reply".
        return False


class MD_Connection_Net_Udp_Server(MD_Connection):
    pass


class MD_Connection_Serial_Client(MD_Connection):
    pass


class MD_Connection_Serial_Async(MD_Connection):
    pass
