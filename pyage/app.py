import sys
import traceback
from typing import Callable, Optional

import pygame
from pysingleton import PySingleton

from pyage.audio_backends.audio_backend import AudioBackend

from .event_processor import EventProcessor
from .output_backends.output_backend import OutputBackend
from .screen_stack import ScreenStack


class App(metaclass=PySingleton):

    """
    The app is the central object which handles the game loop. It is fairly
    simple to use, but very important as well.

    Using :meth:`~pyage.App.show` will initialize the game, while
    :meth:`~pyage.App.process` will run the actual game loop.
    :meth:`~pyage.App.quit` can be used at any time to quit the game.

    Please note that :class:`pyage.App` is a singleton class, thus you
    can import and initialize this class at any time to get access to it.
    """

    _audio_backend: Optional[AudioBackend] = None
    _event_processor: EventProcessor = EventProcessor()
    _fps: int
    _output_backend: Optional[OutputBackend] = None
    _quit: bool = False
    _title: str = ""

    def show(
        self,
        title: str,
        fps: int = 30,
        audio_backend: Optional[AudioBackend] = None,
        output_backend: Optional[OutputBackend] = None,
    ) -> None:

        """
        Initializes the game by providing a window title and the target fps
        rate. You can also inject your custom audio and screen reader output
        backends here.

        Parameters
        ----------
        title

            the window title for the game

        fps

            the amount of fps targeted by the app, default 30

        audio_backend

            a custom audio backend to use, default None, which will use the
            default audio backend, Synthizer.

        output_backend

            a custom screen reader backend to use, default None, which will
            use cytolk for communicating with screen readers when under Windows,
            and accessible_output2 when running under other operating systems.
            Please note that accessible_output2 doesn't get installed by
            default, see the :ref:`additional-packages` section for more
            information.
        """

        self._fps = fps
        self._title = title

        if output_backend is None:
            try:
                if sys.platform == "win32":
                    from pyage.output_backends.tolk import Tolk

                    self._output_backend = Tolk()
                else:
                    from pyage.output_backends.ao2 import Ao2

                    self._output_backend = Ao2()
            except ImportError:
                self._output_backend = None

        else:
            self._output_backend = output_backend

        if audio_backend is None:
            from pyage.audio_backends.synthizer import Synthizer

            self._audio_backend = Synthizer()
        else:
            self._audio_backend = audio_backend

        try:
            pygame.display.init()
        except pygame.error as e:
            self.show_message_box(str(e))
            sys.exit()

        pygame.display.set_mode((320, 240))
        pygame.display.set_caption(self.window_title)
        pygame.display.flip()

    def quit(self) -> None:
        """
        This method will tell the game loop to quit as soon as possible, releasing all resources in the process.
        """

        self._quit = True

    def process(self, fn: Optional[Callable[["App", float], None]] = None) -> None:
        """
        This method will run the game loop and keeps the game going.

        Parameters
        ----------
        fn

            an optional function which will be called once for every frame.
            It should be as fast as possible to prevent frame drops.
            The function needs to take two parameters. The first parameter is
            the App object, and the second parameter is a float which
            determines the delta time since the last frame in seconds.
        """

        clock: pygame.time.Clock = pygame.time.Clock()
        stack: ScreenStack = ScreenStack()

        while not self._quit:

            try:

                clock.tick(self._fps)

                self._event_processor.process()

                if self._quit:
                    break

                stack.update(clock.get_time() / 1000)

                if fn:
                    fn(self, clock.get_time() / 1000)

            except KeyboardInterrupt:

                self.quit()

            except BaseException:
                print(
                    "exception encountered and silently ignored:\n",
                    traceback.format_exc(),
                )

        while stack.pop():
            pass

        pygame.display.quit()

    @property
    def window_title(self) -> str:
        """
        Allows to read the window title for the game.
        """

        return self._title

    def show_message_box(self, message: str, title: Optional[str] = None) -> None:
        """
        Allows you to show a message box which doesn't depend on any external
        library, but only Python standard library tools instead.

        Parameters
        ----------
        message

            the message to be shown

        title

            the window title (default is the app name given to
            :meth:`~pyage.App.show`)

        """

        if not title:
            title = self.window_title

        import tkinter
        from tkinter import messagebox

        try:
            tkscreen = tkinter.Tk()
            tkscreen.wm_withdraw()
            messagebox.showinfo(title, message)
            tkscreen.destroy()
        except tkinter.TclError:
            print(
                "Unable to initialize a message box to output the following message:\n\ttitle: %s\n\tmessage: %s"
                % (title, message)
            )

    @property
    def output_backend(self) -> Optional[OutputBackend]:
        """
        Allows access to the output backend to e.g. send messages to screen
        readers
        """

        return self._output_backend

    @property
    def audio_backend(self) -> Optional[AudioBackend]:
        """
        The audio backend used by pyAGE.
        """

        return self._audio_backend
