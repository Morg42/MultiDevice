#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2020-      Sebastian Helms             Morg @ knx-user-forum
#########################################################################
#  This file aims to become part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  MD_Datatype and derived classes for MultiDevice plugin
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

'''
    Datatype
    -----------

    This is one of the most important classes. By declaration, it contains
    information about the data type and format needed by a device and methods
    to convert its value from selected Python data types used in items to the
    (possibly) special data formats required by devices and vice versa.

    Datatypes are specified in subclasses of Datatype with a nomenclature
    convention of DT_<device data type of format>.

    All datatype classes are imported from Datatypes.py into the 'DT' module.

    New devices probably create the need for new data types.

    For details concerning API and implementation, refer to the reference classes as
    examples.

'''

import json
import logging

datatypes = (
    'int', 'num', 'str', 'dict', 'list', 'tuple', 'bytes', 'bytearray', 'json'
)


class Datatype(object):

    def __init__(self, fail_silent=True):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(__name__)

        self._silent = fail_silent

    def get_send_data(self, data):
        return data

    def get_shng_data(self, data, type=None):
        if type is None or type not in datatypes:
            return data

        if type == 'int':
            try:
                return int(data)
            except ValueError:
                if self._silent:
                    return 0
                else:
                    raise

        if type == 'num':
            try:
                return float(data)
            except ValueError:
                if self._silent:
                    return 0
                else:
                    raise

        if type == 'str':
            return str(data)

        if type == 'dict':
            try:
                return dict(data)
            except ValueError:
                if self._silent:
                    return {}
                else:
                    raise

        if type == 'list':
            try:
                return list(data)
            except ValueError:
                if self._silent:
                    return []
                else:
                    raise

        if type == 'tuple':
            try:
                return tuple(data)
            except ValueError:
                if self._silent:
                    return ()
                else:
                    raise

        if type == 'bytes':
            try:
                return bytes(str(data), 'utf-8')
            except ValueError:
                if self._silent:
                    return b''
                else:
                    raise

        if type == 'bytearray':
            try:
                return bytearray(str(data), 'utf-8')
            except ValueError:
                if self._silent:
                    return bytearray(b'')
                else:
                    raise

        if type == 'json':
            try:
                return json.dumps(data)
            except ValueError:
                if self._silent:
                    return None
                else:
                    raise


class DT_raw(Datatype):
    ''' pass on data, identical to base class '''
    pass


#
# TODO: add error handling on conversion error to DT_ classes...?
#

class DT_int(Datatype):
    ''' cast to int '''
    def get_send_data(self, data):
        return int(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return int(data)

        return super().get_shng_data(data, type)


class DT_num(Datatype):
    ''' cast to float '''
    def get_send_data(self, data):
        return float(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return float(data)

        return super().get_shng_data(data, type)


class DT_str(Datatype):
    ''' cast to str '''
    def get_send_data(self, data):
        return str(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return str(data)
        return super().get_shng_data(data, type)


class DT_list(Datatype):
    ''' enlist '''
    def get_send_data(self, data):
        return list(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return list(data)
        return super().get_shng_data(data, type)


class DT_dict(Datatype):
    ''' dict-ate '''
    def get_send_data(self, data):
        return dict(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return dict(data)
        return super().get_shng_data(data, type)


class DT_tuple(Datatype):
    ''' toupling (meh...) '''
    def get_send_data(self, data):
        return tuple(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return tuple(data)
        return super().get_shng_data(data, type)


class DT_bytes(Datatype):
    def get_send_data(self, data):
        return bytes(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return bytes(data)
        return super().get_shng_data(data, type)


class DT_bytearray(Datatype):
    def get_send_data(self, data):
        return bytearray(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return bytearray(data)
        return super().get_shng_data(data, type)


class DT_json(Datatype):
    def get_send_data(self, data):
        return json.dumps(data)

    def get_shng_data(self, data, type=None):
        if type is None:
            return json.loads(data)
        return super().get_shng_data(data, type)


class DT_shng_ws(Datatype):
    ''' extract value from json '''
    def get_send_data(self, data):
        return data

    def get_shng_data(self, data, type=None):
        if type is None:
            js = json.loads(data)
            arg = js.get('value', None)
            return arg
        return super().get_shng_data(data, type)
