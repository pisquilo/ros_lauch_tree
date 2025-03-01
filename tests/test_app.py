import unittest
from unittest.mock import MagicMock
from textual.widgets.tree import TreeNode
from textual.widgets import Tree
from src.tree import LaunchTree, Node
from src.app import anytree_to_textual_tree, DetailsPanel, TreeApp


class TestAnyTreeToTextualTree(unittest.TestCase):
    def setUp(self):
        self.root_node = Node(name="root", instance=MagicMock())
        self.child_node = Node(
            name="child", instance=MagicMock(), parent=self.root_node
        )
        mock_tree = Tree("Root")
        self.textual_root = TreeNode(tree=mock_tree, parent=None, id="root_id", label="root_label")

    def test_conversion_creates_children(self):
        anytree_to_textual_tree(self.root_node, self.textual_root)
        self.assertEqual(len(self.textual_root.children), 1)

        # Convert label to string before comparison
        actual_label = str(self.textual_root.children[0].label)
        expected_label = repr(self.child_node.instance)

        self.assertEqual(actual_label.strip(), expected_label.strip())


class TestDetailsPanel(unittest.TestCase):
    def setUp(self):
        self.panel = DetailsPanel()
        self.panel.compose()
        self.panel.title = MagicMock()
        self.panel.details_content = MagicMock()
        self.node_mock = MagicMock()
        self.node_mock.instance.details = {"Key1": "Value1", "Key2": "Value2"}


    def test_show_details_updates_title(self):
        self.panel.show_details(self.node_mock)

        # Extract actual markdown content
        actual_content = self.panel.details_content.update.call_args[0][0]

        self.assertIn("Key1", actual_content)
        self.assertIn("Value1", actual_content)


class TestTreeApp(unittest.TestCase):
    def setUp(self):
        self.launch_tree_mock = MagicMock(spec=LaunchTree)
        self.launch_tree_mock.root = MagicMock()
        self.launch_tree_mock.root.instance = "RootInstance"
        self.app = TreeApp(self.launch_tree_mock)

    def test_create_tree(self):
        tree = self.app.create_tree()
        self.assertEqual(str(tree.root.label), "RootInstance")
        self.assertIsNotNone(tree.root.data)

    def test_on_tree_node_highlighted(self):
        event_mock = MagicMock()
        event_mock.node = MagicMock()
        event_mock.node.data = MagicMock()
        event_mock.node.data.name = "TestNode"

        self.app.details_panel = MagicMock()
        self.app.on_tree_node_highlighted(event_mock)
        self.app.details_panel.show_details.assert_called_once_with(
            event_mock.node.data
        )


if __name__ == "__main__":
    unittest.main()
