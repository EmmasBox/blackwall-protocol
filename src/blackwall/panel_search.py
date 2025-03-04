
from textual.app import ComposeResult
from textual.widgets import Button, Input, Label, RadioButton, RadioSet
from textual.containers import HorizontalGroup, VerticalScroll

class SearchSelector(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with RadioSet(id="type-selector",classes="search-selector"):
            yield RadioButton("Any",value=True)
            yield RadioButton("User")
            yield RadioButton("Dataset profile")
            yield RadioButton("Resource profile")
        with RadioSet(id="filter-selector",classes="search-selector"):
            yield RadioButton("All",value=True)
            yield RadioButton("Only one")

class SearchField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Search:")
        yield Input(name="Search",classes="search-field")
        yield Button("Search")

class PanelSearch(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield SearchSelector()
        yield SearchField()
