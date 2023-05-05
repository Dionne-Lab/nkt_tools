# nkt_tools
This repository contains tools for accessing NKT photonics devices via python through the NKT SDK

nkt_tools turns this:

.. code-block:: python

    import NKTP_DLL as nkt
    nkt.registerWriteU8('COM27', 15, 0x30, 0x03, -1)

into this:

.. code-block:: python

    from nkt_tools.extreme import Extreme
    laser = Extreme()
    laser.set_emission(True)

nkt_tools is a wrapper around NKT's DLL to provide object oriented interaction with NKT products. NKT Extreme/Fianium lasers and the Varia system are currently supported. Additional systems can be accessed through the DLL by using the registerRead/Write functions within nkt_tools.NKTP_DLL or interested developers can write new modules by following the development notes provided.
