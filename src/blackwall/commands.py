from . import commands_definition as defintion
from textual.app import ComposeResult

from textual import on
from textual.widgets import Input, Log, Label
from textual.containers import HorizontalGroup
from textual.screen import Screen

import subprocess

command_history = ""

class CommandHistoryScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Label("Command history: ")
        yield Log(command_history)

class MVSCommandField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="cli",max_length=250,classes="commands")

    @on(Input.Submitted)
    def execute_command(self) -> None:
        command = self.query_exactly_one(selector="#cli").value
        if command != "":
            try:
                output = subprocess.run(f'tsocmd "{command}"' , shell=True, check=True, capture_output=True)
                command_history = command_history + output
                self.notify(f"command {command.upper()} successfully completed",severity="information")
            except:
                self.notify(f"Command {command.upper()} failed",severity="error")