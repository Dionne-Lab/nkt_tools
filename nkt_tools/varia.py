"""Python module to control NKT Varia."""
import NKTP_DLL as nkt


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
    
    def __init__(self, portname=None):
        print('init')
        self.portname = None  #: COM port name. Autosearches if not provided.
        self.module_address = None  #: 16-25 for Varia. Auto searches in init.
        self.device_type = None  #: This should update to 0x68 if init is right.
        
        if portname:  # Allow user to init specific NKT Laser on portname
            self.portname = portname
        
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
                result, devList = nkt.deviceGetAllTypes(portName)

                # Address for Varia depends on specific hardware.
                # Search possible addresses (16-25) searching for connection.
                for n in range(9):
                    trial_address = 16 + n  # Address = 16 + Rotary switch # (0..9)
                    try:
                        device_type = devList[trial_address]
                    except(IndexError):
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
                            self.portname = portName
                            self.module_address = trial_address
                            self.device_type = device_type
                            break
                
            # Close all ports
            closeResult = nkt.closePorts('')
            if varia_found:
                print('NKT Varia Found:')
                print('Comport: ', self.portname, 'Device type: ', "0x%0.2X" 
                      % self.device_type, 'at address:', self.module_address)
                
            else:
                print('No Varia Found')

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
        result, byte = nkt.registerReadU16(self.portname, self.module_address,
                                           register_address, -1)
        print(nkt.RegisterResultTypes(result))
        bits = bin(byte)
        for index, bit in enumerate(reversed(bits)):
            if bit == 'b':
                break
            elif bit == '1':
                print(Varia.status_messages[index])
                
        return(bits)

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
              nkt.registerReadF32(self.portname, self.module_address,
                               register_address, -1))
        print( 'registerReadAscii: ',
              nkt.registerReadAscii(self.portname, self.module_address,
                               register_address, -1))

varia = Varia()
varia.get_status()