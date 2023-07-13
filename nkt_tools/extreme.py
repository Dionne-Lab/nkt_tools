"""
Python module to control NKT Extreme and Fianium Lasers.

Note: I chose to use specific setter methods over properties so that the user
explicitly has to adjust potentially dangerous conditions
(i.e. laser.set_emission(True)). I felt this style leaves less ambiguity that
the user is actively turning the laser on (vs. laser.emission = True). Less
dangerous properties follow the dedicated setter method format for consistency.
"""
import nkt_tools.NKTP_DLL as nkt


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
    """
    dict : system status translation bits > string

    =========  ========================================================
    Bit Index  Status
    =========  ========================================================
    Bit 0:     Emission on
    Bit 1:     Interlock relays off
    Bit 2:     Interlock supply voltage low (possible short circuit)
    Bit 3:     Interlock loop open
    Bit 4:     Output Control signal low
    Bit 5:     Supply voltage low
    Bit 6:     Inlet temperature out of range
    Bit 7:     Clock battery low voltage
    ...
    Bit 13:     CRC error on startup (possible module address conflict)
    Bit 14:     Log error code present
    Bit 15:     System error code present
    =========  ========================================================
    """
    setup_options = {
        0: 'Constant current mode',
        1: 'Constant power mode',
        2: 'Externally modulated current mode',
        3: 'Externally modulated power mode',
        4: 'External feedback mode (Power Lock)'
            }

    def __init__(self, portname=None):
        """
        Searches for connected NKT lasers and defines instrument parameters.

        Make sure devices are not connected via another program already.
        If multiple Extreme/Fianium lasers are connected to the same computer,
        specificy the port of the desired laser upon instantiation.

        Parameters
        ----------
        portname : str, optional
            Enter if portname for laser is known/multiple lasers are connected.
            If not supplied, system searches for laser. None by default.

        Raises
        ------
        RuntimeError
            Throws error if multiple NKT lasers are found on one computer.
            Supply portname for desired laser if multiple present.
        """
        print('Searching for connected NKT Laser...')
        self._portname = None  # COM port for laser. Auto found if not given.
        self._module_address = 15  # module address = 15 for Extreme/Fianium
        self._device_type = None  # Should be 0x60 for Extreme/Fianium
        self._system_type = None  # 0 == Extreme; 1 == Fianium
        self._inlet_temperature = None
        self._emission_state = None
        self._setup_status = None
        self._interlock_status = None
        self._pulse_picker_ratio = None
        self._watchdog_interval = None
        self._power_level = None
        self._current_level = None
        self._nim_delay = None


        if portname:  # Allow user to init specific NKT Laser on portname
            self._portname = portname
            self._device_type = 96  # Could put check here

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
            print('Inlet Temperature = %3.1f C' % self.inlet_temperature)

        else:
            print('No Extreme/Fianium Laser Found')

    module_address = property(lambda self: self._module_address)
    """`int`, read-only: Module address = 15 for Extreme/Fianium."""

    device_type = property(lambda self: self._device_type)
    """`int`, read-only: Should be 96 (0x60) for Extreme/Fianium.
    Assigned and checked during object init."""

    portname = property(lambda self: self._portname)
    """`str`, read-only: COM port for laser.
    Autofound during init if not given. User can supply when creating object.
    """

    @property
    def system_type(self):
        """
        `str`, read-only:
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
        `float`, read-only:
        Accesses register 0x11 to return inlet temperature w/ 0.1 C precision.

        Updates the value of non-public attr when called.

        Return
        ------
        float
            Inlet temperature w/ 0.1 C precision.
        """
        register_address = 0x11
        comm_result, value = nkt.registerReadS16(self.portname,
                                                 self.module_address,
                                                 register_address, -1)
        self._inlet_temperature = value / 10
        return self._inlet_temperature

    @property
    def emission_state(self):
        """
        Accesses register 0x30 to return emission state of laser.

        Updates the value of non-public attr when called.

        Return
        ------
        bool
            True = emission off; False = emission on
        """
        register_address = 0x30
        comm_result, value = nkt.registerReadU8(self.portname,
                                                self.module_address,
                                                register_address, -1)
        if value == 3:
            self._emission_state = True
        elif value == 0:
            self._emission_state = False
        else:
            self._emission_state = 'Unknown'
            print('Unknown Emissions State Detected')

        return self._emission_state

    @property
    def setup_status(self):
        """
        Reads value of register 0x16 and returns corresponding status message.

        See Extreme.setup_options for possible outcomes. Use Extreme.set_mode()
        to change value.

        Returns
        -------
        str
            Current setup status of laser based on manual values.
        """
        register_address = 0x16
        comm_result, setup_key = nkt.registerReadU8(self.portname,
                                                    self.module_address,
                                                    register_address, -1)
        self._setup_status = Extreme.setup_options[setup_key]
        return self._setup_status

    @property
    def interlock_status(self):
        """
        Print interlock status to terminal.

        Reads register 0x32 and converts bytes into strings based on manual.

        Manual:
        Reading the interlock register returns the current interlock status,
        which consists of two unsigned bytes. The first byte (LSB) tells if the
        interlock circuit is open or closed. The second byte (MSB) tells where
        the interlock circuit is open, if relevant.

        === === =======================================
        MSB LSB Description
        === === =======================================
        -   0   Interlock off (interlock circuit open)
        0   1   Waiting for interlock reset
        0   2   Interlock is OK
        1   0   Front panel interlock / key switch off
        2   0   Door switch open
        3   0   External module interlock
        4   0   Application interlock
        5   0   Internal module interlock
        6   0   Interlock power failure
        7   0   Interlock disabled by light source
        255 -   Interlock circuit failure
        === === =======================================

        Return
        ------
        tuple(int, str)
            (LSB, Desription) returns result according to table in manual.
        """
        register_address = 0x32
        comm_result, reading = nkt.registerRead(self.portname,
                                                self.module_address,
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
            self._interlock_status = (LSB, 'Interlocked: %s' % reason)

        elif LSB == 1:
            self._interlock_status = (LSB, 'Waiting for interlock reset')

        elif LSB == 2:
            self._interlock_status = (LSB, 'Interlock is OK')
        return self._interlock_status

    @property
    def pulse_picker_ratio(self):
        """
        Get pulse picker ratio by reading register 0x34.

        Manual:
        For SuperK EXTREME Systems featuring the pulse picker option, the
        divide ratio for the pulse picker can be controlled with the pulse
        picker ratio register. Note: When reading the pulse picker value, an
        8-bit unsigned integer will be returned if the ratio is lower than 256,
        and a 16-bit unsigned integer otherwise.This is for historical reasons.

        Return
        ------
        ratio : int
            Pulse picker divide ratio
        """
        register_address = 0x34
        comm_result, ratio = nkt.registerReadU16(self.portname,
                                                 self.module_address,
                                                 register_address, -1)
        self._pulse_picker_ratio = ratio
        return self._pulse_picker_ratio

    @property
    def watchdog_interval(self):
        """
        Get the watchdog interval by reading register 0x36.

        Manual:
        The system can be set to make an automatic shut-off (laser emission
        only – not electrical power) in case of lost communication. The value
        in the watchdog interval register determines how many seconds with no
        communication the system will tolerate. If the value is 0, the
        feature is disabled. 8-bit unsigned integer.

        Return
        ------
        ratio : int
            Pulse picker divide ratio
        """
        register_address = 0x36
        comm_result, interval = nkt.registerReadU8(self.portname,
                                                   self.module_address,
                                                   register_address, -1)
        self._watchdog_interval = interval
        return self._watchdog_interval

    @property
    def power_level(self):
        """
        Get power level setpoint with 0.1% precision.

        Read register 0x37 and converts from permille to percent.

        Return
        ------
        power_level : float
            Power level setpoint in percent w/ 0.1% precision.
        """
        register_address = 0x37
        comm_result, power = nkt.registerReadU16(self.portname,
                                                 self.module_address,
                                                 register_address, -1)
        self._power_level = power / 10
        return self._power_level

    @property
    def current_level(self):
        """
        Get current level setpoint with 0.1% precision.

        Read register 0x38 and converts from permille to percent.

        Return
        ------
        current_level : float
            Current level setpoint in percent w/ 0.1% precision.
        """
        register_address = 0x38
        comm_result, current = nkt.registerReadU16(self.portname,
                                                   self.module_address,
                                                   register_address, -1)
        self._current_level = current / 10
        return self._current_level

    @property
    def nim_delay(self):
        """
        Get NIM trigger delay time.

        Reads register 0x38 and converts from int value to delay in seconds.

        Manual:
        On systems with NIM trigger output, the delay of this trigger signal
        can be adjusted with the NIM delay register. The input for this
        register should be an unsigned 16-bit value from 0 to 1023. The range
        is 0 – 9.2 ns. The average step size is 9 ps.

        Return
        ------
        nim_delay : float
            Delay time given in seconds.
        """
        register_address = 0x38
        step = 9e-12  # Step size for delay is 9 ps
        comm_result, delay = nkt.registerReadU16(self.portname,
                                                self.module_address,
                                                register_address, -1)
        self._nim_delay = delay * step
        return self._nim_delay

    def set_emission(self, state):
        """
        Change emission state of laser to on/off

        Uses nktp_dll to write to register 0x30.

        Parameters
        ----------
        state : bool
            True turns laser on, false turns emission off
        """
        register_address = 0x30
        if state is True:
            nkt.registerWriteU8(self.portname, self.module_address,
                                register_address, 0x03, -1)
        elif state is False:
            nkt.registerWriteU8(self.portname, self.module_address,
                                register_address, 0x00, -1)

    def set_mode(self, setup_key):
        """
        Sets the "setup" of the laser according to options in manual.

        Checks value provided is withing Extreme.setup_options.keys(),
        then writes to register 0x16. Get current status w/
        Extreme.setup_status

        Manual:
        With the Setup register, the operation mode of the SuperK EXTREME
        System can be controlled. The possible values are listed below;
        however, in some systems, not all modes are available.16-bit unsigned
        integer.

        0: Constant current mode
        1: Constant power mode
        2: Externally modulated current mode
        3: Externally modulated power mode
        4: External feedback mode (Power Lock)

        Parameters
        ----------
        setup_key : int
            Interger corresponding to a key inside Extreme.setup_options
        """
        register_address = 0x16
        if setup_key in Extreme.setup_options.keys():
            nkt.registerWriteU8(self.portname, self.module_address,
                                register_address, setup_key, -1)
            print('Mode set to: ', self.setup_status)
        else:
            print('Warning: Invalid Key Provided')
            print('Mode remains as: ', self.setup_status)

    def set_interlock(self, value):
        """
        Reset or trip interlock with >0 or 0, respectively.

        Manual:
        If the door interlock is in place, the key switch on the front plate is
        in On position and the External bus is terminated with e.g. a bus
        defeater then the Interlock circuit can be reset via the Interbus
        interface by sending a value greater than 0 to the Interlock register.
        Additionally, the opposite function (switching interlock relays off)
        can be done by sending the value 0 to the interlock register.

        Parameters
        ----------
        value: int
            0 trips interlock. >0 resets interlock.

        """
        register_address = 0x32
        if value > 0:
            value = 1
        else:
            value = 0
        nkt.registerWriteU8(self.portname, self.module_address,
                            register_address, value, -1)

    def set_pulse_picker_ratio(self, ratio):
        """
        Sets pulse picker ratio by writing register 0x34.

        Manual:
        For SuperK EXTREME Systems featuring the pulse picker option, the
        divide ratio for the pulse picker can be controlled with the pulse
        picker ratio register.

        Parameters
        ----------
        ratio : int
            Interger corresponding to a key inside Extreme.setup_options
        """
        register_address = 0x34
        if type(ratio) is int:
            nkt.registerWriteU16(self.portname, self.module_address,
                                 register_address, ratio, -1)
        else:
            raise ValueError('ratios needs to be int')

    def set_watchdog_interval(self, timeout):
        """
        Set the watchdog interval by calling registerWriteU8 on 0x36.

        Manual:
        The system can be set to make an automatic shut-off (laser emission
        only – not electrical power) in case of lost communication. The value
        in the watchdog interval register determines how many seconds with no
        communication the system will tolerate. If the value is 0, the
        feature is disabled. 8-bit unsigned integer.

        Parameters
        ----------
        timeout : int
            time (seconds) the system will toleratre for communication loss.
        """
        register_address = 0x36
        if type(timeout) is int:
            nkt.registerWriteU8(self.portname, self.module_address,
                                register_address, timeout, -1)
        else:
            raise ValueError('timeout needs to be int')

    def set_power(self, power):
        """
        Set power level setpoint with 0.1% precision.

        Converts from percent to permille and write register 0x37.

        Parameters
        ----------
        power : float
            Power level setpoint in percent w/ 0.1% precision. (0 <= P <= 100)
        """
        register_address = 0x37
        setpoint = int(power * 10)
        if (power >= 0) and (power <= 100):
            nkt.registerWriteU16(self.portname, self.module_address,
                                 register_address, setpoint, -1)
        else:
            self.set_emission(False)
            self.set_power(0)
            raise ValueError("Power must be between 0 and 100%\n"
                             "Setting output to 0.")

    def set_current(self, current):
        """
        Set current level setpoint with 0.1% precision.

        converts from percent to permille and write register 0x38.

        Parameters
        ----------
        current : float
            Current level setpoint in percent w/ 0.1% precision (0 <= I <= 100)
        """
        register_address = 0x38
        setpoint = int(current*10)
        if (current >= 0) and (current <= 100):
            nkt.registerWriteU16(self.portname, self.module_address,
                                 register_address, setpoint, -1)
        else:
            self.set_emission(False)
            self.set_current(0)
            raise ValueError("Current must be between 0 and 100%\n"
                             "Setting output to 0.")

    def set_nim_delay(self, nim_delay):
        """
        Set NIM trigger delay time.

        Writes register 0x38 and converts from delay time in seconds to
        corresponding int value using setpoint = int(nim_delay/9e-12)

        Manual:
        On systems with NIM trigger output, the delay of this trigger signal
        can be adjusted with the NIM delay register. The input for this
        register should be an unsigned 16-bit value from 0 to 1023. The range
        is 0 – 9.2 ns. The average step size is 9 ps.

        Parameters
        ----------
        nim_delay : float
            Delay time given in seconds. (0 <= nim_delay <= 9.207e-9)
        """
        register_address = 0x38
        step = 9e-12  # Step size for delay is 9 ps
        int_delay = int(nim_delay/step)
        if (int_delay >= 0) and (int_delay <= 1023):
            nkt.registerWriteU16(self.portname, self.module_address,
                                 register_address, int_delay, -1)
        else:
            print('NIM Delay Value Out of Range (0 <= Delay <= 9.207e-9)')

    def print_status(self):
        """
        Read system status in bytes, translate to str, print.

        Reads system status using registerReadU16 on register 0x66.
        Translates binary into str for of equipment status through
        Extreme.status_messages.

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
                print(Extreme.status_messages[index])

        return (bits)

    def test_read_funcs(self):
        outputs = (self.system_type,
                   self.inlet_temperature,
                   self.emission_state,
                   self.setup_status,
                   str(self.interlock_status),
                   self.pulse_picker_ratio,
                   self.watchdog_interval,
                   self.power_level,
                   self.current_level,
                   self.nim_delay)
        output_msg = ("""
        System type = %s
        Inlet Temperature = %s
        Emission state = %s
        Setup status = %s
        Interlock Status = %s
        Pulse picker ratio = %s
        Watchdog interval = %s
        Power level = %s
        Current level = %s
        NIM delay = %s
        """ % outputs)
        print(output_msg)


if __name__ == "__main__":
    laser = Extreme()
    laser.print_status()
    laser.test_read_funcs()
