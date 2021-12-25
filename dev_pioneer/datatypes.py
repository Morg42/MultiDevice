#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
    from dev_pioneer import lookup
else:
    from .. import datatypes as DT
    from . import lookup

import re


def dict_rev(d):
    ''' helper routine to return inversed dict (swap key/value) '''
    return {v: k for (k, v) in d.items()}


def dict_get_ci(input_dict, key):
    ''' helper routine for case insensitive dictionary search '''
    return next((value for dict_key, value in input_dict.items() if dict_key.lower() == key.lower()), None)


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
            return f"{dict_get_ci(dict_rev(lookup.DIALOG), data)}ATH"

    def get_shng_data(self, data, type=None):
        return_value = data.split("ATH")[1]
        return dict_get_ci(lookup.DIALOG, return_value)


class DT_PioError(DT.Datatype):
    def get_shng_data(self, data, type=None):
        return_value = data.split("E0")[1]
        return dict_get_ci(lookup.ERROR, return_value)


class DT_PioListening(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:04}SR"
        except Exception:
            return f"{dict_get_ci(dict_rev(lookup.LISTENINGMODE), data)}SR"

    def get_shng_data(self, data, type=None):
        return_value = data.split("SR")[1]
        return dict_get_ci(lookup.LISTENINGMODE, return_value)


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
        return dict_get_ci(lookup.PLAYINGMODE, return_value)


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
            return f"{dict_get_ci(dict_rev(lookup.SOURCE), data)}FN"

    def get_shng_data(self, data, type=None):
        return_value = data.split("FN")[1]
        return dict_get_ci(lookup.SOURCE, return_value)

class DT_PioSource2(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:02}ZS"
        except Exception:
            return f"{dict_get_ci(dict_rev(lookup.SOURCE), data)}ZS"

    def get_shng_data(self, data, type=None):
        return_value = data.split("Z2F")[1]
        return dict_get_ci(lookup.SOURCE, return_value)


class DT_PioHDMIOut(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:01}HO"
        except Exception:
            return f"{dict_get_ci(dict_rev(lookup.HDMIOUT), data)}HO"

    def get_shng_data(self, data, type=None):
        return_value = data.split("HO")[1]
        return dict_get_ci(lookup.HDMIOUT, return_value)

# unused classes from here on
