.. pyAGE documentation master file, created by
   sphinx-quickstart on Fri Nov 27 15:08:06 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyAGE - an audio game engine for beginners and professionals alike
==================================================================

**pyAGE** is an engine to create audio games on the fly. In contradiction to 
video games, audio games usually don't feature graphics and thus pyAGE doesn't 
provide image-processing capabilities, but even more powerful sound management 
tools, as well as keystroke processing and event queues, all baked into a 
simple-to-use interface that is convenient to use for beginners and 
professionals at the same time.

But what can it do for you?
---------------------------

**pyAGE** is a very young project, but it already offers the following benefits:

- compatible with all major Python 3 versions up to version 3.9
- fully type-annotated code can help you and your project in the long run
- extensible audio backend with the possibility to write your own backends, using whatever audio library you want by just implementing a few classes
- same goes for screen reader support, you can easily write your own backend and publish that via PyPI or GitHub, or submit pull requests to pyAGE to make your backend a part of the pyAGE project
- although the default audio and screen reader backend are a few of the most well-known competitors on the market right now, being the currently work-in-progress Synthizer library for audio processing and cytolk to provide screen reader output under Windows
- screen driven development: every menu, scene or situation in your game is a screen living on a stack, which can be pushed or popped at any time to switch between situations accordingly
- menu system with multiple item types to choose from like buttons, sliders or input fields
- and much, much more later on

Getting started / tutorial
--------------------------

Wanna dive right in? We've got you covered!

You can follow our tutorial and create a small game yourself, just by using pyAGE and all its amazing features.

.. toctree::
   :maxdepth: 2
   
   tutorial/index

The API Documentation / Guide
-----------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api
