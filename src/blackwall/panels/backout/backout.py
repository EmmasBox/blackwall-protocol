
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option


class PanelBackout(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Backout changes",classes="backout-title")
        yield OptionList(
            Option("Created user 'BLATEST1' 27/04/2025 at 20:30"),
            None,
            Option("Deleted user 'BLATEST2' 27/04/2025 at 20:30"),
            None,
            Option("Created resource 'BLATEST3.**' profile 27/04/2025 at 20:30"),
            None,
            Option("Updated dataset 'BLATEST7.**' profile 27/04/2025 at 20:30"),
            None,
            Option("Updated system options (SETROPTS) 27/04/2025 at 20:30"),
        )