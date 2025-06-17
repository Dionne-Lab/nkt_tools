"""Python module to control NKT RF Driver."""
import nkt_tools.NKTP_DLL as nkt


class RFDriver:
    status_messages = {
        0: 'Emission',
        1: '-',
        2: '-',
        3: '-',
        4: '-',
        5: 'Supply voltage low',
        6: 'Module temp range',
        7: '-',
        8: '-',
        9: '-',
        10: '-',
        11: '-',
        12: '-',
        13: 'AODS communication timeout',
        14: 'Needs crystal info',
        15: 'Error code present'
        }
    """
    dict : system status translation bits > string.

    =========  ===================
    Bit Index  Status
    =========  ===================
    0	Emission
    1	-
    2	-
    3	-
    4	-
    5	Supply voltage low
    6	Module temp range
    7	-
    8	-
    9	-
    10	-
    11	-
    12	-
    13	AODS communication timeout
    14	Needs crystal info
    15	Error code present
    =========  ===================

    """
    

    def __init__(self, portname=None):
        """
        Searches for connected NKT RF driver and defines instrument parameters.

        Make sure devices are not connected via another program already.

        Parameters
        ----------
        portname : str, optional
            Enter if portname for RF driver is known/multiple lasers are connected.
            If not supplied, system searches for RF driver. None by default.

        Raises
        ------
        RuntimeError
            Throws error if multiple NKT RF drivers are found on one computer.
            Supply portname for desired RF driver if multiple present.
        """
        print('Searching for connected NKT RF driver...')
        self._portname = None  # COM port name. Autosearches if not provided.
        self._module_address = None  # 16 for RF driver. Auto searches in init.
        self._device_type = None  # This should update to 0x66 if init is right

        if portname:  # Allow user to init specific NKT Laser on portname
            self._portname = portname

        else:  # User didn't specify port
            # Open available ports
            nkt.openPorts(nkt.getAllPorts(), 1, 1)

            # Get open NKT ports
            portlist = nkt.getOpenPorts().split(',')
            RF_driver_found = False

            for portName in portlist:
                if portName == '':
                    continue
                # get binary devList of connected nkt devices
                comm_result, devList = nkt.deviceGetAllTypes(portName)

                # Address for RF driver depends on specific hardware.
                # Search possible addresses (16-25) searching for connection.
                for n in range(9):
                    trial_address = 16 + n  # Address=16+Rotary switch #(0..9)
                    try:
                        device_type = devList[trial_address]
                    except (IndexError):
                        print('No RF driver on port: ', portName)
                        break

                    # Check if device_type matches RF driver (0x68)
                    if hex(device_type) == '0x66':  # Check for RF driver in hex
                        if RF_driver_found:  # If RF driver found on other port, error
                            err_msg = ('''Multiple RF drivers found on computer.
                            COM port 1 = %s
                            COM port 2 = %s
                            Please initialize RF driver class with designated \
                            portname to avoid conflict'''
                                       % (self.portname, portName))

                            raise RuntimeError(err_msg)

                        else:  # If first laser found,
                            RF_driver_found = True
                            self._portname = portName
                            self._module_address = trial_address
                            self._device_type = device_type
                            break

            # Close all ports
            closeResult = nkt.closePorts('')
            if RF_driver_found:
                print('NKT RF driver Found:')
                print('Comport: ', self.portname, 'Device type: ', "0x%0.2X"
                      % self.device_type, 'at address:', self.module_address)

            else:
                print('No RF driver Found')

    portname = property(lambda self: self._portname)
    """`str`, read-only: COM port for laser.
    Autofound during init if not given. User can supply when creating object.
    """

    module_address = property(lambda self: self._module_address)
    """`int`, read-only:  # 17 for RF driver. Auto searches in init."""

    device_type = property(lambda self: self._device_type)
    """`int`, read-only: This should update to 104 (0x66) if init is right.
    Assigned and checked during object init."""

    @property
    def rf_power(self):
        register_address = 0x30
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading

    @rf_power.setter
    def rf_power(self, state):
        register_address = 0x30
        nkt.registerWriteU8(self.portname, self.module_address, register_address, state, -1)

    @property
    def setup_bits(self):
        register_address = 0x31
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading

    @setup_bits.setter
    def setup_bits(self, value):
        register_address = 0x31
        nkt.registerWriteU8(self.portname, self.module_address, register_address, value, -1)

    @property
    def min_wavelength(self):
        register_address = 0x34
        comm_result, reading = nkt.registerReadU32(self.portname, self.module_address, register_address, -1)
        return reading

    @property
    def max_wavelength(self):
        register_address = 0x35
        comm_result, reading = nkt.registerReadU32(self.portname, self.module_address, register_address, -1)
        return reading

    @property
    def crystal_temperature(self):
        register_address = 0x38
        comm_result, reading = nkt.registerReadS16(self.portname, self.module_address, register_address, -1)
        return reading / 10.0

    @property
    def fsk_mode(self):
        register_address = 0x3B
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading

    @fsk_mode.setter
    def fsk_mode(self, mode):
        register_address = 0x3B
        nkt.registerWriteU8(self.portname, self.module_address, register_address, mode, -1)

    @property
    def daughter_board(self):
        register_address = 0x3C
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading

    @daughter_board.setter
    def daughter_board(self, value):
        register_address = 0x3C
        nkt.registerWriteU8(self.portname, self.module_address, register_address, value, -1)

    @property
    def connected_crystal(self):
        register_address = 0x75
        comm_result, reading = nkt.registerReadU8(self.portname, self.module_address, register_address, -1)
        return reading

    def get_wavelength(self, channel):
        if 0 <= channel < 8:
            register_address = 0x90 + channel
            comm_result, reading = nkt.registerReadU32(self.portname, self.module_address, register_address, -1)
            return reading
        raise ValueError("Invalid channel index")

    def set_wavelength(self, channel, wavelength):
        if not (0 <= channel < 8):
            raise ValueError("Invalid channel index")
        if wavelength > 4000:
            raise ValueError("Wavelength must be in nm")
        register_address = 0x90 + channel
        setpoint = int(wavelength * 1e3)
        nkt.registerWriteU32(self.portname, self.module_address, register_address, setpoint, -1)

    def get_amplitude(self, channel):
        if 0 <= channel < 8:
            register_address = 0xB0 + channel
            comm_result, reading = nkt.registerReadU16(self.portname, self.module_address, register_address, -1)
            return reading / 10.0
        raise ValueError("Invalid channel index")

    def set_amplitude(self, channel, amplitude):
        if not (0 <= channel < 8):
            raise ValueError("Invalid channel index")
        if not (0 <= amplitude <= 100):
            raise ValueError("Power must be between 0 and 100%")
        register_address = 0xB0 + channel
        setpoint = int(amplitude * 10)
        nkt.registerWriteU16(self.portname, self.module_address, register_address, setpoint, -1)

    def get_modulation(self, channel):
        if 0 <= channel < 8:
            register_address = 0xC0 + channel
            comm_result, reading = nkt.registerReadU16(self.portname, self.module_address, register_address, -1)
            return reading / 10.0
        raise ValueError("Invalid channel index")

    def set_modulation(self, channel, modulation):
        if 0 <= channel < 8:
            register_address = 0xC0 + channel
            nkt.registerWriteU16(self.portname, self.module_address, register_address, modulation, -1)
        else:
            raise ValueError("Invalid channel index")
    
    def get_channels(self, return_ch_status=True, verbose=1):
        """
        Read the current channels and print which ones are on and at what settings.
        Adapted from the NKT_laser_control project.
        """
        channels_status = {'ON': [], 'OFF': []}
        for channel in range(0, 8):
            wavelength_address = f"0x9{channel}"
            wavelength_address = int(wavelength_address, 16)

            amplitude_address = f"0xB{channel}"
            amplitude_address = int(amplitude_address, 16)

            result1 = nkt.registerReadU32(self.portname, self.module_address, wavelength_address, 0)
            result2 = nkt.registerReadU16(self.portname, self.module_address, amplitude_address, -1)

            if result2[1] != 0:
                wavelength_nm = result1[1]/1000
                amplitude = result2[1]/10
                if verbose > 0:
                    print(f'Channel {channel} is ON, wavelength: {wavelength_nm} nm, amplitude: {amplitude} %.')
                channels_status['ON'].append([channel, wavelength_nm, amplitude])
            else:
                channels_status['OFF'].append(channel)
        if verbose > 0:
            print(f'Channels {channels_status['OFF']} are OFF')
        if return_ch_status:
            return channels_status
    
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
        # print(nkt.RegisterResultTypes(result))
        bits = bin(byte)
        for index, bit in enumerate(reversed(bits)):
            if bit == 'b':
                break
            elif bit == '1':
                print(RFDriver.status_messages[index])
        return (bits)
    
    def read_all_properties(self):
        print("RF Power:", self.rf_power)
        print("Setup Bits:", self.setup_bits)
        print("Min Wavelength:", self.min_wavelength)
        print("Max Wavelength:", self.max_wavelength)
        print("Crystal Temperature:", self.crystal_temperature)
        print("Connected Crystal:", self.connected_crystal)
        print("FSK Mode:", self.fsk_mode)

if __name__ == "__main__":
    # rf_driver = RFDriver("COM3", 0x06)
    rf_driver = RFDriver()
    rf_driver.print_status()
    rf_driver.read_all_properties()
    rf_driver.rf_power = 1  # Turn on RF power
