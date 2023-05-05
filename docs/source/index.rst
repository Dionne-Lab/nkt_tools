.. nkt_tools documentation master file, created by
   sphinx-quickstart on Wed May  3 19:01:00 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to nkt_tools's documentation!
=====================================
nkt_tools turns this:

.. code-block:: python

    import NKTP_DLL as nkt
    nkt.registerWriteU8('COM27', 15, 0x30, 0x03, -1)

into this:

.. code-block:: python

    from nkt_tools.extreme import Extreme
    laser = Extreme()
    laser.set_emission(True)

:mod:`nkt_tools` is a wrapper around NKT's DLL to provide object oriented interaction with NKT products. NKT Extreme/Fianium lasers and the Varia system are currently supported. Additional systems can be accessed through the DLL by using the registerRead/Write functions within :mod:`nkt_tools.NKTP_DLL` or interested developers can write new modules by following the :doc:`development notes </development_notes>` provided.

.. toctree::
   :maxdepth: 3
   :caption: Manual

   guide
   examples
   development_notes


.. toctree::
   :maxdepth: 3
   :caption: Documentation

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
