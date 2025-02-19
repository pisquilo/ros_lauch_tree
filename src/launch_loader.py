from roslaunch.xmlloader import XmlLoader
from launch_config import LaunchConfig


class TreeLoader(XmlLoader):
    def _include_tag(self, tag, context, ros_config: LaunchConfig, default_machine, is_core, verbose):
        inc_filename = self.resolve_args(tag.attributes['file'].value, context)
        ros_config.push_level(inc_filename)
        default_machine = super()._include_tag(
            tag, context, ros_config, default_machine, is_core, verbose
        )
        ros_config.pop_level()

        return default_machine

    def load(self, filename, ros_config: LaunchConfig, core=False, argv=None, verbose=True):
        ros_config.add_root(filename)
        return super().load(filename, ros_config, core, argv, verbose)
