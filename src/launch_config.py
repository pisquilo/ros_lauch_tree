from typing import List
from roslaunch.config import ROSLaunchConfig

from tree_objects import TreeNode, TreeParam, TreeTest, TreeArg, TreeRemap, TreeROSParam

from anytree import Node

class LaunchConfig(ROSLaunchConfig):
    """ Wrapper class for RosLaunchConfig

    Adds a dictionary structure of the lunch file
    """

    def __init__(self):
        super().__init__()

    def add_root(self, root_name):
        self.root = Node(name=root_name, instance=root_name)
        self.parent_stack: List[str] = [self.root]

    def push_level(self, name):
        level = Node(name=name, instance=name, parent=self.parent_stack[-1])
        self.parent_stack.append(level)

    def pop_level(self):
        self.parent_stack.pop()

    def _add_to_tree(self, key, instance):
        Node(name=key, instance=instance, parent=self.parent_stack[-1])

    def add_param(self, p, filename=None, verbose=True, command=None):
        result = super().add_param(p, filename, verbose)
        self._add_to_tree(p.key, TreeParam(p.key, p.value))
        return result

    def add_test(self, test, verbose=True):
        result = super().add_test(test, verbose)
        self._add_to_tree(test.name, TreeTest(test.name))
        return result

    def add_node(self, node, core=False, verbose=True):
        result = super().add_node(node, core, verbose)
        self._add_to_tree(node.name, TreeNode(node.name))
        return result

    def add_arg(self, name, default=None, value=None, doc=None):
        self._add_to_tree(name, TreeArg(name, value))

    def add_remap(self, from_topic, to_topic):
        self._add_to_tree(from_topic, TreeRemap(from_topic, to_topic))

    def add_rosparam(self, command, filename, unique_name):
        self._add_to_tree(unique_name, TreeROSParam(unique_name, command))
