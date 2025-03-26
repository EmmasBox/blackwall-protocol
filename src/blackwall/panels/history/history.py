from blackwall.command_line import command_history, CommandHistoryWidget

from textual import on
from textual.app import ComposeResult
from textual.widgets import Log
from textual.containers import VerticalScroll
from textual.events import Click

class PanelHistory(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield CommandHistoryWidget()

    @on(Click)
    def on_click(self):
        log = self.query_one(Log)
        log.clear()
        log.write(command_history)



