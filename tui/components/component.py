from __future__ import annotations
from abc import ABC
from io import StringIO

from ..events import Event, EventListener, EventQueue
from .component_style import Style


class Component(ABC):
    def __init__(
        self, *,
        cid: str = None,
        text: str = "",
        focusable: bool = False,
        style: Style = None,
    ) -> None:
        super().__init__()

        self._cid = cid
        self._text = text

        # Changes are made to _resolved_style throughout the "resolution
        # pipeline". A copy is needed to not have the original style rules in
        # `_style` be altered.
        # `_prev_resolved_style` is used for checking whether the style is
        # "dirty", i.e. re-rendering is needed.
        self._style = style
        self._resolved_style: Style = None
        self._prev_resolved_style: Style = None

        self._is_focusable = focusable

        self._event_queue = EventQueue()

        """Rendering related attributes.
        Might be be moved somewhere else at some point."""
        # Whether `resolved_style` has changed, whether to re-render.
        self._dirty: bool = False
        # Used for faster re-rendering of non-dirty components
        self.render_cache = StringIO()

        self.set_up()

    def set_up(self):
        pass

    def add_event_listener(self, event_listener: EventListener):
        self._event_queue.add_event_listener(event_listener)

    def enqueue_event(self, event: Event):
        self._event_queue.enqueue_event(event)

    def process_events(self):
        self._event_queue.process_events()

    @property
    def is_focusable(self) -> bool:
        return self._is_focusable

    @property
    def cid(self) -> str:
        return self._cid

    @property
    def text(self) -> str:
        return self._text

    @property
    def style(self) -> Style:
        return self._style

    @style.setter
    def style(self, new: Style):
        self._style = new

    @property
    def resolved_style(self) -> Style:
        return self._resolved_style

    @resolved_style.setter
    def resolved_style(self, new: Style):
        self._resolved_style = new

    @property
    def prev_resolved_style(self) -> Style:
        return self._prev_resolved_style

    @prev_resolved_style.setter
    def prev_resolved_style(self, new: Style):
        self._prev_resolved_style = new

    @property
    def dirty(self) -> bool:
        return self._dirty

    @dirty.setter
    def dirty(self, new: bool) -> None:
        self._dirty = new

    def __str__(self) -> str:
        s = self._style
        rs = self._resolved_style
        lines = [
            "Component",
            f"    cid: {self._cid}",
            "    Style:",
            f"        x,y: ({s.x}, {s.y})",
            f"        w,h: ({s.width}, {s.height})",
            "    Resolved style:",
            f"    (r) x,y: ({rs.x}, {rs.y})",
            f"    (r) w,h: ({rs.width}, {rs.height})"
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()


# TODO
class Text:
    def __init__(self, text: str) -> None:
        self._text = text
        self._height = 0
        self._width = 0

    @property
    def min_width(self):
        return 1

    @property
    def max_width(self):
        return len(self._text)

    @property
    def min_height(self):
        return 1

    @property
    def max_height(self):
        return len(self._text)
