import sys
import traceback
from typing import Callable, Optional, cast

import pygame

from .event_processor import EventProcessor
from .output_backend import OutputBackend
from .screen_stack import ScreenStack


class App:

    _event_processor: EventProcessor
    _fps: int
    _output_backend: Optional[OutputBackend] = None
    _quit: bool = False
    _screen_stack: ScreenStack
    _title: str = ""

    def __init__(self) -> None:

        self._event_processor = EventProcessor()
        self._screen_stack = ScreenStack(self)

    def Show(
        self, title: str, fps: int = 30, output_backend: Optional[OutputBackend] = None
    ) -> None:

        self._fps = fps
        self._title = title

        if output_backend is None:
            from pyage.output_backends.tolk import Tolk

            self._output_backend = Tolk()
        else:
            self._output_backend = output_backend

        cast(OutputBackend, self._output_backend).Load()

        try:
            pygame.display.init()
        except pygame.error as e:
            self.MessageBox(e)
            sys.exit()

        pygame.display.set_mode((320, 240))
        pygame.display.set_caption(self.WindowTitle)
        pygame.display.flip()

    def Quit(self) -> None:
        self._quit = True

    def Process(self, fn: Optional[Callable[["App", float], None]] = None) -> None:

        clock: pygame.time.Clock = pygame.time.Clock()

        while not self._quit:

            try:

                clock.tick(self._fps)

                self._event_processor.Process()

                if self._quit:
                    break

                self._screen_stack.Update(clock.get_time() / 1000)

                if fn:
                    fn(self, clock.get_time() / 1000)

            except KeyboardInterrupt:

                self.Quit()

            except BaseException:
                print(
                    "exception encountered and silently ignored:\n",
                    traceback.format_exc(),
                )

        pygame.display.quit()
        cast(OutputBackend, self._output_backend).Unload()

    @property
    def WindowTitle(self) -> str:
        return self._title

    @property
    def EventProcessor(self) -> EventProcessor:
        return self._event_processor

    def MessageBox(self, message: str, title: Optional[str] = None) -> None:

        if not title:
            title = self.WindowTitle

        import Tkinter
        import tkMessageBox

        try:
            tkscreen = Tkinter.Tk()
            tkscreen.wm_withdraw()
            tkMessageBox.showinfo(title, message)
            tkscreen.destroy()
        except Tkinter._tkinter.TclError:
            print(
                "Unable to initialize a message box to output the following message:\n\ttitle: %s\n\tmessage: %s"
                % (title, message)
            )

    @property
    def OutputBackend(self) -> Optional[OutputBackend]:
        return self._output_backend

    @property
    def ScreenStack(self) -> ScreenStack:
        return self._screen_stack
