from typing import Any, List, Optional

from anytree import Node as AnyTreeNode

from tree_objects import File
from tree_objects import TreeElement


class Node(AnyTreeNode):
    def __init__(
        self,
        name: str,
        instance: TreeElement,
        parent: Any = None,
        children: Any = None,
        ifunless: Optional[bool] = None,
    ):
        super().__init__(name, parent, children)
        self.instance: TreeElement = instance
        self.ifunless: Optional[bool] = ifunless

    @property
    def instance(self) -> TreeElement:
        return self._instance  # Return the private attribute

    @instance.setter
    def instance(self, value: TreeElement) -> None:
        self._instance = value  # Set the private attribute

    @property
    def ifunless(self) -> Optional[bool]:
        return self._ifunless  # Return the private attribute

    @ifunless.setter
    def ifunless(self, value: Optional[bool]) -> None:
        self._ifunless = value  # Set the private attribute


class LaunchTree:
    """Wrapper class for anytree

    Creates the launch tree
    """

    def __init__(self, root_name) -> None:
        self.root = Node(name=root_name, instance=File(root_name))
        self.parent_stack: List[Node] = [self.root]

    @property
    def _current_parent(self) -> Node:
        return self.parent_stack[-1]

    def push_level(self, name: str, ifunless: bool = None) -> None:
        level = Node(
            name=name,
            instance=File(name),
            ifunless=ifunless,
            parent=self._current_parent,
        )
        self.parent_stack.append(level)

    def pop_level(self) -> None:
        self.parent_stack.pop()

    def add(self, key: str, instance: TreeElement, ifunless: bool = None) -> None:
        Node(
            name=key, instance=instance, ifunless=ifunless, parent=self._current_parent
        )
