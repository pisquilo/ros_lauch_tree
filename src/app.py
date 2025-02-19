from typing import Dict

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree
from textual.widgets.tree import TreeNode

from launch_config import LaunchConfig  # Assuming you have a class for LaunchConfig
from anytree import Node  # Ensure anytree is installed


# Function to convert anytree structure to textual Tree with labels
def anytree_to_textual_tree(anytree_node: Node, textual_parent: TreeNode):
    """Recursively add nodes from anytree to a textual Tree."""
    for child in anytree_node.children:
        label = repr(child.instance)  # Use repr(child) as the label
        allow_expand = bool(
            child.children
        )  # Only allow expansion if the node has children

        textual_child = textual_parent.add(
            label, allow_expand=allow_expand
        )  # Add child node
        anytree_to_textual_tree(child, textual_child)  # Recursively add children


class TreeApp(App):

    def __init__(self, config: LaunchConfig):
        super().__init__()

        self.config = config

    def compose(self) -> ComposeResult:
        yield Header("Launch Tree Debugger")
        yield Footer()
        yield self.create_tree()

    def create_tree(self) -> Tree:
        tree = Tree(repr(self.config.root.instance))
        root_node = tree.root  # Get the root TreeNode

        anytree_to_textual_tree(self.config.root, root_node)  # Convert the tree

        tree.root.expand_all()  # Expand all nodes

        return tree
