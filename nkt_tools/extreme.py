"""Python module to control NKT Extreme and Fianium Lasers."""
import NKTP_DLL as nkt


class Extreme:
    status_messages = {
        0: 'Emission on',
        1: 'Interlock relays off',
        2: 'Interlock supply voltage low (possible short circuit)',
        3: 'Interlock loop open',
        4: 'Output Control signal low',
        5: 'Supply voltage low',
        6: 'Inlet temperature out of range',
        7: 'Clock battery low voltage',
        8: '-',
        9: '-',
        10: '-',
        11: '-',
        12: '-',
        13: 'CRC error on startup (possible module address conflict)',
        14: 'Log error code present',
        15: 'System error code present'
        }

    def __init__(self, portname=None):
        print('Searching for connected NKT Laser...')
        self._portname = None  # COM port for laser. Auto found if not given.
        self._module_address = 15  # module address = 15 for Extreme/Fianium
        self._device_type = None  # Should be 0x60 for Extreme/Fianium
        self._system_type = None  # 0 == Extreme; 1 == Fianium

        if portname:  # Allow user to init specific NKT Laser on portname
            self._portname = portname

        else:  # Search for connection w/ laser
            # Open available ports
            nkt.openPorts(nkt.getAllPorts(), 1, 1)

            # Get open NKT ports
            portlist = nkt.getOpenPorts().split(',')
            extreme_found = False

            for portName in portlist:  # Sweep open nkt ports
                # get binary devList of connected nkt devices
                comm_result, devList = nkt.deviceGetAllTypes(portName)
                # Get byte at location 15 (device address for extreme/fianium)
                device_type = devList[self.module_address]

                # Double check device_type matches extreme/fianium laser
                if hex(device_type) == '0x60':  # 96 == 0x60 in hex
                    if extreme_found:  # If extreme found on other port, error
                        err_msg = ('''Multiple NKT Lasers found on computer.
                        COM port 1 = %s
                        COM port 2 = %s
                        Please initialize Extreme class with designated \
                        portname to avoid conflict'''
                                   % (self.portname, portName))

                        raise RuntimeError(err_msg)

                    else:  # If this is first laser found,
                        extreme_found = True
                        self._portname = portName
                        self._device_type = device_type

        # Close all ports
        closeResult = nkt.closePorts('')
        if extreme_found:
            print('NKT Extreme/Fianium Found:')
            print('Comport: ', self.portname, 'Device type: ', "0x%0.2X"
                  % self.device_type, 'at address:', self.module_address)
            print('System Type = ', self.system_type)
            print('Inlet Temperature = ', self.inlet_temperature)

        else:
            print('No Extreme/Fianium Laser Found')

    module_address = property(lambda self: self._module_address)
    """int, read-only: Module address = 15 for Extreme/Fianium."""

    device_type = property(lambda self: self._device_type)
    """int, read-only: Should be 96 (0x60) for Extreme/Fianium.
    Assigned and checked during object init."""

    portname = property(lambda self: self._portname)
    """str, read-only: COM port for laser.
    Autofound during init if not given. User can supply when creating object."""

    @property
    def system_type(self):
        """
        Access register 0x6B to determine Extreme/Fianium

        From Manual:
        The system type is a newer implementation used to differentiate systems
        with minor differences. Older versions might not respond to this
        register. In that case the system type should be interpreted as
        0 = SuperK Extreme. 8-bit unsigned integer.
        0 = SuperK Extreme
        1 = SuperK Fianium
        """
        # Determine whether system is Extreme or Fianium
        register_address = 0x6B
        _, type_index = nkt.registerReadU8(self.portname,
                                            self.module_address,
                                            register_address, -1)

        if not type_index:  # Errors should default to Extreme
            type_index = 0
        type_list = ["SuperK Extreme", "SuperK Fianium"]
        self._system_type = type_list[type_index]
        return self._system_type

    @property
    def inlet_temperature(self):
        """
        Accesses register 0x11 to retrun inlet temperate w/ 0.1 C precision.

        Updates the value of non-public attr when called.
        """
        register_address = 0x11
        comm_result, value = nkt.registerReadS16(self.portname, self.module_address,
                                    register_address, -1)
        self._inlet_temperature = value * 10
        return self._inlet_temperature

    def emission(self, state):
        """
        Change emission state of laser to on/off

        Uses nktp_dll to write to register 0x30.

        Parameters:
        state: bool
            True turns laser on, false turns emission off
        """
        register_address = 0x30
        if state is True:
            nkt.registerWriteU8(self.portname, self.module_address,
                                register_address, 0x03, -1)
        elif state is False:
            nkt.registerWriteU8(self.portname, self.module_address,
                                register_address, 0x00, -1)

    def interlock_status(self):
        register_address = 0x32
        result, reading = nkt.registerRead(self.portname, self.module_address,
                                           register_address, -1)

        LSB = reading[0]  # What manual calls first byte
        MSB = reading[1]  # What manual calls second byte
        # Interlock status message based on manual
        output_options = ['Interlock off (interlock circuit open)',
                          'Front panel interlock/key switch off',
                          'Door switch open',
                          'External module interlock',
                          'Application interlock',
                          'Internal module interlock',
                          'Interlock power failure',
                          'Interlock disabled by light source']
        if LSB == 0:
            reason = output_options[MSB]
            print('Interlocked: %s' % reason)

        elif LSB == 1:
            print('Waiting for interlock reset')

        elif LSB == 2:
            print('Interlock is OK')

    def get_status(self):
        register_address = 0x66
        result, byte = nkt.registerReadU16(self.portname, self.module_address,
                                           register_address, -1)
        print(nkt.RegisterResultTypes(result))
        bits = bin(byte)
        for index, bit in enumerate(reversed(bits)):
            if bit == 'b':
                break
            elif bit == '1':
                print(Extreme.status_messages[index])

        return(bits)

if __name__ == "__main__":
    laser = Extreme()
    laser.get_status()
    laser.interlock_status()
