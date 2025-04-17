from blackwall.command_line import CommandHistoryWidget

from textual import on
from textual.app import ComposeResult
from textual.widgets import Log
from textual.containers import VerticalScroll

class PanelHistory(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Log(id="command_log")



