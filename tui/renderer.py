from abc import ABC, abstractmethod
from blessed.terminal import Terminal
from blessed.colorspace import RGB_256TABLE

from components import Component


class Renderer(ABC):
    @abstractmethod
    def render(self):
        pass


class TerminalRenderer(Renderer):
    def __init__(self, component: Component) -> None:
        self._term = Terminal()
        self._component = component

    def _draw_bg(self):
        x, y = self._component.x, self._component.y
        w, h = self._component.w, self._component.h
        bg_color = self._component.background_color
        # Convert to terminal color
        term_color = self._term.on_color_rgb(bg_color.r,
                                             bg_color.g,
                                             bg_color.b)

        output = []
        for row in range(h):
            for col in range(w):
                output.append(self._term.move_xy(x + col, y + row))
                output.append(" ")

        return term_color("".join(output))

    def _draw_fg(self):
        x, y = self._component.x, self._component.y
        w, h = self._component.w, self._component.h
        fg_color = self._component.color
        bg_color = self._component.background_color
        # Convert to terminal color
        bg_term_color = self._term.on_color_rgb(bg_color.r,
                                                bg_color.g,
                                                bg_color.b)
        fg_term_color = self._term.color_rgb(fg_color.r,
                                             fg_color.g,
                                             fg_color.b)

        output = []
        output.append(self._term.move_xy(x, y))
        output.append(self._component.text)

        return bg_term_color(fg_term_color("".join(output)))

    def render(self):
        bg_str = self._draw_bg()
        fg_str = self._draw_fg()
        string = bg_str + fg_str
        print(string, end="", flush=True)
