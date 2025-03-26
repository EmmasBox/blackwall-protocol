from blackwall.command_line import command_history, CommandHistoryWidget

from textual import on
from textual.app import ComposeResult
from textual.widgets import Log
from textual.containers import VerticalScroll
from textual.events import Enter

class PanelHistory(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield CommandHistoryWidget()

    @on(Enter)
    def on_enter(self):
        log = self.query_one(Log)
        log.clear()
        log.write(command_history)



