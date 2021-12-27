#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
    from dev_pioneer import lookup
else:
    from .. import datatypes as DT
    from . import lookup


def dict_rev(d):
    ''' helper routine to return inversed dict (swap key/value) '''
    return {v: k for (k, v) in d.items()}


def dict_get_ci(input_dict, key):
    ''' helper routine for case insensitive dictionary search '''
    return next((value for dict_key, value in input_dict.items() if dict_key.lower() == key.lower()), None)


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


class DT_DenonDynam(DT.Datatype):
    def get_send_data(self, data):
        if data == 1:
            return 'LOW'
        elif data == 2:
            return 'MID'
        elif data == 3:
            return 'HI'
        elif data == 4:
            return 'AUTO'
        else:
            return 'OFF'

    def get_shng_data(self, data, type=None):
        if data == 'LOW':
            return 1
        elif data == 'MID':
            return 2
        elif data == 'HI':
            return 3
        elif data == 'AUTO':
            return 4
        else:
            return 0


class DT_DenonAspect(DT.Datatype):
    def get_send_data(self, data):
        if data == '4:3':
            return 'NRM'
        else:
            return 'FUL'

    def get_shng_data(self, data, type=None):
        if data == 'NRM':
            return '4:3'
        elif data == 'FUL':
            return '16:9'


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
        return 0 if data in ['OFF', 'NON'] else data


class DT_convertAuto(DT.Datatype):
    def get_send_data(self, data):
        return 'AUTO' if data == 0 else data

    def get_shng_data(self, data, type=None):
        return 0 if data == 'AUTO' else data


class DT_remap50to0(DT.Datatype):
    def get_send_data(self, data):
        if int(data) == data:
            # "real" integer
            return f'{(int(data)+50):02}'
        else:
            # float with fractional value
            return f'{(int(data)+50):02}5'

    def get_shng_data(self, data, type=None):
        if len(data) == 3:
            return int(data) / 10 - 50
        else:
            return int(data) - 50


class DT_DenonInputsignal(DT.Datatype):
    def get_shng_data(self, data, type=None):
        return dict_get_ci(lookup.INPUTSIGNAL, data)


class DT_DenonResolution(DT.Datatype):
    def get_send_data(self, data):
        # TODO: kann ich noch verstehen, wenn - direkte - Texteingaben vom Nutzer verarbeitet werden (LC/UC/MC)
        return dict_get_ci(dict_rev(lookup.RESOLUTION), data)

    def get_shng_data(self, data, type=None):
        # TODO: hier verstehe ich CI nicht - vom Gerät sollte doch immer der eindeutige Identifier (lookup: key) kommen?
        return dict_get_ci(lookup.RESOLUTION, data)


class DT_DenonVideoproc(DT.Datatype):
    def get_send_data(self, data):
        return dict_get_ci(dict_rev(lookup.VIDEOPROCESS), data)

    def get_shng_data(self, data, type=None):
        return dict_get_ci(lookup.VIDEOPROCESS, data)
