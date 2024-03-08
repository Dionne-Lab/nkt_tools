"""
Classes for the different NKT Products in order to communicate with them.

classes
------
General
    Common class for all modules.
Basik
    Communication with the Basik module.
"""

from enum import IntEnum, IntFlag
from typing import TypeVar

import nkt_tools.NKTP_DLL as nkt


T = TypeVar("T")


# return is always 0 for success, so return == Error
def handle_register_errors(error_code: int) -> None:
    """Handle an error of register result type."""
    if error_code:
        "error == 15: Application is busy."
        raise ConnectionError(nkt.RegisterResultTypes(error_code))


def interpret_read_response(response: tuple[int, T]) -> T:
    """Interpret the response of a register read."""
    handle_register_errors(response[0])
    return response[1]


def interpret_write_response(response: int) -> None:
    """Interpret the response of a register write."""
    return handle_register_errors(response)


def handle_device_error(error_code: int) -> None:
    """Handle an error of device result type."""
    if error_code:
        raise ConnectionError(nkt.DeviceResultTypes(error_code))


def interpret_device_read(response: tuple[int, T]) -> T:
    """Interpret the read response of a device type connection."""
    handle_register_errors(response[0])
    return response[1]


class General:
    """Base communication with all NKT Photonics modules."""

    def __init__(self, COM, address, *args, **kwargs):
        """
        Initialize the module.

        Parameters
        ----------
        COM : int
            Number of COM port.
        address: int
            Module address
        """
        self.device = COM, address

    def __del__(self):
        """Close the Ports on deletion."""
        return self.closePorts()

    def closePorts(self):
        """Close the Port and return PortResultTypes."""
        # TODO what is the error message, if the port is not present
        # never raise an error?
        error = nkt.closePorts("")
        if error:  # closes all ports because of empty string
            raise ConnectionError(nkt.PortResultTypes(error))

    def setPorts(self, COM=None, autoMode=True, liveMode=True):
        """
        Configure Ports for faster readout.

        - setPorts creates objects which have to live in the creating thread.
          Such that it has to be run in the thread, where the device is handled.
        - It's not necessary for read/write.
        - This command takes a few seconds.
        - Call this method again in order to change the configuration.

        Parameters
        --------
        COM : int
            number of the COM-Port
        autoMode : bool
            find the modules and create devices.
        liveMode : bool
            tell the rack to monitor the registers of the module.
        """
        # TODO what is the advantag/disadvantage of liveMode?
        COM = COM or self.device[0]
        error = nkt.openPorts(COM, 1 if autoMode else 0, 1 if liveMode else 0)
        if error:
            raise ConnectionError(nkt.PortResultTypes(error))
        return error

    def getModuleType(self) -> int:
        """Get the type of the module."""
        return self.module_type

    @property
    def module_type(self):
        """Get the type of the module."""
        return interpret_device_read(nkt.deviceGetType(*self.device))

    def getSerialNumber(self) -> str:
        """Get the serial number of the module."""
        return self.serial_number

    @property
    def serial_number(self) -> str:
        """Get the serial number of the module."""
        # string 0x65
        return interpret_device_read(nkt.deviceGetModuleSerialNumberStr(*self.device))

    """
    it is not necessary to open a port or create a device
    nkt.registerReadxy(portname, devId, regId, index)
    registerWritexy(portname, devId, regId, value, index)
    xy=type+size. for example U8
    index is byte counted, typically -1. it can be used to extract a value from
    a larger register
    """


class BASIK(General):
    """Communication the the BASIK Module by NKT, which begins with K1x2.

    - Module type number is 0x33.
    - Standard module address is 0x1, but may change if several are present.
    """

    # DEFINITION OF DIFFERENT BYTES

    # define the status bits in 0x66
    statusBits = {
        "emission": 0x1,
        "interlockOff": 0x2,
        "moduleDisabled": 0x10,
        "lowSupplyVoltage": 0x20,
        "temperatureOutOfRange": 0x40,
        "waitForTempDrop": 0x800,
        "wavelengthStabilized": 0x4000,
        "error": 0x8000,
    }
    """
    WaitForTempDrop: Waiting for temperature to drop
    WavelengthStabilized is X15 only
    Error: error code present (register 0x67)
    """

    class Status(IntFlag):
        EMISSION = 0x1
        INTERLOCK_OFF = 0x2
        MODULE_DISABLED = 0x10
        LOW_SUPPLY_VOLTAGE = 0x20
        TEMPERATURE_OUT_OF_RANGE = 0x40
        WAIT_FOR_TEMP_DROP = 0x800
        WAVELENGTH_STABILIZED = 0x4000
        ERROR = 0x8000

    # definition of error values in 0x67
    errorValues = {
        0: "no error",
        2: "interlock",
        3: "low voltage",
        7: "module temperature range",
        8: "module disabled",
    }

    # definition of the setup bits in 0x31
    # TODO verify settings
    setupBits = {
        "wlModulationRange": 0x2,
        "wlModulationDC": 0x8,
        "wlModulationInternal": 0x10,
        "wlModulationExternal": 0x20,
        "signalOutput": 0x40,
        "constantCurrent": 0x200,
        "autostart": 0x800,
    }
    """
    Wl == Wavelength
    Bit 0  # -
    Bit 1  # narrow modulation range instead of wide
    Bit 2  #
        # SDK: Enable external wavelength modulation
    Bit 3  # Wl modulation DC coupling
    Bit 4  # internal Wl modulation
    Bit 5  # external Wl modulation
        # SDK: enable modulation output 'ModulationOutput'
    Bit 6  # Function generator - outputting the signal
    Bit 8  #
        # SDK: pump operation constant current
    Bit 9  # 0: constant Power, 1: constant current
        # SDK: external amplitude modulation source:
            'AmplitudeModulationExternal': 0x200,
    Bit 11 # Auto-start: start emission on power up
    """

    class Setup(IntFlag):
        WL_MODULATION_RANGE = 0x2
        WL_MODULATION_DC = 0x8
        WL_MODULATION_INTERNAL = 0x10
        WL_MODULATION_EXTERNAL = 0x20
        SIGNAL_OUTPUT = 0x40
        CONSTANT_CURRENT = 0x200
        AUTOSTART = 0x800

    # modulation setup bits in 0xB7
    modulationBits = {
        "amplitudeFrequency": 0x1,
        "amplitudeWaveform": 0x4,
        "wavelengthFrequency": 0x10,
        "wavelengthWaveform": 0xC0,
    }
    """
    Amplitude/Wavelength Frequency selects between the two saved frequencies in
        the arrays
    AmplitudeWaveform: 0==Sine, 1==Triangle
    Bit 3 is safed for future use, set to 0
    WavelengthWaveform: 0x0 == Sine, 0x40==Triangle, 0x80==Sawtooth (rising),
        0xC0==Sawtooth falling
    """

    class Modulation(IntFlag):
        AMPLITUDE_FREQUENCY_2 = 0x1
        AMPLITUDE_WAVEFORM_TRIANGLE = 0x4
        WAVELENGTH_FREQUENCY_2 = 0x10
        WAVELENGTH_WAVEFORM_TRIANGLE = 0x40
        WAVELENGTH_WAVEFORM_SAWTOOTH = 0x80

    # modulation waveform values
    class Waveform(IntEnum):
        SINE = 0
        TRIANGLE = 1
        SAWTOOTH = 2
        INVERSE_SAWTOOTH = 3

    modulationWaveform = {0x0: "sine", 0x1: "triangle", 0x2: "sawtooth", 0x3: "inverseSawtooth"}

    # trigger setup bits in 0xB4
    triggerBits = {"output": 0x2, "sawtooth": 0x4, "emission": 0x10}
    """
    Bit 1  # Use the trigger contacts as output
    Bit 2  # Use the trigger for sawtooth wavelength modulation
    Bit 4  # Use the trigger to enable emission/inform about emission
    Bit 2 and Bit 4 cannot be used simultaneously
    """

    class Trigger(IntFlag):
        OUTPUT = 0x2
        SAWTOOTH = 0x4
        EMISSION = 0x10

    def __init__(self, COM: str, address: int = 0x1, wlRange=[-350, 350], *args, **kwargs):
        """
        Create the module and read the central wavelength.

        Parameters
        ----------
        COM : str
            Name of the COM Port.
        address : int, optional
            Device address. The default is 0x1.
        wlRange : list of two ints, optional
            Wavelength range around central wavelength in pm.
            The default is [-350, 350].
        """
        super().__init__(COM, address, *args, **kwargs)
        self.wlRange = wlRange

    @property
    def emission_enabled(self):
        """Control emission status (bool)."""
        return self.Status.EMISSION in self.status

    @emission_enabled.setter
    def emission_enabled(self, emission):
        # U8 0x30
        response = nkt.registerWriteU8(*self.device, 0x30, 1 if emission else 0, -1)
        return interpret_write_response(response=response)

    @property
    def setup(self) -> Setup:
        """Control the setup byte with :attr:`Setup` enum."""
        value = interpret_read_response(nkt.registerReadU16(*self.device, 0x31, -1))
        return BASIK.Setup(value)

    @setup.setter
    def setup(self, value: Setup):
        response = nkt.registerWriteU16(*self.device, 0x31, value, -1)
        return interpret_write_response(response=response)

    def update_setup(self, set: Setup | int = 0, unset: Setup | int = 0):
        """Update the setup, setting those defined in `set` and unsetting those in `unset`."""
        setup = self.setup
        self.setup = (setup | set) & ~unset

    @property
    def power_setpoint(self) -> float:
        """Control the output power setpoint in mW."""
        # U16 0x22 in 1/100 mW
        value = interpret_read_response(nkt.registerReadU16(*self.device, 0x22, -1))
        return value / 100

    @power_setpoint.setter
    def power_setpoint(self, value: float) -> None:
        setpoint = int(value * 100)
        return interpret_write_response(nkt.registerWriteU16(*self.device, 0x22, setpoint, -1))

    @property
    def wavelength_setpoint(self):
        """Control the wavelength setpoint in nm."""
        # S16 0x2A
        value = interpret_read_response(nkt.registerReadS16(*self.device, 0x2A, -1))
        return self.central_wavelength + value / 1e4

    @wavelength_setpoint.setter
    def wavelength_setpoint(self, value):
        setpoint = round((value - self.central_wavelength) * 1e4)
        test = self.wlRange[0] * 10 <= setpoint and setpoint <= self.wlRange[1] * 10
        assert test, f"Wavelength range is {self.wlRange}"
        return interpret_write_response(nkt.registerWriteS16(*self.device, 0x2A, setpoint, -1))

    @property
    def central_wavelength(self) -> float:
        """Get central wavelength in nm."""
        # U32 0x32. Wavelength in 1/10 pm if offset is zero
        try:
            return self._central_wavelength
        except AttributeError:
            value = interpret_read_response(nkt.registerReadU32(*self.device, 0x32, -1))
            value /= 1e4
            self._central_wavelength = value
            return value

    @property
    def wavelength(self) -> float:
        """Get the current wavelength in nm."""
        # S32 0x72 in 1/10 pm from standardWavelength
        value = interpret_read_response(nkt.registerReadS16(*self.device, 0x72, -1))
        return self.central_wavelength + value / 1e4

    @property
    def temperature(self) -> float:
        # S16 0x1C in 1/10 °C
        value = interpret_read_response(nkt.registerReadS16(*self.device, 0x1C, -1))
        return value / 10  # in °C

    @property
    def status(self):
        """Get status of the device."""
        value = interpret_read_response(nkt.registerReadU16(*self.device, 0x66, -1))
        return BASIK.Status(value)

    def getError(self):
        """Get the current error."""
        # TODO register type
        # TODO returns an error
        value = interpret_read_response(nkt.registerReadU16(*self.device, 0x67, -1))
        return self.errorValues.get(value)

    @property
    def power(self):
        """Get the current output power in mW."""
        value = interpret_read_response(nkt.registerReadU16(*self.device, 0x17, -1))
        return value / 100  # in mW

    """
    Additional registers:
        0x3A Emission delay time
    """

    # MODULATION FUNCTIONS

    # Wavelength Modulation
    @property
    def wavelength_modulation_frequency1(self) -> float:
        """Control the first wavelength modulation frequency in Hz."""
        # twice F32 0xB8. Array of two 32 bit float values between which can be
        # switched. Unit is Hz. index is 0 for the first, 4 for the second frequency.
        return interpret_read_response(nkt.registerReadF32(*self.device, 0xB8, index=0))

    @wavelength_modulation_frequency1.setter
    def wavelength_modulation_frequency1(self, value: float) -> None:
        assert 0 <= value and value <= 1e5, "Frequency is out of range [8mHz, 100kHz]."
        return interpret_write_response(nkt.registerWriteF32(*self.device, 0xB8, value, 0))

    @property
    def wavelength_modulation_frequency2(self) -> float:
        """Control the second wavelength modulation frequency in Hz."""
        return interpret_read_response(nkt.registerReadF32(*self.device, 0xB8, index=4))

    @wavelength_modulation_frequency2.setter
    def wavelength_modulation_frequency2(self, value: float) -> None:
        assert 0 <= value and value <= 1e5, "Frequency is out of range [8mHz, 100kHz]."
        return interpret_write_response(nkt.registerWriteF32(*self.device, 0xB8, value, 4))

    @property
    def wavelength_modulation_level(self) -> int:
        """Control the wavelength modulation level in promille."""
        return interpret_read_response(nkt.registerReadU16(*self.device, 0x2B, -1))

    @wavelength_modulation_level.setter
    def wavelength_modulation_level(self, value: int) -> None:
        assert 0 <= value and value <= 1000, "Level is out of range [0,1000]."
        return interpret_write_response(nkt.registerWriteU16(*self.device, 0x2B, value, -1))

    @property
    def wavelength_modulation_offset(self) -> int:
        """Control the wavelength modulation offset in promille."""
        return interpret_read_response(nkt.registerReadS16(*self.device, 0x2F, -1))

    @wavelength_modulation_offset.setter
    def wavelength_modulation_offset(self, value: int) -> None:
        # this feature requires setupBits 3 & 4 (DC Coupling and internal
        # modulation)
        assert abs(value) <= 1000, "Level is out of range [-1000,1000]."
        return interpret_write_response(nkt.registerWriteS16(*self.device, 0x2F, value, -1))

    # Amplitude Modulation
    def getAmplitudeModulationFrequency(self, index=0):
        """Get the amplitude modulation frequency in Hz at index."""
        # twice F32 0xB8. Array of two 32 bit float values between which can be
        # switched. Unit is Hz.
        assert index in [0, 4], "Index is 0 or 4."
        return interpret_read_response(nkt.registerReadF32(*self.device, 0xBA, index))

    def setAmplitudeModulationFrequency(self, frequency, index=0):
        """Set the amplitude modulation frequency in Hz between 8mHz and 100 kHz."""
        # for sawtooth only up to 200 Hz
        assert 0 <= frequency and frequency <= 1e5, "Frequency is out of range [8mHz, 100kHz]."
        assert index in [0, 4], "Index is 0 or 4."
        return interpret_write_response(nkt.registerWriteF32(*self.device, 0xBA, frequency, index))

    def getAmplitudeModulationLevel(self):
        """Get the relative amplitude modulation level in promille."""
        value = interpret_read_response(nkt.registerReadU16(*self.device, 0x2C, -1))
        return value

    def setAmplitudeModulationLevel(self, level):
        """Set the relative amplitude modulation level in promille."""
        assert 0 <= level and level <= 1000, "Level is out of range [0,1000]."
        return interpret_write_response(nkt.registerWriteU16(*self.device, 0x2C, level, -1))

    @property
    def modulation_setup(self) -> Modulation:
        """Control the modulation setup with :attr:`Modulation` enum.

        Requires :attr:`setup` set to modulation DC coupled and internal modulation.
        """
        value = interpret_read_response(nkt.registerReadU16(*self.device, 0xB7, -1))
        return BASIK.Modulation(value)

    @modulation_setup.setter
    def modulation_setup(self, value: Modulation) -> None:
        interpret_write_response(nkt.registerWriteU16(*self.device, 0xB7, value, -1))

    def update_modulation_setup(self, set=0, unset=0):
        """Update the modulation setup, setting those in set and unsetting those in unset."""
        setup = self.modulation_setup
        self.modulation_setup = (setup | set) & ~unset

    @property
    def wavelength_modulation_enabled(self) -> bool:
        """Control whether the wavelength modulation is enabled."""
        return bool(interpret_read_response(nkt.registerReadU8(*self.device, 0xB5, -1)))

    @wavelength_modulation_enabled.setter
    def wavelength_modulation_enabled(self, value: bool) -> None:
        # 1 enabled, 0 disabled
        return interpret_write_response(nkt.registerWriteU8(*self.device, 0xB5, int(value), -1))

    @property
    def amplitude_modulation_enabled(self) -> bool:
        """Control whether the amplitude modulation is enabled."""
        # only in registerfiles defined!
        return bool(interpret_read_response(nkt.registerReadU8(*self.device, 0xB6, -1)))

    @amplitude_modulation_enabled.setter
    def amplitude_modulation_enabled(self, value: bool) -> None:
        # 1 enabled, 0 disabled
        return interpret_write_response(nkt.registerWriteU8(*self.device, 0xB6, int(value), -1))

    @property
    def trigger_setup(self) -> Trigger:
        """Control the trigger setup with :attr:`Trigger`."""
        # only in device manual defined
        value = interpret_read_response(nkt.registerReadU8(*self.device, 0xB4, -1))
        return BASIK.Trigger(value)

    @trigger_setup.setter
    def trigger_setup(self, value):
        return interpret_write_response(nkt.registerWriteU8(*self.device, 0xB4, value, -1))
