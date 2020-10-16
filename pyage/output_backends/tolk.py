from cytolk import tolk

from pyage.output_backend import OutputBackend


class Tolk(OutputBackend):
    def __init__(self) -> None:
        tolk.load()

    def __del__(self) -> None:
        tolk.unload()

    def output(self, text: str, interrupt: bool = True) -> None:
        tolk.output(text, interrupt)
