#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

'''
Device class for Kodi Mediacenter.
'''
if MD_standalone:
    from MD_Globals import *
    from MD_Device import MD_Device
    from MD_Command import MD_Command_JSON
else:
    from ..MD_Globals import *
    from ..MD_Device import MD_Device
    from ..MD_Command import MD_Command_JSON

from time import sleep
import logging
import json


class MD_Device(MD_Device):

    def __init__(self, device_type, device_id, **kwargs):

        # get MultiDevice.device logger
        self.logger = logging.getLogger('.'.join(__name__.split('.')[:-2]) + f'.{device_id}')

        # set parameter defaults
        self._params = {'command_class': MD_Command_JSON, 
                        PLUGIN_ARG_CONNECTION: CONN_NET_TCP_JSONRPC,
                        PLUGIN_ARG_NET_HOST: '', 
                        PLUGIN_ARG_NET_PORT: 9090, 
                        PLUGIN_ARG_AUTORECONNECT: True,
                        PLUGIN_ARG_CONN_RETRIES: 5, 
                        PLUGIN_ARG_CONN_CYCLE: 3, 
                        PLUGIN_ARG_TIMEOUT: 3, 
                        PLUGIN_ARG_MSG_REPEAT: 3,
                        PLUGIN_ARG_MSG_TIMEOUT: 5,
                        PLUGIN_ARG_CB_ON_CONNECT: self.on_connect,
                        PLUGIN_ARG_CB_ON_DISCONNECT: self.on_disconnect}

        super().__init__(device_type, device_id, **kwargs)

        self._activeplayers = []
        self._playerid = 0

        # these commands are not meant to control the kodi device, but to
        # communicate with the device class, e.g. triggering updating player
        # info or returning the player_id.
        # As these commands are not sent (directly) to the device, they should
        # not be processed via the MD_Commands class and not listed in commands.py
        self._special_commands = {'read': ['player'], 'write': ['update']}

        # log own initialization with module (i.e. folder) name
        self.logger.debug(f'device initialized from {__spec__.name} with arguments {kwargs}')

#
# further overloaded methods
#

    def on_connect(self, by=None):
        self._update_status()

    def on_data_received(self, command, data):
        '''
        Callback function for received data e.g. from an event loop
        Processes data and dispatches value to plugin class

        :param command: the command in reply to which data was received
        :param data: received data in 'raw' connection format
        :type command: str
        '''
        if command is not None:
            self.logger.debug(f'received data "{data}" for command {command}')
        else:
            self.logger.debug(f'data "{data}" did not identify a known command, ignoring it')

        if not self._data_received_callback:
            self.logger.error('on_data_received callback not set, can not process device reply data, ignoring it')
            return

        if not isinstance(data, dict):
            self.logger.error(f'received data {data} not in JSON (dict) format, ignoring')

        if 'error' in data:
            # errors are handled on connection level
            return

        try:
            result_data = data.get('result')
        except Exception as e:
            self.logger.error(f'Invalid response to command {command} received: {data}, ignoring. Error was: {e}')
            return
        if 'id' in data and result_data is None:
            self.logger.info(f'Empty response to command {command} received, ignoring')
            return

        query_playerinfo = []

        processed = False

        # replies to requests sent by us
        if 'id' in data:
            if command == 'Player.GetActivePlayers':
                processed = True
                if len(result_data) == 1:
                    # one active player
                    query_playerinfo = self._activeplayers = [result_data[0].get('playerid')]
                    self._playerid = self._activeplayers[0]
                    self.logger.debug(f'received GetActivePlayers, set playerid to {self._playerid}')
                    self._data_received_callback(self.device_id, 'player', self._playerid)
                    self._data_received_callback(self.device_id, 'media', result_data[0].get('type').capitalize())
                elif len(result_data) > 1:
                    # multiple active players. Have not yet seen this happen
                    self._activeplayers = []
                    for player in result_data:
                        self._activeplayers.append(player.get('playerid'))
                        query_playerinfo.append(player.get('playerid'))
                    self._playerid = min(self._activeplayers)
                    self.logger.debug(f'received GetActivePlayers, set playerid to {self._playerid}')
                else:
                    # no active players
                    self._activeplayers = []
                    self._data_received_callback(self.device_id, 'state', 'No active player')
                    self._data_received_callback(self.device_id, 'player', 0)
                    self._data_received_callback(self.device_id, 'title', '')
                    self._data_received_callback(self.device_id, 'media', '')
                    self._data_received_callback(self.device_id, 'stop', True)
                    self._data_received_callback(self.device_id, 'playpause', False)
                    self._data_received_callback(self.device_id, 'streams', None)
                    self._data_received_callback(self.device_id, 'subtitles', None)
                    self._data_received_callback(self.device_id, 'audio', '')
                    self._data_received_callback(self.device_id, 'subtitle', '')
                    self._playerid = 0
                    self.logger.debug('received GetActivePlayers, reset playerid to 0')

            # got status info
            elif command == 'Application.GetProperties':
                processed = True
                muted = result_data.get('muted')
                volume = result_data.get('volume')
                self.logger.debug(f'received GetProperties: change mute to {muted} and volume to {volume}')
                self._data_received_callback(self.device_id, 'mute', muted)
                self._data_received_callback(self.device_id, 'volume', volume)

            # got favourites
            elif command == 'Favourites.GetFavourites':
                processed = True
                if not result_data.get('favourites'):
                    self.logger.debug('No favourites found.')
                else:
                    item_dict = {item['title']: item for item in result_data.get('favourites')}
                    self.logger.debug(f'favourites found: {item_dict}')
                    self._data_received_callback(self.device_id, 'get_favourites', item_dict)

            # got item info
            elif command == 'Player.GetItem':
                processed = True
                title = result_data['item'].get('title')
                player_type = result_data['item'].get('type')
                if not title:
                    title = result_data['item'].get('label')
                self._data_received_callback(self.device_id, 'media', player_type.capitalize())
                if player_type == 'audio' and 'artist' in result_data['item']:
                    artist = 'unknown' if len(result_data['item'].get('artist')) == 0 else result_data['item'].get('artist')[0]
                    title = artist + ' - ' + title
                self._data_received_callback(self.device_id, 'title', title)
                self.logger.debug(f'received GetItem: update player info to title={title}, type={player_type}')

            # got player status
            elif command == 'Player.GetProperties':
                processed = True
                self.logger.debug('Received Player.GetProperties, update media data')
                self._data_received_callback(self.device_id, 'speed', result_data.get('speed'))
                self._data_received_callback(self.device_id, 'seek', result_data.get('percentage'))
                self._data_received_callback(self.device_id, 'streams', result_data.get('audiostreams'))
                self._data_received_callback(self.device_id, 'audio', result_data.get('currentaudiostream'))
                self._data_received_callback(self.device_id, 'subtitles', result_data.get('subtitles'))
                if result_data.get('subtitleenabled'):
                    subtitle = result_data.get('currentsubtitle')
                else:
                    subtitle = 'Off'
                self._data_received_callback(self.device_id, 'subtitle', subtitle)

                # speed != 0 -> play; speed == 0 -> pause
                if result_data.get('speed') == 0:
                    self._data_received_callback(self.device_id, 'state', 'Paused')
                    self._data_received_callback(self.device_id, 'stop', False)
                    self._data_received_callback(self.device_id, 'playpause', False)
                else:
                    self._data_received_callback(self.device_id, 'state', 'Playing')
                    self._data_received_callback(self.device_id, 'stop', False)
                    self._data_received_callback(self.device_id, 'playpause', True)

        # not replies, but event notifications.
        elif 'method' in data:

            # no id, notification or other
            if data['method'] == 'Player.OnResume':
                processed = True
                self.logger.debug('received: resumed player')
                self._data_received_callback(self.device_id, 'state', 'Playing')
                self._data_received_callback(self.device_id, 'stop', False)
                self._data_received_callback(self.device_id, 'playpause', True)
                query_playerinfo.append(data['params']['data']['player']['playerid'])

            elif data['method'] == 'Player.OnPause':
                processed = True
                self.logger.debug('received: paused player')
                self._data_received_callback(self.device_id, 'state', 'Paused')
                self._data_received_callback(self.device_id, 'stop', False)
                self._data_received_callback(self.device_id, 'playpause', False)
                query_playerinfo.append(data['params']['data']['player']['playerid'])

            elif data['method'] == 'Player.OnStop':
                processed = True
                self.logger.debug('received: stopped player, set playerid to 0')
                self._data_received_callback(self.device_id, 'state', 'No active player')
                self._data_received_callback(self.device_id, 'media', '')
                self._data_received_callback(self.device_id, 'title', '')
                self._data_received_callback(self.device_id, 'player', 0)
                self._data_received_callback(self.device_id, 'stop', True)
                self._data_received_callback(self.device_id, 'playpause', False)
                self._data_received_callback(self.device_id, 'streams', None)
                self._data_received_callback(self.device_id, 'subtitles', None)
                self._data_received_callback(self.device_id, 'audio', '')
                self._data_received_callback(self.device_id, 'subtitle', '')
                self._activeplayers = []
                self._playerid = 0

            elif data['method'] == 'GUI.OnScreensaverActivated':
                processed = True
                self.logger.debug('received: activated screensaver')
                self._data_received_callback(self.device_id, 'state', 'Screensaver')

            elif data['method'][:9] == 'Player.On':
                processed = True
                self.logger.debug('received: player notification')
                try:
                    p_id = data['params']['data']['player']['playerid']
                    query_playerinfo.append(p_id)
                except KeyError:
                    pass

            elif data['method'] == 'Application.OnVolumeChanged':
                processed = True
                self.logger.debug('received: volume changed, got new values mute: {} and volume: {}'.format(data['params']['data']['muted'], data['params']['data']['volume']))
                self._data_received_callback(self.device_id, 'mute', data['params']['data']['muted'])
                self._data_received_callback(self.device_id, 'volume', data['params']['data']['volume'])

        # if active playerid(s) was changed, update status for active player(s)
        if query_playerinfo:
            self.logger.debug(f'player info query requested for playerid(s) {query_playerinfo}')
            for player_id in set(query_playerinfo):
                self.logger.debug(f'getting player info for player #{player_id}')
                self._connection._send_rpc_message('Player.GetItem', {'properties': ['title', 'artist'], 'playerid': player_id})
                self._connection._send_rpc_message('Player.GetProperties', {'properties': ['speed', 'percentage', 'currentaudiostream', 'audiostreams', 'subtitleenabled', 'currentsubtitle', 'subtitles'], 'playerid': player_id})

        if processed:
            return

        # if we reach this point, no special handling case was detected, so just go on normally...

        try:
            # try and transform the JSON RPC method into the matching command
            command = self._commands.get_command_from_reply(command)
            value = self._commands.get_shng_data(command, data)
        except Exception as e:
            self.logger.info(f'received data "{data}" for command {command}, error occurred while converting. Discarding data. Error was: {e}')
            return

        # pass on data for regular item assignment
        self.logger.debug(f'received data "{data}" for command {command} converted to value {value}')
        self._data_received_callback(self.device_id, command, value)

    def send_command(self, command, value=None, **kwargs):
        '''
        Checks for special commands and handles them, otherwise call the
        base class' method

        :param command: the command to send
        :param value: the data to send, if applicable
        :type command: str
        :return: True if send was successful, False otherwise
        :rtype: bool
        '''
        if not self.alive:
            self.logger.warning(f'trying to send command {command} with value {value}, but device is not active.')
            return False

        if not self._connection:
            self.logger.warning(f'trying to send command {command} with value {value}, but connection is None. This shouldn\'t happen...')
            return False

        if not self._connection.connected:
            self._connection.open()
            if not self._connection.connected:
                self.logger.warning(f'trying to send command {command} with value {value}, but connection could not be established.')
                return False

        if command in self._special_commands['read' if value is None else 'write']:
            if command == 'update':
                if value:
                    self._update_status()
                return True
            elif value is None:
                self.logger.debug(f'Special command {command} called for reading, which is not intended. Ignoring request')
                return True
            else:
                # this shouldn't happen
                self.logger.warning(f'Special command {command} found, no action set for processing. Please inform developers. Ignoring request')
                return True
        else:
            return super().send_command(command, value, playerid=self._playerid, **kwargs)

    def is_valid_command(self, command, read=None):
        '''
        In addition to base class method, allow 'special'
        commands not defined in commands.py which are meant
        to control the plugin device, e.g. 'update' to read
        player status.
        If not special command, call base class method

        :param command: the command to test
        :type command: str
        :param read: check for read (True) or write (False), or both (None)
        :type read: bool | NoneType
        :return: True if command is valid, False otherwise
        :rtype: bool
        '''
        if command in self._special_commands['read' if read else 'write']:
            self.logger.debug(f'Acknowledging special command {command}, read is {read}')
            return True
        else:
            return super().is_valid_command(command, read)

#
# new methods
#

    def notify(self, title, message, image=None, display_time=10000):
        '''
        Send a notification to Kodi to be displayed on the screen

        :param title: the title of the message
        :param message: the message itself
        :param image: an optional image to be displayed alongside the message
        :param display_time: how long the message is displayed in milli seconds
        '''
        params = {'title': title, 'message': message, 'displaytime': display_time}
        if image is not None:
            params['image'] = image
        self._connection._send_rpc_message('GUI.ShowNotification', params)

    def _update_status(self):
        '''
        This method requests several status infos
        '''
        if self.alive:
            self.send_command('get_actplayer', None)
            self.send_command('get_status_au', None)
            if self._playerid:
                self.send_command('get_status_play', None)
                self.send_command('get_item', None)

    # def _check_commands_data(self):
    #     '''
    #     Method checks consistency of imported commands data
# 
    #     This is ported directly from the old kodi plugin; to not clutter things
    #     this method is implemented in the device class, even though it works
    #     on the commands and should have been implemented there. But overloading
    #     the commands class is not something (yet) planned...
# 
    #     :return: True if data is consistent
    #     :rtype: bool
    #     '''
    #     no_method = []
    #     wrong_keys = []
    #     unmatched = []
    #     bounds = []
    #     values = []
    #     for command, cmd_obj in self._commands._commands.items():
# 
    #         if not cmd_obj:
    #             print(f'no obj: {cmd_obj}')
    #             
    #         # verify all keys are present
    #         if not ['method', 'set', 'get', 'params', 'values', 'bounds'].sort() == list(entry.keys()).sort():
    #             wrong_keys.append(command)
    #         elif not ['set', 'special'].sort() == list(entry.keys()).sort():
    #             # check that method is not empty
    #             if not entry['method']:
    #                 no_method.append(command)
    #             par = entry['params']
    #             val = entry['values']
    #             bnd = entry['bounds']
    #             # params and values must be either both None or both lists of equal length
    #             if par is None and val is not None or par is not None and val is None:
    #                 unmatched.append(command)
    #             elif par is not None and val is not None and len(par) != len(val):
    #                 unmatched.append(command)
    #             vals = 0
    #             if val is not None:
    #                 # check that max. one 'VAL' entry is present
    #                 for item in val:
    #                     if item == 'VAL':
    #                         vals += 1
    #                 if vals > 1:
    #                     values.append(command)
    #             # check that bounds are None or list or (tuple and len(bounds)=2)
    #             if bnd is not None and \
    #                not isinstance(bnd, list) and \
    #                (not (isinstance(bnd, tuple) and len(bnd) == 2)):
    #                 bounds.append(command)
    #             # check that bounds are only defined if 'VAL' is present
    #             if vals == 0 and bnd is not None:
    #                 bounds.append(command)
# 
    #     # found any errors?
    #     if len(no_method + wrong_keys + unmatched + bounds + values) > 0:
    #         if len(wrong_keys) > 0:
    #             self.logger.error('Commands data not consistent: commands "' + '", "'.join(wrong_keys) + '" have wrong keys')
    #         if len(no_method) > 0:
    #             self.logger.error('Commands data not consistent: commands "' + '", "'.join(no_method) + '" have no method')
    #         if len(unmatched) > 0:
    #             self.logger.error('Commands data not consistent: commands "' + '", "'.join(unmatched) + '" have unmatched params/values')
    #         if len(bounds) > 0:
    #             self.logger.error('Commands data not consistent: commands "' + '", "'.join(bounds) + '" have erroneous bounds')
    #         if len(values) > 0:
    #             self.logger.error('Commands data not consistent: commands "' + '", "'.join(values) + '" have more than one "VAL" field')
# 
    #         return False
# 
    #     macros = []
    #     for macro, entry in commands.macros.items():
    #         if not isinstance(entry, list):
    #             macros.append(macro)
    #         else:
    #             for step in entry:
    #                 if not isinstance(step, list) or len(step) != 2:
    #                     macros.append(macro)
# 
    #     if len(macros) > 0:
    #         self.logger.error('Macro data not consistent for macros "' + '", "'.join(macros) + '"')
    #         # errors in macro definition don't hinder normal plugin functionality, so just
    #         # refill self._MACRO omitting erroneous entries. With bad luck, _MACRO is empty ;)
    #         self._MACRO = {}
    #         for command, entry in command.macros:
    #             if command not in macros:
    #                 self._MACRO[command] = entry
# 
    #     return True

