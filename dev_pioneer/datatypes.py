#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
else:
    from .. import datatypes as DT

import re


class DT_PioDisplay(DT.Datatype):
    def get_shng_data(self, data, type=None):
        content = data[2:][:28]
        tempvalue = "".join(list(map(lambda i: chr(int(content[2 * i:][:2], 0x10)), range(14)))).strip()
        data = re.sub(r'^[^A-Z0-9]*', '', tempvalue)
        return data


# TODO: obsolete with lookup and reply_pattern implemented
#       most other DT_classes like this can be removed
#       capturing reply value can be done in reply_pattern
#       write_cmd can be written as "MD_VALUE<XXX>", where XXX is the command
#       opcode, ATH in this example
#       Lookup and formatting is done automatically - especially if lookup is 
#       enabled, you get exactly the format you want (if defined properly ;) )
#       This makes int(data) and data:01 obsolete.
#
#       Go on and clean out this file - and the same for denon ;)
#       Error, Source1, Source2 and one or two other classes are already removed
#       you can at least remove DT_PioListening, DT_PioPlayingmode and DT_PioHDMIOut
#
# class DT_PioDialog(DT.Datatype):
#     def get_send_data(self, data):
#         try:
#             data = int(data)
#             return f"{data:01}ATH"
#         except Exception:
#             return f"{data}ATH"
# 
#     def get_shng_data(self, data, type=None):
#         return data.split("ATH")[1]
        

class DT_PioListening(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:04}SR"
        except Exception:
            return f"{data}SR"

    def get_shng_data(self, data, type=None):
        return data.split("SR")[1]


class DT_PioMute(DT.Datatype):
    def get_send_data(self, data):
        return 'MO' if data else 'MF'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data[-4:] == 'MUT0' else False

        return super().get_shng_data(data, type)


class DT_PioPlayingmode(DT.Datatype):
    def get_shng_data(self, data, type=None):
        return data.split("LM")[1]


class DT_PioPwr(DT.Datatype):
    def get_send_data(self, data):
        return 'PO' if data else 'PF'

    def get_shng_data(self, data, type=None):
        if type is None or type == 'bool':
            return True if data in ['PWR0', 'APR0'] else False

        return super().get_shng_data(data, type)


class DT_PioHDMIOut(DT.Datatype):
    def get_send_data(self, data):
        try:
            data = int(data)
            return f"{data:01}HO"
        except Exception:
            return f"{data}HO"

    def get_shng_data(self, data, type=None):
        return data.split("HO")[1]
