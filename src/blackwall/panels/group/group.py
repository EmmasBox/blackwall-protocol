from dataclasses import dataclass

from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.api import group
from blackwall.emoji import get_emoji
from blackwall.notifications import send_notification
from blackwall.panels.panel_mode import PanelMode

from ..traits_ui import generate_trait_section, get_traits_from_input, set_traits_in_input

class PanelGroupNameAndSubgroup(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Group name:")
        yield Input(id="group_name",max_length=8,classes="field-short-generic",tooltip="1-8 character long alphanumeric name used to identify the group")
        yield Label("Superior group:")
        yield Input(max_length=8,id="base_superior_group",classes="field-short-generic",tooltip="")
        yield Label("Owner:")
        yield Input(max_length=8,id="base_owner",classes="field-short-generic",tooltip="")

class PanelGroupInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="base_installation_data",classes="installation-data",tooltip="Optional used defined data. This can be used to put in a description about what the group is used for. Can't be more than 255 characters long.")

class PanelGroupDatasetModel(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Dataset model:")
        yield Input(id="base_data_set_model",classes="field-long-generic")

class PanelGroupSegments(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield from generate_trait_section(title="DFP segment", prefix="dfp", traits_class=group.DFPGroupTraits)

class PanelGroupActionButtons(HorizontalGroup):
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
        yield Button(f"{get_emoji("💾")} Save",action="save",classes="action-button")
        yield Button("Delete",action="delete",variant="error",classes="action-button",disabled=self.delete_is_disabled)

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
        yield PanelGroupNameAndSubgroup()
        yield PanelGroupInstallationData()
        yield PanelGroupDatasetModel()
        yield PanelGroupSegments()
        yield PanelGroupActionButtons(save_action="save_group",delete_action="delete_group")

    group_info: reactive[GroupInfo] = reactive(GroupInfo())

    def on_mount(self) -> None:
        if group.group_exists(self.group_info.group_name):
            self.query_exactly_one("#group_name",Input).value = self.group_info.group_name
            if self.group_info.base_traits is not None:
                set_traits_in_input(self,traits=self.group_info.base_traits,prefix="base")
            
            if self.group_info.dfp_traits is not None:
                set_traits_in_input(self,traits=self.group_info.dfp_traits,prefix="dfp")

    def action_delete_group(self) -> None:
        pass

    def action_save_group(self) -> None:
        group_name = self.get_child_by_type(PanelGroupNameAndSubgroup).get_child_by_id("group_name",Input).value
        group_exists = group.group_exists(group=group_name)

        if group_exists:
            operator = "alter"
        else:
            operator = "add"

        base_segment = get_traits_from_input(operator, self, prefix="base", trait_cls=group.BaseGroupTraits)
        dfp_segment = get_traits_from_input(operator, self, prefix="dfp", trait_cls=group.DFPGroupTraits)
        result = group.update_group(
            group=group_name,
            create=not group_exists,
            base=base_segment,
            dfp=dfp_segment
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