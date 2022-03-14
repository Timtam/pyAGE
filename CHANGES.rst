===============
pyAGE Changelog
===============

0.1.0-a4 (2022-?-?)
=====================

Features added
--------------

* updated dev-dependencies to latest versions
* updated pygame to v2.1.2
* updated synthizer to v0.12.0, which is the latest official version supporting 
  Python 3.8. Since thats currently our main development version, we'll stick 
  with that version for a while, until we spread out to support more than just 
  one Python version.
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
