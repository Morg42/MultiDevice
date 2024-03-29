#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

import urllib.parse

from lib.item import Items
items = Items.get_instance()

if MD_standalone:
    from MD_Globals import (CUSTOM_SEP, PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_NET_PORT, PLUGIN_ATTR_RECURSIVE, PLUGIN_ATTR_CONN_TERMINATOR)
    from MD_Device import MD_Device
else:
    from ..MD_Globals import (CUSTOM_SEP, PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_NET_PORT, PLUGIN_ATTR_RECURSIVE, PLUGIN_ATTR_CONN_TERMINATOR)
    from ..MD_Device import MD_Device


class MD_Device(MD_Device):
    """ Device class for Squeezebox function.

    Most of the work is done by the base class, so we only set default parameters
    for the connection (to be overwritten by device attributes from the plugin
    configuration) and add a fixed terminator byte to outgoing datagrams.

    The know-how is in the commands.py (and some DT_ classes...)
    """

    def _set_device_defaults(self):
        self.custom_commands = 1
        self._token_pattern = '([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}'
        # for substitution in reply_pattern
        self._custom_patterns = {1: '(?:[0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}', 2: '', 3: ''}
        self._use_callbacks = True
        self._params[PLUGIN_ATTR_RECURSIVE] = 1

    def on_connect(self, by=None):
        self.logger.debug("Activating listen mode after connection.")
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

    def _process_additional_data(self, command, data, value, custom, by):

        def _dispatch(command, value, custom=None, send=False):
            if custom:
                command = command + CUSTOM_SEP + custom
            if send:
                self.send_command(command, value)
            elif self._data_received_callback:
                self._data_received_callback(self.device_id, command, value)

        def _trigger_read(command, custom=None):
            if custom:
                command = command + CUSTOM_SEP + custom
            self.logger.debug(f"Sending read command for {command}")
            self.send_command(command)

        if not custom:
            return

        # set alarm
        if command == 'player.control.alarms':
            # This does not really work currently. The created string is somehow correct.
            # However, much more logic has to be included to add/update/delete alarms, etc.
            try:
                for i in value.keys():
                    d = value.get(i)
                    alarm = f"id:{i} "
                    for k, v in d.items():
                        alarm += f"{k}:{v} "
                    alarm = f"alarm add {alarm.strip()}"
                    self.logger.debug(f"Set alarm: {alarm}")
                    _dispatch('player.control.set_alarm', alarm, custom, True)
            except Exception as e:
                self.logger.error(f"Error setting alarm: {e}")

        # set album art URL
        if command == 'player.info.album':
            host = self._params.get(PLUGIN_ATTR_NET_HOST)
            port = self._params.get(PLUGIN_ATTR_NET_PORT)
            url = f'http://{host}:{port}/music/current/cover.jpg?player={custom}'
            _dispatch('player.info.albumarturl', url, custom)

        # update on new song
        if command == 'player.info.title' or (command == 'player.control.playpause' and value == "True"):
            _trigger_read('player.control.playmode', custom)
            _trigger_read('player.playlist.index', custom)
            _trigger_read('player.info.duration', custom)
            _trigger_read('player.info.album', custom)
            _trigger_read('player.info.artist', custom)
            _trigger_read('player.info.genre', custom)
            _trigger_read('player.info.path', custom)

        # update current time info
        if command in ['player.control.forward', 'player.control.rewind']:
            _trigger_read('player.control.time', custom)

        # update play and stop items based on playmode
        if command == 'player.control.playmode':
            mode = data.split("mode")[-1].strip()
            mode = mode.split("playlist")[-1].strip()
            _dispatch('player.control.playpause', True if mode in ["play", "pause 0"] else False, custom)
            _dispatch('player.control.stop', True if mode == "stop" else False, custom)
            _trigger_read('player.control.time', custom)

        # update play and stop items based on playmode
        if command == 'player.control.stop' or (command == 'player.control.playpause' and value == "False"):
            _trigger_read('player.control.playmode', custom)
