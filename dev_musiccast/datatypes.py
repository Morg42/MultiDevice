#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

if MD_standalone:
    import datatypes as DT
else:
    from .. import datatypes as DT

import json


class DT_none(DT.Datatype):

    def get_send_data(self, data, **kwargs):
        return None

    def get_shng_data(self, data, type=None, **kwargs):
        if type is None:
            return data

        # let the base class do some work if type is explicitly requested
        return super().get_shng_data(data, type)


class DT_al_on(DT.Datatype):

    def get_send_data(self, data, **kwargs):
        return json.dumps({"alarm_on": f"{data}"})


class DT_al_time(DT.Datatype):

    def get_send_data(self, data, **kwargs):
        return json.dumps({"detail": {"day": "oneday", "time": data}})


class DT_al_beep(DT.Datatype):

    def get_send_data(self, data, **kwargs):
        return json.dumps({"detail": {"day": "oneday", "beep": data}})
