import unittest
from src.tree_objects import File, TreeElement
from src.tree import Node, LaunchTree

class TestNode(unittest.TestCase):
    def setUp(self):
        self.instance = File("root_file")
        self.node = Node(name="root", instance=self.instance)

    def test_node_creation(self):
        self.assertEqual(self.node.name, "root")
        self.assertEqual(self.node.instance, self.instance)
        self.assertIsNone(self.node.ifunless)

    def test_node_instance_setter(self):
        new_instance = File("new_file")
        self.node.instance = new_instance
        self.assertEqual(self.node.instance, new_instance)

    def test_node_ifunless_setter(self):
        self.node.ifunless = True
        self.assertTrue(self.node.ifunless)

        self.node.ifunless = False
        self.assertFalse(self.node.ifunless)

        self.node.ifunless = None
        self.assertIsNone(self.node.ifunless)


class TestLaunchTree(unittest.TestCase):
    def setUp(self):
        self.tree = LaunchTree("root")

    def test_launch_tree_creation(self):
        self.assertEqual(self.tree.root.name, "root")
        self.assertIsInstance(self.tree.root.instance, File)
        self.assertEqual(len(self.tree.parent_stack), 1)

    def test_push_level(self):
        self.tree.push_level("level1")
        self.assertEqual(len(self.tree.parent_stack), 2)
        self.assertEqual(self.tree._current_parent.name, "level1")

    def test_pop_level(self):
        self.tree.push_level("level1")
        self.tree.pop_level()
        self.assertEqual(len(self.tree.parent_stack), 1)
        self.assertEqual(self.tree._current_parent.name, "root")

    def test_add_node(self):
        file_instance = File("child_file")
        self.tree.add("child", file_instance)
        child_node = self.tree.root.children[0]
        self.assertEqual(child_node.name, "child")
        self.assertEqual(child_node.instance, file_instance)
        self.assertIsNone(child_node.ifunless)


if __name__ == "__main__":
    unittest.main()
