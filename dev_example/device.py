#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    from MD_Device import MD_Device
else:
    from ..MD_Device import MD_Device


class MD_Device(MD_Device):
    """ Example class for TCP client (async receiving) connection. """

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
