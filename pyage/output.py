import pyage


def output(text: str, interrupt: bool = True) -> None:

    app: pyage.App = pyage.App()

    if app.output_backend is not None:
        app.output_backend.output(text, interrupt)
