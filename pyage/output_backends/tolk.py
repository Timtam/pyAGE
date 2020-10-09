import os.path
import sys

from cytolk import tolk

from pyage.output_backend import OutputBackend


class Tolk(OutputBackend):
    def __init__(self) -> None:

        sys.path.insert(0, os.path.dirname(tolk.__file__))

    def Load(self) -> None:
        tolk.load()

    def Unload(self) -> None:
        tolk.unload()

    def Output(self, text: str, interrupt: bool = True) -> None:
        tolk.output(text, interrupt)
