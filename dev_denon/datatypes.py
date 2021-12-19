#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
    from dev_pioneer import lookup
else:
    from .. import datatypes as DT
    from . import lookup

import re

class DT_PioDisplay(DT.Datatype):
    def get_shng_data(self, data, type=None):
        content = data[2:][:28]
        tempvalue = "".join(list(map(lambda i: chr(int(content[2 * i:][:2], 0x10)), range(14)))).strip()
        data = re.sub(r'^[^A-Z0-9]*', '', tempvalue)
        return data

class DT_PioError(DT.Datatype):
    def get_shng_data(self, data, type=None):
        return_value = data.split("E0")[1]
        return lookup.ERROR.get(return_value)

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
            return f"MV{str(data).replace('.', '')}"
        else:
            return f"MV{data}"

    def get_shng_data(self, data, type=None):
        if len(data) == 3:
            return f"{data[0:2]}.{data[2:3]}"
        else:
            return data

class DT_onoff(DT.Datatype):
    def get_send_data(self, data):
        return 'ON' if data else 'OFF'

    def get_shng_data(self, data, type=None):
        return False if data == 'OFF' else True

class DT_PioSource(DT.Datatype):
    def get_send_data(self, data, type=None):
        if data:
            try:
                data = int(data)
                return f"{data:02}FN"
            except Exception:
                return f"{lookup.SOURCE_SET.get(data.upper())}FN"
        else:
            return '?FN'

    def get_shng_data(self, data, type=None):
        return_value = data.split("FN")[1]
        return lookup.SOURCE.get(return_value)

class DT_PioListening(DT.Datatype):
    def get_send_data(self, data):
        if data:
            try:
                data = int(data)
                return f"{data:04}SR"
            except Exception:
                return f"{lookup.SOURCE_SET.get(data.upper())}SR"

    def get_shng_data(self, data, type=None):
        return_value = data.split("SR")[1]
        return lookup.LISTENINGMODE.get(return_value)

class DT_PioPlayingmode(DT.Datatype):
    def get_shng_data(self, data, type=None):
        return_value = data.split("LM")[1]
        return lookup.PLAYINGMODE.get(return_value)

class DT_PioDialog(DT.Datatype):
    def get_send_data(self, data):
        if data:
            try:
                data = int(data)
                return f"{data:01}ATH"
            except Exception:
                return f"{lookup.DIALOG_SET.get(data.upper())}ATH"

    def get_shng_data(self, data, type=None):
        return_value = data.split("ATH")[1]
        return lookup.DIALOG.get(return_value)

class DT_PioHDMIOut(DT.Datatype):
    def get_send_data(self, data):
        if data:
            try:
                data = int(data)
                return f"{data:01}HO"
            except Exception:
                return f"{lookup.DIALOG_SET.get(data.upper())}HO"

    def get_shng_data(self, data, type=None):
        return_value = data.split("HO")[1]
        return lookup.DIALOG.get(return_value)

class DT_PioPwr2(DT.Datatype):
    def get_send_data(self, data):
        return 'APO\rAPO' if data else 'APF'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data == 'APR0' else False

        return super().get_shng_data(data, type)

class DT_PioMute2(DT.Datatype):
    def get_send_data(self, data):
        return 'Z2MO' if data else 'Z2MF'

    def get_shng_data(self, data, type=None):
        return True if data == 'Z2MUT0' else False

class DT_PioSource2(DT.Datatype):
    def get_send_data(self, data):
        if data:
            try:
                data = int(data)
                return f"{data:02}ZS"
            except Exception:
                return f"{lookup.SOURCE_SET.get(data.upper())}ZS"

    def get_shng_data(self, data, type=None):
        return_value = data.split("Z2F")[1]
        return lookup.SOURCE.get(return_value)
