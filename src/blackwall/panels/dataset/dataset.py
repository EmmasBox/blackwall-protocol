from dataclasses import dataclass, fields, Field
from types import UnionType
from typing import get_args

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Label, Select, Input, Collapsible, RadioButton
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll, Horizontal, Right
from textual.reactive import reactive

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

class PanelDatasetVolume(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="base_volume")

def get_actual(field: Field) -> tuple[type,bool]:
    # UnionType is 'str | None'
    if isinstance(field.type, UnionType):
        # parse out actual type out of optional type
        # will be tuple (type(str), type(None))
        args = get_args(field.type)
        # the field is optional if type args contains 'type(None)'
        optional = type(None) in args
        # the actual type is the first non-'type(None)' in args
        actual_type = next((t for t in args if t is not type(None)), field.type)
    else:
        optional = False
        actual_type = field.type
    return actual_type, optional

def get_traits_from_input(widget: Widget, prefix: str, trait_cls: dataset.TraitsBase):
    value = trait_cls()
    for field in fields(trait_cls):
        actual_type, optional = get_actual(field)

        input_id = f"#{prefix}_{field.name}"
        try:
            field_value = widget.query_exactly_one(selector=input_id).value
        except:
            field_value = None

        if actual_type is str:
            if field_value == "":
                field_value = None
        elif actual_type is int:
            if field_value == "" or field_value == 0 or field_value is None:
                field_value = None
            else:
                field_value = int(field_value)
        elif actual_type is bool:
            if field_value is False:
                field_value = None
        setattr(value, field.name, field_value)
    return value

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
        base_segment = get_traits_from_input(self, prefix="base", trait_cls=dataset.BaseDatasetTraits)
        dataset.update_dataset_profile(
            dataset=dataset_name,
            create=not dataset_profile_exists,
            base=base_segment
            )
    def action_delete_dataset_profile(self) -> None:
        pass