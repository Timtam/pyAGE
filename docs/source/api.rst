Developer Interface
===================

.. module:: pyage

App: Where verything begins
---------------------------

**pyAGE** provides a class which runs the event processor and runs the entire 
game in general. This class is documented as follows:

.. autoclass:: pyage.app.App
   :inherited-members:


ScreenStack: changing the sound and feel of your game
-----------------------------------------------------

By accessing the :class:`pyage.screen_stack.ScreenStack` instance through 
:attr:`pyage.app.App.screen_stack`, you can 
:meth:`pyage.screen_stack.ScreenStack.push` new screens on top of the screen 
stack or :meth:`pyage.screen_stack.ScreenStack.pop` unwanted screens from the 
top of the screen stack at any time. The top-most screen will receive all 
events the game has to offer, including :class:`pyage.events.focus.FocusEvent` 
and :class:`pyage.events.key.KeyEvent`.

.. autoclass:: pyage.screen_stack.ScreenStack
   :inherited-members:

