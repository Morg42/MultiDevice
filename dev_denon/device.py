#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    from MD_Globals import *
    from MD_Device import MD_Device
    from MD_Command import MD_Command_ParseStr
else:
    from ..MD_Globals import *
    from ..MD_Device import MD_Device
    from ..MD_Command import MD_Command_ParseStr


class MD_Device(MD_Device):
    """ Device class for Denon AV.

    Most of the work is done by the base class, so we only set default parameters
    for the connection (to be overwritten by device attributes from the plugin
    configuration) and add a fixed terminator byte to outgoing datagrams.

    The know-how is in the commands.py (and some DT_ classes...)
    """

    def _set_custom_vars(self):
        #set our own preferences concerning connections
        if PLUGIN_ATTR_NET_HOST in self._params and self._params[PLUGIN_ATTR_NET_HOST]:
           self._params[PLUGIN_ATTR_CONNECTION] = CONN_NET_TCP_CLI
        elif PLUGIN_ATTR_SERIAL_PORT in self._params and self._params[PLUGIN_ATTR_SERIAL_PORT]:
           self._params[PLUGIN_ATTR_CONNECTION] = CONN_SER_ASYNC
        if PLUGIN_ATTR_CONN_TERMINATOR in self._params:
            b = self._params[PLUGIN_ATTR_CONN_TERMINATOR].encode()
            b = b.decode('unicode-escape').encode()
            self._params[PLUGIN_ATTR_CONN_TERMINATOR] = b

    # we need to receive data via callback, as the "reply" can be unrelated to
    # the sent command. Getting it as return value would assign it to the wrong
    # command and discard it... so break the "return result"-chain
    def _send(self, data_dict):
        self._connection.send(data_dict)
        return None

    def _transform_send_data(self, data=None):
        if data:
            try:
                data['limit_response'] = self._params.get(PLUGIN_ATTR_CONN_TERMINATOR, b'\r')
                data['payload'] = f'{data.get("payload")}\r'
            except Exception as e:
                self.logger.error(f'ERROR {e}')
        return data
