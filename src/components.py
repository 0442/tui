from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple

from events import Event, EventListener, EventQueue
from color import RGB


class Component(ABC):
    def __init__(
        self, *,
        position: Tuple[int, int],
        size: Tuple[int, int],
        color: Tuple[RGB, RGB],
        text: str | None = None,
        parent: Component = None,
        focusable: bool = False
    ) -> None:

        super().__init__()

        self._x = position[0]
        self._y = position[1]
        self._w = size[0]
        self._h = size[1]
        self._fg_color = color[0]
        self._bg_color = color[1]

        self._children = []
        self._parent = parent

        self._is_focusable = focusable

        self._text = text

        self._event_queue = EventQueue()

        self.set_up()

    @abstractmethod
    def set_up(self):
        pass

    def add_child(self, component: Component):
        self._children.append(component)

    def add_event_listener(self, event_listener: EventListener):
        self._event_queue.add_event_listener(event_listener)

    def enqueue_event(self, event: Event):
        self._event_queue.enqueue_event(event)

    def process_events(self):
        self._event_queue.process_events()

    @property
    def is_focusable(self):
        return self._is_focusable

    @property
    def text(self):
        return self._text

    @property
    def background_color(self):
        return self._bg_color

    @background_color.setter
    def background_color(self, new_color: RGB):
        self._bg_color = new_color

    @property
    def color(self):
        return self._fg_color

    @color.setter
    def color(self, new_color: RGB):
        self._fg_color = new_color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h
