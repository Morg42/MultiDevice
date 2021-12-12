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

* alle Geräte, für die jemand die Konfiguration und ggf. notwendige Methoden implementiert, siehe Doku


Konfiguration
-------------

plugin.yaml
~~~~~~~~~~~

Bitte die Dokumentation lesen, die aus den Metadaten der plugin.yaml erzeugt wurde.


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

Derzeit noch nicht implementiert.



TODO:
=====


The MultiDevice-Plugin (MD)
===========================

This plugin aims to support a wide range of devices which work by sending
commands to the device and reading data from it.
By abstracting devices and connections, most devices will be able to be
interfaced by this plugin.

Base Classes
============

MultiDevice
-----------

The 'MultiDevice'-class is derived from the SmartPlugin-class and provides
the framework for handling item associations to the plugin, for storing
item-command associations, for forwarding commands and the associated data
to the device classes and receiving data from the device classes to update
item values.
This class will usually not need to be adjusted, but runs as the plugin itself.


MD_Device
---------

The 'MD_Device'-class provides a framework for receiving (item) data values
from the plugin and forward it to the connection class and vice versa.
A basic framework for managing the device, i.e. (re-)configuring, starting
and stopping the device is already implemented and can be used without code
changed by device configuration.

``MD_Device(device_id, device_name, **kwargs)``

Public methods:

    - ``start()``
    - ``stop()``
    - ``send_command(command, value=None)``
    - ``read_all_commands()``
    - ``on_data_received(command, data)``
    - ``is_valid_command(command, read=None)``
    - ``set_runtime_data(**kwargs)``
    - ``update_device_params(**kwargs)``

Methods possible to overload for inherited classes:

    - ``run_standalone()``
    - ``_set_device_params(**kwargs)``
    - ``_get_connection()``


MD_Connection
-------------

This class and the derived classes provide frameworks for sending and receiving
data to and from devices via serial or network connections. For both hardware
layers implementation of query-response-connections and listening servers
with asynchronous push-to-callback are already available.
If more complex communication setup is needed, this can be implemented on top
of the existing classes.

Data is exchanged with MD_Device in a special dict format:

..code: python

    data_dict = {
        'payload': raw data as needed by the connection}
        'kw1': additional 'keyword' args or data specific to the connection type
        'kw2': additional 'keyword' args or data specific to the connection type
        '...': additional 'keyword' args or data specific to the connection type
    }


``MD_Connection(device_id, device_name, data_received_callback, **kwargs)``

Public methods:

    - ``open()``
    - ``close()``
    - ``send(data_dict)``

Methods necessary to overload for inherited classes:

    - ``_open()``
    - ``_close()``
    - ``_send(data_dict)``


Methods possible to overload for inherited classes:

    - ``_send_init_on_open()``
    - ``_send_init_on_send()``


This class has subclasses defined for the following types of connection:

    - ``MD_Connection_Net_TCP_Client`` for query-reply TCP connections
    - ``MD_Connection_Net_TCP_Server`` for TCP listening server with async callback
    - ``MD_Connection_Net_UDP_Server`` for UDP listering server with async callback
    - ``MD_Connection_Serial_Client`` for query-reply serial connections
    - ``MD_Connection_Serial_Async`` for event-loop serial connection with async callback

For detailed information and necessary configuration parameters, see the
respective class definition docstring.


MD_Commands
-----------

This class is a 'dict on steroids' of MD_Command-objects with error checking as
added value. In addition, it also loads command definitions, datatype sets
and handles datatype association.

No need to find out if ``command`` is defined, just call the methon
and the class will handle failure cases. Beware of NoneType-return values, though.

``MD_Commands(device_id, device_name, command_obj_class=MD_Command, **kwargs)``

Public methods:

    - ``is_valid_command(command, read=None)``
    - ``get_send_data(command, data=None)``
    - ``get_shng_data(command, data)``

Methods possible to overload:

    - ``_parse_commands(device_name, commands)``


MD_Command
----------

This class contains information concerning the command name, the opcode or
URL needed to issue the command, and information about datatypes expected by
SmartHomeNG and the device itself.

Its contents will be initialized by the MD_Commands-class while reading the
command configuration.

``MD_Command(device_name, command_name, dt_class, **kwargs)``

Public methods:

    - ``get_send_data(data)``
    - ``get_shng_data(data)``

Methods possible to overload:

    - ``get_send_data(data)``
    - ``get_shng_data(data)``


The class MD_Command_Str is an example for defining own commands according
to your needs.

This utilizes strings and dicts to build request URLs as payload data for the
MD_Connection_Net_TCP_Client class.


MD_Datatype
-----------

This is one of the most important classes. By declaration, it contains
information about the data type and format needed by a device and methods
to convert its value from selected Python data types used in items to the
(possibly) special data formats required by devices and vice versa.

Datatypes are specified in subclasses of Datatype with a nomenclature
convention of DT_<device data type of format>.

All default datatype classes are imported from Datatypes.py into the 'DT' module.

New devices can ship their own needed datatype classes in a file calles
``datatypes.py`` in the device's folder.

For details concernin API and implementation, refer to the reference classes as
examples.

``Datatype(fail_silent=True)``

Public methods:

    - ``get_send_data(data)``
    - ``get_shng_data(data, type=None)``

Methods necessary to overload:

    - ``get_send_data(data)``
    - ``get_shng_data(data, type=None)``


Configuration
=============

The plugin class is capable of handling an arbitrary number of devices
independently. Necessary configuration include the chosen devices respectively
the device names and possibly device parameter in ``/etc/plugin.yaml``.

The item configuration is supplemented by the attributes ``md_device`` and
``md_command``, which designate the device name from plugin configuration and
the command name from the device configuration, respectively.

The device class needs comprehensive configuration concerning available commands,
the associated sent and received data formats, which will be supplied by way
of configuration files in yaml format. Furthermore, the device-dependent
type and configuration of connection should be set in ``/etc/plugin.yaml`` for
each device used.

The connection classes will be chosen and configured by the device classes.
They should not need further configuration, as all data transformation is done
by the device classes and the connection-specific attributes are provided
from plugin configuration.


New devices
===========

New device types can be implemented by providing the following:

- a device configuration file defining commands and associated data formats
- a specification of needed connection type in /etc/plugin.yaml ('conn_type')
- only if needed:
  * additional methods in the device class to handle special commands which
    do more than assign transformed item data to a single item or which need
    more complex item transformation
  * additional methods in the connection class to handle special forms of
    connection initialization (e.g. serial sync routines)
  * additional data types in the datatype file
