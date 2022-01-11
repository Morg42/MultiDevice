#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    from MD_Globals import *
    from MD_Device import MD_Device
    from MD_Command import MD_Command_Str
else:
    from ..MD_Globals import *
    from ..MD_Device import MD_Device
    from ..MD_Command import MD_Command_Str


class MD_Device(MD_Device):
    """ Example class for TCP client (async receiving) connection. """

    def _set_default_params(self):

        # set parameter defaults
        # TODO: adapt these to actual requirements!
        self._params = {'command_class': MD_Command_Str,            # remember to import the needed class!
                        PLUGIN_ATTR_CONNECTION: CONN_NET_TCP_CLI,   # check MD_Globals.py for constants
                        PLUGIN_ATTR_NET_HOST: '',                   # this creates self._host for network connections
                        PLUGIN_ATTR_NET_PORT: 0, 
                        PLUGIN_ATTR_CONN_AUTO_CONN: True,
                        PLUGIN_ATTR_CONN_RETRIES: 5, 
                        PLUGIN_ATTR_CONN_CYCLE: 3, 
                        PLUGIN_ATTR_CONN_TIMEOUT: 3, 
                        PLUGIN_ATTR_CONN_TERMINATOR: b'\r',
                        'disconnected_callback': None}

    def _post_init(self):
        # if you don't know what to do with this method, just delete it!

        # possibly do things you need to do (assert?) after the base
        # class' __init__ has run

        self.logger.info('Init is done and I did something important.')

        # if for some reason necessary, you _can_ disable loading the
        # device, if so needed... maybe you might want to tell somebody
        # about it

        self.logger.warning('infinite improbability detected, device disabled')
        self._disabled = True
