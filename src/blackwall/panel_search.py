
from textual.app import ComposeResult
from textual.widgets import Button, Input, Label, Collapsible
from textual.containers import HorizontalGroup, VerticalScroll

class SearchField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Search:")
        yield Input(name="Search",classes="search-field")
        yield Button("Search")

class PanelSearch(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield SearchField()
