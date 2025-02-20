from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

class TreeElement(ABC):
    @abstractmethod
    def __repr__(self):
        pass

@dataclass
class TreeNode(TreeElement):
    name: str

    def __repr__(self):
        return f':gear: Node => {self.name}'

@dataclass
class TreeParam(TreeElement):
    key: str
    value: Any

    def __repr__(self):
        return f":parking: Param => {self.key}: {self.value}"


@dataclass
class TreeROSParam(TreeElement):
    unique_name: str
    command: Any

    def __repr__(self):
        return f"[bold red]P[/bold red] ROSParam => {self.unique_name}: {self.command}"


@dataclass
class TreeTest(TreeElement):
    name: str

    def __repr__(self):
        return f":white_check_mark: Test => {self.name}"


@dataclass
class TreeArg(TreeElement):
    name: str
    value: str

    def __repr__(self):
        return f":white_check_mark: Arg => {self.name}: {self.value}"


@dataclass
class TreeRemap(TreeElement):
    from_topic: str
    to_topic: str

    def __repr__(self):
        return f":left_right_arrow: Remap  => {self.from_topic}: {self.to_topic}"
