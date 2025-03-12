
from textual.app import ComposeResult
from textual.widgets import Button, Input, Label, RadioButton, RadioSet, TabbedContent, TabPane
from textual.containers import HorizontalGroup, VerticalScroll

from blackwall.panels.search.results import PanelResultsMixedType

class SearchSelector(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with RadioSet(id="type-selector",classes="search-selector"):
            yield RadioButton("Any",value=True)
            yield RadioButton("User")
            yield RadioButton("Dataset profile")
            yield RadioButton("Resource profile")
        with RadioSet(id="filter-selector",classes="search-selector"):
            yield RadioButton("All",disabled=True)
            yield RadioButton("Only one",value=True)

class SearchField(HorizontalGroup):
    def action_search(self) -> None:
        # This is really stupid but it works *insert shrug emoji*
        tabs = self.parent.parent.parent.parent.parent.query_one(TabbedContent)
        tabs.add_pane(TabPane("Results",PanelResultsMixedType()))

    def compose(self) -> ComposeResult:
        yield Label("Search:")
        yield Input(name="Search",classes="search-field")
        yield Button("Search",action="search")

class PanelSearch(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield SearchSelector()
        yield SearchField()
