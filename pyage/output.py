from pyage import App


def Output(text: str, interrupt: bool = True) -> None:

    if App.OutputBackend is not None:
        App.OutputBackend.Output(text, interrupt)
