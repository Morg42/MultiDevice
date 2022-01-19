#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    from MD_Device import MD_Device
    from MD_Globals import CUSTOM_SEP
else:
    from ..MD_Device import MD_Device
    from ..MD_Globals import CUSTOM_SEP


class MD_Device(MD_Device):
    """
    Device class for Yamaha MusicCast devices.
    """

    def _set_device_defaults(self):
        self._use_callbacks = True

    def on_connect(self, by=None):
        # redirect send_command() output to on_data_received
        self.logger.debug('redirecting callbacks')
        self._plugin_callback = self._data_received_callback
        self._data_received_callback = self.data_callback

    def _transform_send_data(self, data_dict, **kwargs):
        payload = data_dict['payload']
        if self.custom_commands:
            host = kwargs['custom'][self.custom_commands]
        else:
            host = self._params['host']

        url = f'http://{host}/YamahaExtendedControl/{payload}'
        headers = {
            'X-AppName': 'MusicCast/0.42',
            'X-AppPort': f'{self._params["port"]}'
        }
        data_dict['payload'] = url
        data_dict['headers'] = headers

        if data_dict['data'] is not None:
            data_dict['method'] = 'post'
        else:
            data_dict['method'] = 'get'

        return data_dict

    def data_callback(self, device_id, command, data):

        def _dispatch(command, value, custom=None):

            if custom:
                command = command + CUSTOM_SEP + custom
            if self._plugin_callback:
                self._plugin_callback(device_id, command, value)

        self.logger.debug(f'called musiccast on_data_received with command={command} and data={data}')

        custom = None

        # handle returning information.
        if not isinstance(data, dict):
            self.logger.info(f'got unknown reply: {data}, ignoring.')
            return

        if 'response_code' in data and data['response_code']:
            # error, response_code != 0
            lu = self._commands._get_cmd_lookup('info.error')
            if lu:
                result = self._commands._lookup(data['response_code'], lu)
                _dispatch('info.error', result, custom)

        # command = self._commands.get_command_from_reply(data)
        # custom = None
        # f self.custom_commands:
        #    custom = self._get_custom_value(command, data)

        # ry:
        #    if custom:
        #        command = command + CUSTOM_SEP + custom
        # xcept Exception as e:
        #    self.logger.info(f'received data "{data}" for command {command}, error {e} occurred while converting. Discarding data.')
        # lse:
        #    self.logger.debug(f'received data "{data}" for command {command} converted to value {value}')
        #    if self._data_received_callback:
        #        self._data_received_callback(self.device_id, command, value)
        #    else:
        #        self.logger.warning(f'command {command} yielded value {value}, but _data_received_callback is not set. Discarding data.')
