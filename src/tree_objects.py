import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

from roslaunch.core import Node, Test


def _filter_dict(dict: Dict[Any, Any]) -> Dict[Any, Any]:
    return {key: value for key, value in dict.items() if value}


def _escape_char_for_list(text: str) -> str:
    replacements = {"[": r"\["}

    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


class TreeElement(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @property
    def details(self) -> Dict[str, Any]:
        return _filter_dict(self.__dict__)


@dataclass
class ROSNode(TreeElement):
    node: Node
    ifunless: Optional[bool] = None

    @property
    def details(self) -> Dict[str, Any]:
        node_dict = {
            "package": self.node.package,
            "type": self.node.type,
            "name": self.node.name,
            "namespace": self.node.namespace,
            "machine_name": self.node.machine_name,
            "args": self.node.args,
            "respawn": self.node.respawn,
            "output": self.node.output,
            "cwd": self.node.cwd,
            "env_args": self.node.env_args,
            "remap_args": self.node.remap_args,
            "required": self.node.required,
            "launch_prefix": self.node.launch_prefix,
            "if/unless": self.ifunless,
        }
        return _filter_dict(node_dict)

    def __repr__(self) -> str:
        return (
            f":gear:  Node => {self.node.name} ({self.node.package} | {self.node.type})"
        )


@dataclass
class Param(TreeElement):
    key: str
    value: Any

    def __repr__(self) -> str:
        return f":parking:  Param => {self.key}: {self.value}"


@dataclass
class ROSParam(TreeElement):
    command: str = "load"
    name: Optional[str] = None
    file: Optional[str] = None
    namespace: Optional[str] = None
    subst_value: Optional[bool] = None
    body: Optional[str] = None

    def __repr__(self) -> str:
        text = f"  ROSParam => {self.command or self.name}: {self.file or self.body}"

        return "[bold white]P[/bold white]" + _escape_char_for_list(text)


@dataclass
class Test(TreeElement):
    test: Test

    @property
    def details(self) -> Dict[str, Any]:
        test_dict = {
            "package": self.test.package,
            "test_type": self.test.type,
            "name": self.test.name,
            "namespace": self.test.namespace,
            "args": self.test.args,
            "retry": self.test.retry,
            "time_limit": self.test.time_limit,
            "cwd": self.test.cwd,
            "env_args": self.test.env_args,
            "launch_prefix": self.test.launch_prefix,
        }
        return _filter_dict(test_dict)

    def __repr__(self) -> str:
        return f":white_check_mark: Test => {self.name}"


@dataclass
class Arg(TreeElement):
    name: str
    value: str

    def __repr__(self) -> str:
        return f":A:  Arg => {self.name}: {self.value}"


@dataclass
class Remap(TreeElement):
    from_topic: str
    to_topic: str

    def __repr__(self) -> str:
        return f":left_right_arrow:  Remap  => {self.from_topic}: {self.to_topic}"


@dataclass
class File(TreeElement):
    name: str

    @property
    def details(self) -> str:
        """Return the contents of the file as details, or an error message if unreadable."""
        if os.path.isfile(self.name):  # Check if the file exists
            try:
                with open(self.name, "r", encoding="utf-8") as f:
                    return f.read()  # Return file contents
            except Exception as e:
                return f"Error reading file: {e}"  # Handle errors gracefully
        return "File not found."

    def __repr__(self) -> str:
        return f":page_facing_up: File  => {self.name}"
