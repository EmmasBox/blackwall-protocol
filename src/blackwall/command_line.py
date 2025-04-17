
from textual.app import ComposeResult

from textual.suggester import SuggestFromList
from textual import on
from textual.events import ScreenResume
from textual.widgets import Input, Log, Label
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import Screen
from textual.signal import Signal

from blackwall.commands_definition import commands

from blackwall.messages import SubmitCommand

class CommandHistoryWidget(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Command history: ")
        yield Log()
        yield Label("Press 'Esc' to exit command history")

class CommandHistoryScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield CommandHistoryWidget()
    #command_output_change
    @on(ScreenResume)
    def on_resume(self):
        on_change: Signal[str] = self.app.command_output_change # type: ignore
        on_change.subscribe(node=self,callback=self.write_to_log)
    
    def write_to_log(self, output: str):
        log = self.query_one(Log)
        log.clear()
        log.write(output)

class TSOCommandField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="cli",max_length=250,placeholder="Submit a TSO/RACF command...",classes="commands",suggester=SuggestFromList(commands,case_sensitive=False),tooltip="Use this command field to submit TSO and RACF commands. You can view the output in the command history panel")

    @on(Input.Submitted)
    def submit_command(self) -> None:
        command = self.query_exactly_one(selector="#cli").value
        SubmitCommand(command)