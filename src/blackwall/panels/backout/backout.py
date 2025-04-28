
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option


class PanelBackout(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Backout changes",classes="backout-title")
        yield OptionList(
            Option("Create user 27/04/2025 at 20:30"),
            None,
            Option("Delete user 27/04/2025 at 20:30"),
            None,
            Option("Create resource profile 27/04/2025 at 20:30"),
            None,
            Option("Update dataset profile 27/04/2025 at 20:30"),
        )