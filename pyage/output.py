from pyage.app import App


def output(text: str, interrupt: bool = True) -> None:

    app: App = App()

    if app.output_backend is not None:
        app.output_backend.output(text, interrupt)
