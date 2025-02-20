from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree
from textual.widgets.tree import TreeNode

from launch_tree import LaunchTree
from anytree import Node


def anytree_to_textual_tree(anytree_node: Node, textual_parent: TreeNode):
    """Recursively add nodes from anytree to a textual Tree."""
    for child in anytree_node.children:
        if child.ifunless:
            color = "green"
        elif child.ifunless == False:
            color = "red strike"
        else:
            color = "white"
        label = f"[{color}]{repr(child.instance)}[/{color}]"

        allow_expand = bool(child.children)

        textual_child = textual_parent.add(label, allow_expand=allow_expand)
        anytree_to_textual_tree(child, textual_child)


class TreeApp(App):

    def __init__(self, tree: LaunchTree):
        super().__init__()

        self.launch_tree = tree
        self.title = "🚀 Launch Tree Debugger"

    def compose(self) -> ComposeResult:
        header = Header()
        header.styles.text_style = "bold"

        yield header
        yield Footer()
        yield self.create_tree()

    def create_tree(self) -> Tree:
        tree = Tree(repr(self.launch_tree.root))
        root_node = tree.root

        anytree_to_textual_tree(self.launch_tree.root, root_node)

        tree.root.expand_all()

        return tree
