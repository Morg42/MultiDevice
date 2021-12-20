#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
else:
    from .. import datatypes as DT

import re

class DT_DenonDisplay(DT.Datatype):
    def get_shng_data(self, data, type=None):
        infotype = data[3:4]
        returnvalue = None
        if infotype.isdigit():
            infotype = int(infotype)
            data = data[4:] if infotype == 0 else \
                data[5:] if infotype == 1 else data[6:]
            returnvalue = data if infotype in [1, 2] else None
        return returnvalue

class DT_DenonPwr(DT.Datatype):
    def get_send_data(self, data):
        return 'PWON' if data else 'PWSTANDBY'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data == 'ON' else False
        return super().get_shng_data(data, type)

class DT_DenonVol(DT.Datatype):
    def get_send_data(self, data):
        if isinstance(data, float):
            if data.is_integer():
                # strip .0 from float
                return int(data)
            else:
                # convert any other float to three digit value ending with 5 (=xx.5)
                return f"{str(data)[:2]}5"
        else:
            return data

    def get_shng_data(self, data, type=None):
        if len(data) == 3:
            return f"{data[0:2]}.{data[2:3]}"
        else:
            return data

class DT_DenonStandby(DT.Datatype):
    def get_send_data(self, data):
        return 'Z2STBYOFF' if data == 0 else f"Z2STBY{data:01}H"

    def get_shng_data(self, data, type=None):
        return 0 if data == 'OFF' else data.split('H')[0]

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
