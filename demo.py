#!/bin/env python3

from time import sleep, time
from blessed import Terminal
from copy import copy

from tui.components.component import Component
from tui.components.component_style import Style
from tui.components.component_tree import ComponentTree
from tui.components.examples.button import Button
from tui.components.examples.input import Input
# from rendering.renderer import TerminalRenderer
from tui.rendering.renderer import TerminalRenderer
from tui.viewport import Viewport
from tui.window import Window
from tui.utils.logger import log
from tui.color import RGBA

cont_style = Style(
    x=0,
    y=0,
    width="100%",
    height="100%",
    color=RGBA(0, 0, 0, 0),
    background_color=RGBA(20, 20, 50, 0),
    layout_direction="y"
)

clr_1 = RGBA(163, 205, 255, 1)
clr_2 = RGBA(100, 140, 255, 1)

style2 = Style(
    width="100%",
    height=1,
    max_width=20,
    background_color=clr_2,
    color=clr_1
)

box_style = Style(
    height="50%",
    width="50%"
)
box1_style = copy(box_style)
box1_style.layout_direction = "y"
box1_style.background_color = RGBA(255, 100, 100, 1)

box2_style = copy(box_style)
box2_style.layout_direction = "x"
box2_style.background_color = RGBA(100, 100, 255, 1)


def main():
    t = Terminal()
    tree = ComponentTree()
    viewport = Viewport(0, 0, t.width, t.height)
    renderer = TerminalRenderer(tree, t)
    window = Window(renderer, viewport, tree, t)

    cont = Component(id="cont", style=cont_style)
    tree.add_component(cont)

    box = Component(id="v-box", style=box1_style)
    box2 = Component(id="h-box", style=box2_style)
    tree.add_component(box, "cont")
    tree.add_component(box2, "v-box")

    for i in range(1, 5):
        window.component_tree.add_component(
            Button(text=f"Button {i}",
                   id=f"Button{i}",
                   style=copy(style2)),
            "v-box"
        )

    for i in range(6, 9):
        s = copy(style2)
        s.height = i
        s.background_color = RGBA(155, 255, 100, 1)
        s.width = f"{10*i}%"
        s.color = RGBA(32, 52, 20, 1)
        window.component_tree.add_component(
            Button(text=f"Button {i}",
                   id=f"Button{i}",
                   style=s),
            "h-box"
        )

    window.run()

    """
    window.component_tree.add_component(
        Input(id="input1",
              style=copy(style2)),
        "cont"
    )
    """


if __name__ == "__main__":
    main()
