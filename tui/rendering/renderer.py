from time import time
from abc import ABC, abstractmethod
from io import StringIO
from sys import stdout
from blessed import Terminal
from typing import Dict

from ..utils.logger import log
from ..components.component_tree import ComponentTree
from ..components.component import Component


class Renderer(ABC):
    @abstractmethod
    def render(self, tree: ComponentTree):
        pass

    def draw(self):
        pass


class TerminalRenderer(Renderer):
    def __init__(self, term: Terminal) -> None:
        self._term = term
        self._screen_buffer = StringIO()
        self._cache: Dict[int, StringIO] = {}

    def _render_bg(self, component: Component) -> None:
        style = component.resolved_style

        bg_color = style.background_color
        if bg_color.a == 0:
            return

        # Convert to terminal color
        bg_color = self._term.on_color_rgb(bg_color.r, bg_color.g, bg_color.b)

        x, y = style.x, style.y
        w, h = style.width, style.height

        row = bg_color("".join(" " for _ in range(w)))
        for i in range(h):
            c = self._term.move_xy(x, y+i) + row
            self._screen_buffer.write(c)
            self._cache[id(component)].write(c)

    def _render_text(self, component: Component) -> None:
        text = component.text
        style = component.resolved_style

        if not text:
            return

        x, y = style.x, style.y

        fg_color = style.color
        bg_color = style.background_color
        # Convert to terminal color
        bg_color = self._term.on_color_rgb(bg_color.r, bg_color.g, bg_color.b)
        fg_color = self._term.color_rgb(fg_color.r, fg_color.g, fg_color.b)

        content = bg_color(fg_color(self._term.move_xy(x, y) + text))
        self._screen_buffer.write(content)
        self._cache[id(component)].write(content)

    def render(self, tree: ComponentTree) -> None:
        s = time()
        render_count = 0
        self._screen_buffer.seek(0)

        for node in tree.traverse():
            component = node.component
            cache = self._cache.setdefault(id(component), StringIO())

            if component.dirty is True:
                render_count += 1

                cache.seek(0)
                self._render_bg(component)
                self._render_text(component)
                cache.truncate()

            self._screen_buffer.write(cache.getvalue())
            component.dirty = False

        self._screen_buffer.truncate()
        self._screen_buffer.flush()

        e = time()
        log(f"{render_count} components rendered in {e-s} seconds")

    def draw(self) -> None:
        s = time()

        self._screen_buffer.seek(0)
        stdout.write(self._screen_buffer.read())
        stdout.flush()

        e = time()
        log(f"Drawing took {e-s} seconds\n")
