from blackwall.command_line import command_history, CommandHistoryWidget

from textual import on
from textual.app import ComposeResult
from textual.widgets import Log
from textual.containers import VerticalScroll

from blackwall.messages import CommandHistory

class PanelHistory(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield CommandHistoryWidget()

    def on_command_history(self, message: CommandHistory):
        message.stop()
        log = self.query_one(Log)
        log.clear()
        log.write(message.history)



