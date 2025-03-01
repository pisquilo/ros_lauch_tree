from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

class TreeElement(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @property
    def details(self) -> str:
        return self.__dict__


@dataclass
class ROSNode(TreeElement):
    name: str

    def __repr__(self):
        return f":gear:  Node => {self.name}"


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
