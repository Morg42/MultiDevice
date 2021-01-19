#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

from .. import datatypes as DT


class DT_xxx(DT.Datatype):

    def __init__(self, fail_silent=True):
        super().__init__(fail_silent)
        print('xxx')
