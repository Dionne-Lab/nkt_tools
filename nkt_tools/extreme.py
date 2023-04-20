"""Python module to control NKT Extreme and Fianium Lasers."""
import NKTP_DLL as nkt


class Extreme:
    def __init__(self):
        print('init class')
        self.portname = 'COM27'
        self.module_address = 15


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
        result = nkt.registerRead(self.portname, self.module_address,
                                  register_address, -1)
        print(result)


def find_modules():
    print('Find modules on all existing and accessible ports - Might take a few seconds to complete.....')
    if (nkt.getLegacyBusScanning()):
        print('Scanning following ports in legacy mode:', nkt.getAllPorts())
    else:
        print('Scanning following ports in normal mode:', nkt.getAllPorts())

    # Use the openPorts function with Auto & Live settings. This will scan and detect modules
    # on all ports returned by the getAllPorts function.
    # Please note that a port being in use by another application, will show up in this list but will
    # not show any devices due to this port being inaccessible.
    print(nkt.openPorts(nkt.getAllPorts(), 1, 1))

    # All ports returned by the getOpenPorts function has modules (ports with no modules will automatically be closed)
    print('Following ports has modules:', nkt.getOpenPorts())

    # Traverse the getOpenPorts list and retrieve found modules via the deviceGetAllTypes function
    portlist = nkt.getOpenPorts().split(',')
    for portName in portlist:
        result, devList = nkt.deviceGetAllTypes(portName)
        for devId in range(0, len(devList)):
            if (devList[devId] != 0):
                print('Comport:', portName, 'Device type:', "0x%0.2X" % devList[devId], 'at address:', devId)

    # Close all ports
    closeResult = nkt.closePorts('')
    print('Close result: ', nkt.PortResultTypes(closeResult))
