from typing import Iterable

from textual.app import SystemCommand
from textual.screen import Screen

class Subcommands():
    def get_system_commands(self) -> Iterable[SystemCommand]:
        yield SystemCommand("User creation", "Open a new tab with the user creation panel", self.bell)  