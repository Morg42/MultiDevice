#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
else:
    from .. import datatypes as DT


class DT_PioPwr(DT.Datatype):
    def get_send_data(self, data):
        return 'PO\rPO' if data else 'PF'

    def get_shng_data(self, data, type=None):

        if type is None or type == 'bool':
            return True if data == 'PWR0' else False

        return super().get_shng_data(data, type)


class DT_PioVol(DT.Datatype):
    def get_send_data(self, data):
        return f"{data:03}VL"

    def get_shng_data(self, data, type=None):
        return data.split("VOL")[1]


class DT_PioMute(DT.Datatype):
    def get_send_data(self, data):
        return 'MO' if data else 'MF'

    def get_shng_data(self, data, type=None):
        return True if data == 'MUT0' else False


class DT_PioSource(DT.Datatype):
    def get_send_data(self, data):
        return f"{data:02}FN"

    def get_shng_data(self, data, type=None):
        return data.split("FN")[1]
