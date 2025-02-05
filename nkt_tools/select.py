"""Python module to control NKT Select."""
import nkt_tools.NKTP_DLL as nkt


class Select:
    status_messages = {
        0: '-',
        1: 'Interlock off',
        2: 'Interlock loop in',
        3: 'Interlock loop out',
        4: '-',
        5: 'Supply voltage low',
        6: 'Module temp range',
        7: '-',
        8: 'Shutter sensor 1',
        9: 'Shutter sensor 2',
        10: 'New crystal1 temperature',
        11: 'New crystal2 temperature',
        12: '-',
        13: '-',
        14: '-',
        15: 'Error code present'
        }
    """
    dict : system status translation bits > string.

    =========  ===================
    Bit Index  Status
    =========  ===================
    0	-
    1	Interlock off
    2	Interlock loop in
    3	Interlock loop out
    4	-
    5	Supply voltage low
    6	Module temp range
    7	-
    8	Shutter sensor1
    9	Shutter sensor2
    10	New crystal1 temperature
    11	New crystal2 temperature
    12	-
    13	-
    14	-
    15	Error code present
    =========  ===================

    """
    

    def __init__(self, portname=None):
        """
        Searches for connected NKT Select and defines instrument parameters.

        Make sure devices are not connected via another program already.

        Parameters
        ----------
        portname : str, optional
            Enter if portname for Select is known/multiple lasers are connected.
            If not supplied, system searches for Select. None by default.

        Raises
        ------
        RuntimeError
            Throws error if multiple NKT Selects are found on one computer.
            Supply portname for desired Select if multiple present.
        """
        print('Searching for connected NKT Select...')
        self._portname = None  # COM port name. Autosearches if not provided.
        self._module_address = None  # 16 for Select. Auto searches in init.
        self._device_type = None  # This should update to 0x67 if init is right

        if portname:  # Allow user to init specific NKT Laser on portname
            self._portname = portname

        else:  # User didn't specify port
            # Open available ports
            nkt.openPorts(nkt.getAllPorts(), 1, 1)

            # Get open NKT ports
            portlist = nkt.getOpenPorts().split(',')
            Select_found = False

            for portName in portlist:
                if portName == '':
                    continue
                # get binary devList of connected nkt devices
                comm_result, devList = nkt.deviceGetAllTypes(portName)

                # Address for Select depends on specific hardware.
                # Search possible addresses (16-25) searching for connection.
                for n in range(9):
                    trial_address = 16 + n  # Address=16+Rotary switch #(0..9)
                    try:
                        device_type = devList[trial_address]
                    except (IndexError):
                        print('No Select on port: ', portName)
                        break

                    # Check if device_type matches Select (0x68)
                    if hex(device_type) == '0x67':  # Check for Select in hex
                        if Select_found:  # If Select found on other port, error
                            err_msg = ('''Multiple Selects found on computer.
                            COM port 1 = %s
                            COM port 2 = %s
                            Please initialize Select class with designated \
                            portname to avoid conflict'''
                                       % (self.portname, portName))

                            raise RuntimeError(err_msg)

                        else:  # If first laser found,
                            Select_found = True
                            self._portname = portName
                            self._module_address = trial_address
                            self._device_type = device_type
                            break

            # Close all ports
            closeResult = nkt.closePorts('')
            if Select_found:
                print('NKT Select Found:')
                print('Comport: ', self.portname, 'Device type: ', "0x%0.2X"
                      % self.device_type, 'at address:', self.module_address)

            else:
                print('No Select Found')

    portname = property(lambda self: self._portname)
    """`str`, read-only: COM port for laser.
    Autofound during init if not given. User can supply when creating object.
    """

    module_address = property(lambda self: self._module_address)
    """`int`, read-only:  # 16 for Select. Auto searches in init."""

    device_type = property(lambda self: self._device_type)
    """`int`, read-only: This should update to 104 (0x67) if init is right.
    Assigned and checked during object init."""

    # @property
    # def monitor_1_readout(self):
    #     """
    #     Readout from optional optical power monitor no. 1 in tenths of percent (permille, ‰).

    #     Calls registerREad16U on register 0x10. Converts reading from in to
    #     float. Requires the optional monitor to be attached for this register
    #     content to be valid.

    #     Returns
    #     -------
    #     float
    #         Output power given in percent with 0.1% precision.
    #     """
    #     register_address = 0x10
    #     comm_result, reading = nkt.registerReadU16(self.portname,
    #                                                self.module_address,
    #                                                register_address, -1)
    #     output_power = reading / 10
    #     return output_power

    # @property
    # def monitor_1_gain(self):
    #     """
    #     Gain setting for optional optical power monitor no.1. 
    #     There are eight gain levels, numbered 0..7, with 0 being thet lowest gain level. 
    #     Each level increase doubles the sensitivity.

    #     Note
    #     ----
    #     Monitor gain settings should not be altered when the SuperK light source is 
    #     running in external feedback mode (Power Lock).

    #     Parameters
    #     ----------
    #     value : float
    #         Gain.
    #     """
    #     register_address = 0x32
    #     comm_result, reading = nkt.registerReadU8(self.portname,
    #                                                self.module_address,
    #                                                register_address, -1)
    #     return reading



    @property
    def monitor_1_readout(self):
        register_address = 0x10
        comm_result, reading = nkt.registerReadU16(self.portname, self.module_address, register_address, -1)
        return reading / 10
    
    @property
    def monitor_2_readout(self):
        register_address = 0x11
        comm_result, reading = nkt.registerReadU16(self.portname, self.module_address, register_address, -1)
        return reading / 10
    
    @property
    def monitor_1_gain(self):
        register_address = 0x32
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading
    
    @monitor_1_gain.setter
    def monitor_1_gain(self, gain):
        register_address = 0x32
        nkt.registerWriteU8(self.portname, self.module_address, register_address, gain, -1)
    
    @property
    def monitor_2_gain(self):
        register_address = 0x33
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading
    
    @monitor_2_gain.setter
    def monitor_2_gain(self, gain):
        register_address = 0x33
        nkt.registerWriteU8(self.portname, self.module_address, register_address, gain, -1)
    
    @property
    def rf_switch(self):
        register_address = 0x34
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading
    
    @rf_switch.setter
    def rf_switch(self, state):
        register_address = 0x34
        nkt.registerWriteU8(self.portname, self.module_address, register_address, state, -1)
    
    @property
    def monitor_switch(self):
        register_address = 0x35
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading
    
    @monitor_switch.setter
    def monitor_switch(self, state):
        register_address = 0x35
        nkt.registerWriteU8(self.portname, self.module_address, register_address, state, -1)
    
    @property
    def crystal_1_min_wavelength(self):
        register_address = 0x90
        comm_result, reading = nkt.registerReadU32(self.portname, self.module_address, register_address, -1)
        return reading / 1e3
    
    @property
    def crystal_1_max_wavelength(self):
        register_address = 0x91
        comm_result, reading = nkt.registerReadU32(self.portname, self.module_address, register_address, -1)
        return reading / 1e3
    
    @property
    def crystal_2_min_wavelength(self):
        register_address = 0xA0
        comm_result, reading = nkt.registerReadU32(self.portname, self.module_address, register_address, -1)
        return reading / 1e3
    
    @property
    def crystal_2_max_wavelength(self):
        register_address = 0xA1
        comm_result, reading = nkt.registerReadU32(self.portname, self.module_address, register_address, -1)
        return reading / 1e3
    
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
                print(Select.status_messages[index])

        return (bits)
    
    def read_all_properties(self):
        print('Monitor 1 Readout =', self.monitor_1_readout)
        print('Monitor 2 Readout =', self.monitor_2_readout)
        print('Monitor 1 Gain =', self.monitor_1_gain)
        print('Monitor 2 Gain =', self.monitor_2_gain)
        print('RF Switch =', self.rf_switch)
        print('Monitor Switch =', self.monitor_switch)
        print('Crystal 1 Min Wavelength =', self.crystal_1_min_wavelength)
        print('Crystal 1 Max Wavelength =', self.crystal_1_max_wavelength)
        print('Crystal 2 Min Wavelength =', self.crystal_2_min_wavelength)
        print('Crystal 2 Max Wavelength =', self.crystal_2_max_wavelength)

if __name__ == "__main__":
    # select = Select("COM3", 0x67)
    select = Select()
    select.print_status()
    select.read_all_properties()

