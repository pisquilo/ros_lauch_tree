from roslaunch.core import Node, Test
from roslaunch.loader import convert_value
from roslaunch.xmlloader import XmlLoader

from tree_objects import (
    TreeNode,
    TreeParam,
    TreeTest,
    TreeArg,
    TreeRemap,
    TreeROSParam,
)
from launch_tree import LaunchTree

class TreeLoader(XmlLoader):

    def __init__(self, resolve_anon=True, args_only=False):
        super().__init__(resolve_anon, args_only)

        self.tree = None

    def _ifunless_atribute(self, tag, context):
        if_val, unless_val = self.opt_attrs(tag, context, ["if", "unless"])
        if if_val is None and unless_val is None:
            return None
        if if_val is not None:
            if_val = convert_value(if_val, "bool")
            if if_val:
                return True
        elif unless_val is not None:
            unless_val = convert_value(unless_val, "bool")
            if not unless_val:
                return True

    def _include_tag(self, tag, context, ros_config, default_machine, is_core, verbose):
        inc_filename = self.resolve_args(tag.attributes['file'].value, context)
        ifunless = self._ifunless_atribute(tag, context)

        self.tree.push_level(inc_filename, ifunless)
        default_machine = super()._include_tag(
            tag, context, ros_config, default_machine, is_core, verbose
        )
        self.tree.pop_level()

        return default_machine

    def _param_tag(self, tag, context, ros_config, force_local=False, verbose=True):
        param = super()._param_tag(tag, context, ros_config, force_local, verbose)
        self.tree.add(param.key, TreeParam(param.key, param.value))
        return param

    def _node_tag(
        self, tag, context, ros_config, default_machine, is_test=False, verbose=True
    ):
        node = super()._node_tag(
            tag, context, ros_config, default_machine, is_test, verbose
        )
        if isinstance(node, Node):
            self.tree.add(node.name, TreeNode(node.name))
        elif isinstance(node, Test):
            self.tree.add(node.test_name, TreeTest(node.test_name))
        return node

    def _arg_tag(self, tag, context, ros_config, verbose=True):
        name = self.reqd_attrs(tag, context, ["name"])
        value = self.opt_attrs(tag, context, ["value"])
        self.tree.add(name, TreeArg(name, value))

        return super()._arg_tag(tag, context, ros_config, verbose)

    def _remap_tag(self, tag, context, ros_config):
        from_topic, to_topic = super()._remap_tag(tag, context, ros_config)
        self.tree.add(from_topic, TreeRemap(from_topic, to_topic))

        return from_topic, to_topic

    def _rosparam_tag(self, tag, context, ros_config, verbose=True):
        return super()._rosparam_tag(tag, context, ros_config, verbose)

    def load(self, filename, ros_config, core=False, argv=None, verbose=True):
        self.tree = LaunchTree(filename)
        super().load(filename, ros_config, core, argv, verbose)

    def add_rosparam(self, command, filename, unique_name):
        self._add_to_tree(unique_name, TreeROSParam(unique_name, command))
