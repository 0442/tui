from __future__ import annotations

from typing import List, Generator

from .component import Component
from .component_style import Style


class ComponentTreeNode:
    def __init__(self,
                 component: Component,
                 parent: ComponentTreeNode = None,
                 children: List[ComponentTreeNode] = None) -> None:
        self._component = component
        self._parent = parent
        if children is None:
            self._children = []
        else:
            self._children = children

    def add_child(self, component: Component):
        node = ComponentTreeNode(component, self, None)
        self._children.append(node)

    def get_node_by_component(self, component: Component) -> ComponentTreeNode | None:
        if self._component == component:
            return self

        for child in self._children:
            node = child.get_node_by_component(component)
            if node is not None:
                return node

        return None

    def get_node_by_component_id(self, cid: str) -> ComponentTreeNode | None:
        if self._component.cid == cid:
            return self

        for child in self._children:
            node = child.get_node_by_component_id(cid)
            if node:
                return node

        return None

    def traverse(self, reverse: bool = False) -> Generator[ComponentTreeNode, None, None]:
        if reverse is False:
            yield self

        for child in self._children:
            yield from child.traverse(reverse=reverse)

        if reverse is True:
            yield self

    def traverse_components(self, reverse: bool = False) -> Generator[Component, None, None]:
        if reverse is False:
            yield self._component

        for child in self._children:
            yield from child.traverse_components(reverse=reverse)

        if reverse is True:
            yield self._component

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, new):
        self._component = new

    def __str__(self):
        lines = [
            "Component tree node:",
            f"    parent: {self._parent.component.cid if self._parent else None}",
            f"    Children: {[c.component.cid for c in self._children]}"
        ]
        lines += [f"    {line}" for line in str(self.component).split("\n")]

        return "\n".join(lines)

    def __repr__(self) -> str:
        return self.__str__()


class ComponentTree:
    def __init__(self) -> None:
        root_style = Style(position="relative", x=0, y=0,
                           width="100%", height="100%")
        self._root = ComponentTreeNode(
            Component(cid="root", style=root_style)
        )

    def remove_component(self, component: Component) -> None:
        node = self._root.get_node_by_component(component)
        if node is None:
            raise ValueError(f"Component '{component}' not "
                             "found in the component tree.")

        node.parent.children.remove(node)

    def get_component_by_id(self, cid: str) -> Component:
        node = self._root.get_node_by_component_id(cid)
        return node.component if node is not None else None

    def add_component(self, component: Component, parent_id: str = None) -> None:
        if parent_id is None:
            self._root.add_child(component)
            return

        parent_node = self._root.get_node_by_component_id(parent_id)
        if parent_node is None:
            raise ValueError(f"Component with id '{parent_id}' not "
                             "found in the component tree.")

        parent_node.add_child(component)

    def traverse(self, reverse: bool = False) -> Generator[ComponentTreeNode, None, None]:
        yield from self._root.traverse(reverse=reverse)

    def traverse_components(self, reverse: bool = False) -> Generator[Component, None, None]:
        yield from self._root.traverse_components(reverse=reverse)

    def join_tree(self):
        ...


class ComponentTreeBuilder:
    ...
