#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

import urllib.parse

from lib.item import Items
items = Items.get_instance()

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
    CUSTOM_ITEMS = {}

    def _set_device_defaults(self):

        self.custom_commands = 1
        self._custom_pattern = '([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}'
        self._use_callbacks = True

        # set our own preferences concerning connections
        if not self._params.get(PLUGIN_ATTR_CONNECTION):
            if PLUGIN_ATTR_NET_HOST in self._params and self._params.get(PLUGIN_ATTR_NET_HOST):
                self._params[PLUGIN_ATTR_CONNECTION] = CONN_NET_TCP_CLI
            elif PLUGIN_ATTR_SERIAL_PORT in self._params and self._params.get(PLUGIN_ATTR_SERIAL_PORT):
                self._params[PLUGIN_ATTR_CONNECTION] = CONN_SER_ASYNC

    def set_custom_item(self, item, command, index, value):
        """ this is called by parse_items if md_custom[123] is found. """
        self._custom_values[index].append(value)
        self._custom_values[index] = list(set(self._custom_values[index]))
        self.CUSTOM_ITEMS[item] = value

    def on_connect(self, by=None):
        self.logger.debug("Activating listen mode after connection.")
        for item in items.find_items('md_albumart'):
            player_id = self.CUSTOM_ITEMS.get(item)
            art_item = None
            for child in item.return_children():
                if 'currentalbumarturl' in child.property.path:
                    art_item = child
            if player_id and art_item:
                try:
                    host = self._params.get(PLUGIN_ATTR_NET_HOST)
                    port = self._params.get('port') # should be PLUGIN_ATTR_NET_PORT ?
                    url = f'http://{host}:{port}/music/current/cover.jpg?player={player_id}'
                    art_item(url, 'multidevice', 'start')
                    self.logger.debug(f'Albumart folder for item {art_item} set to {url}')
                except Exception as e:
                    self.logger.error(f"Problem setting album art URL: {e}")
            else:
                self.logger.debug(f'No albumart folder for item {item} could be set.')

        self.send_command('server.listenmode', True)

    def _transform_send_data(self, data=None, **kwargs):
        if data:
            try:
                data['limit_response'] = self._params.get(PLUGIN_ATTR_CONN_TERMINATOR, "\r")
                data['payload'] = f'{data.get("payload")}{data.get("limit_response")}'
            except Exception as e:
                self.logger.error(f'ERROR transforming send data: {e}')
        return data

    def _transform_received_data(self, data):
        # fix weird representation of MAC address (%3A = :), etc.
        return urllib.parse.unquote_plus(data)
