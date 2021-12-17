#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file aims to become part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  Globals for MultiDevice plugin
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

from lib.utils import Utils
from ast import literal_eval


#############################################################################################################################################################################################################################################
#
# global constants used to configure plugin, device, connection and items
#
#############################################################################################################################################################################################################################################

# plugin arguments, used in plugin config 'device'
PLUGIN_ARG_CONNECTION   = 'conn_type'
PLUGIN_ARG_NET_HOST     = 'host'
PLUGIN_ARG_NET_PORT     = 'port'
PLUGIN_ARG_SERIAL_PORT  = 'serial'
PLUGIN_ARG_TIMEOUT      = 'timeout'

PLUGIN_ARGS = (PLUGIN_ARG_CONNECTION, PLUGIN_ARG_NET_HOST, PLUGIN_ARG_NET_PORT, PLUGIN_ARG_SERIAL_PORT, PLUGIN_ARG_TIMEOUT)

# connection types for PLUGIN_ARG_CONNECTION
CONN_NET_TCP_REQ        = 'net_tcp_request'  # TCP client connection with URL-based requests
CONN_NET_TCP_SYN        = 'net_tcp_reply'    # persistent TCP client connection with immediate query-reply logic
CONN_NET_TCP_CLI        = 'net_tcp_client'   # persistent TCP client connection with async callback for responses
CONN_NET_UDP_SRV        = 'net_udp_server'   # UDP server connection with async data callback
CONN_SER_CLI            = 'serial_client'    # serial connection with query-reply logic
CONN_SER_ASYNC          = 'serial_async'     # serial connection with async data callback

CONNECTION_TYPES = (CONN_NET_TCP_REQ, CONN_NET_TCP_SYN, CONN_NET_TCP_CLI, CONN_NET_UDP_SRV, CONN_SER_CLI, CONN_SER_ASYNC)

# item attributes (as defines in plugin.yaml)
ITEM_ATTR_DEVICE        = 'md_device'
ITEM_ATTR_COMMAND       = 'md_command'
ITEM_ATTR_READ          = 'md_read'
ITEM_ATTR_CYCLE         = 'md_read_cycle'
ITEM_ATTR_READ_INIT     = 'md_read_initial'
ITEM_ATTR_WRITE         = 'md_write'
ITEM_ATTR_READ_ALL      = 'md_read_all'

ITEM_ATTRS = (ITEM_ATTR_DEVICE, ITEM_ATTR_COMMAND, ITEM_ATTR_READ, ITEM_ATTR_CYCLE, ITEM_ATTR_READ_INIT, ITEM_ATTR_WRITE, ITEM_ATTR_READ_ALL)

# command definition
COMMAND_READ            = True
COMMAND_WRITE           = False

# commands definition parameters
COMMAND_PARAMS          = ('opcode', 'read', 'write', 'item_type', 'dev_datatype', 'read_cmd', 'write_cmd', 'read_data', 'reply_token', 'reply_pattern', 'bounds')


#############################################################################################################################################################################################################################################
#
# non-class functions
#
#############################################################################################################################################################################################################################################

def sanitize_param(val):
    '''
    Try to correct type of val:
    - return int(val) if val is integer
    - return float(val) if val is float
    - return bool(val) is val follows conventions for bool
    - try if string can be converted to list, tuple or dict; do so if possible
    - return val unchanged otherwise

    :param val: value to sanitize
    :return: sanitized (or unchanged) value
    '''
    if Utils.is_int(val):
        val = int(val)
    elif Utils.is_float(val):
        val = float(val)
    elif val.lower() in ('true', 'false', 'on', 'off', 'yes', 'no'):
        val = Utils.to_bool(val)
    else:
        try:
            new = literal_eval(val)
            if type(new) in (list, dict, tuple):
                val = new
        except Exception:
            pass
    return val
