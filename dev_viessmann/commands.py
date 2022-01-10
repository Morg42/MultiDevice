#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab

""" commands for dev viessmann """

# models defined:
#
# V200KW2
# V200KO1B
# V200WO1C
# V200HO1C


commands = {
    'ALL': {
        'Anlagentyp':   {'read': True,  'write': False, 'opcode': '00f8', 'reply_token': '00f8', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 2], 'lookup': 'devicetypes'},     # getAnlTyp -- Information - Allgemein: Anlagentyp (204D)
        },
    'V200KO1B': {
        # Kessel
        'Aussentemperatur':                         {'read': True,  'write': False, 'opcode': '0800', 'reply_token': '0800', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Aussentemperatur
        'Aussentemperatur_TP':                      {'read': True,  'write': False, 'opcode': '5525', 'reply_token': '5525', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Aussentemperatur_tiefpass
        'Aussentemperatur_Dp':                      {'read': True,  'write': False, 'opcode': '5527', 'reply_token': '5527', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Aussentemperatur in Grad C (Gedaempft)
        'Kesseltemperatur':                         {'read': True,  'write': False, 'opcode': '0802', 'reply_token': '0802', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Kesseltemperatur
        'Kesseltemperatur_TP':                      {'read': True,  'write': False, 'opcode': '0810', 'reply_token': '0810', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Kesseltemperatur_tiefpass
        'Kesselsolltemperatur':                     {'read': True,  'write': False, 'opcode': '555a', 'reply_token': '555a', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Kesselsolltemperatur
        'Temp_Speicher_Ladesensor':                 {'read': True,  'write': False, 'opcode': '0812', 'reply_token': '0812', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Temperatur Speicher Ladesensor Komfortsensor
        'Auslauftemperatur':                        {'read': True,  'write': False, 'opcode': '0814', 'reply_token': '0814', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Auslauftemperatur
        'Abgastemperatur':                          {'read': True,  'write': False, 'opcode': '0816', 'reply_token': '0816', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Abgastemperatur
        'Gem_Vorlauftemperatur':                    {'read': True,  'write': False, 'opcode': '081a', 'reply_token': '081a', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Gem. Vorlauftemperatur
        'Relais_K12':                               {'read': True,  'write': False, 'opcode': '0842', 'reply_token': '0842', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Relais K12 Interne Anschlußerweiterung
        'Eingang_0-10_V':                           {'read': True,  'write': False, 'opcode': '0a86', 'reply_token': '0a86', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Eingang 0-10 V
        'EA1_Kontakt_0':                            {'read': True,  'write': False, 'opcode': '0a90', 'reply_token': '0a90', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # EA1: Kontakt 0
        'EA1_Kontakt_1':                            {'read': True,  'write': False, 'opcode': '0a91', 'reply_token': '0a91', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # EA1: Kontakt 1
        'EA1_Kontakt_2':                            {'read': True,  'write': False, 'opcode': '0a92', 'reply_token': '0a92', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # EA1: Kontakt 2
        'EA1_Externer_Soll_0-10V':                  {'read': True,  'write': False, 'opcode': '0a93', 'reply_token': '0a93', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # EA1: Externer Sollwert 0-10V
        'EA1_Relais_0':                             {'read': True,  'write': False, 'opcode': '0a95', 'reply_token': '0a95', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # EA1: Relais 0
        'AM1_Ausgang_1':                            {'read': True,  'write': False, 'opcode': '0aa0', 'reply_token': '0aa0', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # AM1 Ausgang 1
        'AM1_Ausgang_2':                            {'read': True,  'write': False, 'opcode': '0aa1', 'reply_token': '0aa1', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # AM1 Ausgang 2
        'TempKOffset':                              {'read': True,  'write': True,  'opcode': '6760', 'reply_token': '6760', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 1193045}},     # Kesseloffset KT ueber WWsoll in Grad C
        'Systemtime':                               {'read': True,  'write': True,  'opcode': '088e', 'reply_token': '088e', 'item_type': 'bool', 'dev_datatype': 'TI','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Systemzeit
        'Anlagenschema':                            {'read': True,  'write': False, 'opcode': '7700', 'reply_token': '7700', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 2], 'lookup': 'systemschemes'},     # Anlagenschema
        'Inventory':                                {'read': True,  'write': False, 'opcode': '08e0', 'reply_token': '08e0', 'item_type': 'str',  'dev_datatype': 'SN','params': ['value', 'len'], 'param_values': ['VAL', 7]},     # Sachnummer
        'CtrlId':                                   {'read': True,  'write': False, 'opcode': '08e0', 'reply_token': '08e0', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 7], 'lookup': 'devicetypes'},     # Reglerkennung
        # Fehler                
        'Sammelstoerung':                           {'read': True,  'write': False, 'opcode': '0a82', 'reply_token': '0a82', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},     # Sammelstörung
        'Error0':                                   {'read': True,  'write': False, 'opcode': '7507', 'reply_token': '7507', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 1
        'Error1':                                   {'read': True,  'write': False, 'opcode': '7510', 'reply_token': '7510', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 2
        'Error2':                                   {'read': True,  'write': False, 'opcode': '7519', 'reply_token': '7519', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 3
        'Error3':                                   {'read': True,  'write': False, 'opcode': '7522', 'reply_token': '7522', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 4
        'Error4':                                   {'read': True,  'write': False, 'opcode': '752b', 'reply_token': '752b', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 5
        'Error5':                                   {'read': True,  'write': False, 'opcode': '7534', 'reply_token': '7534', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 6
        'Error6':                                   {'read': True,  'write': False, 'opcode': '753d', 'reply_token': '753d', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 7
        'Error7':                                   {'read': True,  'write': False, 'opcode': '7546', 'reply_token': '7546', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 8
        'Error8':                                   {'read': True,  'write': False, 'opcode': '754f', 'reply_token': '754f', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 9
        'Error9':                                   {'read': True,  'write': False, 'opcode': '7558', 'reply_token': '7558', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 10
        # Pumpen                
        'Speicherladepumpe':                        {'read': True,  'write': False, 'opcode': '6513', 'reply_token': '6513', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Speicherladepumpe
        'Zirkulationspumpe':                        {'read': True,  'write': False, 'opcode': '6515', 'reply_token': '6515', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Zirkulationspumpe
        'Interne_Pumpe':                            {'read': True,  'write': False, 'opcode': '7660', 'reply_token': '7660', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Interne Pumpe
        'Heizkreispumpe_A1M1':                      {'read': True,  'write': False, 'opcode': '2906', 'reply_token': '2906', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Heizkreispumpe A1
        'Heizkreispumpe_A1M1_RPM':                  {'read': True,  'write': False, 'opcode': '7663', 'reply_token': '7663', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Heizkreispumpe A1M1 Drehzahl
        'Heizkreispumpe_M2':                        {'read': True,  'write': False, 'opcode': '3906', 'reply_token': '3906', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Heizkreispumpe M2
        'Heizkreispumpe_M2_RPM':                    {'read': True,  'write': False, 'opcode': '7665', 'reply_token': '7665', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Heizkreispumpe M2 Drehzahl
        'Relais_Status_Pumpe_A1M1':                 {'read': True,  'write': False, 'opcode': 'a152', 'reply_token': 'a152', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Relais-Status Heizkreispumpe 1
        # Brenner               
        'Brennerstarts':                            {'read': True,  'write': True,  'opcode': '088a', 'reply_token': '088a', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 4], 'settings': {'force_min': 0, 'force_max': 1193045}},     # Brennerstarts
        'Brenner_Betriebsstunden':                  {'read': True,  'write': True,  'opcode': '08a7', 'reply_token': '08a7', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4], 'settings': {'force_min': 0, 'force_max': 1193045}},     # Brenner-Betriebsstunden
        'Brennerstatus_1':                          {'read': True,  'write': False, 'opcode': '0842', 'reply_token': '0842', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Brennerstatus Stufe1
        'Brennerstatus_2':                          {'read': True,  'write': False, 'opcode': '0849', 'reply_token': '0849', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Brennerstatus Stufe2
        'Oeldurchsatz':                             {'read': True,  'write': True,  'opcode': '5726', 'reply_token': '5726', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 4], 'settings': {'force_min': 0, 'force_max': 1193045}},     # Oeldurchsatz Brenner in Dezi-Liter pro Stunde
        'Oelverbrauch':                             {'read': True,  'write': True,  'opcode': '7574', 'reply_token': '7574', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 1000, True, 4]},     # Oelverbrauch kumuliert
        # Solar
        'Nachladeunterdrueckung':                   {'read': True,  'write': False, 'opcode': '6551', 'reply_token': '6551', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},
        'SolarPumpe':                               {'read': True,  'write': False, 'opcode': '6552', 'reply_token': '6552', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     
        'Kollektortemperatur':                      {'read': True,  'write': False, 'opcode': '6564', 'reply_token': '6564', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},
        'Speichertemperatur':                       {'read': True,  'write': False, 'opcode': '6566', 'reply_token': '6566', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     
        'Solar_Betriebsstunden':                    {'read': True,  'write': False, 'opcode': '6568', 'reply_token': '6568', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 100, 4]},
        'Solarsteuerung':                           {'read': True,  'write': False, 'opcode': '7754', 'reply_token': '7754', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 2]},
        # Heizkreis A1M1
        'Raumtemperatur_A1M1':                      {'read': True,  'write': False, 'opcode': '0896', 'reply_token': '0896', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1]},     # Raumtemperatur A1M1
        'Raumtemperatur_Soll_Normalbetrieb_A1M1':   {'read': True,  'write': True,  'opcode': '2306', 'reply_token': '2306', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 3, 'force_max': 37}},     # Raumtemperatur Soll Normalbetrieb A1M1
        'Raumtemperatur_Soll_Red_Betrieb_A1M1':     {'read': True,  'write': True,  'opcode': '2307', 'reply_token': '2307', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 3, 'force_max': 37}},     # Raumtemperatur Soll Reduzierter Betrieb A1M1
        'Raumtemperatur_Soll_Party_Betrieb_A1M1':   {'read': True,  'write': True,  'opcode': '2308', 'reply_token': '2308', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 3, 'force_max': 37}},     # Raumtemperatur Soll Party Betrieb A1M1
        'Aktuelle_Betriebsart_A1M1':                {'read': True,  'write': False, 'opcode': '2301', 'reply_token': '2301', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'operatingmodes'},     # Aktuelle Betriebsart A1M1
        'Betriebsart_A1M1':                         {'read': True,  'write': True,  'opcode': '2323', 'reply_token': '2323', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 4}},     # Betriebsart A1M1
        'Sparbetrieb_A1M1':                         {'read': True,  'write': False, 'opcode': '2302', 'reply_token': '2302', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Sparbetrieb A1M1
        'Zustand_Sparbetrieb_A1M1':                 {'read': True,  'write': True,  'opcode': '2331', 'reply_token': '2331', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Zustand Sparbetrieb A1M1        
        'Partybetrieb_A1M1':                        {'read': True,  'write': False, 'opcode': '2303', 'reply_token': '2303', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Partybetrieb A1M1
        'Zustand_Partybetrieb_A1M1':                {'read': True,  'write': True,  'opcode': '2330', 'reply_token': '2330', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Zustand Partybetrieb A1M1        
        'Vorlauftemperatur_A1M1':                   {'read': True,  'write': False, 'opcode': '2900', 'reply_token': '2900', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur A1M1
        'Vorlauftemperatur_Soll_A1M1':              {'read': True,  'write': False, 'opcode': '2544', 'reply_token': '2544', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur Soll A1M1
        'StatusFrost_A1M1':                         {'read': True,  'write': False, 'opcode': '2500', 'reply_token': '2500', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Status Frostwarnung A1M1
        'Externe_Raumsolltemperatur_Normal_A1M1':   {'read': True,  'write': True,  'opcode': '2321', 'reply_token': '2321', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 37}},     # Externe Raumsolltemperatur Normal A1M1
        'Externe_Betriebsartenumschaltung_A1M1':    {'read': True,  'write': True,  'opcode': '2549', 'reply_token': '2549', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 4}},     # Externe Betriebsartenumschaltung A1M1
        'Speichervorrang_A1M1':                     {'read': True,  'write': True,  'opcode': '27a2', 'reply_token': '27a2', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 15}},     # Speichervorrang auf Heizkreispumpe und Mischer
        'Frostschutzgrenze_A1M1':                   {'read': True,  'write': True,  'opcode': '27a3', 'reply_token': '27a3', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -9, 'force_max': 15}},     # Frostschutzgrenze
        'Frostschutz_A1M1':                         {'read': True,  'write': True,  'opcode': '27a4', 'reply_token': '27a4', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Frostschutzgrenze
        'Heizkreispumpenlogik_A1M1':                {'read': True,  'write': True,  'opcode': '27a5', 'reply_token': '27a5', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 15}},     # HeizkreispumpenlogikFunktion
        'Sparschaltung_A1M1':                       {'read': True,  'write': True,  'opcode': '27a6', 'reply_token': '27a6', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 5, 'force_max': 35}},     # AbsolutSommersparschaltung
        'Mischersparfunktion_A1M1':                 {'read': True,  'write': True,  'opcode': '27a7', 'reply_token': '27a7', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Mischersparfunktion
        'Pumpenstillstandzeit_A1M1':                {'read': True,  'write': True,  'opcode': '27a9', 'reply_token': '27a9', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 15}},     # Pumpenstillstandzeit
        'Vorlauftemperatur_min_A1M1':               {'read': True,  'write': True,  'opcode': '27c5', 'reply_token': '27c5', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 1, 'force_max': 127}},     # Minimalbegrenzung der Vorlauftemperatur
        'Vorlauftemperatur_max_A1M1':               {'read': True,  'write': True,  'opcode': '27c6', 'reply_token': '27c6', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 10, 'force_max': 127}},     # Maximalbegrenzung der Vorlauftemperatur
        'Neigung_Heizkennlinie_A1M1':               {'read': True,  'write': True,  'opcode': '27d3', 'reply_token': '27d3', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 1], 'settings': {'force_min': 0.2, 'force_max': 3.5}},     # Neigung Heizkennlinie A1M1
        'Niveau_Heizkennlinie_A1M1':                {'read': True,  'write': True,  'opcode': '27d4', 'reply_token': '27d4', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -13, 'force_max': 40}},     # Niveau Heizkennlinie A1M1
        'Partybetrieb_Zeitbegrenzung_A1M1':         {'read': True,  'write': True,  'opcode': '27f2', 'reply_token': '27f2', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 12}},     # Zeitliche Begrenzung für Partybetrieb oder externe BetriebsprogrammUmschaltung mit Taster
        'Temperaturgrenze_red_Betrieb_A1M1':        {'read': True,  'write': True,  'opcode': '27f8', 'reply_token': '27f8', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -61, 'force_max': 10}},     # Temperaturgrenze für Aufhebung des reduzierten Betriebs -5 ºC
        'Temperaturgrenze_red_Raumtemp_A1M1':       {'read': True,  'write': True,  'opcode': '27f9', 'reply_token': '27f9', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -60, 'force_max': 10}},     # Temperaturgrenze für Anhebung des reduzierten RaumtemperaturSollwertes
        'Vorlauftemperatur_Erhoehung_Soll_A1M1':    {'read': True,  'write': True,  'opcode': '27fa', 'reply_token': '27fa', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 50}},     # Erhöhung des Kesselwasser- bzw. Vorlauftemperatur-Sollwertes beim Übergang von Betrieb mit reduzierter Raumtemperatur in den Betrieb mit normaler Raumtemperatur um 20 %
        'Vorlauftemperatur_Erhoehung_Zeit_A1M1':    {'read': True,  'write': True,  'opcode': '27fa', 'reply_token': '27fa', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 150}},     # Zeitdauer für die Erhöhung des Kesselwasser bzw.VorlauftemperaturSollwertes (siehe Codieradresse „FA“) 60 min.
        # Heizkreis M2
        'Raumtemperatur_M2':                        {'read': True,  'write': False, 'opcode': '0898', 'reply_token': '0898', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1]},     # Raumtemperatur
        'Raumtemperatur_Soll_Normalbetrieb_M2':     {'read': True,  'write': True,  'opcode': '3306', 'reply_token': '3306', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 3, 'force_max': 37}},     # Raumtemperatur Soll Normalbetrieb
        'Raumtemperatur_Soll_Red_Betrieb_M2':       {'read': True,  'write': True,  'opcode': '3307', 'reply_token': '3307', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 3, 'force_max': 37}},     # Raumtemperatur Soll Reduzierter Betrieb
        'Raumtemperatur_Soll_Party_Betrieb_M2':     {'read': True,  'write': True,  'opcode': '3308', 'reply_token': '3308', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 3, 'force_max': 37}},     # Raumtemperatur Soll Party Betrieb
        'Aktuelle_Betriebsart_M2':                  {'read': True,  'write': False, 'opcode': '3301', 'reply_token': '3301', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'operatingmodes'},     # Aktuelle Betriebsart
        'Betriebsart_M2':                           {'read': True,  'write': True,  'opcode': '3323', 'reply_token': '3323', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 4}},     # Betriebsart
        'Sparbetrieb_M2':                           {'read': True,  'write': False, 'opcode': '3302', 'reply_token': '3302', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Sparbetrieb
        'Zustand_Sparbetrieb_M2':                   {'read': True,  'write': True,  'opcode': '3331', 'reply_token': '3331', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Zustand Sparbetrieb 
        'Partybetrieb_M2':                          {'read': True,  'write': False, 'opcode': '3303', 'reply_token': '3303', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Partybetrieb
        'Zustand_Partybetrieb_M2':                  {'read': True,  'write': True,  'opcode': '3330', 'reply_token': '3330', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Zustand Partybetrieb        
        'Vorlauftemperatur_M2':                     {'read': True,  'write': False, 'opcode': '3900', 'reply_token': '3900', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur
        'Vorlauftemperatur_Soll_M2':                {'read': True,  'write': False, 'opcode': '3544', 'reply_token': '3544', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur Soll
        'StatusFrost_M2':                           {'read': True,  'write': False, 'opcode': '3500', 'reply_token': '3500', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Status Frostwarnung
        'Externe_Raumsolltemperatur_Normal_M2':     {'read': True,  'write': True,  'opcode': '3321', 'reply_token': '3321', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 37}},     # Externe Raumsolltemperatur Normal
        'Externe_Betriebsartenumschaltung_M2':      {'read': True,  'write': True,  'opcode': '3549', 'reply_token': '3549', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 4}},     # Externe Betriebsartenumschaltung
        'Speichervorrang_M2':                       {'read': True,  'write': True,  'opcode': '37a2', 'reply_token': '37a2', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 15}},     # Speichervorrang auf Heizkreispumpe und Mischer
        'Frostschutzgrenze_M2':                     {'read': True,  'write': True,  'opcode': '37a3', 'reply_token': '37a3', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -9, 'force_max': 15}},     # Frostschutzgrenze
        'Frostschutz_M2':                           {'read': True,  'write': True,  'opcode': '37a4', 'reply_token': '37a4', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Frostschutzgrenze
        'Heizkreispumpenlogik_M2':                  {'read': True,  'write': True,  'opcode': '37a5', 'reply_token': '37a5', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 15}},     # HeizkreispumpenlogikFunktion
        'Sparschaltung_M2':                         {'read': True,  'write': True,  'opcode': '37a6', 'reply_token': '37a6', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 5, 'force_max': 35}},     # AbsolutSommersparschaltung
        'Mischersparfunktion_M2':                   {'read': True,  'write': True,  'opcode': '37a7', 'reply_token': '37a7', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Mischersparfunktion
        'Pumpenstillstandzeit_M2':                  {'read': True,  'write': True,  'opcode': '37a9', 'reply_token': '37a9', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 15}},     # Pumpenstillstandzeit
        'Vorlauftemperatur_min_M2':                 {'read': True,  'write': True,  'opcode': '37c5', 'reply_token': '37c5', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 1, 'force_max': 127}},     # Minimalbegrenzung der Vorlauftemperatur
        'Vorlauftemperatur_max_M2':                 {'read': True,  'write': True,  'opcode': '37c6', 'reply_token': '37c6', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 10, 'force_max': 127}},     # Maximalbegrenzung der Vorlauftemperatur
        'Neigung_Heizkennlinie_M2':                 {'read': True,  'write': True,  'opcode': '37d3', 'reply_token': '37d3', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 1], 'settings': {'force_min': 0.2, 'force_max': 3.5}},     # Neigung Heizkennlinie
        'Niveau_Heizkennlinie_M2':                  {'read': True,  'write': True,  'opcode': '37d4', 'reply_token': '37d4', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -13, 'force_max': 40}},     # Niveau Heizkennlinie
        'Partybetrieb_Zeitbegrenzung_M2':           {'read': True,  'write': True,  'opcode': '37f2', 'reply_token': '37f2', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 12}},     # Zeitliche Begrenzung für Partybetrieb oder externe BetriebsprogrammUmschaltung mit Taster
        'Temperaturgrenze_red_Betrieb_M2':          {'read': True,  'write': True,  'opcode': '37f8', 'reply_token': '37f8', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -61, 'force_max': 10}},     # Temperaturgrenze für Aufhebung des reduzierten Betriebs -5 ºC
        'Temperaturgrenze_red_Raumtemp_M2':         {'read': True,  'write': True,  'opcode': '37f9', 'reply_token': '37f9', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -60, 'force_max': 10}},     # Temperaturgrenze für Anhebung des reduzierten RaumtemperaturSollwertes
        'Vorlauftemperatur_Erhoehung_Soll_M2':      {'read': True,  'write': True,  'opcode': '37fa', 'reply_token': '37fa', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 50}},     # Erhöhung des Kesselwasser- bzw. Vorlauftemperatur-Sollwertes beim Übergang von Betrieb mit reduzierter Raumtemperatur in den Betrieb mit normaler Raumtemperatur um 20 %
        'Vorlauftemperatur_Erhoehung_Zeit_M2':      {'read': True,  'write': True,  'opcode': '37fb', 'reply_token': '37fb', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 150}},     # Zeitdauer für die Erhöhung des Kesselwasser bzw.VorlauftemperaturSollwertes (siehe Codieradresse „FA“) 60 min.
         # Warmwasser
        'Warmwasser_Temperatur':                    {'read': True,  'write': False, 'opcode': '0804', 'reply_token': '0804', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Warmwassertemperatur in Grad C
        'Warmwasser_Solltemperatur':                {'read': True,  'write': True,  'opcode': '6300', 'reply_token': '6300', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 10, 'force_max': 95}},     # Warmwasser-Solltemperatur
        'Status_Warmwasserbereitung':               {'read': True,  'write': True,  'opcode': '650a', 'reply_token': '650a', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Satus Warmwasserbereitung
        'WarmwasserPumpenNachlauf':                 {'read': True,  'write': True,  'opcode': '6762', 'reply_token': '6762', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 2], 'settings': {'force_min': 0, 'force_max': 1}},     # Warmwasserpumpennachlauf
        # Ferienprogramm HK_A1M1
        'Ferienprogramm_A1M1':                      {'read': True,  'write': False, 'opcode': '2535', 'reply_token': '2535', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Ferienprogramm A1M1
        'Ferien_Abreisetag_A1M1':                   {'read': True,  'write': True,  'opcode': '2309', 'reply_token': '2309', 'item_type': 'bool', 'dev_datatype': 'DA','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Ferien Abreisetag A1M1
        'Ferien_Rückreisetag_A1M1':                 {'read': True,  'write': True,  'opcode': '2311', 'reply_token': '2311', 'item_type': 'bool', 'dev_datatype': 'DA','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Ferien Rückreisetag A1M1
        # Ferienprogramm HK_M2              
        'Ferienprogramm_M2':                        {'read': True,  'write': False, 'opcode': '3535', 'reply_token': '3535', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Ferienprogramm M2
        'Ferien_Abreisetag_M2':                     {'read': True,  'write': True,  'opcode': '3309', 'reply_token': '3309', 'item_type': 'bool', 'dev_datatype': 'DA','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Ferien Abreisetag M2
        'Ferien_Rückreisetag_M2':                   {'read': True,  'write': True,  'opcode': '3311', 'reply_token': '3311', 'item_type': 'bool', 'dev_datatype': 'DA','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Ferien Rückreisetag M2
        # Schaltzeiten Warmwasser               
        'Timer_Warmwasser_Mo':                      {'read': True,  'write': True,  'opcode': '2100', 'reply_token': '2100', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Montag
        'Timer_Warmwasser_Di':                      {'read': True,  'write': True,  'opcode': '2108', 'reply_token': '2108', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Dienstag
        'Timer_Warmwasser_Mi':                      {'read': True,  'write': True,  'opcode': '2110', 'reply_token': '2110', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Mittwoch
        'Timer_Warmwasser_Do':                      {'read': True,  'write': True,  'opcode': '2118', 'reply_token': '2118', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Donnerstag
        'Timer_Warmwasser_Fr':                      {'read': True,  'write': True,  'opcode': '2120', 'reply_token': '2120', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Freitag
        'Timer_Warmwasser_Sa':                      {'read': True,  'write': True,  'opcode': '2128', 'reply_token': '2128', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Samstag
        'Timer_Warmwasser_So':                      {'read': True,  'write': True,  'opcode': '2130', 'reply_token': '2130', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Sonntag
        # Schaltzeiten HK_A1M1              
        'Timer_A1M1_Mo':                            {'read': True,  'write': True,  'opcode': '2000', 'reply_token': '2000', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Montag
        'Timer_A1M1_Di':                            {'read': True,  'write': True,  'opcode': '2008', 'reply_token': '2008', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Dienstag
        'Timer_A1M1_Mi':                            {'read': True,  'write': True,  'opcode': '2010', 'reply_token': '2010', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Mittwoch
        'Timer_A1M1_Do':                            {'read': True,  'write': True,  'opcode': '2018', 'reply_token': '2018', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Donnerstag
        'Timer_A1M1_Fr':                            {'read': True,  'write': True,  'opcode': '2020', 'reply_token': '2020', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Freitag
        'Timer_A1M1_Sa':                            {'read': True,  'write': True,  'opcode': '2028', 'reply_token': '2028', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Samstag
        'Timer_A1M1_So':                            {'read': True,  'write': True,  'opcode': '2030', 'reply_token': '2030', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Sonntag
        # Schaltzeiten HK_M2                
        'Timer_M2_Mo':                              {'read': True,  'write': True,  'opcode': '3000', 'reply_token': '3000', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Montag
        'Timer_M2_Di':                              {'read': True,  'write': True,  'opcode': '3008', 'reply_token': '3008', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Dienstag
        'Timer_M2_Mi':                              {'read': True,  'write': True,  'opcode': '3010', 'reply_token': '3010', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Mittwoch
        'Timer_M2_Do':                              {'read': True,  'write': True,  'opcode': '3018', 'reply_token': '3018', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Donnerstag
        'Timer_M2_Fr':                              {'read': True,  'write': True,  'opcode': '3020', 'reply_token': '3020', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Freitag
        'Timer_M2_Sa':                              {'read': True,  'write': True,  'opcode': '3028', 'reply_token': '3028', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Samstag
        'Timer_M2_So':                              {'read': True,  'write': True,  'opcode': '3030', 'reply_token': '3030', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Sonntag
        # Schaltzeiten Zirkulation              
        'Timer_Zirku_Mo':                           {'read': True,  'write': True,  'opcode': '2200', 'reply_token': '2200', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Zirkulationspumpe Montag
        'Timer_Zirku_Di':                           {'read': True,  'write': True,  'opcode': '2208', 'reply_token': '2208', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Zirkulationspumpe Dienstag
        'Timer_Zirku_Mi':                           {'read': True,  'write': True,  'opcode': '2210', 'reply_token': '2210', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Zirkulationspumpe Mittwoch
        'Timer_Zirku_Do':                           {'read': True,  'write': True,  'opcode': '2218', 'reply_token': '2218', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Zirkulationspumpe Donnerstag
        'Timer_Zirku_Fr':                           {'read': True,  'write': True,  'opcode': '2220', 'reply_token': '2220', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Zirkulationspumpe Freitag
        'Timer_Zirku_Sa':                           {'read': True,  'write': True,  'opcode': '2228', 'reply_token': '2228', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Zirkulationspumpe Samstag
        'Timer_Zirku_So':                           {'read': True,  'write': True,  'opcode': '2230', 'reply_token': '2230', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Zirkulationspumpe Sonntag
    },
    'V200HO1C': {
        # Allgemein
        'Anlagenschema':                        {'read': True,  'write': False, 'opcode': '7700', 'reply_token': '7700', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 2], 'lookup': 'systemschemes'},     # Anlagenschema
        'Frostgefahr':                          {'read': True,  'write': False, 'opcode': '2510', 'reply_token': '2510', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Frostgefahr
        'Aussentemperatur_TP':                  {'read': True,  'write': False, 'opcode': '5525', 'reply_token': '5525', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Aussentemperatur_tiefpass
        'Aussentemperatur_Dp':                  {'read': True,  'write': False, 'opcode': '5527', 'reply_token': '5527', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Aussentemperatur in Grad C (Gedaempft)
        'Anlagenleistung':                      {'read': True,  'write': False, 'opcode': 'a38f', 'reply_token': 'a38f', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Anlagenleistung
        # Kessel
        'Kesseltemperatur_TP':                  {'read': True,  'write': False, 'opcode': '0810', 'reply_token': '0810', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Kesseltemperatur_tiefpass
        'Kesselsolltemperatur':                 {'read': True,  'write': False, 'opcode': '555a', 'reply_token': '555a', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Kesselsolltemperatur
        'Abgastemperatur':                      {'read': True,  'write': False, 'opcode': '0816', 'reply_token': '0816', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Abgastemperatur
        # Fehler
        'Sammelstoerung':                       {'read': True,  'write': False, 'opcode': '0a82', 'reply_token': '0a82', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},     # Sammelstörung
        'Error0':                               {'read': True,  'write': False, 'opcode': '7507', 'reply_token': '7507', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 1
        'Error1':                               {'read': True,  'write': False, 'opcode': '7510', 'reply_token': '7510', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 2
        'Error2':                               {'read': True,  'write': False, 'opcode': '7519', 'reply_token': '7519', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 3
        'Error3':                               {'read': True,  'write': False, 'opcode': '7522', 'reply_token': '7522', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 4
        'Error4':                               {'read': True,  'write': False, 'opcode': '752b', 'reply_token': '752b', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 5
        'Error5':                               {'read': True,  'write': False, 'opcode': '7534', 'reply_token': '7534', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 6
        'Error6':                               {'read': True,  'write': False, 'opcode': '753d', 'reply_token': '753d', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 7
        'Error7':                               {'read': True,  'write': False, 'opcode': '7546', 'reply_token': '7546', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 8
        'Error8':                               {'read': True,  'write': False, 'opcode': '754f', 'reply_token': '754f', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 9
        'Error9':                               {'read': True,  'write': False, 'opcode': '7558', 'reply_token': '7558', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 10
        # Pumpen
        'Speicherladepumpe':                    {'read': True,  'write': False, 'opcode': '6513', 'reply_token': '6513', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Speicherladepumpe für Warmwasser
        'Zirkulationspumpe':                    {'read': True,  'write': True,  'opcode': '6515', 'reply_token': '6515', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Zirkulationspumpe
        'Interne_Pumpe':                        {'read': True,  'write': False, 'opcode': '7660', 'reply_token': '7660', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Interne Pumpe
        'Heizkreispumpe_HK1':                   {'read': True,  'write': False, 'opcode': '2906', 'reply_token': '2906', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Heizkreispumpe A1
        'Heizkreispumpe_HK2':                   {'read': True,  'write': False, 'opcode': '3906', 'reply_token': '3906', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Heizkreispumpe M2
        # Brenner
        'Brennerstarts':                        {'read': True,  'write': False, 'opcode': '088a', 'reply_token': '088a', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 4]},     # Brennerstarts
        'Brennerleistung':                      {'read': True,  'write': False, 'opcode': 'a305', 'reply_token': 'a305', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Brennerleistung
        'Brenner_Betriebsstunden':              {'read': True,  'write': False, 'opcode': '08a7', 'reply_token': '08a7', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4]},     # Brenner-Betriebsstunden
        # Solar
        'SolarPumpe':                           {'read': True,  'write': False, 'opcode': '6552', 'reply_token': '6552', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Solarpumpe
        'Kollektortemperatur':                  {'read': True,  'write': False, 'opcode': '6564', 'reply_token': '6564', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Kollektortemperatur
        'Speichertemperatur':                   {'read': True,  'write': False, 'opcode': '6566', 'reply_token': '6566', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Spichertemperatur
        'Solar_Betriebsstunden':                {'read': True,  'write': False, 'opcode': '6568', 'reply_token': '6568', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 100, 4]},     # Solar Betriebsstunden
        'Solar_Waermemenge':                    {'read': True,  'write': False, 'opcode': '6560', 'reply_token': '6560', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 2]},     # Solar Waermemenge
        'Solar_Ausbeute':                       {'read': True,  'write': False, 'opcode': 'cf30', 'reply_token': 'cf30', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # Solar Ausbeute
        # Heizkreis 1            
        'Betriebsart_HK1':                      {'read': True,  'write': True,  'opcode': '2500', 'reply_token': '2500', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 3}},     # Betriebsart (0=Abschaltbetrieb, 1=Red. Betrieb, 2=Normalbetrieb (Schaltuhr), 3=Normalbetrieb (Dauernd))
        'Heizart_HK1':                          {'read': True,  'write': True,  'opcode': '2323', 'reply_token': '2323', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 4}},     # Heizart     (0=Abschaltbetrieb, 1=Nur Warmwasser, 2=Heizen und Warmwasser, 3=Normalbetrieb (Reduziert), 4=Normalbetrieb (Dauernd))
        'Vorlauftemperatur_Soll_HK1':           {'read': True,  'write': False, 'opcode': '2544', 'reply_token': '2544', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur Soll
        'Vorlauftemperatur_HK1':                {'read': True,  'write': False, 'opcode': '2900', 'reply_token': '2900', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur Ist
        # Heizkreis 2            
        'Betriebsart_HK2':                      {'read': True,  'write': True,  'opcode': '3500', 'reply_token': '3500', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 3}},     # Betriebsart (0=Abschaltbetrieb, 1=Red. Betrieb, 2=Normalbetrieb (Schaltuhr), 3=Normalbetrieb (Dauernd))
        'Heizart_HK2':                          {'read': True,  'write': True,  'opcode': '3323', 'reply_token': '3323', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 4}},     # Heizart     (0=Abschaltbetrieb, 1=Nur Warmwasser, 2=Heizen und Warmwasser, 3=Normalbetrieb (Reduziert), 4=Normalbetrieb (Dauernd))
        'Vorlauftemperatur_Soll_HK2':           {'read': True,  'write': False, 'opcode': '3544', 'reply_token': '3544', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur Soll
        'Vorlauftemperatur_HK2':                {'read': True,  'write': False, 'opcode': '3900', 'reply_token': '3900', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur Ist
        # Warmwasser            
        'Warmwasser_Temperatur':                {'read': True,  'write': False, 'opcode': '0812', 'reply_token': '0812', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Warmwassertemperatur in Grad C
        'Warmwasser_Solltemperatur':            {'read': True,  'write': True,  'opcode': '6300', 'reply_token': '6300', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 10, 'force_max': 80}},     # Warmwasser-Solltemperatur
        'Warmwasser_Austrittstemperatur':       {'read': True,  'write': False, 'opcode': '0814', 'reply_token': '0814', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Warmwasseraustrittstemperatur in Grad C
    },
    'V200KW2': {
        # Allgemein
        'Anlagenschema':                            {'read': True,  'write': False, 'opcode': '7700', 'reply_token': '7700', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 2], 'lookup': 'systemschemes'},     # Anlagenschema
        'AnlagenSoftwareIndex':                     {'read': True,  'write': False, 'opcode': '7330', 'reply_token': '7330', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Bedienteil SoftwareIndex
        'Aussentemperatur':                         {'read': True,  'write': False, 'opcode': '0800', 'reply_token': '0800', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Aussentemperatur_tiefpass
        'Aussentemperatur_Dp':                      {'read': True,  'write': False, 'opcode': '5527', 'reply_token': '5527', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # Aussentemperatur in Grad C (Gedaempft)
        'Systemtime':                               {'read': True,  'write': True,  'opcode': '088e', 'reply_token': '088e', 'item_type': 'bool', 'dev_datatype': 'TI','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Systemzeit
        # Kessel            
        'TempKOffset':                              {'read': True,  'write': True,  'opcode': '6760', 'reply_token': '6760', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 10, 'force_max': 50}},     # Kesseloffset KT ueber WWsoll in Grad C
        'Kesseltemperatur':                         {'read': True,  'write': False, 'opcode': '0802', 'reply_token': '0802', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Kesseltemperatur
        'Kesselsolltemperatur':                     {'read': True,  'write': True,  'opcode': '5502', 'reply_token': '5502', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Kesselsolltemperatur
        # Fehler            
        'Sammelstoerung':                           {'read': True,  'write': False, 'opcode': '0847', 'reply_token': '0847', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},     # Sammelstörung
        'Brennerstoerung':                          {'read': True,  'write': False, 'opcode': '0883', 'reply_token': '0883', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},
        'Error0':                                   {'read': True,  'write': False, 'opcode': '7507', 'reply_token': '7507', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 1
        'Error1':                                   {'read': True,  'write': False, 'opcode': '7510', 'reply_token': '7510', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 2
        'Error2':                                   {'read': True,  'write': False, 'opcode': '7519', 'reply_token': '7519', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 3
        'Error3':                                   {'read': True,  'write': False, 'opcode': '7522', 'reply_token': '7522', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 4
        'Error4':                                   {'read': True,  'write': False, 'opcode': '752b', 'reply_token': '752b', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 5
        'Error5':                                   {'read': True,  'write': False, 'opcode': '7534', 'reply_token': '7534', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 6
        'Error6':                                   {'read': True,  'write': False, 'opcode': '753d', 'reply_token': '753d', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 7
        'Error7':                                   {'read': True,  'write': False, 'opcode': '7546', 'reply_token': '7546', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 8
        'Error8':                                   {'read': True,  'write': False, 'opcode': '754f', 'reply_token': '754f', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 9
        'Error9':                                   {'read': True,  'write': False, 'opcode': '7558', 'reply_token': '7558', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 9], 'lookup': 'errors'},     # Fehlerhistory Eintrag 10
        # Pumpen            
        'Speicherladepumpe':                        {'read': True,  'write': False, 'opcode': '0845', 'reply_token': '0845', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Speicherladepumpe für Warmwasser
        'Zirkulationspumpe':                        {'read': True,  'write': False, 'opcode': '0846', 'reply_token': '0846', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Zirkulationspumpe
        'Heizkreispumpe_A1M1':                      {'read': True,  'write': False, 'opcode': '2906', 'reply_token': '2906', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Heizkreispumpe A1M1
        'Heizkreispumpe_M2':                        {'read': True,  'write': False, 'opcode': '3906', 'reply_token': '3906', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Heizkreispumpe M2
        # Brenner            
        'Brennertyp':                               {'read': True,  'write': False, 'opcode': 'a30b', 'reply_token': 'a30b', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Brennertyp 0=einstufig 1=zweistufig 2=modulierend
        'Brennerstufe':                             {'read': True,  'write': False, 'opcode': '551e', 'reply_token': '551e', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},     # Ermittle die aktuelle Brennerstufe
        'Brennerstarts':                            {'read': True,  'write': True,  'opcode': '088a', 'reply_token': '088a', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 2], 'settings': {'force_min': 0, 'force_max': 1193045}},     # Brennerstarts
        'Brennerstatus_1':                          {'read': True,  'write': False, 'opcode': '55d3', 'reply_token': '55d3', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Brennerstatus Stufe1
        'Brennerstatus_2':                          {'read': True,  'write': False, 'opcode': '0849', 'reply_token': '0849', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Brennerstatus Stufe2
        'Brenner_BetriebsstundenStufe1':            {'read': True,  'write': True,  'opcode': '0886', 'reply_token': '0886', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4], 'settings': {'force_min': 0, 'force_max': 1193045}},     # Brenner-Betriebsstunden Stufe 1
        'Brenner_BetriebsstundenStufe2':            {'read': True,  'write': True,  'opcode': '08a3', 'reply_token': '08a3', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4], 'settings': {'force_min': 0, 'force_max': 1193045}},     # Brenner-Betriebsstunden Stufe 2
        # Heizkreis A1M1            
        'Betriebsart_A1M1':                         {'read': True,  'write': True,  'opcode': '2301', 'reply_token': '2301', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'operatingmodes'},     # Betriebsart A1M1
        'Aktuelle_Betriebsart_A1M1':                {'read': True,  'write': False, 'opcode': '2500', 'reply_token': '2500', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'operatingmodes'},     # Aktuelle Betriebsart A1M1
        'Sparbetrieb_A1M1':                         {'read': True,  'write': True,  'opcode': '2302', 'reply_token': '2302', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Sparbetrieb A1M1
        'Partybetrieb_A1M1_Zeit':                   {'read': True,  'write': True,  'opcode': '27f2', 'reply_token': '27f2', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 12}},     # Partyzeit M2
        'Partybetrieb_A1M1':                        {'read': True,  'write': True,  'opcode': '2303', 'reply_token': '2303', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Partybetrieb A1M1
        'Vorlauftemperatur_A1M1':                   {'read': True,  'write': False, 'opcode': '2900', 'reply_token': '2900', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur A1M1
        'Vorlauftemperatur_Soll_A1M1':              {'read': True,  'write': False, 'opcode': '2544', 'reply_token': '2544', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur Soll A1M1
        'Raumtemperatur_Soll_Normalbetrieb_A1M1':   {'read': True,  'write': True,  'opcode': '2306', 'reply_token': '2306', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 4, 'force_max': 37}},     # Raumtemperatur Soll Normalbetrieb A1M1
        'Raumtemperatur_Soll_Red_Betrieb_A1M1':     {'read': True,  'write': True,  'opcode': '2307', 'reply_token': '2307', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 4, 'force_max': 37}},     # Raumtemperatur Soll Reduzierter Betrieb A1M1
        'Raumtemperatur_Soll_Party_Betrieb_A1M1':   {'read': True,  'write': True,  'opcode': '2308', 'reply_token': '2308', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 4, 'force_max': 37}},     # Raumtemperatur Soll Party Betrieb A1M1
        'Neigung_Heizkennlinie_A1M1':               {'read': True,  'write': True,  'opcode': '2305', 'reply_token': '2305', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 1], 'settings': {'force_min': 0.2, 'force_max': 3.5}},     # Neigung Heizkennlinie A1M1
        'Niveau_Heizkennlinie_A1M1':                {'read': True,  'write': True,  'opcode': '2304', 'reply_token': '2304', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -13, 'force_max': 40}},     # Niveau Heizkennlinie A1M1
        'MischerM1':                                {'read': True,  'write': False, 'opcode': '254c', 'reply_token': '254c', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 2.55, 1]},     # Ermittle Mischerposition M1
        'Heizkreispumpenlogik_A1M1':                {'read': True,  'write': True,  'opcode': '27a5', 'reply_token': '27a5', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 15}},     # 0=ohne HPL-Funktion, 1=AT > RTsoll + 5 K, 2=AT > RTsoll + 4 K, 3=AT > RTsoll + 3 K, 4=AT > RTsoll + 2 K, 5=AT > RTsoll + 1 K, 6=AT > RTsoll, 7=AT > RTsoll - 1 K, 8=AT > RTsoll - 2 K, 9=AT > RTsoll - 3 K, 10=AT > RTsoll - 4 K, 11=AT > RTsoll - 5 K, 12=AT > RTsoll - 6 K, 13=AT > RTsoll - 7 K, 14=AT > RTsoll - 8 K, 15=AT > RTsoll - 9 K
        'Sparschaltung_A1M1':                       {'read': True,  'write': True,  'opcode': '27a6', 'reply_token': '27a6', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 5, 'force_max': 36}},     # AbsolutSommersparschaltung
        # Heizkreis M2            
        'Betriebsart_M2':                           {'read': True,  'write': True,  'opcode': '3301', 'reply_token': '3301', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'operatingmodes'},     # Betriebsart M2
        'Aktuelle_Betriebsart_M2':                  {'read': True,  'write': False, 'opcode': '3500', 'reply_token': '3500', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'operatingmodes'},     # Aktuelle Betriebsart M2
        'Sparbetrieb_M2':                           {'read': True,  'write': True,  'opcode': '3302', 'reply_token': '3302', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Sparbetrieb
        'Partybetrieb_M2':                          {'read': True,  'write': True,  'opcode': '3303', 'reply_token': '3303', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # Partybetrieb A1M1
        'Partybetrieb_M2_Zeit':                     {'read': True,  'write': True,  'opcode': '37f2', 'reply_token': '37f2', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 12}},     # Partyzeit M2
        'Raumtemperatur_Soll_Normalbetrieb_M2':     {'read': True,  'write': True,  'opcode': '3306', 'reply_token': '3306', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 4, 'force_max': 37}},     # Raumtemperatur Soll Normalbetrieb
        'Raumtemperatur_Soll_Red_Betrieb_M2':       {'read': True,  'write': True,  'opcode': '3307', 'reply_token': '3307', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 4, 'force_max': 37}},     # Raumtemperatur Soll Reduzierter Betrieb
        'Raumtemperatur_Soll_Party_Betrieb_M2':     {'read': True,  'write': True,  'opcode': '3308', 'reply_token': '3308', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 4, 'force_max': 37}},     # Raumtemperatur Soll Party Betrieb
        'Neigung_Heizkennlinie_M2':                 {'read': True,  'write': True,  'opcode': '3305', 'reply_token': '3305', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 1], 'settings': {'force_min': 0.2, 'force_max': 3.5}},     # Neigung Heizkennlinie M2
        'Niveau_Heizkennlinie_M2':                  {'read': True,  'write': True,  'opcode': '3304', 'reply_token': '3304', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': -13, 'force_max': 40}},     # Niveau Heizkennlinie M2
        'MischerM2':                                {'read': True,  'write': False, 'opcode': '354c', 'reply_token': '354c', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 2.55, 1]},     # Ermittle Mischerposition M2
        'MischerM2Auf':                             {'read': True,  'write': True,  'opcode': '084d', 'reply_token': '084d', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # MischerM2 Auf 0=AUS;1=EIN
        'MischerM2Zu':                              {'read': True,  'write': True,  'opcode': '084c', 'reply_token': '084c', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 1}},     # MischerM2 Zu 0=AUS;1=EIN
        'Vorlauftemperatur_Soll_M2':                {'read': True,  'write': True,  'opcode': '37c6', 'reply_token': '37c6', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2], 'settings': {'force_min': 10, 'force_max': 80}},     # Vorlauftemperatur Soll
        'Vorlauftemperatur_M2':                     {'read': True,  'write': False, 'opcode': '080c', 'reply_token': '080c', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Vorlauftemperatur Ist
        'Vorlauftemperatur_min_M2':                 {'read': True,  'write': True,  'opcode': '37c5', 'reply_token': '37c5', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 1, 'force_max': 127}},     # Minimalbegrenzung der Vorlauftemperatur
        'Vorlauftemperatur_max_M2':                 {'read': True,  'write': True,  'opcode': '37c6', 'reply_token': '37c6', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 1, 'force_max': 127}},     # Maximalbegrenzung der Vorlauftemperatur
        'Heizkreispumpenlogik_M2':                  {'read': True,  'write': True,  'opcode': '37a5', 'reply_token': '37a5', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 0, 'force_max': 15}},     # 0=ohne HPL-Funktion, 1=AT > RTsoll + 5 K, 2=AT > RTsoll + 4 K, 3=AT > RTsoll + 3 K, 4=AT > RTsoll + 2 K, 5=AT > RTsoll + 1 K, 6=AT > RTsoll, 7=AT > RTsoll - 1 K, 8=AT > RTsoll - 2 K, 9=AT > RTsoll - 3 K, 10=AT > RTsoll - 4 K, 11=AT > RTsoll - 5 K, 12=AT > RTsoll - 6 K, 13=AT > RTsoll - 7 K, 14=AT > RTsoll - 8 K, 15=AT > RTsoll - 9 K
        'Sparschaltung_M2':                         {'read': True,  'write': True,  'opcode': '37a6', 'reply_token': '37a6', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 5, 'force_max': 36}},     # AbsolutSommersparschaltung
        'StatusKlemme2':                            {'read': True,  'write': False, 'opcode': '3904', 'reply_token': '3904', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # 0=OK, 1=Kurzschluss, 2=nicht vorhanden, 3-5=Referenzfehler, 6=nicht vorhanden
        'StatusKlemme17':                           {'read': True,  'write': False, 'opcode': '3905', 'reply_token': '3905', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # 0=OK, 1=Kurzschluss, 2=nicht vorhanden, 3-5=Referenzfehler, 6=nicht vorhanden
        # Warmwasser            
        'Warmwasser_Status':                        {'read': True,  'write': False, 'opcode': '650A', 'reply_token': '650A', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # 0=Ladung inaktiv, 1=in Ladung, 2=im Nachlauf
        'Warmwasser_KesselOffset':                  {'read': True,  'write': True,  'opcode': '6760', 'reply_token': '6760', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 10, 'force_max': 50}},     # Warmwasser Kessel Offset in K
        'Warmwasser_BeiPartyDNormal':               {'read': True,  'write': True,  'opcode': '6764', 'reply_token': '6764', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 2}},     # WW Heizen bei Party 0=AUS, 1=nach Schaltuhr, 2=EIN
        'Warmwasser_Temperatur':                    {'read': True,  'write': False, 'opcode': '0804', 'reply_token': '0804', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 2]},     # Warmwassertemperatur in Grad C
        'Warmwasser_Solltemperatur':                {'read': True,  'write': True,  'opcode': '6300', 'reply_token': '6300', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'signed', 'len'], 'param_values': ['VAL', True, 1], 'settings': {'force_min': 10, 'force_max': 80}},     # Warmwasser-Solltemperatur
        'Warmwasser_SolltemperaturAktuell':         {'read': True,  'write': False, 'opcode': '6500', 'reply_token': '6500', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 1]},      # Warmwasser-Solltemperatur aktuell
        'Warmwasser_SollwertMax':                   {'read': True,  'write': False, 'opcode': '675a', 'reply_token': '675a', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # 0=inaktiv, 1=aktiv
        # Ferienprogramm HK_A1M1            
        'Ferienprogramm_A1M1':                      {'read': True,  'write': False, 'opcode': '2535', 'reply_token': '2535', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Ferienprogramm A1M1 0=inaktiv 1=aktiv
        'Ferien_Abreisetag_A1M1':                   {'read': True,  'write': True,  'opcode': '2309', 'reply_token': '2309', 'item_type': 'bool', 'dev_datatype': 'DA','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Ferien Abreisetag A1M1
        'Ferien_Rückreisetag_A1M1':                 {'read': True,  'write': True,  'opcode': '2311', 'reply_token': '2311', 'item_type': 'bool', 'dev_datatype': 'DA','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Ferien Rückreisetag A1M1
        # Ferienprogramm HK_M2            
        'Ferienprogramm_M2':                        {'read': True,  'write': False, 'opcode': '3535', 'reply_token': '3535', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # Ferienprogramm M2 0=inaktiv 1=aktiv
        'Ferien_Abreisetag_M2':                     {'read': True,  'write': True,  'opcode': '3309', 'reply_token': '3309', 'item_type': 'bool', 'dev_datatype': 'DA','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Ferien Abreisetag M2
        'Ferien_Rückreisetag_M2':                   {'read': True,  'write': True,  'opcode': '3311', 'reply_token': '3311', 'item_type': 'bool', 'dev_datatype': 'DA','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Ferien Rückreisetag M2
        # Schaltzeiten Warmwasser            
        'Timer_Warmwasser_Mo':                      {'read': True,  'write': True,  'opcode': '2100', 'reply_token': '2100', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Montag
        'Timer_Warmwasser_Di':                      {'read': True,  'write': True,  'opcode': '2108', 'reply_token': '2108', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Dienstag
        'Timer_Warmwasser_Mi':                      {'read': True,  'write': True,  'opcode': '2110', 'reply_token': '2110', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Mittwoch
        'Timer_Warmwasser_Do':                      {'read': True,  'write': True,  'opcode': '2118', 'reply_token': '2118', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Donnerstag
        'Timer_Warmwasser_Fr':                      {'read': True,  'write': True,  'opcode': '2120', 'reply_token': '2120', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Freitag
        'Timer_Warmwasser_Sa':                      {'read': True,  'write': True,  'opcode': '2128', 'reply_token': '2128', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Samstag
        'Timer_Warmwasser_So':                      {'read': True,  'write': True,  'opcode': '2130', 'reply_token': '2130', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Warmwasserbereitung Sonntag
        # Schaltzeiten HK_A1M1            
        'Timer_A1M1_Mo':                            {'read': True,  'write': True,  'opcode': '2000', 'reply_token': '2000', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Montag
        'Timer_A1M1_Di':                            {'read': True,  'write': True,  'opcode': '2008', 'reply_token': '2008', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Dienstag
        'Timer_A1M1_Mi':                            {'read': True,  'write': True,  'opcode': '2010', 'reply_token': '2010', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Mittwoch
        'Timer_A1M1_Do':                            {'read': True,  'write': True,  'opcode': '2018', 'reply_token': '2018', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Donnerstag
        'Timer_A1M1_Fr':                            {'read': True,  'write': True,  'opcode': '2020', 'reply_token': '2020', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Freitag
        'Timer_A1M1_Sa':                            {'read': True,  'write': True,  'opcode': '2028', 'reply_token': '2028', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Samstag
        'Timer_A1M1_So':                            {'read': True,  'write': True,  'opcode': '2030', 'reply_token': '2030', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Sonntag
        # Schaltzeiten HK_M2            
        'Timer_M2_Mo':                              {'read': True,  'write': True,  'opcode': '3000', 'reply_token': '3000', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Montag
        'Timer_M2_Di':                              {'read': True,  'write': True,  'opcode': '3008', 'reply_token': '3008', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Dienstag
        'Timer_M2_Mi':                              {'read': True,  'write': True,  'opcode': '3010', 'reply_token': '3010', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Mittwoch
        'Timer_M2_Do':                              {'read': True,  'write': True,  'opcode': '3018', 'reply_token': '3018', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Donnerstag
        'Timer_M2_Fr':                              {'read': True,  'write': True,  'opcode': '3020', 'reply_token': '3020', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Freitag
        'Timer_M2_Sa':                              {'read': True,  'write': True,  'opcode': '3028', 'reply_token': '3028', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Samstag
        'Timer_M2_So':                              {'read': True,  'write': True,  'opcode': '3030', 'reply_token': '3030', 'item_type': 'list', 'dev_datatype': 'CT','params': ['value', 'len'], 'param_values': ['VAL', 8]},     # Timer Heizkreis_A1M1 Sonntag
    },
    'V200WO1C': {
        # generelle Infos
        'Aussentemperatur':         {'read': True,  'write': False, 'opcode': '0101', 'reply_token': '0101', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempA -- Information - Allgemein: Aussentemperatur (-40..70)
        # Anlagenstatus            
        'Betriebsart':              {'read': True,  'write': True,  'opcode': 'b000', 'reply_token': 'b000', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'operatingmodes'},     # getBetriebsart -- Bedienung HK1 - Heizkreis 1: Betriebsart (Textstring)
        'Manuell':                  {'read': True,  'write': True,  'opcode': 'b020', 'reply_token': 'b020', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'settings': {'force_min': 0, 'force_max': 2}},     # getManuell / setManuell -- 0 = normal, 1 = manueller Heizbetrieb, 2 = 1x Warmwasser auf Temp2
        'Sekundaerpumpe':           {'read': True,  'write': False, 'opcode': '0484', 'reply_token': '0484', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},     # getStatusSekP -- Diagnose - Anlagenuebersicht: Sekundaerpumpe 1 (0..1)
        'Heizkreispumpe':           {'read': True,  'write': False, 'opcode': '048d', 'reply_token': '048d', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},     # getStatusPumpe -- Information - Heizkreis HK1: Heizkreispumpe (0..1)
        'Zirkulationspumpe':        {'read': True,  'write': False, 'opcode': '0490', 'reply_token': '0490', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},     # getStatusPumpeZirk -- Information - Warmwasser: Zirkulationspumpe (0..1)
        'VentilHeizenWW':           {'read': True,  'write': False, 'opcode': '0494', 'reply_token': '0494', 'item_type': 'bool', 'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1], 'lookup': 'returnstatus'},     # getStatusVentilWW -- Diagnose - Waermepumpe: 3-W-Ventil Heizen WW1 (0 (Heizen)..1 (WW))
        'Vorlaufsolltemp':          {'read': True,  'write': False, 'opcode': '1800', 'reply_token': '1800', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempVLSoll -- Diagnose - Heizkreis HK1: Vorlaufsolltemperatur HK1 (0..95)
        'Outdoor_Fanspeed':         {'read': True,  'write': False, 'opcode': '1a52', 'reply_token': '1a52', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getSpdFanOut -- Outdoor Fanspeed
        'Status_Fanspeed':          {'read': True,  'write': False, 'opcode': '1a53', 'reply_token': '1a53', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getSpdFan -- Geschwindigkeit Luefter
        'Kompressor_Freq':          {'read': True,  'write': False, 'opcode': '1a54', 'reply_token': '1a54', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getSpdKomp -- Compressor Frequency
        # Temperaturen            
        'SolltempWarmwasser':       {'read': True,  'write': True,  'opcode': '6000', 'reply_token': '6000', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2], 'settings': {'force_min': 10, 'force_max': 60}},     # getTempWWSoll -- Bedienung WW - Betriebsdaten WW: Warmwassersolltemperatur (10..60 (95))
        'VorlauftempSek':           {'read': True,  'write': False, 'opcode': '0105', 'reply_token': '0105', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempSekVL -- Information - Heizkreis HK1: Vorlauftemperatur Sekundaer 1 (0..95)
        'RuecklauftempSek':         {'read': True,  'write': False, 'opcode': '0106', 'reply_token': '0106', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempSekRL -- Diagnose - Anlagenuebersicht: Ruecklauftemperatur Sekundaer 1 (0..95)
        'Warmwassertemperatur':     {'read': True,  'write': False, 'opcode': '010d', 'reply_token': '010d', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempWWIstOben -- Information - Warmwasser: Warmwassertemperatur oben (0..95)
        # Stellwerte            
        'Raumsolltemp':             {'read': True,  'write': False, 'opcode': '2000', 'reply_token': '2000', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempRaumSollNormal -- Bedienung HK1 - Heizkreis 1: Raumsolltemperatur normal (10..30)
        'RaumsolltempReduziert':    {'read': True,  'write': False, 'opcode': '2001', 'reply_token': '2001', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempRaumSollRed -- Bedienung HK1 - Heizkreis 1: Raumsolltemperatur reduzierter Betrieb (10..30)
        'HeizkennlinieNiveau':      {'read': True,  'write': False, 'opcode': '2006', 'reply_token': '2006', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getHKLNiveau -- Bedienung HK1 - Heizkreis 1: Niveau der Heizkennlinie (-15..40)
        'HeizkennlinieNeigung':     {'read': True,  'write': False, 'opcode': '2007', 'reply_token': '2007', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getHKLNeigung -- Bedienung HK1 - Heizkreis 1: Neigung der Heizkennlinie (0..35)
        'RaumsolltempParty':        {'read': True,  'write': False, 'opcode': '2022', 'reply_token': '2022', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempRaumSollParty -- Bedienung HK1 - Heizkreis 1: Party Solltemperatur (10..30)
        # Statistiken / Laufzeiten            
        'EinschaltungenSekundaer':  {'read': True,  'write': False, 'opcode': '0504', 'reply_token': '0504', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getAnzQuelleSek -- Statistik - Schaltzyklen Anlage: Einschaltungen Sekundaerquelle (?)
        'EinschaltungenHeizstab1':  {'read': True,  'write': False, 'opcode': '0508', 'reply_token': '0508', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getAnzHeizstabSt1 -- Statistik - Schaltzyklen Anlage: Einschaltungen Heizstab Stufe 1 (?)
        'EinschaltungenHeizstab2':  {'read': True,  'write': False, 'opcode': '0509', 'reply_token': '0509', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getAnzHeizstabSt2 -- Statistik - Schaltzyklen Anlage: Einschaltungen Heizstab Stufe 2 (?)
        'EinschaltungenHK':         {'read': True,  'write': False, 'opcode': '050d', 'reply_token': '050d', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getAnzHK -- Statistik - Schaltzyklen Anlage: Einschaltungen Heizkreis (?)
        'LZSekundaerpumpe':         {'read': True,  'write': False, 'opcode': '0584', 'reply_token': '0584', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4]},     # getLZPumpeSek -- Statistik - Betriebsstunden Anlage: Betriebsstunden Sekundaerpumpe (?)
        'LZHeizstab1':              {'read': True,  'write': False, 'opcode': '0588', 'reply_token': '0588', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4]},     # getLZHeizstabSt1 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Heizstab Stufe 1 (?)
        'LZHeizstab2':              {'read': True,  'write': False, 'opcode': '0589', 'reply_token': '0589', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4]},     # getLZHeizstabSt2 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Heizstab Stufe 2 (?)
        'LZPumpeHK':                {'read': True,  'write': False, 'opcode': '058d', 'reply_token': '058d', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4]},     # getLZPumpe -- Statistik - Betriebsstunden Anlage: Betriebsstunden Pumpe HK1 (0..1150000)
        'LZWWVentil':               {'read': True,  'write': False, 'opcode': '0594', 'reply_token': '0594', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4]},     # getLZVentilWW -- Statistik - Betriebsstunden Anlage: Betriebsstunden Warmwasserventil (?)
        'LZVerdichterStufe1':       {'read': True,  'write': False, 'opcode': '1620', 'reply_token': '1620', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getLZVerdSt1 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 1 (?)
        'LZVerdichterStufe2':       {'read': True,  'write': False, 'opcode': '1622', 'reply_token': '1622', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getLZVerdSt2 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 2 (?)
        'LZVerdichterStufe3':       {'read': True,  'write': False, 'opcode': '1624', 'reply_token': '1624', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getLZVerdSt3 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 3 (?)
        'LZVerdichterStufe4':       {'read': True,  'write': False, 'opcode': '1626', 'reply_token': '1626', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getLZVerdSt4 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 4 (?)
        'LZVerdichterStufe5':       {'read': True,  'write': False, 'opcode': '1628', 'reply_token': '1628', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 4]},     # getLZVerdSt5 -- Statistik - Betriebsstunden Anlage: Betriebsstunden Verdichter auf Stufe 5 (?)
        'VorlauftempSekMittel':     {'read': True,  'write': False, 'opcode': '16b2', 'reply_token': '16b2', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempSekVLMittel -- Statistik - Energiebilanz: mittlere sek. Vorlauftemperatur (0..95)
        'RuecklauftempSekMittel':   {'read': True,  'write': False, 'opcode': '16b3', 'reply_token': '16b3', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'signed', 'len'], 'param_values': ['VAL', 10, True, 2]},     # getTempSekRLMittel -- Statistik - Energiebilanz: mittlere sek.Temperatur RL1 (0..95)
        'OAT_Temperature':          {'read': True,  'write': False, 'opcode': '1a5c', 'reply_token': '1a5c', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getTempOAT -- OAT Temperature
        'ICT_Temperature':          {'read': True,  'write': False, 'opcode': '1a5d', 'reply_token': '1a5d', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getTempICT -- OCT Temperature
        'CCT_Temperature':          {'read': True,  'write': False, 'opcode': '1a5e', 'reply_token': '1a5e', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getTempCCT -- CCT Temperature
        'HST_Temperature':          {'read': True,  'write': False, 'opcode': '1a5f', 'reply_token': '1a5f', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getTempHST -- HST Temperature
        'OMT_Temperature':          {'read': True,  'write': False, 'opcode': '1a60', 'reply_token': '1a60', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getTempOMT -- OMT Temperature
        'LZVerdichterWP':           {'read': True,  'write': False, 'opcode': '5005', 'reply_token': '5005', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 3600, 4]},     # getLZWP -- Statistik - Betriebsstunden Anlage: Betriebsstunden Waermepumpe  (0..1150000)
        'SollLeistungVerdichter':   {'read': True,  'write': False, 'opcode': '5030', 'reply_token': '5030', 'item_type': 'int',  'dev_datatype': 'V', 'params': ['value', 'len'], 'param_values': ['VAL', 1]},     # getPwrSollVerdichter -- Diagnose - Anlagenuebersicht: Soll-Leistung Verdichter 1 (0..100)
        'WaermeWW12M':              {'read': True,  'write': False, 'opcode': '1660', 'reply_token': '1660', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 4]},     # Wärmeenergie für WW-Bereitung der letzten 12 Monate (kWh)
        'ElektroWW12M':             {'read': True,  'write': False, 'opcode': '1670', 'reply_token': '1670', 'item_type': 'num',  'dev_datatype': 'V', 'params': ['value', 'mult', 'len'], 'param_values': ['VAL', 10, 4]},     # elektr. Energie für WW-Bereitung der letzten 12 Monate (kWh)
    }
}

lookups = {
    'ALL': {
        'devicetypes': {
            '2098': 'V200KW2',   # Protokoll: KW
            '2053': 'GWG_VBEM',  # Protokoll: GWG
            '20CB': 'VScotHO1',  # Protokoll: P300
            '2094': 'V200KW1',   # Protokoll: KW
            '209F': 'V200KO1B',  # Protokoll: P300
            '204D': 'V200WO1C',  # Protokoll: P300
            '20B8': 'V333MW1',
            '20A0': 'V100GC1',
            '20C2': 'VDensHO1',
            '20A4': 'V200GW1',
            '20C8': 'VPlusHO1',
            '2046': 'V200WO1',
            '2047': 'V200WO1',
            '2049': 'V200WO1',
            '2032': 'VBC550',
            '2033': 'VBC550'
        },
        'errors': {
            '00': 'Regelbetrieb (kein Fehler)',
            '0F': 'Wartung (fuer Reset Codieradresse 24 auf 0 stellen)',
            '10': 'Kurzschluss Aussentemperatursensor',
            '18': 'Unterbrechung Aussentemperatursensor',
            '19': 'Unterbrechung Kommunikation Aussentemperatursensor RF',
            '1D': 'Keine Kommunikation mit Sensor',
            '1E': 'Strömungssensor defekt',
            '1F': 'Strömungssensor defekt',
            '20': 'Kurzschluss Vorlauftemperatursensor',
            '21': 'Kurzschluss Ruecklauftemperatursensor',
            '28': 'Unterbrechung Aussentemperatursensor / Vorlauftemperatursensor Anlage',
            '29': 'Unterbrechung Ruecklauftemperatursensor',
            '30': 'Kurzschluss Kesseltemperatursensor',
            '38': 'Unterbrechung Kesseltemperatursensor',
            '40': 'Kurzschluss Vorlauftemperatursensor M2',
            '42': 'Unterbrechung Vorlauftemperatursensor M2',
            '44': 'Kurzschluss Vorlauftemperatursensor Heizkreis 3',
            '48': 'Unterbrechung Vorlauftemperatursensor Heizkreis 3',
            '50': 'Kurzschluss Speichertemperatursensor',
            '51': 'Kurzschluss Auslauftemperatursensor',
            '58': 'Unterbrechung Speichertemperatursensor',
            '59': 'Unterbrechung Auslauftemperatursensor',
            '92': 'Solar: Kurzschluss Kollektortemperatursensor',
            '93': 'Solar: Kurzschluss Sensor S3',
            '94': 'Solar: Kurzschluss Speichertemperatursensor',
            '9A': 'Solar: Unterbrechung Kollektortemperatursensor',
            '9B': 'Solar: Unterbrechung Sensor S3',
            '9C': 'Solar: Unterbrechung Speichertemperatursensor',
            '9E': 'Solar: Zu geringer bzw. kein Volumenstrom oder Temperaturwächter ausgeloest',
            '9F': 'Solar: Fehlermeldung Solarteil (siehe Solarregler)',
            'A4': 'Amx. Anlagendruck überschritten',
            'A7': 'Bedienteil defekt',
            'A8': 'Luft in der internen Umwaelzpumpe oder Mindest-Volumenstrom nicht erreicht',
            'B0': 'Kurzschluss Abgastemperatursensor',
            'B1': 'Kommunikationsfehler Bedieneinheit',
            'B4': 'Interner Fehler (Elektronik)',
            'B5': 'Interner Fehler (Elektronik)',
            'B6': 'Ungueltige Hardwarekennung (Elektronik)',
            'B7': 'Interner Fehler (Kesselkodierstecker)',
            'B8': 'Unterbrechung Abgastemperatursensor',
            'B9': 'Interner Fehler (Dateneingabe wiederholen)',
            'V': 'Kommunikationsfehler Erweiterungssatz fuer Mischerkreis M2',
            'BB': 'Kommunikationsfehler Erweiterungssatz fuer Mischerkreis 3',
            'BC': 'Kommunikationsfehler Fernbedienung Vitorol, Heizkreis M1',
            'BD': 'Kommunikationsfehler Fernbedienung Vitorol, Heizkreis M2',
            'BE': 'Falsche Codierung Fernbedienung Vitorol',
            'BF': 'Falsches Kommunikationsmodul LON',
            'C1': 'Externe Sicherheitseinrichtung (Kessel kuehlt aus)',
            'C2': 'Kommunikationsfehler Solarregelung',
            'C3': 'Kommunikationsfehler Erweiterung AM1',
            'C4': 'Kommunikationsfehler Erweiterumg Open Therm',
            'C5': 'Kommunikationsfehler drehzahlgeregelte Heizkreispumpe, Heizkreis M1',
            'C6': 'Kommunikationsfehler drehzahlgeregelte Heizkreispumpe, Heizkreis M2',
            'C7': 'Falsche Codierung der Heizkreispumpe',
            'C8': 'Kommunikationsfehler drehzahlgeregelte, externe Heizkreispumpe 3',
            'C9': 'Stoermeldeeingang am Schaltmodul-V aktiv',
            'CD': 'Kommunikationsfehler Vitocom 100 (KM-BUS)',
            'CE': 'Kommunikationsfehler Schaltmodul-V',
            'CF': 'Kommunikationsfehler LON Modul',
            'D1': 'Brennerstoerung',
            'D4': 'Sicherheitstemperaturbegrenzer hat ausgeloest oder Stoermeldemodul nicht richtig gesteckt',
            'D6': 'Eingang DE1 an Erweiterung EA1 meldet eine Stoerung',
            'D7': 'Eingang DE2 an Erweiterung EA1 meldet eine Stoerung',
            'D8': 'Eingang DE3 an Erweiterung EA1 meldet eine Stoerung',
            'DA': 'Kurzschluss Raumtemperatursensor, Heizkreis M1',
            'DB': 'Kurzschluss Raumtemperatursensor, Heizkreis M2',
            'DC': 'Kurzschluss Raumtemperatursensor, Heizkreis 3',
            'DD': 'Unterbrechung Raumtemperatursensor, Heizkreis M1',
            'DE': 'Unterbrechung Raumtemperatursensor, Heizkreis M2',
            'DF': 'Unterbrechung Raumtemperatursensor, Heizkreis 3',
            'E0': 'Fehler externer LON Teilnehmer',
            'E1': 'Isolationsstrom waehrend des Kalibrierens zu hoch',
            'E3': 'Zu geringe Wärmeabnahme während des Kalibrierens, Temperaturwächter hat ausgeschaltet',
            'E4': 'Fehler Versorgungsspannung',
            'E5': 'Interner Fehler, Flammenverstärker(Ionisationselektrode)',
            'E6': 'Abgas- / Zuluftsystem verstopft, Anlagendruck zu niedrig',
            'E7': 'Ionisationsstrom waehrend des Kalibrierens zu gering',
            'E8': 'Ionisationsstrom nicht im gültigen Bereich',
            'EA': 'Ionisationsstrom waehrend des Kalibrierens nicht im gueltigen Bereich',
            'EB': 'Wiederholter Flammenverlust waehrend des Kalibrierens',
            'EC': 'Parameterfehler waehrend des Kalibrierens',
            'ED': 'Interner Fehler',
            'EE': 'Flammensignal ist bei Brennerstart nicht vorhanden oder zu gering',
            'EF': 'Flammenverlust direkt nach Flammenbildung (waehrend der Sicherheitszeit)',
            'F0': 'Interner Fehler (Regelung tauschen)',
            'F1': 'Abgastemperaturbegrenzer ausgeloest',
            'F2': 'Temperaturbegrenzer ausgeloest',
            'F3': 'Flammensigal beim Brennerstart bereits vorhanden',
            'F4': 'Flammensigal nicht vorhanden',
            'F7': 'Differenzdrucksensor defekt, Kurzschluss ider Wasserdrucksensor',
            'F8': 'Brennstoffventil schliesst zu spaet',
            'F9': 'Geblaesedrehzahl beim Brennerstart zu niedrig',
            'FA': 'Geblaesestillstand nicht erreicht',
            'FC': 'Gaskombiregler defekt oder fehlerhafte Ansteuerung Modulationsventil oder Abgasweg versperrt',
            'FD': 'Fehler Gasfeuerungsautomat, Kesselkodierstecker fehlt(in Verbindung mit B7)',
            'FE': 'Starkes Stoerfeld (EMV) in der Naehe oder Elektronik defekt',
            'FF': 'Starkes Stoerfeld (EMV) in der Naehe oder interner Fehler'
        },
        'operatingmodes': {
            '00': 'Abschaltbetrieb',
            '01': 'Reduzierter Betrieb',
            '02': 'Normalbetrieb',
            '03': 'Dauernd Normalbetrieb'
        },
        'returnstatus': {
            '00': '0',
            '01': '1',
            '03': '2',
            'AA': 'NOT OK',
        },
        'setreturnstatus': {
            '00': 'OK',
            '05': 'SYNC (NOT OK)',
        }
    },
    'V200KW2': {
        'operatingmodes': {
            '00': 'Warmwasser (Schaltzeiten)',
            '01': 'reduziert Heizen (dauernd)',
            '02': 'normal Heizen (dauernd)',
            '04': 'Heizen und Warmwasser (FS)',
            '03': 'Heizen und Warmwasser (Schaltzeiten)',
            '05': 'Standby'
        },
        'systemschemes': {
            '00': '-',
            '01': 'A1',
            '02': 'A1 + WW',
            '03': 'M2',
            '04': 'M2 + WW',
            '05': 'A1 + M2',
            '06': 'A1 + M2 + WW',
            '07': 'M2 + M3',
            '08': 'M2 + M3 + WW',
            '09': 'M2 + M3 + WW',
            '10': 'A1 + M2 + M3 + WW'
        },
    },
    'V200KO1B': {
        'operatingmodes': {
            '00': 'Warmwasser (Schaltzeiten)',
            '01': 'reduziert Heizen (dauernd)',
            '02': 'normal Heizen (dauernd)',
            '04': 'Heizen und Warmwasser (FS)',
            '03': 'Heizen und Warmwasser (Schaltzeiten)',
            '05': 'Standby'
        },
        'systemschemes': {
            '01': 'A1',
            '02': 'A1 + WW',
            '04': 'M2',
            '03': 'M2 + WW',
            '05': 'A1 + M2',
            '06': 'A1 + M2 + WW'
        }
    },
    'V200WO1C': {
        'operatingmodes': {
            '00': 'Abschaltbetrieb',
            '01': 'Warmwasser',
            '02': 'Heizen und Warmwasser',
            '03': 'undefiniert',
            '04': 'dauernd reduziert',
            '05': 'dauernd normal',
            '06': 'normal Abschalt',
            '07': 'nur kühlen'
        },
        'systemschemes': {
            '01': 'WW',
            '02': 'HK + WW',
            '04': 'HK + WW',
            '05': 'HK + WW'
        },
    },
    'V200HO1C': {
        'operatingmodes': {
            '00': 'Abschaltbetrieb',
            '01': 'Warmwasser',
            '02': 'Heizen und Warmwasser',
            '03': 'Normal reduziert',
            '04': 'Normal dauernd'
        },
        'systemschemes': {
            '01': 'WW',
            '02': 'HK + WW',
            '04': 'HK + WW',
            '05': 'HK + WW'
        }
    }
}
