from __future__ import annotations
from time import time
from typing import List, Self, TypeVar
from collections.abc import Callable
from functools import wraps
from dataclasses import replace
from copy import copy

from ..utils.logger import log
from ..components.component_tree import ComponentTree, ComponentTreeNode
from ..viewport import Viewport
from .units import Position, Size, Axis
from .resolution_utils import clamp

T = TypeVar("T")
A = TypeVar("A")


class StyleResolver:
    def __init__(self, tree: ComponentTree, viewport: Viewport) -> None:
        self._tree = tree
        self._viewport = viewport

    def _lay_items(self, node: ComponentTreeNode, axis: Axis) -> None:
        """Lays out the node's children one after another, in the directions of
        the node's `layout_direction`, by modifying their positions. Final
        sizes for components should be calculated before using this function to
        to lay out components.

        Args:
            node (ComponentTreeNode): The node to work on.
        """

        pos_name = axis
        size = "width" if axis == "x" else "height"
        layout_dir = node.component.style.layout_direction

        rl_pos_children: List[ComponentTreeNode] = [
            child_node for child_node in node.children
            if child_node.component.style.position == "relative"
        ]

        # Place the components one after the other
        start_pos = getattr(node.component.resolved_style, pos_name)
        for child_node in rl_pos_children:
            rstyle = child_node.component.resolved_style

            if layout_dir == axis:
                setattr(rstyle, pos_name, start_pos)
                start_pos += getattr(rstyle, size)
            else:
                setattr(rstyle,
                        pos_name,
                        getattr(node.component.resolved_style, pos_name))

    def _get_children_required_size(self, node: ComponentTreeNode, axis: Axis) -> int:
        """Calculates the size(width/height) of the children of a given node,
        in the given axis, take up. (currently just sum of their height/width,
        i.e. size if they are stuck together with no spacing.)

        Only count children using relative positioning

        Args:
            node (ComponentTreeNode): The node whose children to calc.
            axis (Axis): The axis for which to calculate the children's size.

        Returns:
            (int): The sum of children's size in the direction of axis.
        """
        layout_dir = node.component.style.layout_direction
        size_name = "width" if axis == "x" else "height"

        children_required_size = 0
        for child_node in node.children:
            if child_node.component.style.position != "relative":
                continue
            csz = getattr(child_node.component.resolved_style, size_name)
            if layout_dir == axis:
                children_required_size += csz
            else:
                children_required_size = max(children_required_size, csz)

        return children_required_size

    def _adjust_sizes(self, node: ComponentTreeNode, axis: Axis) -> None:
        """Needs to be given nodes acquired by reverse traversal of the
        component tree, i.e. from leaves to root / bottom to top so that for
        every component their children are resolved before themselve.

        Uses the node's childrens' size values to adjust its own if it is set
        to None (i.e. 'auto'). The node's size is also clamped to fit within
        its min- and max-widths.

        After this the children's sizes are adjusted to fit the restrictions
        posed by their parent(this node). (This part maybe could/should be
        separated into its own function)

        Args:
            node (ComponentTreeNode): The node to work on.
        """
        size_name = "width" if axis == "x" else "height"
        min_size_name = "min_width" if axis == "x" else "min_height"
        max_size_name = "max_width" if axis == "x" else "max_height"

        children_required_size = self._get_children_required_size(node, axis)

        rstyle = node.component.resolved_style
        sz = getattr(rstyle, size_name)

        if axis == "x":
            s = getattr(rstyle, min_size_name)
            min_size = s if s is not None else len(node.component.text)
        else:
            s = getattr(rstyle, min_size_name)
            min_size = (s if s is not None else
                        (1 if node.component.text else 0))

        # if size is given for node(i.e. not auto), clamp relative to it.
        # Otherwise get the base size from children's required size.
        if sz is not None:
            sz = clamp(min_size,
                       sz,
                       getattr(rstyle, max_size_name))
        else:
            sz = clamp(min_size,
                       children_required_size,
                       getattr(rstyle, max_size_name))

        setattr(node.component.resolved_style, size_name, sz)
        setattr(node.component.resolved_style, min_size_name, min_size)

    def _fit_within_parent(self, node: ComponentTreeNode, axis: Axis):
        # Restrict children's sizes to parent's size
        # The children are scale down so that they retain their relative sizes
        # to each other, i.e. a child with width 10 will be 2 times larger than
        # a child with width 5. Min_widths are still respected, children will
        # overflow if they cannot scale down enough.

        size_name = "width" if axis == "x" else "height"
        min_size_name = "min_width" if axis == "x" else "min_height"
        max_size_name = "max_width" if axis == "x" else "max_height"

        children_required_size = self._get_children_required_size(node, axis)

        avail_space = getattr(node.component.resolved_style, size_name)
        if children_required_size > avail_space:
            for child_node in node.children:
                rs = child_node.component.resolved_style
                cur_size = getattr(rs, size_name)
                new_size = (avail_space/children_required_size) * cur_size
                new_size = clamp(getattr(rs, min_size_name),
                                 new_size, getattr(rs, max_size_name))
                setattr(child_node.component.resolved_style,
                        size_name,
                        int(new_size))

    def _resolve_abs_positions(self, node: ComponentTreeNode) -> None:
        """Simply sets a component's positions(x,y) to 0 if they are not
        defined and the object is using position="absolute".

        Args:
            node (ComponentTreeNode): The node to work on.
        """
        if node.component.style.position != "absolute":
            return

        rstyle = node.component.resolved_style
        rstyle.x = rstyle.x or 0
        rstyle.y = rstyle.y or 0

    def _resolve_relative_values(self, node: ComponentTreeNode, axis: Axis) -> None:
        """Resolves initial size and position values from strings to numericals.
        These may not be the final values, they might be modified e.g. by min-
        and max-widths and size restrictions by parent components, in later
        phases.

        Args:
            node (ComponentTreeNode): The node to work on.
        """
        # NOTE: perfomance could be optimized, function could be be ran only
        # for nodes whose parents have changed size or position.

        pos_name = axis
        size_name = "width" if axis == "x" else "height"

        style = node.component.resolved_style

        # If root component, values are inherited from viewport.
        if node.parent is None:
            new_style = replace(style,
                                x=self._viewport.x,
                                y=self._viewport.y,
                                width=self._viewport.width,
                                height=self._viewport.height)

            node.component.resolved_style = new_style
            return

        parent_style = node.parent.component.resolved_style

        cur_pos = getattr(style, pos_name)
        cur_size = getattr(style, size_name)
        parent_pos = getattr(parent_style, pos_name)
        parent_size = getattr(parent_style, size_name)

        if cur_pos is not None:
            new_pos = Position(cur_pos).resolve(parent_pos, parent_size)
            setattr(style, pos_name, new_pos)

        if cur_size is not None:
            new_size = Size(cur_size).resolve(parent_size)
            setattr(style, size_name, new_size)

    def _set_resolved_style(self, node: ComponentTreeNode):
        res_style = copy(node.component.style)
        node.component.resolved_style = res_style

    # Parts of the resolution pipeline.
    # Need to be split into separate passes as direction of tree
    # traversal must change.

    def _first_pass(self) -> None:
        """Sets initial values for e.g. sizes and positions with percentage
        values. These are further modified (e.g. confined to size restrictions
        etc.) by subsequent passes.
        """
        for node in self._tree.traverse():
            self._set_resolved_style(node)
            self._resolve_relative_values(node, "x")
            self._resolve_relative_values(node, "y")
            self._resolve_abs_positions(node)

    def _second_pass(self) -> None:
        """Does more adjustments on initial sizes assigned by first_pass.
        Nodes must be traverses from leaves to root / bottom to top.
        """
        for node in self._tree.traverse(reverse=True):
            self._adjust_sizes(node, "x")
            self._adjust_sizes(node, "y")
            self._fit_within_parent(node, "x")
            self._fit_within_parent(node, "y")

    def _third_pass(self) -> None:
        """The second pass adjusts sizes, this pass adjusts positions. Having
        the final sizes calculated, does things like laying out the components
        along their parent's `layout_axis` one after another.
        """
        for node in self._tree.traverse():
            self._lay_items(node, "x")
            self._lay_items(node, "y")

    @staticmethod
    def flag_dirty_components(
        func: Callable[[StyleResolver, *T], A]
    ) -> Callable[[StyleResolver, *T], A]:
        """A decorator for comparing the state of all components'
        `resolved_style`s to their `prev_resolved_style`s. Marks a component
        as dirty if changes have occured. This decorator also handles
        updating the `prev_resolved_style`s for these components

        Args:
            func (Callable[[StyleResolver, T], A]): The function during
            which components' styles may be updates.

        Returns:
            Callable[[StyleResolver, T], A]: The resulting wrapped function.
        """
        @wraps(func)
        def wrapper(self: Self, *args: T, **kwargs: T) -> A:
            return_value = func(self, *args, **kwargs)

            for node in self._tree.traverse():
                before = node.component.prev_resolved_style
                after = node.component.resolved_style

                if not before or not after:
                    node.component.dirty = True

                elif before != after:
                    node.component.dirty = True

                node.component.prev_resolved_style = after

            return return_value

        return wrapper

    @flag_dirty_components
    def _resolution_pipeline(self) -> None:
        """Wraps together all the steps for resolving styles for all nodes'
        components in `self._tree`(ComponentNodeTree). When finished, all
        components have their resolved styles set in their `resolved_style`.
        """
        self._first_pass()
        self._second_pass()
        self._third_pass()

    def resolve(self) -> None:
        """Resolve the styles for all components in tree.
        """
        s = time()
        self._resolution_pipeline()
        e = time()
        log(f"Styles resolved in {e-s} seconds")
