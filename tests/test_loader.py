import unittest
from unittest.mock import MagicMock, patch
from xml.dom.minidom import parseString

from roslaunch.core import Node as ROSLaunchNode, Test as ROSLaunchTest
from roslaunch.xmlloader import XmlParseException

from src.tree_objects import ROSNode, Param, Test, Arg, Remap, ROSParam
from src.tree import LaunchTree
from src.loader import TreeLoader


class TestTreeLoader(unittest.TestCase):
    def setUp(self):
        self.loader = TreeLoader()
        self.loader.tree = MagicMock(spec=LaunchTree)

    def test_ifunless_attribute_if(self):
        tag = parseString('<node if="true"/>').documentElement
        result = self.loader._ifunless_atribute(tag, {})
        self.assertTrue(result)

    def test_ifunless_attribute_unless(self):
        tag = parseString('<node unless="false"/>').documentElement
        result = self.loader._ifunless_atribute(tag, {})
        self.assertTrue(result)

    def test_ifunless_attribute_none(self):
        tag = parseString("<node/>").documentElement
        result = self.loader._ifunless_atribute(tag, {})
        self.assertIsNone(result)

    @patch("src.loader.XmlLoader._include_tag")
    def test_include_tag(self, mock_include_tag):
        tag = parseString('<include file="test.launch"/>').documentElement
        self.loader._include_tag(tag, {}, None, None, False, False)
        self.loader.tree.push_level.assert_called_once_with("test.launch", None)
        self.loader.tree.pop_level.assert_called_once()

    @patch("src.loader.XmlLoader._param_tag")
    def test_param_tag(self, mock_param_tag):
        tag = parseString('<param name="test_param" value="42"/>').documentElement
        mock_param_tag.return_value.key = "test_param"
        mock_param_tag.return_value.value = "42"

        self.loader._param_tag(tag, {}, None)
        self.loader.tree.add.assert_called_once_with(
            "test_param", Param("test_param", "42")
        )

    @patch("src.loader.XmlLoader._node_tag")
    def test_node_tag(self, mock_node_tag):
        tag = parseString('<node name="test_node"/>').documentElement
        mock_node = ROSLaunchNode("package", "executable", name="test_node")
        mock_node_tag.return_value = mock_node

        self.loader._node_tag(tag, {}, None, None)
        self.loader.tree.add.assert_called_once_with("test_node", ROSNode("test_node"))

    @patch("src.loader.XmlLoader._arg_tag")
    def test_arg_tag(self, mock_arg_tag):
        tag = parseString('<arg name="test_arg" value="10"/>').documentElement
        self.loader._arg_tag(tag, {}, None)
        self.loader.tree.add.assert_called_once_with(["test_arg"], Arg(["test_arg"], ["10"]))

    @patch("src.loader.XmlLoader._remap_tag")
    def test_remap_tag(self, mock_remap_tag):
        tag = parseString('<remap from="old_topic" to="new_topic"/>').documentElement
        mock_remap_tag.return_value = ("old_topic", "new_topic")

        self.loader._remap_tag(tag, {}, None)
        self.loader.tree.add.assert_called_once_with(
            "old_topic", Remap("old_topic", "new_topic")
        )

    @patch("src.loader.XmlLoader._rosparam_tag")
    def test_rosparam_tag(self, mock_rosparam_tag):
        tag = parseString(
            '<rosparam command="load" file="config.yaml"/>'
        ).documentElement
        self.loader._rosparam_tag(tag, {}, None)
        mock_rosparam_tag.assert_called_once()

    @patch("src.loader.XmlLoader.load")
    def test_load(self, mock_load):
        self.loader.load("test.launch", None)
        self.assertIsInstance(self.loader.tree, LaunchTree)
        mock_load.assert_called_once_with("test.launch", None, False, None, True)


if __name__ == "__main__":
    unittest.main()
