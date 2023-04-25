"""Python module to control NKT Varia."""
import NKTP_DLL as nkt


class Varia:
    def __init__(self, portname=None):
        print('init')
        self.portname = None  #: COM port name. Autosearches if not provided.
        self.module_address = None  #: 16-25 for Varia. Auto searches in init.
        if portname:  # Allow user to init specific NKT Laser on portname
            self.portname = portname
        else:
            # Open available ports
            nkt.openPorts(nkt.getAllPorts(), 1, 1)

            # Get open NKT ports
            portlist = nkt.getOpenPorts().split(',')
            varia_found = False

            for portName in portlist:

                # get binary devList of connected nkt devices
                result, devList = nkt.deviceGetAllTypes(portName)

                # Address for Varia depends on specific hardware.
                # Search possible addresses (16-25) searching for connection.
                for n in range(9):
                    trial_address = 16 + n  # Address = 16 + Rotary switch # (0..9)
                    device_type = devList[trial_address]
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
                            self.portname = portName
                            self.module_address = trial_address

    def monitor_input(self):
        register_address = 0x13
        result = nkt.registerRead(self.portname, self.module_address,
                                  register_address, -1)
        print(result)
        output_power = 'not yet implemented'

        return output_power

    def nd_setpoint(self, value):
        register_address = 0x32
        value = int(value/10)  # convert percent to permille
        nkt.registerWrite(self.portname, self.module_address,
                          register_address, value, -1)

    def swp_setpoint(self, value):
        register_address = 0x33
        value = int(value/10)  # convert nm to 1/10 nm
        nkt.registerWrite(self.portname, self.module_address,
                          register_address, value, -1)

    def lwp_setpoint(self, value):
        register_address = 0x34
        value = int(value/10)  # convert nm to 1/10 nm
        nkt.registerWrite(self.portname, self.module_address,
                          register_address, value, -1)

    def get_status(self):
        register_address = 0x66
        result = nkt.registerRead(self.portname, self.module_address,
                                  register_address, -1)
        print(result)

    def demo_read_funcs(self):
        register_address = 0x66
        print( 'registerRead: ',
              nkt.registerRead(self.portname, self.module_address,
                               register_address, -1))
        print( 'registerReadU8: ',
              nkt.registerReadU8(self.portname, self.module_address,
                               register_address, -1))
        print( 'registerReadS8: ',
              nkt.registerReadS8(self.portname, self.module_address,
                               register_address, -1))
        print( 'registerReadU16: ',
              nkt.registerReadU16(self.portname, self.module_address,
                               register_address, -1))
        print( 'registerReadU32: ',
              nkt.registerReadU32(self.portname, self.module_address,
                               register_address, -1))
        print( 'registerReadF32: ',
              nkt.registerReadU32(self.portname, self.module_address,
                               register_address, -1))
        print( 'registerReadAscii: ',
              nkt.registerReadAscii(self.portname, self.module_address,
                               register_address, -1))
