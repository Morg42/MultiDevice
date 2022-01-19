#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
else:
    from .. import datatypes as DT


# handle feedback if rescan is running or not
class DT_SqueezeRescan(DT.Datatype):
    def get_shng_data(self, data, type=None, **kwargs):
        return True if data in ["1", "done"] else False
