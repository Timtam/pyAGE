"""
Everything asset-related lives within this package.

.. currentmodule:: pyage.assets

.. autosummary::
   :toctree:

   AssetCollection
   AssetManager
   Sound
   Stream
"""

from .collection import AssetCollection
from .manager import AssetManager
from .sound import Sound
from .stream import Stream

__all__ = (
    "AssetCollection",
    "AssetManager",
    "Sound",
    "Stream",
)
