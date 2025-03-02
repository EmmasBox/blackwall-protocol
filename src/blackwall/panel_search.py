
from textual.app import ComposeResult
from textual.widgets import Button, Input, Collapsible
from textual.containers import HorizontalGroup, VerticalScroll

class SearchField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input()
        yield Button("Search")

class PanelSearch(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield SearchField()
