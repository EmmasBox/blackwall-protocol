from dataclasses import dataclass

from textual.app import ComposeResult
from textual.widgets import Button, Label, Select, Input, Collapsible, RadioButton
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.reactive import reactive

from blackwall.panels.traits_ui import get_traits_from_input

from blackwall.panels.panel_mode import PanelMode

from blackwall.api import dataset

class PanelDatasetName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input(id="dataset_name")

class PanelDatasetOwner(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Owner:")
        yield Input(id="base_owner")

class PanelDatasetInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="base_installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelDatasetAudit(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible(title="Auditing"):
            yield Label("Notify user:")
            yield Input(id="base_notify_userid",max_length=8,classes="field-short-generic") 
            yield Label("Audit NONE:")
            yield Input(id="base_audit_none",classes="field-medium-generic")
            yield Label("Audit READ:")
            yield Input(id="base_audit_read",classes="field-medium-generic")
            yield Label("Audit UPDATE:")
            yield Input(id="base_audit_update",classes="field-medium-generic")
            yield Label("Audit CONTROL:")
            yield Input(id="base_audit_control",classes="field-medium-generic")
            yield Label("Audit ALTER:")
            yield Input(id="base_audit_alter",classes="field-medium-generic")
        
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
        yield Select([("NONE", "NONE"),("READ", "READ"),("EXECUTE", "EXECUTE"),("UPDATE", "UPDATE"),("CONTROL", "CONTROL"),("ALTER", "ALTER")],value="NONE",classes="uacc-select",id="base_universal_access")

class PanelDatasetNotify(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Notify user:")
        yield Input(id="base_notify_userid",max_length=8,classes="field-short-generic")

class PanelDatasetVolume(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="base_volume")

class PanelDatasetActionButtons(HorizontalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    if edit_mode is True:
        delete_is_disabled = False
    else:
        delete_is_disabled = True

    def __init__(self, save_action: str, delete_action: str):
        super().__init__()
        self.save_action = save_action
        self.delete_action = delete_action
    
    def compose(self) -> ComposeResult:
        yield Button("Save",action="save",classes="action-button")
        yield Button("Delete",action="delete",classes="action-button",disabled=self.delete_is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

@dataclass
class DatasetInfo:
    mode: PanelMode = PanelMode.create

class PanelDataset(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelDatasetName()
        yield PanelDatasetOwner()
        yield PanelDatasetInstallationData()
        yield PanelDatasetUACC()
        yield PanelDatasetSecurityLevelAndCategories()
        yield PanelDatasetAudit()
        yield PanelDatasetActionButtons(save_action="save_dataset_profile", delete_action="delete_dataset_profile")

    def action_save_dataset_profile(self) -> None:
        dataset_name = self.query_exactly_one(selector="#dataset_name").value
        dataset_profile_exists = dataset.dataset_profile_exists(dataset=dataset_name)

        if dataset_profile_exists:
            operator = "alter"
        else:
            operator = "add"

        base_segment = get_traits_from_input(operator,self, prefix="base", trait_cls=dataset.BaseDatasetTraits)
        result = dataset.update_dataset_profile(
            dataset=dataset_name,
            create=not dataset_profile_exists,
            base=base_segment
            )
        
        if not dataset_profile_exists:
            if (result == 0 or result == 4):
                self.notify(f"Dataset profile {dataset_name} created, return code: {result}",severity="information")
                #self.set_edit_mode()
            else:
                self.notify(f"Unable to create dataset profile, return code: {result}",severity="error")
        else:
            if (result == 0 or result == 4):
                self.notify(f"Dataset profile {dataset_name} updated, return code: {result}",severity="information")
            else:
                self.notify(f"Unable to update dataset profile, return code: {result}",severity="error")

    def action_delete_dataset_profile(self) -> None:
        pass