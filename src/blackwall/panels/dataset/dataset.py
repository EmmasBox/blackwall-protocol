from dataclasses import dataclass, fields, Field

from textual.app import ComposeResult
from textual.widgets import Button, Label, Select, Input, Collapsible, RadioButton
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll, Horizontal, Right

from blackwall.panels.panel_mode import PanelMode

class PanelDatasetName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input()

class PanelDatasetInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=254,id="base_installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelDatasetAudit(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible(title="Auditing"):
            yield Label("Notify user:")
            yield Input(id="base_notify_userid",max_length=8,classes="field-short-generic") 
            yield RadioButton(label="NONE",id="base_audit_none")
            yield RadioButton(label="READ",id="base_audit_read")
            yield RadioButton(label="UPDATE",id="base_audit_update")
            yield RadioButton(label="CONTROL",id="base_audit_control")
            yield RadioButton(label="ALTER",id="base_audit_alter")
        
class PanelDatasetSecurityLevelAndCategories(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible(title="Security level and category"):
            yield Label("Security level")
            yield Input(max_length=8,id="base_security_level",classes="field-short-generic")
            yield Label("Security category:")
            yield Input(max_length=8,id="base_security_category",classes="field-short-generic")
            yield Label("Security label:")
            yield Input(max_length=8,id="base_security_label",classes="field-short-generic")

class PanelDatasetUACC(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("UACC:")
        yield Select([("NONE", 1),("READ", 2),("EXECUTE", 3),("UPDATE", 4),("CONTROL", 5),("ALTER", 6)],value=1,classes="uacc-select",id="base_universal_access")

class PanelDatasetNotify(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Notify user:")
        yield Input(id="base_notify_userid",max_length=8,classes="notify-user") 

class PanelDatasetActionButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Save",classes="action-button")
        yield Button("Delete",classes="action-button")

class PanelDatasetVolume(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="base_volume")

@dataclass
class DatasetInfo:
    mode: PanelMode = PanelMode.create

class PanelDataset(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelDatasetName()
        yield PanelDatasetInstallationData()
        yield PanelDatasetUACC()
        yield PanelDatasetSecurityLevelAndCategories()
        yield PanelDatasetAudit()
        yield PanelDatasetActionButtons()