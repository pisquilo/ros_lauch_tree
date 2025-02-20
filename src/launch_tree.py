from typing import List

from anytree import Node


class LaunchTree:
    """Wrapper class for anytree

    Creates the launch tree
    """

    def __init__(self, root_name):
        self.root = Node(name=root_name, instance=root_name)
        self.parent_stack: List[str] = [self.root]

    def push_level(self, name, ifunless=None):
        level = Node(
            name=name, instance=name, ifunless=ifunless, parent=self.parent_stack[-1]
        )
        self.parent_stack.append(level)

    def pop_level(self):
        self.parent_stack.pop()

    def add(self, key, instance, ifunless=None):
        Node(
            name=key, instance=instance, ifunless=ifunless, parent=self.parent_stack[-1]
        )
