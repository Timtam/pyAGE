Developer Interface
===================

.. module:: pyage

Core Components
---------------

The following components are the center of everything **pyAGE** can do for you. 
They'll include everything from running the game loop, over playing cached and 
streamed sounds to handling keystrokes and system events.

App: Where it all begins
~~~~~~~~~~~~~~~~~~~~~~~~

**pyAGE** provides a class which runs the event processor and runs the entire 
game in general. This class is documented as follows:

.. autoclass:: pyage.app.App
   :inherited-members:


ScreenStack: changing scenes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By accessing the :class:`pyage.screen_stack.ScreenStack` instance through 
:attr:`pyage.app.App.screen_stack`, you can 
:meth:`pyage.screen_stack.ScreenStack.push` new screens on top of the screen 
stack or :meth:`pyage.screen_stack.ScreenStack.pop` unwanted screens from the 
top of the screen stack at any time. The top-most screen will receive all 
events the game has to offer, including :class:`pyage.events.focus.FocusEvent` 
and :class:`pyage.events.key.KeyEvent`.

.. autoclass:: pyage.screen_stack.ScreenStack
   :inherited-members:


EventProcessor: listening to the game engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although you'll not have to work with the event processor itself most of the 
time, it can be pretty useful to know the various capabilities it can offer 
you. Most of the things will be hidden from you and be done automatically in 
the background though.

The event processor takes the important role of translating all the events 
provided by the game engine in the background (pygame by default) into 
pyAGE-internal events, which you can subscribe to so that a callback gets 
called whenever an event with the specified parameters occurs.
A very popular example would be a key event. By using 
:meth:`pyage.event_processor.EventProcessor.add_key_event` you can add a 
callback function which gets called whenever a certain key gets pressed. 
The corresponding :meth:`pyage.event_processor.EventProcessor.remove_key_event` 
method can be used to stop calling your function when its not necessary anymore.

There are quite a few event types that you can subscribe to, and there will 
probably be more in the future, and all of those can be accessed via the 
dedicated methods in the below class.

.. autoclass:: pyage.event_processor.EventProcessor
   :inherited-members:


SoundBank: let's get noisy
~~~~~~~~~~~~~~~~~~~~~~~~~~

The sound system of **pyAGE** is fairly complex, but everything begins in the 
global sound bank, which fulfills the job to cache all your sounds and allows 
access to the several underlying buffers in order to create a new sound. The 
remaining parts of the sound system will be discussed in the specific 
:ref:`chapter <sound-system>`, but the :class:`pyage.sound_bank.SoundBank` 
class will be listed here.

.. autoclass:: pyage.sound_bank.SoundBank
   :inherited-members:


Pre-defined screens
-------------------

When defining scenes, like a level in your game or even just a configuration 
menu, **pyAGE** will have you to work with so-called screens. A screen thereby 
is a situation which can handle various events, like key inputs, but represents 
a certain state in time. You cannot have multiple screens open at the same 
time, just like it doesn't make much sense to have multiple menus running at 
the same time. PyAGE already provides several screens for you, which you'll 
have to inherit or use in order to interact with the user. The available classes will be explained below.

Screen
~~~~~~

.. autoclass:: pyage.screen.Screen
   :inherited-members:


Menu
~~~~

.. autoclass:: pyage.screens.menu.Menu
   :inherited-members:


.. _sound-system:

The in-depth discussion of pyAGE's sound system
-----------------------------------------------
