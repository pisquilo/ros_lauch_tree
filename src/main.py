import os

from rqt_launchtree.launchtree_loader import LaunchtreeLoader
from rqt_launchtree.launchtree_config import LaunchtreeConfig

from roslaunch.xmlloader import XmlLoader
from launch_config import  LaunchConfig
from launch_loader import TreeLoader

from app import TreeApp
from anytree import RenderTree
def main(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(filename)

    # loader = LaunchtreeLoader()
    # config = LaunchtreeConfig()

    loader = TreeLoader()
    config = LaunchConfig()

    loader.load(filename, config, verbose=False)

    app = TreeApp(config)
    app.run()

if __name__ == "__main__":
    filename = os.path.join(
        "/home/ferreira/workspace/ros_lauch_tree", "launch", "test.launch"
    )
    main(filename)
