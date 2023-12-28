from collections import deque
from string import printable

from ...events import Event, EventType, EventListener, EventQueue
from ...utils.logger import log
from ..component import Component


class Input(Component):
    def set_up(self):
        self._is_focusable = True

        self._max_len = 100
        self._value = []

        self._max_hist_len = 100
        self._history = deque()
        self._hist_pointer = 0

        self._cursor_pos = 0

        key_listener = EventListener(
            [EventType.KEY_PRESS], self._handle_key_event)
        self._event_queue.add_event_listener(key_listener)

    def _update_history(self) -> None:
        # Checks if history is branching; if yes, clears previous
        # branch, i.e. clears the changes newer than current hist_pointer
        if self._hist_pointer != 0:
            pop_count = self._hist_pointer
            for _ in range(pop_count):
                self._history.popleft()
            self._hist_pointer = 0

        if len(self._history) > self._max_hist_len:
            self._history.pop()

        self._history.appendleft(self._value)

    def _undo(self) -> None:
        if self._hist_pointer < len(self._history) - 1:
            self._hist_pointer += 1
            self._value = self._history[self._hist_pointer]

    def _redo(self) -> None:
        if self._hist_pointer > 0:
            self._hist_pointer -= 1
            self._value = self._history[self._hist_pointer]

    def _write(self, char: str) -> None:
        new_value = self._value[:]
        new_value.insert(self._cursor_pos, char)

        if len(new_value) <= self._max_len:
            self._value = new_value
            self._update_history()
            self._cursor_pos += 1

    def _erase(self) -> None:
        if self._cursor_pos <= 0:
            return
        if len(self._value) <= 0:
            return

        new_value = self._value[:]
        new_value.pop(self._cursor_pos-1)
        self._value = new_value
        self._update_history()
        self._cursor_pos -= 1

    def _move_pointer(self, steps: int) -> None:
        if self._cursor_pos + steps < 0:
            self._cursor_pos = 0
        elif self._cursor_pos + steps > len(self._value):
            self._cursor_pos = len(self._value)
        else:
            self._cursor_pos += steps

    def _clear(self) -> None:
        self._value = []
        self._update_history()

    def _handle_key_event(self, event: Event):
        key = event.data["key"]
        if not key:
            return

        if len(key) != 1:
            if key == "KEY_BACKSPACE":  # backspace
                self._erase()
            elif key == "KEY_ENTER":
                self._event_queue.enqueue_event(Event(EventType.ACTIVATE))
            elif key == "KEY_RIGHT":
                self._move_pointer(1)
            elif key == "KEY_LEFT":
                self._move_pointer(-1)
        elif str(key) in printable:
            self._write(str(key))

        self._resolved_style.dirty = True
        self._text = "".join(self._value)
        log(key, self._text)
