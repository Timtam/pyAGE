import sys
import traceback
from typing import Callable, Optional

import pygame
from py_singleton import singleton

from .audio_backend import AudioBackend
from .event_processor import EventProcessor
from .output_backend import OutputBackend
from .screen_stack import ScreenStack
from .sound_bank import SoundBank


@singleton
class App:

    _audio_backend: Optional[AudioBackend] = None
    _event_processor: EventProcessor = EventProcessor()
    _fps: int
    _output_backend: Optional[OutputBackend] = None
    _quit: bool = False
    _screen_stack: ScreenStack
    _sound_bank: SoundBank
    _title: str = ""

    def __init__(self) -> None:

        self._screen_stack = ScreenStack(self)
        self._sound_bank = SoundBank(self)

    def show(
        self,
        title: str,
        fps: int = 30,
        audio_backend: Optional[AudioBackend] = None,
        output_backend: Optional[OutputBackend] = None,
    ) -> None:

        self._fps = fps
        self._title = title

        if output_backend is None:
            from pyage.output_backends.tolk import Tolk

            self._output_backend = Tolk()
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
            self.show_message_box(e)
            sys.exit()

        pygame.display.set_mode((320, 240))
        pygame.display.set_caption(self.window_title)
        pygame.display.flip()

    def quit(self) -> None:
        self._quit = True

    def process(self, fn: Optional[Callable[["App", float], None]] = None) -> None:

        clock: pygame.time.Clock = pygame.time.Clock()

        while not self._quit:

            try:

                clock.tick(self._fps)

                self._event_processor.process()

                if self._quit:
                    break

                self._screen_stack.update(clock.get_time() / 1000)

                if fn:
                    fn(self, clock.get_time() / 1000)

            except KeyboardInterrupt:

                self.quit()

            except BaseException:
                print(
                    "exception encountered and silently ignored:\n",
                    traceback.format_exc(),
                )

        while self._screen_stack.pop():
            pass

        self._sound_bank.unload_all()
        pygame.display.quit()

    @property
    def window_title(self) -> str:
        return self._title

    @property
    def event_processor(self) -> EventProcessor:
        return self._event_processor

    def show_message_box(self, message: str, title: Optional[str] = None) -> None:

        if not title:
            title = self.window_title

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
    def output_backend(self) -> Optional[OutputBackend]:
        return self._output_backend

    @property
    def screen_stack(self) -> ScreenStack:
        return self._screen_stack

    @property
    def audio_backend(self) -> Optional[AudioBackend]:
        return self._audio_backend

    @property
    def sound_bank(self) -> SoundBank:
        return self._sound_bank
