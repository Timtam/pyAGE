from cytolk import tolk

from pyage.output_backend import OutputBackend


class Tolk(OutputBackend):
    def Load(self) -> None:
        tolk.load()

    def Unload(self) -> None:
        tolk.unload()

    def Output(self, text: str, interrupt: bool = True) -> None:
        tolk.output(text, interrupt)
