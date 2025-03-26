from blackwall.command_line import command_history, CommandHistoryWidget

from textual import on
from textual.app import ComposeResult
from textual.widgets import Log
from textual.containers import VerticalScroll

from blackwall.messages import CommandHistory

class PanelHistory(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Log(id="command_log")

    @on(CommandHistory)
    async def on_command_history(self, message: CommandHistory):
        pass



