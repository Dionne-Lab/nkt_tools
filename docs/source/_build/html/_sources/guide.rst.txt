==========
User Guide
==========

Introduction
============
:mod:`nkt_tools` provides python based tools for the automation of NKT Photonics devices. :mod:`nkt_tools` utilizes the NKTPDLL provided by NKT, wrapping over the DLL with simplified python classes (e.g. :class:`~nkt_tools.extreme.Extreme`, :class:`~nkt_tools.varia.Varia`).

Without :mod:`nkt_tools`, using the NKTPDLL requires reading/writing formatted values to specific byte registers with commands like :func:`nkt_tools.NKTP_DLL.registerWriteU16`, at times requiring the user to tranlate bytes to some values according to the manual.

.. code-block:: python

    import NKTP_DLL as nkt
    nkt.registerWriteU8('COM27', 15, 0x30, 0x03, -1)

:mod:`nkt_tools` transforms this into a more simple verion:

.. code-block:: python

    from nkt_tools.extreme import Extreme
    laser = Extreme()
    laser.set_emission(True)

.. note::
    There is also a Matlab package to control an NKT Laser+Varia if Matlab is you cup of tea (`<https://github.com/villadsegede/NKTcontrol>`_)

Installation
============
:mod:`nkt_tools` functions as a stand alone package. Necessary file for connecting with NKT hardware is included in the package already, so the user should only need to pip install the package.

.. code-block::

    pip install nkt_tools

Extreme/Fianium
===============

.. code-block:: python

    from nkt_tools.extreme import Extreme
    laser = Extreme()
    laser.set_emission(True)

Varia
=====

.. code-block:: python

    from nkt_tools.varia import Varia
    varia = Varia()
    varia.long_setpoint = 600
    varia.short_setpoint = 550

Other NKT devices
=================

So far, I've only written the package to support NKT Varia and Extreme/Fianium lasers. I don't have plans to expand this the library to all supported NKT products, but addition of new devices should be relatively straight forward. To assist interested developers with this process, I've written :doc:`development notes </development_notes>` detailing the process I went through to develop the :mod:`Varia <nkt_tools.varia>` and :mod:`Extreme <nkt_tools.extreme>` modules. My hope is that these modules serve as examples for interested devleopers to make it easier to create new modules for other devices supported by the NKTPDLL. If you do write a new module, please submit a pull request on GitHub so it can be added to the main package!

Additionally, the entire DLL can be accessed through :mod:`nkt_tools.NKTP_DLL`. All supported devices can be interacted with through registerRead/Write commands by following the :download:`instruction manual <../../manuals/SDK Instruction manual.pdf>`.

I tried to leverage AI to automatically generate some modules, but found the formatting produced to be too inconsistent. I posted notes about my attempt in the :ref:`chatgpt` section of the :doc:`/development_notes`.
