
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option


class PanelBackout(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Attention: changes done through commands cannot be reverted through this panel",classes="backout-label")
        yield Label("Changes available for backout",classes="backout-label")
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