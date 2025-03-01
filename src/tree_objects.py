from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

from roslaunch.core import Node


def filter_dict(dict: Dict[Any, Any]) -> Dict[Any, Any]:
    return {key: value for key, value in dict.items() if value}


class TreeElement(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @property
    def details(self) -> Dict[str, Any]:
        return filter_dict(self.__dict__)


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
        return filter_dict(node_dict)

    def __repr__(self):
        return (
            f":gear:  Node => {self.node.name} ({self.node.package} | {self.node.type})"
        )


@dataclass
class Param(TreeElement):
    key: str
    value: Any

    def __repr__(self):
        return f":parking:  Param => {self.key}: {self.value}"


@dataclass
class ROSParam(TreeElement):
    unique_name: str
    command: Any

    def __repr__(self):
        return f"[bold red]P[/bold red]  ROSParam => {self.unique_name}: {self.command}"


@dataclass
class Test(TreeElement):
    name: str

    def __repr__(self):
        return f":white_check_mark: Test => {self.name}"


@dataclass
class Arg(TreeElement):
    name: str
    value: str

    def __repr__(self):
        return f":A:  Arg => {self.name}: {self.value}"


@dataclass
class Remap(TreeElement):
    from_topic: str
    to_topic: str

    def __repr__(self):
        return f":left_right_arrow:  Remap  => {self.from_topic}: {self.to_topic}"


@dataclass
class File(TreeElement):
    name: str

    def __repr__(self):
        return f":page_facing_up: File  => {self.name}"
