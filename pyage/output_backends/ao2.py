import accessible_output2.outputs

from pyage.output_backend import OutputBackend


class Ao2(OutputBackend):
    def __init__(self) -> None:
        self.speaker = accessible_output2.outputs.auto.Auto()

    def __del__(self) -> None:
        self.speaker = None

    def output(self, text: str, interrupt: bool = True) -> None:
        self.speaker.output(text, interrupt)
