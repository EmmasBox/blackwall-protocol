import commands_definition as definition
from textual.app import ComposeResult

from textual.widgets import Input
from textual.containers import HorizontalGroup

class MVSCommandField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="cli",max_length=250)