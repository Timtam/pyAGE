===============
pyAGE Changelog
===============

0.1.0-a4 (2021-?-?)
=====================

Features added
--------------

* updated dev-dependencies to latest versions
* updated pygame to v2.1.2
* updated synthizer to v0.12.0, which is the latest official version supporting 
  Python 3.8. Since thats currently our main development version, we'll stick 
  with that version for a while, until we spread out to support more than just 
  one Python version.
* added loop parameter to EventProcessor.add_schedule_event, allowing schedule 
  events to be looped until removed manually
* added EventProcessor.remove_schedule_event to manually remove scheduled callbacks
* improved internal reference management to prevent bound methods to create 
  cyclic references and therefore prevent the garbage collector from doing its work

Bugs fixed
----------

* fixed some crashes when deleting texts in menu text inputs
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
