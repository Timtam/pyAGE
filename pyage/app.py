import sys
import time
import traceback
from typing import Callable, Optional, cast

import pygame

from .event_processor import EventProcessor
from .output_backend import OutputBackend


class App:

    _event_processor: EventProcessor
    _fps: int
    _output_backend: Optional[OutputBackend] = None
    _quit: bool = False
    _title: str = ""

    def __init__(self) -> None:

        self._event_processor = EventProcessor()

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

    def Process(self, fn: Optional[Callable[[], None]] = None) -> None:

        current_time: float
        frame_length: float = 1.0 / self._fps
        frame_time: float
        time_diff: float

        while not self._quit:

            frame_time = time.time()

            try:
                self._event_processor.Process()

                if self._quit:
                    break

                if fn:
                    fn()

                current_time = time.time()

                time_diff = current_time - frame_time

                if time_diff < frame_length:
                    time.sleep(frame_length - time_diff)

            except KeyboardInterrupt:

                self._quit = True

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
