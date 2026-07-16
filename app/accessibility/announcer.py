from __future__ import annotations

try:
    from accessible_output2.outputs.auto import Auto
except ImportError:
    Auto = None


class Announcer:
    def __init__(self) -> None:
        self._output = Auto() if Auto else None

    def say(self, message: str) -> None:
        if self._output:
            try:
                self._output.speak(message, interrupt=True)
            except Exception:
                return

