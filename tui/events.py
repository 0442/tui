from __future__ import annotations
from collections import deque
from typing import Callable, List
from enum import Enum, auto


class EventType(Enum):
    FOCUS_IN = auto()
    FOCUS_OUT = auto()
    ACTIVATE = auto()
    DEACTIVATE = auto()

    UPDATE = auto()
    KEY_PRESS = auto()

    ANY = auto()

    def __eq__(self, other):
        """Adds special functionality for equality checks with event type `ANY`.

        Comparisons between all event types and the event type `ANY` will
        result in True.
        """
        if self is EventType.ANY or other is EventType.ANY:
            return True
        return super().__eq__(other)

    def __hash__(self):
        return hash(self.value)


class Event:
    """Represents an event of given type.

    All events carry `data` and an event type `type`, both of which
    can be retrieved e.g. when handling the event.
    """

    def __init__(self, event_type: EventType, data: int | str | None = None) -> None:
        self._data = data
        self._event_type = event_type

    @property
    def data(self):
        return self._data

    @property
    def event_type(self):
        return self._event_type

    def __str__(self) -> str:
        return f"{self._event_type.name} : {self._data}"


class EventListener:
    def __init__(self,
                 listening_to: List[EventType] | set[EventType],
                 callback: Callable[[Event], None]) -> None:
        """
        Args:
            event_type (EventType): The event type this
            the event listener listens to / is subscribed to.
        """
        super().__init__()
        self._listening_to = set(listening_to)
        self._callback = callback

    def handle_event(self, event: Event):
        self._callback(event)

    @property
    def listening_to(self) -> set[EventType]:
        return self._listening_to


class EventEmitter:
    def __init__(self, event: Event, event_manager: EventQueue) -> None:
        self._event = event
        self._event_manager = event_manager

    def emit_event(self):
        """Calling this function emits the event (given as constructor param)
        to the EventQueue (given as constructor param)."""

        self._event_manager.enqueue_event(self._event)


class EventQueue:
    def __init__(self) -> None:
        self._event_listeners: List[EventListener] = []
        self._event_queue: deque[Event] = deque()

    def add_event_listener(self, event_listener: EventListener):
        self._event_listeners.append(event_listener)

    def enqueue_event(self, event: Event):
        self._event_queue.append(event)

    def _notify_listeners(self, event: Event):
        for event_listener in self._event_listeners:
            if event.event_type in event_listener.listening_to:
                event_listener.handle_event(event)

    def process_events(self):
        """Goes through all queued events and "notifies" event listeners of
        them.

        Only goes through the events that were in the queue at the beginning of
        running this function. New events added during the processing are
        processed on the next run.
        """
        event = None
        event_count = len(self._event_queue)
        for _ in range(event_count):
            event = self._event_queue.popleft()
            self._notify_listeners(event)
