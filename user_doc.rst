multidevice
===========

Anforderungen
-------------

Nix besonderes.

Notwendige Software
~~~~~~~~~~~~~~~~~~~

* pyserial

Unterstützte Geräte
~~~~~~~~~~~~~~~~~~~

Alle Geräte, für die jemand die Konfiguration und ggf. notwendige Methoden implementiert. Derzeit sind dies:

* Pioneer AV-Receiver (pioneer)

  * SC-LX87
  * SC-LX77
  * SC-LX57
  * SC-2023
  * SC-1223
  * VSX-1123
  * VSX-923

* Denon AV-Receiver (denon)

  * AVR-X6300H
  * AVR-X4300H
  * AVR-X3300W
  * AVR-X2300W
  * AVR-X1300W

* Kodi Mediencenter (kodi)
* Viessmann-Heizungen (viessmann)

  * V200KW2
  * V200KO1B
  * V200WO1C
  * V200HO1C


Konfiguration
-------------

plugin.yaml
~~~~~~~~~~~

Liste von Geräten und ggf. deren Konfiguration. 

Geräte-ID ist eine
eindeutige Kennzeichnung, die auch in der Item-Konfiguration in der
Option ``md_deviceid`` angegeben wird; Geräte-Typ ist der Name des
Gerätes im Ordner ``dev_<Geräte-Typ>``. 

Mindestangabe ist
der Geräte-Typ; wenn keine Geräte-ID vergeben wird, ist diese
gleich dem Geräte-Typ (beachte: pro Geräte-Typ nur einmal möglich).

Unterhalb der Listenebene der Geräte sind weitere Konfigurations-
attribute für die Geräte in der Listenform <Attribut>: <Wert>
möglich, z.B. Verbindungsattribute wie `host`, `port`, `serial` o.ä.

Eine Auflistung der grundsätzlich unterstützten Attribute findet sich
in der Datei ``MD_Globals.py``. Dort finden sich auch symbolische
Bezeichner ("Konstanten") für einige der Attribute. Diese können in 
der Konfiguration für bessere Übersichtlichkeit verwendet werden.

Für die Konfiguration der einzelnen Geräte sollte sich die Dokumentation der jeweils
notwendigen und unterstützen Attribute im Geräte-Ordner ``dev_<device>`` finden.

Beispiel:

.. code:: yaml

	devices:
	    - <Geräte-Typ>         # Geräte-ID = Geräte-Typ
	    - <Geräte-Typ>:        # Geräte-ID = Geräte-Typ
	        - <Attribut1>: <Wert1>
	        -...
	    - <Geräte-ID>: <Geräte-Typ>
	    - <Geräte-ID>:         # Geräte-Typ = Geräte-ID
	        - <Attribut1>: <Wert1>
	        - ...
	    - <Geräte-ID>:
	        - device_type: <Geräte-Typ>
	        - <Attribut1>: <Wert1>
	        - ...


Bitte zusätzlich die Dokumentation lesen, die aus den Metadaten der plugin.yaml erzeugt wurde.


items.yaml
~~~~~~~~~~

Bitte die Dokumentation lesen, die aus den Metadaten der plugin.yaml erzeugt wurde.


logic.yaml
~~~~~~~~~~

Bitte die Dokumentation lesen, die aus den Metadaten der plugin.yaml erzeugt wurde.


Funktionen
~~~~~~~~~~

Bitte die Dokumentation lesen, die aus den Metadaten der plugin.yaml erzeugt wurde.


Beispiele
---------

Hier können ausführlichere Beispiele und Anwendungsfälle beschrieben werden.


Web Interface
-------------

Derzeit noch nicht weitergehend implementiert.



Entwicklung von eigenen Geräte-Klassen
======================================

Die Entwicklerdokumentation existiert derzeit nur auf englisch.

.. automodule:: plugins.multidevice

