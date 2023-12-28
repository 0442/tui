from .events import Event, EventType
from .components.component import Component
from .components.component_tree import ComponentTree


class FocusManager:
    def __init__(self, component_tree: ComponentTree) -> None:
        self._focused_component: Component | None = None
        self._component_tree = component_tree

    def remove_focus(self):
        if self._focused_component:
            self._focused_component.enqueue_event(Event(EventType.FOCUS_OUT))

        self._focused_component = None

    def set_focus(self, component: Component):
        if self._focused_component:
            self._focused_component.enqueue_event(Event(EventType.FOCUS_OUT))

        self._focused_component = component
        self._focused_component.enqueue_event(Event(EventType.FOCUS_IN))

    def focus_first_focusable(self):
        for c in self._component_tree.traverse_components():
            if c.is_focusable is True:
                self.set_focus(c)
                break

    def focus_next(self):
        if self._focused_component is None:
            self.focus_first_focusable()
            return

        is_after_current = False
        for c in self._component_tree.traverse_components():
            if c == self._focused_component:
                is_after_current = True
            elif c.is_focusable is True and is_after_current is True:
                self.set_focus(c)
                break

    def focus_previous(self):
        if self._focused_component is None:
            self.focus_first_focusable()
            return

        comp_gen = self._component_tree.traverse_components()
        prev_component = next(comp_gen)
        for c in comp_gen:
            if c == self._focused_component and prev_component.is_focusable is True:
                self.set_focus(prev_component)
                break
            if c.is_focusable is True:
                prev_component = c

    @property
    def focused_component(self):
        return self._focused_component
