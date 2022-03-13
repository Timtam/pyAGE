"""
Any scene in a game is a screen, and the base screen, as well as the
pre-defined screens can be found within this package.

.. currentmodule:: pyage.screens

.. autosummary::
   :toctree:

   Menu
   Screen
"""

from pyage.screens.menu import Menu
from pyage.screens.screen import Screen

__all__ = (
    "Menu",
    "Screen",
)
