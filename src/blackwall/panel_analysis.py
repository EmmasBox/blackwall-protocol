
from textual.app import ComposeResult
from textual.widgets import Button, Label, RadioButton, RadioSet, Log
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll, Horizontal

class AnalysisSelector(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Select desired health checks: ")
        with RadioSet(id="selector-health-checks",classes="selector-health-checks"):
            yield RadioButton("All",value=True)
            yield RadioButton("z/OS Unix excessive permissions")
            yield RadioButton("Unprotected APF datasets")
            yield RadioButton("Unused users")

class AnalysisLog(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Log()

class AnalysisConfirm(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Run",classes="analysis-confirm")

class AnalysisMainView(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield AnalysisSelector()
        yield AnalysisLog()

class PanelAnalysis(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield AnalysisMainView()
        yield AnalysisConfirm()