"""Python module to control NKT Varia."""
import nkt_tools.NKTP_DLL as nkt


class Varia:
    status_messages = {
        0: '-',
        1: 'Interlock off',
        2: 'Interlock loop in',
        3: 'Interlock loop out',
        4: '-',
        5: 'Supply voltage low',
        6: '-',
        7: '-',
        8: 'Shutter sensor 1',
        9: 'Shutter sensor 2',
        10: '-',
        11: '-',
        12: 'Filter 1 moving',
        13: 'Filter 2 moving',
        14: 'Filter 3 moving',
        15: 'Error code present'
        }
    """
    dict : system status translation bits > string.

    =========  ===================
    Bit Index  Status
    =========  ===================
    Bit 0:     -
    Bit 1:     Interlock off
    Bit 2:     Interlock loop in
    Bit 3:     Interlock loop out
    Bit 4:     -
    Bit 5:     Supply voltage low
    Bit 6:     -
    Bit 7:     -
    Bit 8:     Shutter sensor 1
    Bit 9:     Shutter sensor 2
    Bit 10:    -
    Bit 11:    -
    Bit 12:    Filter 1 moving
    Bit 13:    Filter 2 moving
    Bit 14:    Filter 3 moving
    Bit 15:    Error code present
    =========  ===================

    """

    def __init__(self, portname=None):
        """
        Searches for connected NKT Varia and defines instrument parameters.

        Make sure devices are not connected via another program already.
        If multiple Varias are connected to the same computer,
        specificy the port of the desired Varia upon instantiation.

        Parameters
        ----------
        portname : str, optional
            Enter if portname for Varia is known/multiple lasers are connected.
            If not supplied, system searches for Varia. None by default.

        Raises
        ------
        RuntimeError
            Throws error if multiple NKT Varias are found on one computer.
            Supply portname for desired Varia if multiple present.
        """
        print('Searching for connected NKT Varia...')
        self._portname = None  # COM port name. Autosearches if not provided.
        self._module_address = None  # 16-25 for Varia. Auto searches in init.
        self._device_type = None  # This should update to 0x68 if init is right

        if portname:  # Allow user to init specific NKT Laser on portname
            self._portname = portname

        else:  # User didn't specify port
            # Open available ports
            nkt.openPorts(nkt.getAllPorts(), 1, 1)

            # Get open NKT ports
            portlist = nkt.getOpenPorts().split(',')
            varia_found = False

            for portName in portlist:
                if portName == '':
                    continue
                # get binary devList of connected nkt devices
                comm_result, devList = nkt.deviceGetAllTypes(portName)

                # Address for Varia depends on specific hardware.
                # Search possible addresses (16-25) searching for connection.
                for n in range(9):
                    trial_address = 16 + n  # Address=16+Rotary switch #(0..9)
                    try:
                        device_type = devList[trial_address]
                    except (IndexError):
                        print('No Varia on port: ', portName)
                        break

                    # Check if device_type matches varia (0x68)
                    if hex(device_type) == '0x68':  # Check for varia in hex
                        if varia_found:  # If varia found on other port, error
                            err_msg = ('''Multiple Varias found on computer.
                            COM port 1 = %s
                            COM port 2 = %s
                            Please initialize Varia class with designated \
                            portname to avoid conflict'''
                                       % (self.portname, portName))

                            raise RuntimeError(err_msg)

                        else:  # If first laser found,
                            varia_found = True
                            self._portname = portName
                            self._module_address = trial_address
                            self._device_type = device_type
                            break

            # Close all ports
            closeResult = nkt.closePorts('')
            if varia_found:
                print('NKT Varia Found:')
                print('Comport: ', self.portname, 'Device type: ', "0x%0.2X"
                      % self.device_type, 'at address:', self.module_address)

            else:
                print('No Varia Found')

    portname = property(lambda self: self._portname)
    """`str`, read-only: COM port for laser.
    Autofound during init if not given. User can supply when creating object.
    """

    module_address = property(lambda self: self._module_address)
    """`int`, read-only:  # 16-25 for Varia. Auto searches in init."""

    device_type = property(lambda self: self._device_type)
    """`int`, read-only: This should update to 104 (0x68) if init is right.
    Assigned and checked during object init."""

    @property
    def monitor_input(self):
        """
        Uses optional monitor to get laser power in percent.

        Calls registerREad16U on register 0x13. Converts reading from in to
        float. Requires the optional monitor to be attached for this register
        content to be valid.

        Returns
        -------
        float
            Output power given in percent with 0.1% precision.
        """
        register_address = 0x13
        comm_result, reading = nkt.registerReadU16(self.portname,
                                                   self.module_address,
                                                   register_address, -1)
        output_power = reading / 10
        return output_power

    @property
    def nd_setpoint(self):
        """
        Unclear what this parameter actually controls.

        Writes to register 0x32.

        Manual:
        The output level of the SuperK VARIA is controlled with an unsigned
        16-bit integer value sent to the neutral density filter setpoint
        register. The value in this register is in tenths of percent
        (permille, ‰).

        Parameters
        ----------
        value : float
            Setpoint for neutral density filter given in % with 0.1% precision.
        """
        register_address = 0x32
        comm_result, reading = nkt.registerReadU16(self.portname,
                                                   self.module_address,
                                                   register_address, -1)
        return reading/10

    @nd_setpoint.setter
    def nd_setpoint(self, value):
        register_address = 0x32
        value = int(value * 10)  # convert percent to permille
        nkt.registerWriteU16(self.portname, self.module_address,
                             register_address, value, -1)

    @property
    def long_setpoint(self):
        """
        Sets the short wave pass value with 0.1 nm precision.

        Converts wavelength value [nm] to int [1/10 nm] then writes to register
        0x33.

        Parameters
        ----------
        wavelength : float
            Lower bandpass value given in nanometers w/ 0.1 nm precision.
        """
        register_address = 0x33
        comm_result, reading = nkt.registerReadU16(self.portname,
                                                   self.module_address,
                                                   register_address, -1)
        return reading/10

    @long_setpoint.setter
    def long_setpoint(self, wavelength):
        register_address = 0x33
        value = int(wavelength * 10)  # convert nm to 1/10 nm
        nkt.registerWriteU16(self.portname, self.module_address,
                             register_address, value, -1)

    @property
    def short_setpoint(self):
        """
        Sets the long wave pass value with 0.1 nm precision.

        Converts wavelength value [nm] to int [1/10 nm] then writes to register
        0x34.

        Parameters
        ----------
        wavelength : float
            Upper bandpass value given in nanometers w/ 0.1 nm precision.
        """
        register_address = 0x34
        comm_result, reading = nkt.registerReadU16(self.portname,
                                                   self.module_address,
                                                   register_address, -1)
        return reading/10

    @short_setpoint.setter
    def short_setpoint(self, wavelength):
        register_address = 0x34
        value = int(wavelength * 10)  # convert nm to 1/10 nm
        nkt.registerWriteU16(self.portname, self.module_address,
                             register_address, value, -1)

    def print_status(self):
        """
        Read system status in bytes, translate to str, print.

        Reads system status using registerReadU16 on register 0x66.
        Translates binary into str for of equipment status through
        Varia.status_messages.

        Returns
        -------
        str : bits
            binary results of register read in string format.
        """
        register_address = 0x66
        result, byte = nkt.registerReadU16(self.portname, self.module_address,
                                           register_address, -1)
        print(nkt.RegisterResultTypes(result))
        bits = bin(byte)
        for index, bit in enumerate(reversed(bits)):
            if bit == 'b':
                break
            elif bit == '1':
                print(Varia.status_messages[index])

        return (bits)

    def read_all_properties(self):
        print('Input Power = ', self.monitor_input)
        print('ND Setpoint = ', self.nd_setpoint)
        print('Long Setpoint = ', self.long_setpoint)
        print('Short Setpoint = ', self.short_setpoint)

    def demo_nkt_registerReads(self):
        """
        Tests various registerRead functions supplied by NKTPDLL.

        Makes read request to register 0x66 (system status) using various
        registerRead commands as an example of the data type returned by each.
        """
        register_address = 0x66
        print('registerRead: ',
              nkt.registerRead(self.portname, self.module_address,
                               register_address, -1))
        print('registerReadU8: ',
              nkt.registerReadU8(self.portname, self.module_address,
                                 register_address, -1))
        print('registerReadS8: ',
              nkt.registerReadS8(self.portname, self.module_address,
                                 register_address, -1))
        print('registerReadU16: ',
              nkt.registerReadU16(self.portname, self.module_address,
                                  register_address, -1))
        print('registerReadU32: ',
              nkt.registerReadU32(self.portname, self.module_address,
                                  register_address, -1))
        print('registerReadF32: ',
              nkt.registerReadF32(self.portname, self.module_address,
                                  register_address, -1))
        print('registerReadAscii: ',
              nkt.registerReadAscii(self.portname, self.module_address,
                                    register_address, -1))


if __name__ == "__main__":
    varia = Varia()
    varia.print_status()
    varia.read_all_properties()
    varia.demo_nkt_registerReads()
