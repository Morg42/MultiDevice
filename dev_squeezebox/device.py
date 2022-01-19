#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

import re
import urllib.parse


if MD_standalone:
    from MD_Globals import (PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_CONNECTION, PLUGIN_ATTR_SERIAL_PORT, PLUGIN_ATTR_CONN_TERMINATOR, CONN_NET_TCP_CLI, CONN_SER_ASYNC)
    from MD_Device import MD_Device
else:
    from ..MD_Globals import (PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_CONNECTION, PLUGIN_ATTR_SERIAL_PORT, PLUGIN_ATTR_CONN_TERMINATOR, CONN_NET_TCP_CLI, CONN_SER_ASYNC)
    from ..MD_Device import MD_Device


class MD_Device(MD_Device):
    """ Device class for Squeezebox function.

    Most of the work is done by the base class, so we only set default parameters
    for the connection (to be overwritten by device attributes from the plugin
    configuration) and add a fixed terminator byte to outgoing datagrams.

    The know-how is in the commands.py (and some DT_ classes...)
    """

    def _set_custom_vars(self):
        self.custom_commands = 1
        self._use_callbacks = True
        # set our own preferences concerning connections
        if not self._params.get(PLUGIN_ATTR_CONNECTION):
            if PLUGIN_ATTR_NET_HOST in self._params and self._params.get(PLUGIN_ATTR_NET_HOST):
                self._params[PLUGIN_ATTR_CONNECTION] = CONN_NET_TCP_CLI
            elif PLUGIN_ATTR_SERIAL_PORT in self._params and self._params.get(PLUGIN_ATTR_SERIAL_PORT):
                self._params[PLUGIN_ATTR_CONNECTION] = CONN_SER_ASYNC
        if PLUGIN_ATTR_CONN_TERMINATOR in self._params:
            b = self._params[PLUGIN_ATTR_CONN_TERMINATOR].encode()
            b = b.decode('unicode-escape').encode()
            self._params[PLUGIN_ATTR_CONN_TERMINATOR] = b

    def on_connect(self, by=None):
        self.logger.debug("On connect squeezebox")
        super().on_connect(by)
        self.send_command('server.listenmode', True)

    def _transform_send_data(self, data=None, **kwargs):
        if kwargs.get('custom') and kwargs['custom'].get(1) is not None:
            player_id = f"{kwargs['custom'][1]} "
        else:
            player_id = ''
        if data:
            try:
                data['limit_response'] = self._params.get(PLUGIN_ATTR_CONN_TERMINATOR, b'\r')
                data['payload'] = f'{player_id}{data.get("payload")}\r'
            except Exception as e:
                self.logger.error(f'ERROR {e}')
        return data

    def _transform_received_data(self, data):
        return urllib.parse.unquote_plus(data)

    def get_custom_value(self, command, data):
        """ extract custom value from data. Needs to be overwritten """
        if not self.custom_commands:
            return None
        res = re.match('([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}', data)
        if not res:
            self.logger.debug(f'custom token not found or no valid MAC address in {data}, ignoring')
            return None
        elif res[0] in self._custom_values[self.custom_commands]:
            return res[0]
        else:
            self.logger.debug(f'received custom token {res[0]}, not in list of known tokens {self._custom_values[self.custom_commands]}')
            return None
