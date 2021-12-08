#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

from .. import datatypes as DT


class DT_xxx(DT.Datatype):
    ''' Example class for Datatype definitions. Not used in class. '''
    def __init__(self, fail_silent=True):
        super().__init__(fail_silent)
        self.logger.info(f'DT class {self.__class__.__name__} initialized. Do something about this.')
