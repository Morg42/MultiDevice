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


class DT_PioDialog(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:01}ATH"
        except Exception:
            return f"{dict_rev(lookup.DIALOG).get(data.upper())}ATH"

    def get_shng_data(self, data, type=None):
        return_value = data.split("ATH")[1]
        return lookup.DIALOG.get(return_value)


class DT_PioError(DT.Datatype):
    def get_shng_data(self, data, type=None):
        return_value = data.split("E0")[1]
        return lookup.ERROR.get(return_value)


class DT_PioListening(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:04}SR"
        except Exception:
            return f"{dict_rev(lookup.LISTENINGMODE).get(data.upper())}SR"

    def get_shng_data(self, data, type=None):
        return_value = data.split("SR")[1]
        return lookup.LISTENINGMODE.get(return_value)


class DT_PioMute(DT.Datatype):
    def get_send_data(self, data):
        return 'MO' if data else 'MF'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data[-4:] == 'MUT0' else False

        return super().get_shng_data(data, type)


class DT_PioPlayingmode(DT.Datatype):
    def get_shng_data(self, data, type=None):
        return_value = data.split("LM")[1]
        return lookup.PLAYINGMODE.get(return_value)


class DT_PioPwr(DT.Datatype):
    def get_send_data(self, data):
        return 'PO' if data else 'PF'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data in ['PWR0', 'APR0'] else False

        return super().get_shng_data(data, type)


class DT_PioSource(DT.Datatype):
    def get_send_data(self, data, type=None):
        try:
            data = int(data)
            return f"{data:02}FN"
        except Exception:
            return f"{dict_rev(lookup.SOURCE).get(data.upper())}FN"

    def get_shng_data(self, data, type=None):
        return_value = data.split("FN")[1]
        return lookup.SOURCE.get(return_value)

class DT_PioSource2(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:02}ZS"
        except Exception:
            return f"{dict_rev(lookup.SOURCE).get(data.upper())}ZS"

    def get_shng_data(self, data, type=None):
        return_value = data.split("Z2F")[1]
        return lookup.SOURCE.get(return_value)


class DT_PioHDMIOut(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:01}HO"
        except Exception:
            return f"{dict_rev(lookup.HDMIOUT).get(data.upper())}HO"

    def get_shng_data(self, data, type=None):
        return_value = data.split("HO")[1]
        return lookup.HDMIOUT.get(return_value)

# unused classes from here on
