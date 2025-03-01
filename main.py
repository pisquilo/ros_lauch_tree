import os
import argparse

from roslaunch.config import ROSLaunchConfig

from src.launch_loader import TreeLoader
from src.app import TreeApp


def main(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    loader = TreeLoader()
    config = ROSLaunchConfig()

    loader.load(filename, config, verbose=False)

    app = TreeApp(loader.tree)
    app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch Tree Debugger")
    parser.add_argument(
        "filename",
        nargs="?",
        default=os.path.join(
            "/home/ferreira/workspace/ros_lauch_tree", "launch", "test.launch"
        ),
        help="Path to the ROS launch file (default: test.launch)",
    )

    args = parser.parse_args()
    main(args.filename)
