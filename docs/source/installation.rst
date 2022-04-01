Installing pyAGE
================

Installation via pip
--------------------

The easiest way is to install pyAGE with the help of pip, the Python package manager, which comes bundled with Python by default. It is as easy as typing

.. code-block:: text

   pip install python-pyage
   
This will make sure to always install the latest version that is considered a release version from PyPI, the Python package index. Using pip will enable you to always stay up to date on all the latest features pyAGE has to offer.

Make sure to take a look into the :ref:`additional-packages` section and install additional packages as needed.

Installation from source
------------------------

If you for some reason don't want to install from pip, because you want to test the latest bleeding edge code or cannot install from PyPI, you can also install pyAGE from source. You'll need to clone the repository via git and install it by running the setup.py file found within the repository. The following example demonstrates the process.

.. code-block:: text

   git clone https://github.com/Timtam/pyAGE.git
   cd pyAGE
   python setup.py install

This installation method is intended for advanced users however, thus i'm sure that you can help yourself in case anything goes wrong. Feel free to open an issue on GitHub however if you encounter any problems.

Make sure to take a look into the :ref:`additional-packages` section and install additional packages as needed.

.. _additional-packages:

Additional packages
===================

pyAGE depends on various packages which will not be installed by default with it because you're free to decide on your setup as freely as possible. The following table therefore lists all optional and default packages that pyAGE can utilize natively and their purpose. Feel free to install and use them as needed.

.. list-table:: Additional packages
   :widths: 5 5 5 30 55
   :header-rows: 1
   
   * - Python package name
     - pyAGE module
     - platform(s) supported
     - purpose
     - notes
   * - cytolk
     - pyage.output_backends.tolk
     - Windows
     - Screen Reader support for NVDA, JAWS, System Access, Dolphin, Window-Eyes, Super Nova, ZoomText and SAPI5
     - will automatically be installed on Windows when installing pyAGE
   * - accessible_output2
     - pyage.output_backends.ao2
     - Windows, Mac OS, Linux
     - Screen Reader support for JAWS, NVDA, PC Talker, System Access, Window-Eyes, Dolphin, ZDSR, SAPI4 and SAPI5 on Windows, VoiceOver on Mac OS, eSpeak and Speech Dispatcher under Linux
     - the latest version of accessible_output2 on PyPI is outdated and e.g. lacks support for ZDSR under Windows. For that reason, you'll probably want to install directly from the Git repository here: `<https://github.com/accessibleapps/accessible_output2>`_
   * - synthizer
     - pyage.audio_backends.synthizer
     - Windows
     - Audio support
     - this is the default audio engine supported by pyAGE and will most likely receive the best support. Attempts will be made to add support for all major platforms with this package.
