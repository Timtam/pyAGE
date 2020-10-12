from pyage import App


def output(text: str, interrupt: bool = True) -> None:

    if App.output_backend is not None:
        App.output_backend.output(text, interrupt)
