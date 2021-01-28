from typing import Any, Callable

FocusEventCallback = Callable[[bool, Any], None]
KeyEventCallback = Callable[[bool, Any], None]
ScheduleEventCallback = Callable[[Any], None]
TextEventCallback = Callable[[str, Any], None]
