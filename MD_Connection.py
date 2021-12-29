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
from time import sleep
import requests
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
                setattr(self, '_' + arg, sanitize_param(self._params[arg]))


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
        self.connected = False

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ARG_NET_HOST: '', PLUGIN_ARG_NET_PORT: 0, 'autoreconnect': True, 'connect_retries': 1, 'connect_cycle': 3, 'disconnected_callback': None, 'timeout': 3, 'terminator': b'\r\n'}
        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()
        self._autoreconnect = self._params[PLUGIN_ARG_AUTORECONNECT]
        self._connect_retries = self._params[PLUGIN_ARG_CONN_RETRIES]
        self._connect_cycle = self._params[PLUGIN_ARG_CONN_CYCLE]
        self._terminator = self._params[PLUGIN_ARG_TERMINATOR]

        self._data_received_callback = data_received_callback
        self._disconnected_callback = self._params['disconnected_callback']

        # initialize connection
        self._tcp = Tcp_client(host=self._host, port=self._port, name=f'{device_id}-TcpConnection',
                               autoreconnect=self._autoreconnect, connect_retries=self._connect_retries,
                               connect_cycle=self._connect_cycle, terminator=self._terminator)
        self._tcp.set_callbacks(data_received=self.on_data_received,
                                disconnected=self.on_disconnect)

        # tell someone about our actual class
        self.logger.debug(f'connection initialized from {self.__class__.__name__}')

    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} "opening connection" as {__name__} with params {self._params}')
        if not self._tcp.connected():
            self._tcp.connect()
            sleep(2)
        return self._tcp.connected()

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} "closing connection" as {__name__}')
        self._tcp.close()

    def on_disconnect(self, client):
        self.logger.debug(f'connection was closed by {client.name}')
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
    # to be implemented
    pass


class MD_Connection_Serial_Client(MD_Connection):
    # to be implemented
    pass


class MD_Connection_Serial_Async(MD_Connection):
    # to be implemented
    pass
