from textual.app import ComposeResult
from textual.widgets import Button, Label, Select, Input
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll, Horizontal, Right

class PanelDatasetName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input()

class PanelDatasetInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=254,id="installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelDatasetAudit(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Audit:")
        yield Select([("ALL", 1),("FAILURES", 2),("NONE", 3),("SUCCESS", 4)],value=2,classes="uacc-select")

class PanelDatasetUACC(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("UACC:")
        yield Select([("NONE", 1),("READ", 2),("EXECUTE", 3),("UPDATE", 4),("CONTROL", 5),("ALTER", 6)],value=1,classes="uacc-select")

class PanelDatasetNotify(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Notify user:")
        yield Input(max_length=8,classes="notify-user") 

class PanelDatasetAccessSettings(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield PanelDatasetUACC()
        yield PanelDatasetAudit()
        yield PanelDatasetNotify()

class PanelDatasetActionButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Save",classes="action-button")
        yield Button("Delete",classes="action-button")

class PanelDataset(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelDatasetName()
        yield PanelDatasetInstallationData()
        yield PanelDatasetAccessSettings()
        yield PanelDatasetActionButtons()