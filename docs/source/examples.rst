========
Examples
========

Extreme/Fianium
===============

.. code-block:: python
    :caption: Initializing object

    from nkt_tools.extreme import Extreme

    laser = Extreme()

    # Loading x64 DLL from: C:\src\repos\nkt_tools\nkt_tools\NKTPDLL\x64\NKTPDLL.dll
    # Searching for connected NKT Laser...
    # NKT Extreme/Fianium Found:
    # Comport:  COM4 Device type:  0x60 at address: 15
    # System Type =  SuperK Extreme
    # Inlet Temperature = 22.8 C

.. code-block:: python
    :caption: reading system's current conditions

    laser.portname
    # Out[]: 'COM4'

    laser.module_address
    # Out[]: 15

    laser.device_type
    # Out[]: 96

    laser.current_level
    # Out[]: 1.1

    laser.power_level
    # Out[]: 100.0

    laser.emission_state
    # Out[]: False

    laser.inlet_temperature
    # Out[]: 22.9

    laser.interlock_status
    # Out[]: (0, 'Interlocked: Front panel interlock/key switch off')

    laser.nim_delay
    # Out[]: 9.9e-11

    laser.pulse_picker_ratio
    # Out[]: 1

    laser.watchdog_interval
    # Out[]: 30

    laser.setup_status
    # Out[]: 'Constant current mode'

.. code-block:: python
    :caption: test_read_funcs() method demonstrates the output of each property read and prints it.

    laser.test_read_funcs()

            System type = SuperK Extreme
            Inlet Temperature = 22.8
            Emission state = False
            Setup status = Constant current mode
            Interlock Status = (0, 'Interlocked: Front panel interlock/key switch off')
            Pulse picker ratio = 1
            Watchdog interval = 30
            Power level = 100.0
            Current level = 1.1
            NIM delay = 9.9e-11

.. code-block:: python
    :caption: print_status() method shows current condition of laser

    laser.print_status()
    0:RegResultSuccess
    Interlock relays off
    Interlock loop open
    Out[16]: '0b1010'

Varia
=====

.. code-block:: python
    :caption: Initializing the object and setting parameters

    from nkt_tools.varia import Varia
    varia = Varia()
    varia.short_setpoint = 550
    varia.long_setpoint = 600

.. code-block:: python
    :caption: varia communication properties

    varia.portname
    # Out[1]: 'COM4'

    varia.device_type
    # Out[2]: 104

    varia.module_address
    # Out[3]: 17

.. code-block:: python
    :caption: reading varia's main settings

    varia.short_setpoint
    # Out[4]: 550.0

    varia.long_setpoint
    # Out[5]: 600.0

    varia.nd_setpoint
    # Out[6]: 350.0

    varia.monitor_input
    # 0
    # Out[7]: 0.0

.. code-block:: python
    :caption: These two methods print the varia's status to the console.

    varia.print_status()
    # Interlock off
    # Shutter sensor 1
    # Out[8]: '0b100000010'

    varia.read_all_properties()
    # 0
    # Input Power =  0.0
    # ND Setpoint =  350.0
    # Long Setpoint =  430.7
    # Short Setpoint =  420.7

.. code-block:: python
    :caption: This method demonstrates the output type of various registerRead calls from the DLL. This call is made to the system status register which is meant to return a byte array (\x02\x01).

    varia.demo_nkt_registerReads()
    # registerRead:  (0, b'\x02\x01')
    # registerReadU8:  (0, 2)
    # registerReadS8:  (0, 2)
    # registerReadU16:  (0, 258)
    # registerReadU32:  (8, 258)
    # registerReadF32:  (8, 3.615350037958028e-43)
    # registerReadAscii:  (0, b'\x02\x01')
