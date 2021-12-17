#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
    from dev_pioneer import lookup
else:
    from .. import datatypes as DT
    from . import lookup

import re

class DT_fstring(DT.Datatype):
    def get_send_data(self, data, type=None):
        return eval(data)

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

class DT_PioPwr(DT.Datatype):
    def get_send_data(self, data):
        return 'PO\rPO' if data else 'PF'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data == 'PWR0' else False

        return super().get_shng_data(data, type)

class DT_PioVol(DT.Datatype):
    def get_send_data(self, data):
        data = max(10,min(160,int(data)))
        return f"{data:03}VL"

    def get_shng_data(self, data, type=None):
        return data.split("VOL")[1]

class DT_PioMute(DT.Datatype):
    def get_send_data(self, data):
        return 'MO' if data else 'MF'

    def get_shng_data(self, data, type=None):
        return True if data == 'MUT0' else False

class DT_PioSource(DT.Datatype):
    def get_send_data(self, data, type=None):
        try:
            data = int(data)
            return f"{data:02}FN"
        except Exception:
            return f"{lookup.SOURCE_SET.get(data.upper())}FN"

    def get_shng_data(self, data, type=None):
        return_value = data.split("FN")[1]
        return lookup.SOURCE.get(return_value)

class DT_PioListening(DT.Datatype):
    def get_send_data(self, data):
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

class DT_PioSpeakers(DT.Datatype):
    def get_send_data(self, data):
        data = data if data == '9' else max(0,min(3,int(data)))
        return f"{data:01}SPK"

    def get_shng_data(self, data, type=None):
        return data.split("SPK")[1]

class DT_PioTone(DT.Datatype):
    def get_send_data(self, data):
        return '1TO' if data else '0TO'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data == 'TO0' else False

        return super().get_shng_data(data, type)

class DT_PioTreble(DT.Datatype):
    def get_send_data(self, data):
        data = max(0,min(12,int(data)))
        return f"{data:02}TR"

    def get_shng_data(self, data, type=None):
        return data.split("TR")[1]

class DT_PioBass(DT.Datatype):
    def get_send_data(self, data):
        data = max(0,min(12,int(data)))
        return f"{data:02}BA"

    def get_shng_data(self, data, type=None):
        return data.split("BA")[1]

class DT_PioDialog(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            data = max(0,min(9,data))
            return f"{data:01}ATH"
        except Exception:
            return f"{lookup.DIALOG_SET.get(data.upper())}ATH"

    def get_shng_data(self, data, type=None):
        return_value = data.split("ATH")[1]
        return lookup.DIALOG.get(return_value)

class DT_PioHDMIOut(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:01}HO"
        except Exception:
            return f"{lookup.DIALOG_SET.get(data.upper())}HO"

    def get_shng_data(self, data, type=None):
        return_value = data.split("HO")[1]
        return lookup.DIALOG.get(return_value)

class DT_PioTunerpreset(DT.Datatype):
    def get_send_data(self, data):
        data_class = data[:1]
        data_preset = f"{max(0,min(9,int(data[1:]))):02}"
        return f"{data_class}{data_preset}PR"

    def get_shng_data(self, data, type=None):
        return data.split("PR")[1]

class DT_PioPwr2(DT.Datatype):
    def get_send_data(self, data):
        return 'APO\rAPO' if data else 'APF'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data == 'APR0' else False

        return super().get_shng_data(data, type)

class DT_PioVol2(DT.Datatype):
    def get_send_data(self, data):
        data = max(0,min(81,int(data)))
        return f"{data:03}ZV"

    def get_shng_data(self, data, type=None):
        return data.split("ZV")[1]

class DT_PioMute2(DT.Datatype):
    def get_send_data(self, data):
        return 'Z2MO' if data else 'Z2MF'

    def get_shng_data(self, data, type=None):
        return True if data == 'Z2MUT0' else False

class DT_PioSource2(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:02}ZS"
        except Exception:
            return f"{lookup.SOURCE_SET.get(data.upper())}ZS"

    def get_shng_data(self, data, type=None):
        return_value = data.split("Z2F")[1]
        return lookup.SOURCE.get(return_value)
