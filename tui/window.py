from blessed import Terminal

from .utils.logger import log
from .events import Event, EventListener, EventQueue, EventType
from .components.component_tree import ComponentTree
from .style_resolver.style_resolver import StyleResolver
from .viewport import Viewport
from .rendering.renderer import Renderer
from .focus_manager import FocusManager


class Window:
    def __init__(self, renderer: Renderer, viewport: Viewport,
                 component_tree: ComponentTree, t: Terminal) -> None:
        self._viewport = viewport
        self._component_tree = component_tree
        self._event_queue = EventQueue()
        self._focus_manager = FocusManager(self._component_tree)
        self._renderer = renderer
        self._style_resolver = StyleResolver(self._component_tree,
                                             self._viewport)

        self._is_running = False

        # TODO: Try to get rid of terminal as attribute.
        self._t = t

        self._setup_event_listeners()

        self._key_bindings = {
            "KEY_DOWN": self._focus_manager.focus_next,
            "KEY_UP": self._focus_manager.focus_previous,
            "KEY_ENTER": lambda: (
                self._focus_manager.focused_component.enqueue_event(
                    Event(EventType.ACTIVATE)
                ) if self._focus_manager.focused_component else None
            ),
            "q": self.quit,
            " ": lambda: None
        }

    def quit(self):
        self._is_running = False

    def _setup_event_listeners(self):
        key_event_listener = EventListener(
            [EventType.KEY_PRESS], self._handle_key_event
        )
        screen_update_listener = EventListener(
            [EventType.UPDATE], self._update_screen
        )
        self._event_queue.add_event_listener(key_event_listener)
        self._event_queue.add_event_listener(screen_update_listener)

    def _update_screen(self, _event: Event):
        self._viewport.width, self._viewport.height = self._t.width, self._t.height

        self._style_resolver.resolve()
        self._renderer.render()
        self._renderer.draw()

    def _handle_key_event(self, event: Event):
        key = event.data.get("key", "")
        log("key_event:", key)
        func = self._key_bindings.get(key)

        if func is not None:
            func()

        # This event is handled the next time events are processed.
        # This is also why in `run` events are processed twice.
        self._event_queue.enqueue_event(Event(EventType.UPDATE))

    def run(self):
        with self._t.fullscreen(), self._t.cbreak(), self._t.hidden_cursor():
            self._event_queue.enqueue_event(Event(EventType.UPDATE))

            self._is_running = True
            while self._is_running:
                key = self._t.inkey(0.01)
                key = key.name if key.name else key

                if key:
                    key_event = Event(EventType.KEY_PRESS, {"key": str(key)})
                    self._event_queue.enqueue_event(key_event)

                if self._viewport.width != self._t.width or self._viewport.height != self._t.height:
                    self._event_queue.enqueue_event(Event(EventType.UPDATE))
                    self._viewport.width, self._viewport.height = self._t.width, self._t.height

                self._event_queue.process_events()
                for c in self._component_tree.traverse():
                    c.component.process_events()
                self._event_queue.process_events()

    @property
    def component_tree(self):
        return self._component_tree
