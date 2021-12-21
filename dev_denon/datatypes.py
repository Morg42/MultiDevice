#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
else:
    from .. import datatypes as DT

import re  # unused as of now...


class DT_DenonDisplay(DT.Datatype):
    def get_shng_data(self, data, type=None):
        infotype = data[3:4]
        if infotype.isdigit():
            if infotype == 0:
                data = data[4:]
            elif infotype == 1:
                data = data[5:]
            else:
                data = data[6:]
            return data

        return None


class DT_DenonPwr(DT.Datatype):
    def get_send_data(self, data):
        return 'PWON' if data else 'PWSTANDBY'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data == 'ON' else False

        return super().get_shng_data(data, type)


class DT_DenonVol(DT.Datatype):
    def get_send_data(self, data):
        if int(data) == data:
            # "real" integer
            return f'{int(data):02}'
        else:
           # float with fractional value
           return f'{int(data):02}5'

    def get_shng_data(self, data, type=None):
        if len(data) == 3:
            return int(data) / 10
        else:
            return data


class DT_DenonStandby(DT.Datatype):
    def get_send_data(self, data):
        return 'OFF' if data == 0 else f"{data:01}H"

    def get_shng_data(self, data, type=None):
        return 0 if data == 'OFF' else data.split('H')[0]


class DT_DenonStandby1(DT.Datatype):
    def get_send_data(self, data):
        return 'OFF' if data == 0 else f"{data:02}M"

    def get_shng_data(self, data, type=None):
        return 0 if data == 'OFF' else data.split('M')[0]


class DT_DenonDialog(DT.Datatype):
    def get_send_data(self, data):
        if data == 1:
            return 'LOW'
        elif data == 2:
            return 'MED'
        elif data == 3:
            return 'HIGH'
        else:
            return 'OFF'

    def get_shng_data(self, data, type=None):
        if data == 'LOW':
            return 1
        elif data == 'MED':
            return 2
        elif data == 'HIGH':
            return 3
        else:
            return 0


class DT_onoff(DT.Datatype):
    def get_send_data(self, data):
        return 'ON' if data else 'OFF'

    def get_shng_data(self, data, type=None):
        return False if data == 'OFF' else True


class DT_convert0(DT.Datatype):
    def get_send_data(self, data):
        return 'OFF' if data == 0 else f"{data:03}"

    def get_shng_data(self, data, type=None):
        return 0 if data == 'OFF' else data
