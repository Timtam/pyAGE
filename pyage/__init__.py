"""
This package contains all core objects that build the foundation of every pyAGE game.

.. currentmodule:: pyage

.. autosummary::
   :toctree:

   App
   EventProcessor
   ScreenStack
"""

from pyage.app import App
from pyage.event_processor import EventProcessor
from pyage.screen_stack import ScreenStack

__version__: str = "0.1.0-a5"

__all__ = (
    "App",
    "EventProcessor",
    "ScreenStack",
)
