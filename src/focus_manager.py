from events import Event, EventType
from components import Component


class FocusManager:
    def __init__(self) -> None:
        self._focused_component: Component | None = None

    def remove_focus(self):
        if self._focused_component:
            self._focused_component.enqueue_event(Event(EventType.FOCUS_OUT))

        self._focused_component = None

    def set_focus(self, component: Component):
        if self._focused_component:
            self._focused_component.enqueue_event(Event(EventType.FOCUS_OUT))
        else:
            self._focused_component = component
            self._focused_component.enqueue_event(Event(EventType.FOCUS_IN))

    @property
    def focused_component(self):
        return self._focused_component
