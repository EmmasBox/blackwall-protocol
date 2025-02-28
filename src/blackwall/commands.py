from . import commands_definition as defintion
from textual.app import ComposeResult

from textual import on
from textual.widgets import Input, Log, Label
from textual.containers import HorizontalGroup
from textual.screen import Screen

import subprocess

class CommandHistoryScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Command history: ")
        yield Log()

class MVSCommandField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="cli",max_length=250,classes="commands")

    @on(Input.Submitted)
    def execute_command(self) -> None:
        command = self.query_exactly_one(selector="#cli").value
        if command != "":
            try:
                output = subprocess.run(f'tsocmd "{command}"' , shell=True, check=True, capture_output=True,encoding="utf-8")
                log = self.parent.query_one(Log)
                log.write(output.stdout)
                self.notify(f"command {command.upper()} successfully completed",severity="information")
            except BaseException as e:
                self.notify(f"Command {command.upper()} failed: {e}",severity="error")