#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file aims to become part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  MD_Protocol and derived classes for MultiDevice plugin
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
from time import time

if MD_standalone:
    from MD_Globals import *
    from MD_Connection import MD_Connection, MD_Connection_Net_Tcp_Client
else:
    from .MD_Globals import *
    from .MD_Connection import MD_Connection, MD_Connection_Net_Tcp_Client


from collections import OrderedDict
import threading
import queue
import json


#############################################################################################################################################################################################################################################
#
# class MD_Protocol and subclasses
#
#############################################################################################################################################################################################################################################

class MD_Protocol(MD_Connection):
    '''
    This class implements a basic protocol layer to act as a standin between
    the MD_Device-class and the MD_Connection-class. Its purpose is to enable
    establishing a control layer, so the connection only has to care for the
    'physical' connection and the device only needs to operate on commmand basis.

    This implementation can also be seen as a 'NULL' protocol, it only passes
    along everything.

    By overloading this class, different protocols can be implemented independent
    of the device and the connection classes.
    '''

    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        self.logger.debug(f'protocol initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._data_received_callback = data_received_callback

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ARG_CB_ON_DISCONNECT: None,
                        PLUGIN_ARG_CB_ON_CONNECT: None,
                        PLUGIN_ARG_CONNECTION: MD_Connection}
        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()

        # initialize connection
        conn_params = self._params.copy()
        conn_params.update({PLUGIN_ARG_CB_ON_CONNECT: self.on_connect, PLUGIN_ARG_CB_ON_DISCONNECT: self.on_disconnect})
        self._connection = self._params[PLUGIN_ARG_CONNECTION](device_type, device_id, self.on_data_received, **conn_params)

        # tell someone about our actual class
        self.logger.debug(f'protocol initialized from {self.__class__.__name__}')

    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} opening protocol with params {self._params}')
        if not self._connection.connected():
            self._connection.open()

        return self._connection.connected()

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} closing protocol')
        self._connection.close()

    def _send(self, data_dict):
        return self._connection.send(data_dict)


class MD_Protocol_Jsonrpc(MD_Protocol):
    '''
    This class implements a protocol to send JSONRPC 2.0  compatible messages
    As JSONRPC includes message-ids, replies can be associated to their respective
    queries and reply tracing and command repeat functions are implemented.

    Data received is dispatched via callback, thus the send()-method does not
    return any response data.

    Callback syntax is:
        def connected_callback(by=None)
        def disconnected_callback(by=None)
        def data_received_callback(by, message, command=None)
    If callbacks are class members, they need the additional first parameter 'self'

    :param device_type: device type as used in commands.py name
    :param device_id: device id for use in item configuration and logs
    :type device_type: str
    :type device_id: str
    '''
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        self.logger.debug(f'protocol initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
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
                        PLUGIN_ARG_CB_ON_CONNECT: None,
                        PLUGIN_ARG_CONNECTION: CONN_NET_TCP_CLI}
        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()

        # self._message_archive[str message_id] = [time() sendtime, str method, str params or None, int repeat]
        self._message_archive = {}

        self._check_stale_cycle = float(self._message_timeout) / 2
        self._next_stale_check = 0
        self._last_stale_check = 0

        self._data_received_callback = data_received_callback

        # initialize connection
        conn_params = self._params.copy()
        conn_params.update({PLUGIN_ARG_CB_ON_CONNECT: self.on_connect, PLUGIN_ARG_CB_ON_DISCONNECT: self.on_disconnect})
        self._connection = self._params[PLUGIN_ARG_CONNECTION](device_type, device_id, self.on_data_received, **conn_params)

        # tell someone about our actual class
        self.logger.debug(f'protocol initialized from {self.__class__.__name__}')

    def on_connect(self, by=None):
        self.logger.info(f'onconnect called by {by}, send queue contains {self._send_queue.qsize()} commands')
        super().on_connect(by)

    def on_disconnect(self, obj=None):
        super().on_disconnect(by)

        # did we power down kodi? then clear queues
        if self._shutdown_active:
            old_queue = self._send_queue
            self._send_queue = queue.Queue()
            del old_queue
            self._stale_lock.acquire()
            self._message_archive = {}
            self._stale_lock.release()
            self._shutdown_active = False

    def on_data_received(self, connection, response):
        if isinstance(response, (bytes, bytearray)):
            response = str(response, 'utf-8').strip()

        # split multi-response data into list items
        try:
            datalist = response.replace('}{', '}-#-{').split('-#-')
            datalist = list(OrderedDict((x, True) for x in datalist).keys())
        except Exception:
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
                self._data_received_callback(connection, jdata, method)

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
        method = data_dict.get('payload')
        params = data_dict.get('data', None)
        message_id = data_dict.get('message_id', None)
        repeat = data_dict.get('repeat', 0)

        self._send_rpc_message(method, params, message_id, repeat)

        # we don't get a response (this goes via on_data_received), so we signal "no response"
        return None

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
            self._connection.send({'payload': data})
            # !! self.logger.debug('Adding cmd to message archive: {} - {} (try #{})'.format(message_id, data, repeat))
            self._message_archive[message_id] = [time(), method, params, repeat]
            # !! self.logger.debug('Sent msg {} - {}'.format(message_id, data))
        # !! self.logger.debug('Processing queue finished - {} elements remaining'.format(self._send_queue.qsize()))
