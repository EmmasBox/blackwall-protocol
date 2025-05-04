from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Input, Label, RadioButton

from blackwall.api import group
from blackwall.emoji import get_emoji
from blackwall.modals import generic_confirmation_modal
from blackwall.notifications import send_notification
from blackwall.panels.panel_mode import PanelMode
from blackwall.regex import racf_id_regex

from ..traits_ui import (
    generate_trait_section,
    get_traits_from_input,
    set_traits_in_input,
)


class PanelGroupInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Creation date:",classes="date-labels")
        yield Input(id="base_create_date",disabled=True,classes="date-fields")

class PanelGroupNameAndSubgroup(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Group name:")
        yield Input(id="group_name",restrict=racf_id_regex,max_length=8,classes="field-short-generic",tooltip="1-8 character long alphanumeric name used to identify the group")
        yield Label("Superior group:")
        yield Input(max_length=8,restrict=racf_id_regex,id="base_superior_group",classes="field-short-generic",tooltip="Superior group in the RACF database")
        yield Label("Owner:")
        yield Input(max_length=8,restrict=racf_id_regex,id="base_owner",classes="field-short-generic",tooltip="Owner of the group, can be a user or group.")

class PanelGroupInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="base_installation_data",classes="installation-data",tooltip="Optional used defined data. This can be used to put in a description about what the group is used for. Can't be more than 255 characters long.")

class PanelGroupDatasetModel(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Dataset model:")
        yield Input(id="base_data_set_model",classes="field-long-generic")

class PanelGroupTerminalUACC(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield RadioButton(label="Terminal UACC",id="base_terminal_universal_access",classes="generic-checkbox-medium")

class PanelGroupSegments(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield from generate_trait_section(title="DFP segment", prefix="dfp", traits_class=group.DFPGroupTraits)
        yield from generate_trait_section(title="z/OS Unix (OMVS) segment", prefix="omvs", traits_class=group.OMVSGroupTraits)

class PanelGroupActionButtons(HorizontalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    delete_is_disabled = edit_mode is not True

    def __init__(self, save_action: str, delete_action: str):
        super().__init__()
        self.save_action = save_action
        self.delete_action = delete_action
    
    def compose(self) -> ComposeResult:
        yield Button("Create",id="save",action="save",classes="action-button")
        yield Button("Delete",id="delete",action="delete",variant="error",classes="action-button",disabled=self.delete_is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

@dataclass
class GroupInfo:
    base_traits: group.BaseGroupTraits | None = None
    dfp_traits: group.DFPGroupTraits | None = None

    group_name: str = ""

class PanelGroup(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelGroupInfo()
        yield PanelGroupNameAndSubgroup()
        yield PanelGroupInstallationData()
        yield PanelGroupDatasetModel()
        yield PanelGroupTerminalUACC()
        yield PanelGroupSegments()
        yield PanelGroupActionButtons(save_action="save_group",delete_action="delete_group")

    group_info: reactive[GroupInfo] = reactive(GroupInfo())

    def set_edit_mode(self):
        self.query_exactly_one("#group_name",Input).disabled = True
        self.query_exactly_one("#delete",Button).disabled = False
        self.query_exactly_one("#save",Button).label = f"{get_emoji("💾")} Save"
        self.notify("Switched to edit mode",severity="information")

    def on_mount(self) -> None:
        if group.group_exists(self.group_info.group_name):
            self.query_exactly_one("#group_name",Input).value = self.group_info.group_name.upper()
            if self.group_info.base_traits is not None:
                set_traits_in_input(self,traits=self.group_info.base_traits,prefix="base")
            
            if self.group_info.dfp_traits is not None:
                set_traits_in_input(self,traits=self.group_info.dfp_traits,prefix="dfp")
            self.set_edit_mode()

    def action_delete_group_api(self) -> None:
        group_name = self.get_child_by_type(PanelGroupNameAndSubgroup).get_child_by_id("group_name",Input).value
        if group.group_exists(group_name):
            message, return_code = group.delete_group(group=group_name)
            
            if (return_code == 0):
                self.notify(f"Group {group_name} deleted, return code: {return_code}",severity="warning")
            else:
                self.notify(f"{message}, return code: {return_code}",severity="error")

    def action_delete_group(self) -> None:
        group_name = self.get_child_by_type(PanelGroupNameAndSubgroup).get_child_by_id("group_name",Input).value
        generic_confirmation_modal(self,modal_text=f"Are you sure you want to delete group {group_name}?",confirm_action="delete_group_api",action_widget=self)

    def action_save_group(self) -> None:
        group_name = self.get_child_by_type(PanelGroupNameAndSubgroup).get_child_by_id("group_name",Input).value
        group_exists = group.group_exists(group=group_name)

        operator = "alter" if group_exists else "add"

        base_segment = get_traits_from_input(operator, self, prefix="base", trait_cls=group.BaseGroupTraits)
        dfp_segment = get_traits_from_input(operator, self, prefix="dfp", trait_cls=group.DFPGroupTraits)

        group_object = group.GroupObject(base_traits=base_segment,dfp_traits=dfp_segment)

        result = group.update_group(
            group=group_name,
            create=not group_exists,
            group_object=group_object,
        )

        if not group_exists:
            if (result == 0 or result == 4):
                self.notify(f"Group {group_name} created, return code: {result}",severity="information")
            else:
                send_notification(self,message=f"Unable to create group, return code: {result}",severity="error")
        else:
            if (result == 0):
                self.notify(f"Group {group_name} updated, return code: {result}",severity="information")
            else:
                send_notification(self,message=f"Unable to update group, return code: {result}",severity="error")