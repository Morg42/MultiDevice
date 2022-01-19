#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    from MD_Device import MD_Device
    # from MD_Globals import PLUGIN_ATTR_CMD_CLASS
    # from MD_Command import MD_Command_ParseStr
else:
    from ..MD_Device import MD_Device
    # from ..MD_Globals import PLUGIN_ATTR_CMD_CLASS
    # from ..MD_Command import MD_Command_ParseStr


class MD_Device(MD_Device):
    """
    Device class for Yamaha MusicCast devices.
    """

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
