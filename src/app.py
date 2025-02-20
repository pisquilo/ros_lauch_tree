import re
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, Static, Markdown
from textual.containers import Horizontal, Container
from textual.widgets.tree import TreeNode

from launch_tree import LaunchTree, Node


# Function to convert anytree structure to textual Tree with labels
def anytree_to_textual_tree(launch_node: Node, textual_parent: TreeNode):
    """Recursively add nodes from anytree to a textual Tree."""
    for child in launch_node.children:
        if child.ifunless:
            color = "green"
        elif child.ifunless is False:
            color = "red strike"
        else:
            color = "white"

        label = (
            f"[{color}]{repr(child.instance)}[/{color}]"
            if hasattr(child, "instance")
            else f"[{color}]{repr(child)}[/{color}]"
        )

        allow_expand = bool(child.children)

        textual_child = textual_parent.add(label, allow_expand=allow_expand, data=child)

        anytree_to_textual_tree(child, textual_child)


class DetailsPanel(Container):
    """Widget to show details of the selected tree node with a wrapped table."""

    def compose(self) -> ComposeResult:
        """Create the details panel layout dynamically."""
        self.title = Static("🔍 Select a node to view details", id="details-title")
        self.space = Static("")
        self.details_content = Markdown(
            "**Details will appear here.**", id="details-content"
        )

        yield self.title
        yield self.space
        yield self.details_content

    def on_mount(self) -> None:
        """Apply styles after mounting."""
        self.details_content.styles.overflow = "hidden"  # ✅ Prevent scrollbars

    def show_details(self, node: Node):
        """Update the panel with the selected node's details."""
        instance = node.instance
        class_name = instance.__class__.__name__  # Get the class name of node.instance

        # ✅ Update the title widget
        self.title.update(f"🔍 **Class: {class_name}**  \n")

        details = getattr(instance, "details", {})

        if isinstance(details, dict):  # Ensure it's a dictionary
            table_header = "| **Key** | **Value** |\n|---|---|\n"
            table_rows = "\n".join(
                f"| {key} | {value} |" for key, value in details.items()
            )
            formatted_table = table_header + table_rows
        else:
            formatted_table = "**Error:** Details format is invalid"

        self.details_content.update(formatted_table)  # ✅ Update Markdown table


class TreeApp(App):
    """Main Textual App for Tree Navigation with Side Panel."""

    def __init__(self, any_tree: LaunchTree):
        super().__init__()
        self.any_tree = any_tree
        self.textual_tree = None

    def compose(self) -> ComposeResult:
        header = Header("🚀 Launch Tree Debugger")
        header.styles.auto_color = True
        header.styles.text_style = "bold"

        with Horizontal():
            with Container(id="tree-container"):
                self.textual_tree = self.create_tree()
                yield self.textual_tree

            with Container(id="details-container"):
                self.details_panel = (
                    DetailsPanel()
                )  # ✅ Fix: Use new DetailsPanel class
                yield self.details_panel

        yield header
        yield Footer()

    def on_mount(self) -> None:
        """Set layout styles after mounting."""
        self.query_one("#details-container").styles.width = "42%"
        self.textual_tree.node_highlighted = self.on_tree_node_highlighted

    def create_tree(self) -> Tree:
        """Creates the textual Tree widget with the structure from anytree."""
        tree = Tree(repr(self.any_tree.root.instance))
        tree.root.data = self.any_tree.root

        anytree_to_textual_tree(self.any_tree.root, tree.root)

        tree.root.expand_all()

        return tree

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        """Handles node highlight (keyboard navigation) and updates the details panel."""
        if self.details_panel.styles.display == "none":
            return

        highlighted_node = event.node

        self.log(f"🔍 Highlighted Node Data: {highlighted_node.data.name}")

        self.details_panel.show_details(highlighted_node.data)


# Run the App with a sample tree (if needed)
if __name__ == "__main__":
    sample_root = Node("Root")  # Example AnyTree structure
    tree = LaunchTree(sample_root)  # Assuming LaunchTree takes a root node
    TreeApp(tree).run()
