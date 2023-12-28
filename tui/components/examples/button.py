from ...events import Event, EventType, EventListener
from ..component import Component


class Button(Component):
    def set_up(self):
        self._is_focusable = True

        def focus_in(_: Event):
            b = self._style.background_color
            self._style.background_color = self._style.color
            self._style.color = b

        def focus_out(_: Event):
            b = self._style.background_color
            self._style.background_color = self._style.color
            self._style.color = b

        def click(_):
            focus_out(_)

        def click_exit(_):
            focus_in(_)

        self.add_event_listener(EventListener(
            [EventType.FOCUS_IN],
            focus_in
        ))

        self.add_event_listener(EventListener(
            [EventType.FOCUS_OUT],
            focus_out
        ))

        self.add_event_listener(EventListener(
            [EventType.ACTIVATE],
            click
        ))
        self.add_event_listener(EventListener(
            [EventType.DEACTIVATE],
            click_exit
        ))
