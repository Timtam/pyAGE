===============
pyAGE Changelog
===============

0.1.0-a7 (2022-04-12)
=====================

Features added
--------------

* added :attr:`pyage.assets.Sound.pan` attribute to pan sounds within the 
  stereo field
* added :attr:`pyage.screens.Menu.pan` to automatically pan all items within 
  the menu to a position in the stereo field, depending on the amount of items 
  within the menu

Other changes
-------------

* :class:`pyage.output_backends.Ao2` is now the default output backend for 
  every OS except Windows.
* added installation documentation, listing all the optional/default 
  dependencies that might need to be installed manually.
* removed ao2 from dependencies since git links are not compatible with PyPI

0.1.0-a6 (2022-03-29)
=====================

0.1.0-a4 re-release due to CI scripts failure.

0.1.0-a5 (2022-03-29)
=====================

0.1.0-a4 re-release due to CI scripts failure.

0.1.0-a4 (2022-03-29)
=====================

Features added
--------------

* updated dev-dependencies to latest versions
* updated pygame to v2.1.2
* updated synthizer to v0.12.3
* added loop parameter to :meth:`pyage.EventProcessor.add_schedule_event`, 
  allowing schedule events to be looped until removed manually
* added :meth:`pyage.EventProcessor.remove_schedule_event` to manually remove 
  scheduled callbacks
* improved internal reference management to prevent bound methods to create 
  cyclic references and therefore prevent the garbage collector from doing its work
* added new Ao2 output backend to support speech output via accessible_output2, 
  even on Linux and Mac OS (patch by TheQuinbox)
* rewrote entire sound system into a more flexible asset system which supports 
  more than just sound assets. This is a breaking change and will require you 
  to adapt your existing pyAGE projects.
* added a new :class:`pyage.assets.Stream` asset which allows you to stream 
  stereo audio instead of just playing back mono audio sources.
* added :attr:`pyage.assets.Playable.looping` option to allow looping sounds and
  streams.
* added :attr:`pyage.assets.Playable.position` and 
  :attr:`pyage.assets.Playable.length` attributes to control playback position 
  within sounds and streams.

Bugs fixed
----------

* fixed some crashes when deleting texts in menu text inputs
* fix crash in event processor when two events of the same type get fired at 
  the exact same time
* added py.typed to properly indicate typing support

0.1.0-a3 (2021-02-04)
=====================

0.1.0-a1 re-release due to CI scripts failure.

0.1.0-a2 (2021-02-04)
=====================

0.1.0-a1 re-release due to CI scripts failure.

0.1.0-a1 (2021-02-04)
=====================

This is the initial release of pyAGE and still far from finished. It is ment 
for testing purposes only and will get new features in the future. It is 
however required for writing the tutorial.
