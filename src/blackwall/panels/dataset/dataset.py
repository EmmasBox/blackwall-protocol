from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Collapsible, Input, Label, RadioButton, Select

from blackwall.api import dataset
from blackwall.emoji import get_emoji
from blackwall.modals import generic_confirmation_modal
from blackwall.notifications import send_notification
from blackwall.panels.panel_mode import PanelMode
from blackwall.panels.traits_ui import get_traits_from_input, set_traits_in_input
from blackwall.regex import racf_id_regex


class PanelDatasetInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Last change date:",classes="date-labels")
        yield Input(id="base_last_change_date",disabled=True,classes="date-fields")
        yield Label("Creation date:",classes="date-labels")
        yield Input(id="base_create_date",disabled=True,classes="date-fields")

class PanelDatasetName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input(id="profile_name")

class PanelDatasetOwner(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Owner:")
        yield Input(id="base_owner",max_length=8,restrict=racf_id_regex)

class PanelDatasetInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="base_installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelDatasetAudit(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible(title="Auditing"):
            yield Label("Notify user:")
            yield Input(id="base_notify_userid",max_length=8,restrict=racf_id_regex,classes="field-short-generic") 
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
        yield Input(id="base_notify_userid",restrict=racf_id_regex,max_length=8,classes="field-short-generic")

class PanelDatasetVolume(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="base_volume")

class PanelDatasetSettings(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible(title="General settings"):
            yield RadioButton(id="base_erase_data_sets_on_delete",label="Erase dataset on deletion")
            yield Label("Model profile volume:")
            yield Input(id="base_model_profile_volume",max_length=8,classes="field-short-generic")
            yield Label("Model profile class:")
            yield Input(id="base_model_profile_class",max_length=8,classes="field-short-generic")
            yield Label("Model profile generic:")
            yield Input(id="base_model_profile_generic",max_length=255,classes="field-long-generic")
            yield Label("Model profile:")
            yield Input(id="base_model_profile",max_length=255,classes="field-long-generic")
            yield Label("Dataset model profile:")
            yield Input(id="base_data_set_model_profile",max_length=255,classes="field-long-generic")
            yield Label("Volume:")
            yield Input(id="base_volume",max_length=8,classes="field-short-generic")

class PanelDatasetActionButtons(HorizontalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    delete_is_disabled = edit_mode is not True

    def __init__(self, save_action: str, delete_action: str):
        super().__init__()
        self.save_action = save_action
        self.delete_action = delete_action
    
    def compose(self) -> ComposeResult:
        yield Button("Create",id="save",action="save",classes="action-button")
        yield Button("Delete",action="delete",id="delete",variant="error",classes="action-button",disabled=self.delete_is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

@dataclass
class DatasetInfo:
    base_traits: dataset.BaseDatasetTraits | None = None
    mode: PanelMode = PanelMode.create

    profile_name: str = ""

class PanelDataset(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelDatasetInfo()
        yield PanelDatasetName()
        yield PanelDatasetOwner()
        yield PanelDatasetInstallationData()
        yield PanelDatasetUACC()
        yield PanelDatasetSettings()
        yield PanelDatasetSecurityLevelAndCategories()
        yield PanelDatasetAudit()
        yield PanelDatasetActionButtons(save_action="save_dataset_profile", delete_action="delete_dataset_profile")

    dataset_info: reactive[DatasetInfo] = reactive(DatasetInfo())

    def set_edit_mode(self):
        self.query_exactly_one("#profile_name",Input).disabled = True
        self.query_exactly_one("#delete",Button).disabled = False
        self.query_exactly_one("#save",Button).label = f"{get_emoji("💾")} Save"
        self.notify("Switched to edit mode",severity="information")

    def on_mount(self) -> None:
        if dataset.dataset_profile_exists(self.dataset_info.profile_name):
            self.query_exactly_one("#profile_name",Input).value = self.dataset_info.profile_name
            if self.dataset_info.base_traits is not None:
                set_traits_in_input(self,traits=self.dataset_info.base_traits,prefix="base")

            self.set_edit_mode()

    def action_delete_dataset_api(self) -> None:
        dataset_name = self.get_child_by_type(PanelDatasetName).get_child_by_id("profile_name",Input).value
        if dataset.dataset_profile_exists(dataset_name):
            message, return_code = dataset.delete_dataset_profile(dataset_name)
            
            if (return_code == 0):
                self.notify(f"Dataset profile {dataset_name} deleted, return code: {return_code}",severity="warning")
            else:
                self.notify(f"{message}, return code: {return_code}",severity="error")

    def action_delete_dataset_profile(self) -> None:
        dataset_name = self.get_child_by_type(PanelDatasetName).get_child_by_id("profile_name",Input).value
        generic_confirmation_modal(self,modal_text=f"Are you sure you want to delete dataset profile {dataset_name}?",confirm_action="delete_dataset_api",action_widget=self)

    def action_save_dataset_profile(self) -> None:
        dataset_name = self.get_child_by_type(PanelDatasetName).get_child_by_id("profile_name",Input).value
        dataset_profile_exists = dataset.dataset_profile_exists(dataset=dataset_name)

        operator = "alter" if dataset_profile_exists else "add"

        base_segment = get_traits_from_input(operator,self, prefix="base", trait_cls=dataset.BaseDatasetTraits)

        dataset_object = dataset.DatasetObject(
            base_traits=base_segment,
        )

        result = dataset.update_dataset_profile(
            dataset=dataset_name,
            create=not dataset_profile_exists,
            dataset_object=dataset_object,
            )
        
        if not dataset_profile_exists:
            if (result == 0 or result == 4):
                self.notify(f"Dataset profile {dataset_name} created, return code: {result}",severity="information")
                #self.set_edit_mode()
            else:
                send_notification(self,message=f"Unable to create dataset profile, return code: {result}",severity="error")
        else:
            if result == 0:
                self.notify(f"Dataset profile {dataset_name} updated, return code: {result}",severity="information")
            else:
                send_notification(self,message=f"Unable to update dataset profile, return code: {result}",severity="error")