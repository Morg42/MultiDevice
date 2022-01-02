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
import json
import queue
import threading

from collections import OrderedDict
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
        self._params = {PLUGIN_ARG_NET_HOST: '',
                        PLUGIN_ARG_NET_PORT: 0,
                        PLUGIN_ARG_AUTORECONNECT: True,
                        PLUGIN_ARG_CONN_RETRIES: 1,
                        PLUGIN_ARG_CONN_CYCLE: 3,
                        PLUGIN_ARG_TIMEOUT: 3,
                        PLUGIN_ARG_TERMINATOR: b'\r\n',
                        'disconnected_callback': None}

        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()

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


class MD_Connection_Net_Tcp_Jsonrpc(MD_Connection):
    '''
    This class implements a TCP connection to send JSONRPC 2.0 compatible messages
    and an anynchronous listener with callback for receiving data. As JSONRPC includes
    message-ids, replies can be associated to their respective queries and reply
    tracing and command repeat functions are implemented.

    Data received is dispatched via callback, thus the send()-method does not
    return any response data.

    Callback syntax is:
        def connected_callback(by)
        def disconnected_callback()
        def data_received_callback(command, message)
    If callbacks are class members, they need the additional first parameter 'self'

    :param device_type: device type as used in commands.py name
    :param device_id: device id for use in item configuration and logs
    :type device_type: str
    :type device_id: str
    '''
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        self.logger.debug(f'connection initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self.connected = False
        self._shutdown_active = False

        self._message_id = 0
        self._msgid_lock = threading.Lock()
        self._send_queue = queue.Queue()
        self._stale_lock = threading.Lock()

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ARG_NET_HOST: '',
                        PLUGIN_ARG_NET_PORT: 9090,
                        PLUGIN_ARG_AUTORECONNECT: True,
                        PLUGIN_ARG_CONN_RETRIES: 1,
                        PLUGIN_ARG_CONN_CYCLE: 3,
                        PLUGIN_ARG_TIMEOUT: 3,
                        PLUGIN_ARG_MSG_REPEAT: 3,
                        PLUGIN_ARG_MSG_TIMEOUT: 5,
                        PLUGIN_ARG_CB_ON_DISCONNECT: None,
                        PLUGIN_ARG_CB_ON_CONNECT: None}

        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()

        # self._message_archive[str message_id] = [time() sendtime, str method, str params or None, int repeat]
        self._message_archive = {}

        self._check_stale_cycle = float(self._message_timeout) / 2
        self._next_stale_check = 0
        self._last_stale_check = 0

        self._data_received_callback = data_received_callback
        self._disconnected_callback = self._params['disconnected_callback']

        # initialize connection
        self._tcp = Tcp_client(host=self._host, port=self._port, name=f'{device_id}-TcpConnection',
                               autoreconnect=self._autoreconnect, connect_retries=self._connect_retries,
                               connect_cycle=self._connect_cycle)
        self._tcp.set_callbacks(data_received=self.on_data_received,
                                disconnected=self.on_disconnect,
                                connected=self.on_connect)

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

    def on_connect(self, by=None):
        '''
        Recall method for succesful connect

        :param by: caller information
        :type by: str
        '''
        self.connected = True
        if isinstance(by, (dict, Tcp_client)):
            by = 'TCP_Connect'
        self.logger.info(f'Connected to {self._host}, onconnect called by {by}, send queue contains {self._send_queue.qsize()} commands')
        if self._connected_callback:
            self._connected_callback(by)

    def on_disconnect(self, obj=None):
        ''' Recall method for TCP disconnect '''
        self.logger.info(f'Received disconnect from {self._host}')
        self.connected = False

        # did we power down kodi? then clear queues
        if self._shutdown_active:
            old_queue = self._send_queue
            self._send_queue = queue.Queue()
            del old_queue
            self._stale_lock.acquire()
            self._message_archive = {}
            self._stale_lock.release()
            self._shutdown_active = False

        if self._disconnected_callback:
            self._disconnected_callback()

    def on_data_received(self, connection, response):
        ''' Recall method for TCP message reception '''
        if response:
            self.logger.debug(f'received raw data "{response}" from {connection.name}')
        else:
            return

        response = str(response, 'utf-8').strip()

        # split multi-response data into list items
        try:
            datalist = response.replace('}{', '}-#-{').split('-#-')
            datalist = list(OrderedDict((x, True) for x in datalist).keys())
        except:
            datalist = [response]

        # process all response items
        for data in datalist:
            self.logger.debug(f'Processing received data item #{datalist.index(data)} ({data})')

            try:
                jdata = json.loads(data)
            except Exception as err:
                self.logger.warning(f'Could not json.load data item {data} with error {err}')
                continue

            method = None

            # check messageid for replies
            if 'id' in jdata:
                response_id = jdata['id']

                # reply or error received, remove command
                if response_id in self._message_archive:
                    # possibly the command was resent and removed before processing the reply
                    # so let's 'try' at least...
                    try:
                        method = self._message_archive[response_id][1]
                        del self._message_archive[response_id]
                    except KeyError:
                        method = '(deleted)' if '_' not in response_id else response_id[response_id.find('_') + 1:]
                else:
                    method = None

                # log possible errors
                if 'error' in jdata:
                    self.logger.error(f'received error {jdata} in response to command {method}')
                elif method:
                    self.logger.debug(f'command {method} sent successfully')

            # process data
            if self._data_received_callback:
                self._data_received_callback(method, jdata)

        # check _message_archive for old commands - check time reached?
        if self._next_stale_check < time():

            # try to lock check routine, fail quickly if already locked = running
            if self._stale_lock.acquire(False):

                # we cannot deny access to self._message_archive as this would block sending
                # instead, copy it and check the copy
                stale_messages = self._message_archive.copy()
                remove_ids = []
                requeue_cmds = []

                # self._message_archive[message_id] = [time(), method, params, repeat]
                self.logger.debug('Checking for unanswered commands, last check was {} seconds ago, {} commands saved'.format(int(time()) - self._last_stale_check, len(self._message_archive)))
                # !! self.logger.debug('Stale commands: {}'.format(stale_messages))
                for (message_id, (send_time, method, params, repeat)) in stale_messages.items():

                    if send_time + self._message_timeout < time():

                        # reply timeout reached, check repeat count
                        if repeat <= self._message_repeat:

                            # send again, increase counter
                            self.logger.info('Repeating unanswered command {} ({}), try {}'.format(method, params, repeat + 1))
                            requeue_cmds.append([method, params, message_id, repeat + 1])
                        else:
                            self.logger.info('Unanswered command {} ({}) repeated {} times, giving up.'.format(method, params, repeat))
                            remove_ids.append(message_id)

                for msgid in remove_ids:
                    # it is possible that while processing stale commands, a reply arrived
                    # and the command was removed. So just to be sure, 'try' and delete...
                    self.logger.debug('Removing stale msgid {} from archive'.format(msgid))
                    try:
                        del self._message_archive[msgid]
                    except KeyError:
                        pass

                # resend pending repeats - after original
                for (method, params, message_id, repeat) in requeue_cmds:
                    self._send_rpc_message(method, params, message_id, repeat)

                # set next stale check time
                self._last_stale_check = time()
                self._next_stale_check = self._last_stale_check + self._check_stale_cycle

                del stale_messages
                del requeue_cmds
                del remove_ids
                self._stale_lock.release()

            else:
                self.logger.debug(f'Skipping stale check {time() - self._last_stale_check} seconds after last check')

    def _send(self, data_dict):
        '''
        wrapper to prepare json rpc message to send. extracts method, id, repeat and
        params (data) from data_dict and call send_rpc_message(method, params, id, repeat)
        '''
        method = data_dict.get('payload', None)
        if not method:
            self.logger.error(f'can not send without "payload" data from data_dict {data_dict}, aborting')
            return False

        params = data_dict.get('data', None)
        message_id = data_dict.get('message_id', None)
        repeat = data_dict.get('repeat', 0)

        self._send_rpc_message(method, params, message_id, repeat)

        # we don't get a response (this goes via on_data_received), so we signal "no response"
        return False

    def _send_rpc_message(self, method, params=None, message_id=None, repeat=0):
        '''
        Send a JSON RPC message.
        The  JSON string is extracted from the supplied method and the given parameters.

        :param method: the Kodi method to be triggered
        :param params: parameters dictionary
        :param message_id: the message ID to be used. If none, use the internal counter
        :param repeat: counter for how often the message has been repeated
        '''
        self.logger.debug(f'preparing message to send method {method} with data {params}, try #{repeat}')

        if message_id is None:
            # safely acquire next message_id
            # !! self.logger.debug('Locking message id access ({})'.format(self._message_id))
            self._msgid_lock.acquire()
            self._message_id += 1
            new_msgid = self._message_id
            self._msgid_lock.release()
            message_id = str(new_msgid) + '_' + method
            # !! self.logger.debug('Releasing message id access ({})'.format(self._message_id))

        # create message packet
        data = {'jsonrpc': '2.0', 'id': message_id, 'method': method}
        if params:
            data['params'] = params
        try:
            send_command = json.dumps(data, separators=(',', ':'))
        except Exception as err:
            raise ValueError(f'problem with json.dumps: {err}, ignoring message. Error was {err}')

        # push message in queue
        # !! self.logger.debug('Queuing message {}'.format(send_command))
        self._send_queue.put([message_id, send_command, method, params, repeat])
        # !! self.logger.debug('Queued message {}'.format(send_command))

        # try to actually send all queued messages
        self.logger.debug(f'processing queue - {self._send_queue.qsize()} elements')
        while not self._send_queue.empty():
            (message_id, data, method, params, repeat) = self._send_queue.get()
            self.logger.debug(f'sending queued msg {message_id} - {data} (#{repeat})')
            self._tcp.send((data + '\r\n').encode())
            # !! self.logger.debug('Adding cmd to message archive: {} - {} (try #{})'.format(message_id, data, repeat))
            self._message_archive[message_id] = [time(), method, params, repeat]
            # !! self.logger.debug('Sent msg {} - {}'.format(message_id, data))
        # !! self.logger.debug('Processing queue finished - {} elements remaining'.format(self._send_queue.qsize()))


class MD_Connection_Net_Udp_Server(MD_Connection):
    # to be implemented
    pass


class MD_Connection_Serial_Client(MD_Connection):
    # to be implemented
    pass


class MD_Connection_Serial_Async(MD_Connection):
    # to be implemented
    pass
