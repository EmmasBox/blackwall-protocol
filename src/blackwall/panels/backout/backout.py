
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option


class PanelBackout(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Backout changes",classes="backout-title")
        yield OptionList(
            Option("27/04/2025 at 20:30 - Created user 'BLATEST1'"),
            None,
            Option("27/04/2025 at 20:30 - Deleted user 'BLATEST2'"),
            None,
            Option("27/04/2025 at 20:30 - Created resource 'BLATEST3.**' profile"),
            None,
            Option("27/04/2025 at 20:30 - Updated dataset 'BLATEST7.**' profile"),
            None,
            Option("27/04/2025 at 20:30 - Updated system options (SETROPTS)"),
        )