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

**ReadtheDocs Page:**
https://nkt-tools.readthedocs.io/en/latest/

**PyPI Page:**
https://pypi.org/project/nkt-tools/

Please also check out my related package, CataLight, which automates data collection and processing for photocatalysis research!

**ReadtheDocs Page:**
https://catalight.readthedocs.io/en/latest/

**PyPI Page:**
https://pypi.org/project/catalight/

Citing
^^^^^^

.. image:: https://zenodo.org/badge/629268582.svg
   :target: https://zenodo.org/badge/latestdoi/629268582

If you utilize the nkt_tools package for you research, we'd appreciate you referencing our Zenodo upload such that others might find our work:

Briley Bourgeois, & Jennifer Dionne. (2023). Dionne-Lab/nkt_tools: 0.0.8 (0.0.8). Zenodo. https://doi.org/10.5281/zenodo.8145215
