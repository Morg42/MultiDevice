#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
else:
    from .. import datatypes as DT

import re


class DT_PioDisplay(DT.Datatype):
    def get_shng_data(self, data, type=None):
        tempvalue = "".join(list(map(lambda i: chr(int(data[2 * i:][:2], 0x10)), range(14)))).strip()
        data = re.sub(r'^[^A-Z0-9]*', '', tempvalue)
        return data


class DT_PioChannelVol(DT.Datatype):
    def get_send_data(self, data):
        return f"{int(data * 2 + 50):02}"

    def get_shng_data(self, data, type=None):
        return (int(data) - 50) / 2


class DT_onoff(DT.Datatype):
    def get_send_data(self, data):
        return 'O' if data else 'F'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data == '0' else False

        return super().get_shng_data(data, type)
