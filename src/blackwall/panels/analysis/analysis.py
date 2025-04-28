
import importlib.util

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, Label, Log, RadioButton, RadioSet

zoau_enabled = importlib.util.find_spec('zoautil_py')

#Check if ZOAU can be imported
#if zoau_enabled:
    #from zoautil_py import zsystem  # type: ignore
#else:
    #print("##BLKWL_ERROR_1 Warning: could not find ZOAU, certain features will be disabled such as diplaying system and LPAR names")    

class AnalysisSelector(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Select desired health checks: ")
        with RadioSet(id="selector-health-checks",classes="selector-health-checks"):
            yield RadioButton("UACC best practice",value=True, tooltip="Checks if UACC is being used instead of any=*")
            yield RadioButton("z/OS Unix excessive permissions",tooltip="Checks if files have RWX set for everyone on the system")
            yield RadioButton("Unprotected APF datasets",tooltip="Checks if APF datasets are unprotected by a dataset profile")
            yield RadioButton("Unused users",tooltip="Checks if users haven't been used in a really long time")

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