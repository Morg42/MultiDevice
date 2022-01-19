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

if MD_standalone:
    from MD_Globals import (CONN_NET_TCP_CLI, CONN_SER_DIR, PLUGIN_ATTR_CB_ON_CONNECT, PLUGIN_ATTR_CB_ON_DISCONNECT, PLUGIN_ATTR_CONNECTION, PLUGIN_ATTR_CONN_AUTO_CONN, PLUGIN_ATTR_CONN_BINARY, PLUGIN_ATTR_CONN_CYCLE, PLUGIN_ATTR_CONN_RETRIES, PLUGIN_ATTR_CONN_TIMEOUT, PLUGIN_ATTR_MSG_REPEAT, PLUGIN_ATTR_MSG_TIMEOUT, PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_NET_PORT, PLUGIN_ATTR_SERIAL_BAUD, PLUGIN_ATTR_SERIAL_BSIZE, PLUGIN_ATTR_SERIAL_PARITY, PLUGIN_ATTR_SERIAL_PORT, PLUGIN_ATTR_SERIAL_STOP)
    from MD_Connection import MD_Connection, MD_Connection_Net_Tcp_Client, MD_Connection_Serial
else:
    from .MD_Globals import (CONN_NET_TCP_CLI, CONN_SER_DIR, PLUGIN_ATTR_CB_ON_CONNECT, PLUGIN_ATTR_CB_ON_DISCONNECT, PLUGIN_ATTR_CONNECTION, PLUGIN_ATTR_CONN_AUTO_CONN, PLUGIN_ATTR_CONN_BINARY, PLUGIN_ATTR_CONN_CYCLE, PLUGIN_ATTR_CONN_RETRIES, PLUGIN_ATTR_CONN_TIMEOUT, PLUGIN_ATTR_MSG_REPEAT, PLUGIN_ATTR_MSG_TIMEOUT, PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_NET_PORT, PLUGIN_ATTR_SERIAL_BAUD, PLUGIN_ATTR_SERIAL_BSIZE, PLUGIN_ATTR_SERIAL_PARITY, PLUGIN_ATTR_SERIAL_PORT, PLUGIN_ATTR_SERIAL_STOP)
    from .MD_Connection import MD_Connection, MD_Connection_Net_Tcp_Client, MD_Connection_Serial


from collections import OrderedDict
from time import time, sleep
import threading
import queue
import json


#############################################################################################################################################################################################################################################
#
# class MD_Protocol and subclasses
#
#############################################################################################################################################################################################################################################

class MD_Protocol(MD_Connection):
    """ MD_Protocol class to provide protocol support for MD_Device

    This class implements a basic protocol layer to act as a standin between
    the MD_Device-class and the MD_Connection-class. Its purpose is to enable
    establishing a control layer, so the connection only has to care for the
    'physical' connection and the device only needs to operate on commmand basis.

    This implementation can also be seen as a 'NULL' protocol, it only passes
    along everything.

    By overwriting this class, different protocols can be implemented independent
    of the device and the connection classes.
    """

    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        if MD_standalone:
            self.logger = logging.getLogger('__main__')

        self.logger.debug(f'protocol initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._data_received_callback = data_received_callback

        # make sure we have a basic set of parameters
        self._params = {PLUGIN_ATTR_CB_ON_DISCONNECT: None,
                        PLUGIN_ATTR_CB_ON_CONNECT: None,
                        PLUGIN_ATTR_CONNECTION: MD_Connection}
        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()

        # initialize connection
        conn_params = self._params.copy()
        conn_params.update({PLUGIN_ATTR_CB_ON_CONNECT: self.on_connect, PLUGIN_ATTR_CB_ON_DISCONNECT: self.on_disconnect})
        self._connection = self._params[PLUGIN_ATTR_CONNECTION](device_type, device_id, self.on_data_received, **conn_params)

        # tell someone about our actual class
        self.logger.debug(f'protocol initialized from {self.__class__.__name__}')

    def _open(self):
        self.logger.debug(f'{self.__class__.__name__} _open called, opening protocol with params {self._params}')
        if not self._connection.connected():
            self._connection.open()

        self._is_connected = self._connection.connected()
        return self._is_connected

    def _close(self):
        self.logger.debug(f'{self.__class__.__name__} _close called, closing protocol')
        self._connection.close()
        self._is_connected = False

    def _send(self, data_dict):
        self.logger.debug(f'{self.__class__.__name__} _send called with {data_dict}')
        return self._connection.send(data_dict)


class MD_Protocol_Jsonrpc(MD_Protocol):
    """ Protocol support for JSON-RPC 2.0

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
    """
    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        if MD_standalone:
            self.logger = logging.getLogger('__main__')

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
        self._params = {PLUGIN_ATTR_NET_HOST: '',
                        PLUGIN_ATTR_NET_PORT: 9090,
                        PLUGIN_ATTR_CONN_AUTO_CONN: True,
                        PLUGIN_ATTR_CONN_RETRIES: 1,
                        PLUGIN_ATTR_CONN_CYCLE: 3,
                        PLUGIN_ATTR_CONN_TIMEOUT: 3,
                        PLUGIN_ATTR_MSG_REPEAT: 3,
                        PLUGIN_ATTR_MSG_TIMEOUT: 5,
                        PLUGIN_ATTR_CB_ON_DISCONNECT: None,
                        PLUGIN_ATTR_CB_ON_CONNECT: None,
                        PLUGIN_ATTR_CONNECTION: CONN_NET_TCP_CLI}
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
        conn_params.update({PLUGIN_ATTR_CB_ON_CONNECT: self.on_connect, PLUGIN_ATTR_CB_ON_DISCONNECT: self.on_disconnect})
        self._connection = self._params[PLUGIN_ATTR_CONNECTION](device_type, device_id, self.on_data_received, **conn_params)

        # tell someone about our actual class
        self.logger.debug(f'protocol initialized from {self.__class__.__name__}')

    def on_connect(self, by=None):
        self.logger.info(f'onconnect called by {by}, send queue contains {self._send_queue.qsize()} commands')
        super().on_connect(by)

    def on_disconnect(self, by=None):
        super().on_disconnect(by)

        # did we power down kodi? then clear queues
        if self._shutdown_active:
            self._send_queue = queue.Queue()
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
        """
        wrapper to prepare json rpc message to send. extracts method, id, repeat and
        params (data) from data_dict and call send_rpc_message(method, params, id, repeat)
        """
        method = data_dict.get('payload')
        params = data_dict.get('data', None)
        message_id = data_dict.get('message_id', None)
        repeat = data_dict.get('repeat', 0)

        self._send_rpc_message(method, params, message_id, repeat)

        # we don't get a response (this goes via on_data_received), so we signal "no response"
        return None

    def _send_rpc_message(self, method, params=None, message_id=None, repeat=0):
        """
        Send a JSON RPC message.
        The  JSON string is extracted from the supplied method and the given parameters.

        :param method: the Kodi method to be triggered
        :param params: parameters dictionary
        :param message_id: the message ID to be used. If none, use the internal counter
        :param repeat: counter for how often the message has been repeated
        """
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


class MD_Protocol_Viessmann(MD_Protocol):
    """ Protocol support for Viessmann heating systems

    This class implements a Viessmann protocol layer. By default, this uses
    the P300 protocol. By supplying the 'viess_proto' attribute, the older 'KW'
    protocol can be selected.

    At the moment, this is oriented towards serial connections. By supplying
    your own connection type, you could try to use it over networked connections.
    Be advised that the necessary "reply" client and the methods needed are not
    implemented for network access as of this time...
    """

    def __init__(self, device_type, device_id, data_received_callback, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-1]) + f'.{device_id}')

        if MD_standalone:
            self.logger = logging.getLogger('__main__')

        self.logger.debug(f'protocol initializing from {self.__class__.__name__} with arguments {kwargs}')

        # set class properties
        self.device_type = device_type
        self.device_id = device_id
        self._is_connected = False
        self._error_count = 0
        self._lock = threading.Lock()
        self._is_initialized = False
        self._data_received_callback = data_received_callback

        self._controlsets = {
            'P300': {
                'baudrate': 4800,
                'bytesize': 8,
                'parity': 'E',
                'stopbits': 2,
                'timeout': 0.5,
                'startbyte': 0x41,
                'request': 0x00,
                'response': 0x01,
                'error': 0x03,
                'read': 0x01,
                'write': 0x02,
                'functioncall': 0x7,
                'acknowledge': 0x06,
                'not_initiated': 0x05,
                'init_error': 0x15,
                'reset_command': 0x04,
                'reset_command_response': 0x05,
                'sync_command': 0x160000,
                'sync_command_response': 0x06,
                'command_bytes_read': 5,
                'command_bytes_write': 5,
                # init:              send'Reset_Command' receive'Reset_Command_Response' send'Sync_Command'
                # request:           send('StartByte' 'Länge der Nutzdaten als Anzahl der Bytes zwischen diesem Byte und der Prüfsumme' 'Request' 'Read' 'addr' 'checksum')
                # request_response:  receive('Acknowledge' 'StartByte' 'Länge der Nutzdaten als Anzahl der Bytes zwischen diesem Byte und der Prüfsumme' 'Response' 'Read' 'addr' 'Anzahl der Bytes des Wertes' 'Wert' 'checksum')
            },
            'KW': {
                'baudrate': 4800,
                'bytesize': 8,          # 'EIGHTBITS'
                'parity': 'E',          # 'PARITY_EVEN',
                'stopbits': 2,          # 'STOPBITS_TWO',
                'timeout': 1,
                'startbyte': 0x01,
                'read': 0xF7,
                'write': 0xF4,
                'acknowledge': 0x01,
                'reset_command': 0x04,
                'not_initiated': 0x05,
                'write_ack': 0x00,
            },
        }

        # get protocol or default to P300
        self._viess_proto = kwargs.get('viess_proto', 'P300')
        if self._viess_proto not in self._controlsets:
            self._viess_proto = 'P300'
        # select controlset for viess_proto
        self._controlset = self._controlsets[self._viess_proto]

        # make sure we have a basic set of parameters for the TCP connection
        self._params = {PLUGIN_ATTR_SERIAL_PORT: '',
                        PLUGIN_ATTR_SERIAL_BAUD: self._controlset[PLUGIN_ATTR_SERIAL_BAUD],
                        PLUGIN_ATTR_SERIAL_BSIZE: self._controlset[PLUGIN_ATTR_SERIAL_BSIZE],
                        PLUGIN_ATTR_SERIAL_PARITY: self._controlset[PLUGIN_ATTR_SERIAL_PARITY],
                        PLUGIN_ATTR_SERIAL_STOP: self._controlset[PLUGIN_ATTR_SERIAL_STOP],
                        PLUGIN_ATTR_CONN_TIMEOUT: self._controlset[PLUGIN_ATTR_CONN_TIMEOUT],
                        PLUGIN_ATTR_CONN_AUTO_CONN: True,
                        PLUGIN_ATTR_CONN_BINARY: True,
                        PLUGIN_ATTR_CONN_RETRIES: 0,
                        PLUGIN_ATTR_CONN_CYCLE: 3,
                        PLUGIN_ATTR_CB_ON_CONNECT: None,
                        PLUGIN_ATTR_CB_ON_DISCONNECT: None,
                        PLUGIN_ATTR_CONNECTION: CONN_SER_DIR}
        self._params.update(kwargs)

        # check if some of the arguments are usable
        self._set_connection_params()

        # initialize connection
        conn_params = self._params.copy()
        # don't supply callback, we do only reply-based work
        conn_params.update({PLUGIN_ATTR_CB_ON_CONNECT: None, PLUGIN_ATTR_CB_ON_DISCONNECT: None})
        self._connection = self._params[PLUGIN_ATTR_CONNECTION](device_type, device_id, None, **conn_params)

        # set "method pointers"
        self._send_bytes = self._connection._send_bytes
        self._read_bytes = self._connection._read_bytes

        # tell someone about our actual class
        self.logger.debug(f'protocol initialized from {self.__class__.__name__}')

    def _close(self):
        self._is_initialized = False
        super()._close()

    def _send_init_on_send(self):
        """
        setup the communication protocol prior to sending

        :return: Returns True, if communication was established successfully, False otherwise
        :rtype: bool
        """
        if self._viess_proto == 'P300' and not self._is_initialized:

            # init procedure is
            # interface: 0x04 (reset)
            #                           device: 0x05 (repeated)
            # interface: 0x160000 (sync)
            #                           device: 0x06 (sync ok)
            # interface: resume communication, periodically send 0x160000 as keepalive if necessary

            RESET = self._int2bytes(self._controlset['reset_command'], 1)
            NOTINIT = self._int2bytes(self._controlset["not_initiated"], 1)
            ACK = self._int2bytes(self._controlset['acknowledge'], 1)
            SYNC = self._int2bytes(self._controlset['sync_command'], 3)
            ERR = self._int2bytes(self._controlset['init_error'], 1)

            self.logger.debug('init communication....')
            syncsent = False

            self.logger.debug(f'send_bytes: send reset command {RESET}')
            self._send_bytes(RESET)

            readbyte = self._read_bytes(1)
            self.logger.debug(f'read_bytes: read {readbyte}')

            for i in range(10):
                if syncsent and readbyte == ACK:
                    self.logger.debug('device acknowledged initialization')
                    self._is_initialized = True
                    break
                elif readbyte == NOTINIT:
                    self.logger.debug(f'send_bytes: send sync command {SYNC}')
                    self._send_bytes(SYNC)
                    syncsent = True
                elif readbyte == ERR:
                    self.logger.error(f'interface reported an error, loop increment {i}')
                    self.logger.debug(f'send_bytes: send reset command {RESET}')
                    self._send_bytes(RESET)
                    syncsent = False
                else:   # elif readbyte != b'':
                    self.logger.debug(f'send_bytes: send reset command {RESET}')
                    self._send_bytes(RESET)
                    syncsent = False
                readbyte = self._read_bytes(1)
                self.logger.debug(f'read_bytes: read {readbyte}')

            self.logger.debug(f'communication initialized: {self._is_initialized}')
            return self._is_initialized

        elif self._viess_proto == 'KW':

            retries = 5
            RESET = self._int2bytes(self._controlset['reset_command'], 1)
            NOINIT = self._int2bytes(self._controlset['not_initiated'], 1, signed=False)

            # try to reset communication, especially if previous P300 comms is still open
            self._send_bytes(RESET)

            attempt = 0
            while attempt < retries:
                self.logger.debug(f'starting sync loop - attempt {attempt + 1}/{retries}')

                self._connection.reset_input_buffer()
                chunk = self._read_bytes(1)
                # enable for 'raw' debugging
                # self.logger.debug(f'sync loop - got {self._bytes2hexstring(chunk)}')
                if chunk == NOINIT:
                    self.logger.debug('got sync, commencing command send')
                    self._is_initialized = True
                    return True
                sleep(.8)
                attempt = attempt + 1
            self.logger.error(f'sync not acquired after {attempt} attempts')
            self._close()
            return False

        return True

    def _send(self, data_dict):
        """
        send data. data_dict needs to contain the following information:

        data_dict['payload']: address from/to which to read/write (hex, str)
        data_dict['data']['len']: length of command to send
        data_dict['data']['value']: value bytes to write, None if reading

        :param data_dict: send data
        :param read_response: KW only: read response value (True) or only return status byte
        :type data_dict: dict
        :type read_response: bool
        :return: Response packet (bytearray) if no error occured, None otherwise
        """
        (packet, responselen) = self._build_payload(data_dict)

        # send payload
        self._lock.acquire()
        try:
            self._send_bytes(packet)
            self.logger.debug(f'successfully sent packet {self._bytes2hexstring(packet)}')

            # receive response
            response_packet = bytearray()
            self.logger.debug(f'trying to receive {responselen} bytes of the response')
            chunk = self._read_bytes(responselen)
            if self._viess_proto == 'P300':
                self.logger.debug(f'received {len(chunk)} bytes chunk of response as hexstring {self._bytes2hexstring(chunk)} and as bytes {chunk}')
                if len(chunk) != 0:
                    if chunk[:1] == self._int2bytes(self._controlset['error'], 1):
                        self.logger.error(f'interface returned error, response was {chunk}')
                    elif len(chunk) == 1 and chunk[:1] == self._int2bytes(self._controlset['not_initiated'], 1):
                        self.logger.error('received invalid chunk, connection not initialized, forcing re-initialize...')
                        self._initialized = False
                    elif chunk[:1] != self._int2bytes(self._controlset['acknowledge'], 1):
                        self.logger.error(f'received invalid chunk, not starting with ACK, response was {chunk}')
                        self._error_count += 1
                        if self._error_count >= 5:
                            self.logger.warning('encountered 5 invalid chunks in sequence, maybe communication was lost, forcing re-initialize')
                            self._initialized = False
                    else:
                        response_packet.extend(chunk)
                        self._error_count = 0
                        return self._parse_response(response_packet)
                else:
                    self.logger.error(f'received 0 bytes chunk - ignoring response_packet, chunk was {chunk}')
            elif self._protocol == 'KW':
                self.logger.debug(f'received {len(chunk)} bytes chunk of response as hexstring {self._bytes2hexstring(chunk)} and as bytes {chunk}')
                if len(chunk) != 0:
                    response_packet.extend(chunk)
                    return self._parse_response(response_packet, data_dict['data']['value'] is None)
                else:
                    self.logger.error('received 0 bytes chunk - this probably is a communication error, possibly a wrong datapoint address?')
        except IOError as e:
            self.logger.error(f'send_command_packet failed with IO error, trying to reconnect. Error was: {e}')
            self._close()
        except Exception as e:
            self.logger.error(f'send_command_packet failed with error: {e}')
        finally:
            try:
                self._lock.release()
            except RuntimeError:
                pass

        # if we didn't return with data earlier, we hit an error. Act accordingly
        return None

    def _parse_response(self, response, read_response=True):
        """
        Process device response data, try to parse type and value

        :param response: Data received from device
        :type response: bytearray
        :param read_response: True if command was read command and value is expected, False if only status byte is expected (only needed for KW protocol)
        :type read_response: bool
        :return: tuple of (parsed response value, commandcode) or None if error
        """
        if self._viess_proto == 'P300':

            # A read_response telegram looks like this: ACK (1 byte), startbyte (1 byte), data length in bytes (1 byte), request/response (1 byte), read/write (1 byte), addr (2 byte), amount of valuebytes (1 byte), value (bytes as per last byte), checksum (1 byte)
            # A write_response telegram looks like this: ACK (1 byte), startbyte (1 byte), data length in bytes (1 byte), request/response (1 byte), read/write (1 byte), addr (2 byte), amount of bytes written (1 byte), checksum (1 byte)

            # Validate checksum
            checksum = self._calc_checksum(response[1:len(response) - 1])  # first, cut first byte (ACK) and last byte (checksum) and then calculate checksum
            received_checksum = response[len(response) - 1]
            if received_checksum != checksum:
                self.logger.error(f'calculated checksum {checksum} does not match received checksum of {received_checksum}! Ignoring reponse')
                return None

            # Extract command/address, valuebytes and valuebytecount out of response
            responsetypecode = response[3]  # 0x00 = query, 0x01 = reply, 0x03 = error
            responsedatacode = response[4]  # 0x01 = ReadData, 0x02 = WriteData, 0x07 = Function Call
            valuebytecount = response[7]

            # Extract databytes out of response
            rawdatabytes = bytearray()
            rawdatabytes.extend(response[8:8 + (valuebytecount)])
        elif self._protocol == 'KW':

            # imitate P300 response code data for easier combined handling afterwards
            # a read_response telegram consists only of the value bytes
            # a write_response telegram is 0x00 for OK, 0xXX for error
            responsetypecode = 1
            valuebytecount = len(response)
            rawdatabytes = response

            if read_response:
                # value response to read request, error detection by empty = no response
                responsedatacode = 1
                if len(rawdatabytes) == 0:
                    # error, no answer means wrong address (?)
                    responsetypecode = 3
            else:
                # status response to write request
                responsedatacode = 2
                if (len(rawdatabytes) == 1 and rawdatabytes[0] != 0) or len(rawdatabytes) == 0:
                    # error if status reply is not 0x00
                    responsetypecode = 3

        self.logger.debug(f'Response decoded to: responsedatacode: {responsedatacode}, valuebytecount: {valuebytecount}, responsetypecode: {responsetypecode}')

        if responsetypecode == 3:
            raise ValueError(f'error on reading reply {rawdatabytes}')

        if responsedatacode == 2:
            self.logger.debug('write request successful')
            return None

        self.logger.debug(f'read request successful, read bytes {rawdatabytes}')
        return rawdatabytes

    def _build_payload(self, data_dict):
        """
        create payload from data_dict. Necessary data:

        data_dict['payload']: address from/to which to read/write (hex, str)
        data_dict['data']['len']: length of command to send
        data_dict['data']['value']: value bytes to write, None if reading
        data_dict['data']['kwseq']: packet is follow-up packet in KW

        :param data_dict: data to convert
        :type data_dict: dict
        :return: (packet, responselen)
        :rtype: tuple
        """
        try:
            addr = data_dict['payload'].lower()
            cmdlen = data_dict['data']['len']
            valuebytes = data_dict['data']['value']
            KWFollowUp = data_dict['data'].get('kwseq', False)
        except Exception as e:
            raise ValueError(f'data_dict {data_dict} not usable, data not sent. Error was: {e}')

        write = valuebytes is not None

        # build payload
        if write:
            payloadlength = int(self._controlset.get('command_bytes_write', 0)) + int(valuebytes)
            self.logger.debug(f'Payload length is: {payloadlength} bytes')

        packet = bytearray()
        if not KWFollowUp:
            packet.extend(self._int2bytes(self._controlset['startbyte'], 1))
        if self._viess_proto == 'P300':
            if write:
                packet.extend(self._int2bytes(payloadlength, 1))
            else:
                packet.extend(self._int2bytes(self._controlset['command_bytes_read'], 1))
            packet.extend(self._int2bytes(self._controlset['request'], 1))

        if write:
            packet.extend(self._int2bytes(self._controlset['write'], 1))
        else:
            packet.extend(self._int2bytes(self._controlset['read'], 1))
        packet.extend(bytes.fromhex(addr))
        packet.extend(self._int2bytes(cmdlen, 1))
        if write:
            packet.extend(valuebytes)
        if self._viess_proto == 'P300':
            packet.extend(self._int2bytes(self._calc_checksum(packet), 1))

        if self._viess_proto == 'P300':
            responselen = int(self._controlset['command_bytes_read']) + 4 + (0 if write else int(cmdlen))
        else:
            responselen = 1 if write else int(cmdlen)

        if write:
            self.logger.debug(f'created payload to be sent as hexstring: {self._bytes2hexstring(packet)} and as bytes: {packet} with value {self._bytes2hexstring(valuebytes)})')
        else:
            self.logger.debug(f'created payload to be sent as hexstring: {self._bytes2hexstring(packet)} and as bytes: {packet}')

        return (packet, responselen)

    def _calc_checksum(self, packet):
        """
        Calculate checksum for P300 protocol packets

        :parameter packet: Data packet for which to calculate checksum
        :type packet: bytearray
        :return: Calculated checksum
        :rtype: int
        """
        checksum = 0
        if len(packet) > 0:
            if packet[:1] == b'\x41':
                packet = packet[1:]
                checksum = sum(packet)
                checksum = checksum - int(checksum / 256) * 256
            else:
                self.logger.error('bytes to calculate checksum from not starting with start byte')
        else:
            self.logger.error('no bytes received to calculate checksum')
        return checksum

    def _int2bytes(self, value, length, signed=False):
        """
        Convert value to bytearray with respect to defined length and sign format.
        Value exceeding limit set by length and sign will be truncated

        :parameter value: Value to convert
        :type value: int
        :parameter length: number of bytes to create
        :type length: int
        :parameter signed: True if result should be a signed int, False for unsigned
        :type signed: bool
        :return: Converted value
        :rtype: bytearray
        """
        value = value % (2 ** (length * 8))
        return value.to_bytes(length, byteorder='big', signed=signed)

    def _bytes2int(self, rawbytes, signed):
        """
        Convert bytearray to value with respect to sign format

        :parameter rawbytes: Bytes to convert
        :type value: bytearray
        :parameter signed: True if result should be a signed int, False for unsigned
        :type signed: bool
        :return: Converted value
        :rtype: int
        """
        return int.from_bytes(rawbytes, byteorder='little', signed=signed)

    def _bytes2hexstring(self, bytesvalue):
        """
        Create hex-formatted string from bytearray
        :param bytesvalue: Bytes to convert
        :type bytesvalue: bytearray
        :return: Converted hex string
        :rtype: str
        """
        return ''.join(f'{c:02x}' for c in bytesvalue)
