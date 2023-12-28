from timeit import timeit
from copy import copy
from blessed import Terminal

from tui.components.component import Component
from tui.components.component_tree import ComponentTree
from tui.components.examples.button import Button
from tui.rendering.renderer import TerminalRenderer
from tui.components.component_style import Style
from tui.color import RGBA
from tui.style_resolver.style_resolver import StyleResolver
from tui.viewport import Viewport

cont_style = Style(x=0, y=0,
                   width="100%",
                   height="100%",
                   background_color=RGBA(20, 20, 50, 0),
                   layout_direction="y")

clr_1 = RGBA(163, 205, 255, 1)
clr_2 = RGBA(100, 140, 255, 1)

btn_style = Style(width="100%",
                  height=1,
                  background_color=clr_2,
                  color=clr_1)


tree = ComponentTree()
t = Terminal()
renderer = TerminalRenderer(t)
viewport = Viewport(0, 0, 500, 500)
resolver = StyleResolver(tree, viewport)


def layout():
    cont = Component(cid="cont", style=cont_style)
    tree.add_component(cont)

    for i in range(1, 30):
        tree.add_component(
            Button(text=f"Button {i}",
                   cid=f"Button{i}",
                   style=copy(btn_style)),
            "cont"
        )


def render():
    resolver.resolve()
    for c in tree.traverse():
        c.component.dirty = True

    renderer.render(tree)


def main():
    layout()
    print("timing...")
    print(timeit(render, number=1000))


if __name__ == "__main__":
    main()
