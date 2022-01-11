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
    """ Example class for TCP request connections.

    This class reads arbitrary URLs or parametrized URLs using plugin configuration
    for `host` and `port`.

    See ``commands.py`` for command usage.
    """

    def _set_default_params(self):

        # set parameter defaults
        # TODO: adapt these to actual requirements!
        self._params = {'command_class': MD_Command_Str,            # remember to import the needed class!
                        PLUGIN_ATTR_CONNECTION: CONN_NET_TCP_REQ}    # check MD_Globals.py for constants
