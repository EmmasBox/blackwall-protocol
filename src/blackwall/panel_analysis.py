
from textual.app import ComposeResult
from textual.widgets import Button, Label, RadioButton, RadioSet
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

class AnalysisSelector(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Select desired health checks: ")
        with RadioSet(id="selector-health-checks",classes="selector-health-checks"):
            yield RadioButton("All",value=True)
            yield RadioButton("z/OS Unix excessive permissions")
            yield RadioButton("Unprotected APF datasets")
            yield RadioButton("Unused users")

class AnalysisConfirm(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Run")

class PanelAnalysis(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield AnalysisSelector()
        yield AnalysisConfirm()