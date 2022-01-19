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
# do not change if not absolutely sure about the consequences!
#
#############################################################################################################################################################################################################################################

# plugin attributes, used in plugin config 'device'

# general attributes
PLUGIN_ATTR_ENABLED          = 'enabled'                 # set to False to disable loading of device
PLUGIN_ATTR_MODEL            = 'model'                   # select model if applicable. Don't set if not necessary!
PLUGIN_ATTR_CLEAN_STRUCT     = 'clean_structs'           # remove items from stucts not supported by chosen model
PLUGIN_ATTR_CMD_CLASS        = 'command_class'           # name of class to use for commands
PLUGIN_ATTR_RECURSIVE        = 'recursive_custom'        # indices of custom item attributes for which to enable recursive lookup (number or list of numbers)

# general connection attributes
PLUGIN_ATTR_CONNECTION       = 'conn_type'               # manually set connection class, classname or type (see below)
PLUGIN_ATTR_CB_ON_CONNECT    = 'connected_callback'      # callback function, called if connection is established
PLUGIN_ATTR_CB_ON_DISCONNECT = 'disconnected_callback'   # callback function, called if connection is lost
PLUGIN_ATTR_CONN_TIMEOUT     = 'timeout'                 # timeout for reading from network or serial
PLUGIN_ATTR_CONN_TERMINATOR  = 'terminator'              # terminator for reading from network or serial
PLUGIN_ATTR_CONN_BINARY      = 'binary'                  # tell connection to handle data for binary parsing
PLUGIN_ATTR_CONN_AUTO_CONN   = 'autoreconnect'           # (re)connect automatically on send
PLUGIN_ATTR_CONN_RETRIES     = 'connect_retries'         # if autoreconnect: how often to reconnect
PLUGIN_ATTR_CONN_CYCLE       = 'connect_cycle'           # if autoreconnect: how many seconds to wait between retries

# network attributes
PLUGIN_ATTR_NET_HOST         = 'host'                    # hostname / IP for network connection
PLUGIN_ATTR_NET_PORT         = 'port'                    # port for network connection

# serial attributes
PLUGIN_ATTR_SERIAL_PORT      = 'serialport'              # serial port for serial connection
PLUGIN_ATTR_SERIAL_BAUD      = 'baudrate'                # baudrate for serial connection
PLUGIN_ATTR_SERIAL_BSIZE     = 'bytesize'                # bytesize for serial connection
PLUGIN_ATTR_SERIAL_PARITY    = 'parity'                  # parity for serial connection
PLUGIN_ATTR_SERIAL_STOP      = 'stopbits'                # stopbits for serial connection

# protocol attributes
PLUGIN_ATTR_PROTOCOL         = 'protocol'                # manually choose protocol class, classname or type (see below). Don't set if not necessary!
PLUGIN_ATTR_MSG_TIMEOUT      = 'message_timeout'         # how many seconds to wait for reply to command (JSON-RPC only)
PLUGIN_ATTR_MSG_REPEAT       = 'message_repeat'          # how often to repeat command till reply is received? (JSON-RPC only)

PLUGIN_ATTRS = (PLUGIN_ATTR_ENABLED, PLUGIN_ATTR_MODEL, PLUGIN_ATTR_CLEAN_STRUCT, PLUGIN_ATTR_CMD_CLASS, PLUGIN_ATTR_RECURSIVE,
                PLUGIN_ATTR_CONNECTION, PLUGIN_ATTR_CB_ON_CONNECT, PLUGIN_ATTR_CB_ON_DISCONNECT, PLUGIN_ATTR_CONN_TIMEOUT,
                PLUGIN_ATTR_CONN_TERMINATOR, PLUGIN_ATTR_CONN_AUTO_CONN, PLUGIN_ATTR_CONN_RETRIES, PLUGIN_ATTR_CONN_CYCLE,
                PLUGIN_ATTR_CONN_BINARY, PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_NET_PORT,
                PLUGIN_ATTR_SERIAL_PORT, PLUGIN_ATTR_SERIAL_BAUD, PLUGIN_ATTR_SERIAL_BSIZE, PLUGIN_ATTR_SERIAL_PARITY, PLUGIN_ATTR_SERIAL_STOP,
                PLUGIN_ATTR_PROTOCOL, PLUGIN_ATTR_MSG_TIMEOUT, PLUGIN_ATTR_MSG_REPEAT)

# connection types for PLUGIN_ATTR_CONNECTION
CONN_NULL                   = ''                 # use base connection class without real connection functionality, for testing
CONN_NET_TCP_REQ            = 'net_tcp_request'  # TCP client connection with URL-based requests
CONN_NET_TCP_CLI            = 'net_tcp_client'   # persistent TCP client connection with async callback for responses
CONN_NET_TCP_JSONRPC        = 'net_tcp_jsonrpc'  # JSON RPC via persistent TCP client connection with async callback for responses
CONN_NET_UDP_SRV            = 'net_udp_server'   # UDP server connection with async data callback
CONN_SER_DIR                = 'serial'           # serial connection with query-reply logic
CONN_SER_ASYNC              = 'serial_async'     # serial connection with only async data callback

CONNECTION_TYPES = (CONN_NULL, CONN_NET_TCP_REQ, CONN_NET_TCP_CLI, CONN_NET_TCP_JSONRPC, CONN_NET_UDP_SRV, CONN_SER_DIR, CONN_SER_ASYNC)

# protocol types for PLUGIN_ATTR_PROTOCOL
PROTO_NULL                  = ''                 # use base protocol class without added functionality (why??)
PROTO_JSONRPC               = 'jsonrpc'          # JSON-RPC 2.0 support with send queue, msgid and resend of unanswered commands
PROTO_VIESSMANN             = 'viessmann'        # Viessmann P300 / KW

PROTOCOL_TYPES = (PROTO_NULL, PROTO_JSONRPC, PROTO_VIESSMANN)

# item attributes (as defines in plugin.yaml)
ITEM_ATTR_DEVICE            = 'md_device'
ITEM_ATTR_COMMAND           = 'md_command'
ITEM_ATTR_READ              = 'md_read'
ITEM_ATTR_CYCLE             = 'md_read_cycle'
ITEM_ATTR_READ_INIT         = 'md_read_initial'
ITEM_ATTR_GROUP             = 'md_read_group'
ITEM_ATTR_WRITE             = 'md_write'
ITEM_ATTR_READ_GRP          = 'md_read_group_trigger'
ITEM_ATTR_LOOKUP            = 'md_lookup'
ITEM_ATTR_CUSTOM_PREFIX     = 'md_custom'
ITEM_ATTR_CUSTOM1           = 'md_custom1'
ITEM_ATTR_CUSTOM2           = 'md_custom2'
ITEM_ATTR_CUSTOM3           = 'md_custom3'

ITEM_ATTRS = (ITEM_ATTR_DEVICE, ITEM_ATTR_COMMAND, ITEM_ATTR_READ, ITEM_ATTR_CYCLE, ITEM_ATTR_READ_INIT, ITEM_ATTR_WRITE, ITEM_ATTR_READ_GRP, ITEM_ATTR_GROUP, ITEM_ATTR_LOOKUP, ITEM_ATTR_CUSTOM1, ITEM_ATTR_CUSTOM2, ITEM_ATTR_CUSTOM3)

# command definition
COMMAND_READ                = True
COMMAND_WRITE               = False
COMMAND_SEP                 = '.'
CUSTOM_SEP                  = '#'

# command definition attributes
CMD_ATTR_OPCODE             = 'opcode'
CMD_ATTR_READ               = 'read'
CMD_ATTR_WRITE              = 'write'
CMD_ATTR_ITEM_TYPE          = 'item_type'
CMD_ATTR_DEV_TYPE           = 'dev_datatype'
CMD_ATTR_READ_CMD           = 'read_cmd'
CMD_ATTR_WRITE_CMD          = 'write_cmd'
CMD_ATTR_REPLY_TOKEN        = 'reply_token'
CMD_ATTR_REPLY_PATTERN      = 'reply_pattern'
CMD_ATTR_CMD_SETTINGS       = 'cmd_settings'
CMD_ATTR_LOOKUP             = 'lookup'
CMD_ATTR_PARAMS             = 'params'
CMD_ATTR_PARAM_VALUES       = 'param_values'
CMD_ATTR_ITEM_ATTRS         = 'item_attrs'

CMD_IATTR_RG_LEVELS         = 'read_group_levels'
CMD_IATTR_LOOKUP_ITEM       = 'lookup_item'
CMD_IATTR_ATTRIBUTES        = 'attributes'
CMD_IATTR_READ_GROUPS       = 'read_groups'
CMD_IATTR_ENFORCE           = 'enforce'
CMD_IATTR_INITIAL           = 'initial'
CMD_IATTR_CYCLE             = 'cycle'
CMD_IATTR_TEMPLATE          = 'item_template'

# commands definition parameters
COMMAND_PARAMS = (CMD_ATTR_OPCODE, CMD_ATTR_READ, CMD_ATTR_WRITE, CMD_ATTR_ITEM_TYPE, CMD_ATTR_DEV_TYPE, CMD_ATTR_READ_CMD,
                  CMD_ATTR_WRITE_CMD, CMD_ATTR_REPLY_TOKEN, CMD_ATTR_REPLY_PATTERN, CMD_ATTR_CMD_SETTINGS,
                  CMD_ATTR_LOOKUP, CMD_ATTR_PARAMS, CMD_ATTR_PARAM_VALUES, CMD_ATTR_ITEM_ATTRS)

COMMAND_ITEM_ATTRS = (CMD_IATTR_RG_LEVELS, CMD_IATTR_LOOKUP_ITEM, CMD_IATTR_ATTRIBUTES, CMD_IATTR_TEMPLATE,
                      CMD_IATTR_READ_GROUPS, CMD_IATTR_CYCLE, CMD_IATTR_INITIAL, CMD_IATTR_ENFORCE)

# keys for min / max values for data bounds
MINMAXKEYS                  = ('valid_min', 'valid_max', 'force_min', 'force_max')

# name of non-model specific key for commands, models and lookups
INDEX_GENERIC               = 'ALL'


#############################################################################################################################################################################################################################################
#
# Exceptions
#
#############################################################################################################################################################################################################################################

class CommandsError(Exception):
    pass


#############################################################################################################################################################################################################################################
#
# non-class functions
#
#############################################################################################################################################################################################################################################

def sanitize_param(val):
    """
    Try to correct type of val if val is string:
    - return int(val) if val is integer
    - return float(val) if val is float
    - return bool(val) is val follows conventions for bool
    - try if string can be converted to list, tuple or dict; do so if possible
    - return val unchanged otherwise

    :param val: value to sanitize
    :return: sanitized (or unchanged) value
    """
    if isinstance(val, (int, float, bool)):
        return val
    if Utils.is_int(str(val)):
        val = int(val)
    elif Utils.is_float(str(val)):
        val = float(val)
    elif isinstance(val, str) and val.lower() in ('true', 'false', 'on', 'off', 'yes', 'no'):
        val = Utils.to_bool(val)
    else:
        try:
            new = literal_eval(val)
            if type(new) in (list, dict, tuple):
                val = new
        except Exception:
            pass
    return val
