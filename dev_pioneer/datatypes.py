#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

from .. import datatypes as DT


class DT_PioPwr(DT.Datatype):
    ''' Example class for Datatype definitions. Not used in class. '''
    def __init__(self, fail_silent=True):
        super().__init__(fail_silent)
        self.logger.info(f'DT class {self.__class__.__name__} initialized. Yay.')

    def get_send_data(self, data):
        # simpel - wenn data ( == True ) ist, dann "PO" zurückgeben, sonst "PF"
        return 'PO\rPO\r' if data else 'PF\r'

    def get_shng_data(self, data, type=None):

        # wenn kein (gewünschter) Datentyp angegeben ist, dann "default" zurückgeben, hier Bool gem. Konvertierung
        # hier Bool abfangen, weil die Basisklasse das nicht (richtig) kann
        if type is None or type == 'bool':
            return True if data == 'PWR0' else False

        # wenn ausdrücklich Datentyp xy gefordert ist: lass die Basisklasse konvertieren (oder mache es ggf. selbst)
        return super().get_shng_data(data, type)
