#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

import urllib.parse

if MD_standalone:
    from MD_Globals import (CUSTOM_SEP, PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_NET_PORT, PLUGIN_ATTR_RECURSIVE)
    from MD_Device import MD_Device
else:
    from ..MD_Globals import (CUSTOM_SEP, PLUGIN_ATTR_NET_HOST, PLUGIN_ATTR_NET_PORT, PLUGIN_ATTR_RECURSIVE)
    from ..MD_Device import MD_Device


class MD_Device(MD_Device):
    """ Device class for Squeezebox function.

    Most of the work is done by the base class, so we only set default parameters
    for the connection (to be overwritten by device attributes from the plugin
    configuration) and add a fixed terminator byte to outgoing datagrams.

    The know-how is in the commands.py (and some DT_ classes...)
    """

    def _set_device_defaults(self):
        self._discard_unknown_command = False
        self.custom_commands = 1
        self._token_pattern = '([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}'
        # for substitution in reply_pattern
        self._custom_patterns = {1: '(?:[0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2}', 2: '', 3: ''}
        self._use_callbacks = True
        self._params[PLUGIN_ATTR_RECURSIVE] = 1

    def _transform_received_data(self, data):
        # fix weird representation of MAC address (%3A = :), etc.
        return urllib.parse.unquote_plus(data)

<<<<<<< Updated upstream
=======
    def _transform_send_data(self, data_dict, **kwargs):
        host = self._params['host']
        port = self._params['port']

        url = f'http://{host}:{port}/jsonrpc.js'
        data_dict['payload'] = url
        data_dict['method'] = 'slim.request'
        data_dict['request_method'] = 'post'
        self.logger.error(f'data: {data_dict}')
        return data_dict

>>>>>>> Stashed changes
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
                    alarm = f"update {alarm.strip()}"
                    self.logger.debug(f"Set alarm: {alarm} without executing the command.")
                    _dispatch('player.control.set_alarm', alarm, custom, False)
            except Exception as e:
                self.logger.error(f"Error setting alarm: {e}")

        # update on new song
        if command == 'player.info.status':
            _dispatch('player.info.name', data.get("player_name"), custom)
            _dispatch('player.info.connected', data.get("player_connected"), custom)
            _dispatch('player.info.signalstrength', data.get("signalstrength"), custom)
            _dispatch('player.info.playmode', data.get("mode"), custom)
            _dispatch('player.info.time', data.get("time"), custom)
            _dispatch('player.info.rate', data.get("rate"), custom)
            _dispatch('player.info.duration', data.get("duration"), custom)
            _dispatch('player.info.title', data.get("current_title"), custom)
            _dispatch('player.control.power', data.get("power"), custom)
            _dispatch('player.control.volume', data.get("mixer volume"), custom)
            _dispatch('player.playlist.repeat', data.get("playlist repeat"), custom)
            _dispatch('player.playlist.shuffle', data.get("playlist shuffle"), custom)
            _dispatch('player.playlist.mode', data.get("playlist mode"), custom)
            _dispatch('player.playlist.seq_no', data.get("seq_no"), custom)
            _dispatch('player.playlist.index', data.get("playlist_cur_index"), custom)
            _dispatch('player.playlist.timestamp', data.get("playlist_timestamp"), custom)
            _dispatch('player.playlist.tracks', data.get("playlist_tracks"), custom)
            _dispatch('player.playlist.nextsong1', data["remoteMeta"]["playlist_loop"][1].get("title"), custom)
            _dispatch('player.playlist.nextsong2', data["remoteMeta"]["playlist_loop"][2].get("title"), custom)
            _dispatch('player.playlist.nextsong3', data["remoteMeta"]["playlist_loop"][3].get("title"), custom)
            _dispatch('player.playlist.nextsong4', data["remoteMeta"]["playlist_loop"][4].get("title"), custom)
            _dispatch('player.playlist.nextsong5', data["remoteMeta"]["playlist_loop"][5].get("title"), custom)
