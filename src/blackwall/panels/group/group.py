from dataclasses import dataclass

from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.api import group
from blackwall.panels.panel_mode import PanelMode

from ..traits_ui import generate_trait_section, get_traits_from_input

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

class PanelGroupSegments(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield from generate_trait_section(title="DFP", prefix="dfp", traits_class=group.DFPGroupTraits)

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
        yield Button("Save",action="save",classes="action-button")
        yield Button("Delete",action="delete",classes="action-button",disabled=self.delete_is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

class PanelGroup(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelGroupNameAndSubgroup()
        yield PanelGroupInstallationData()
        yield PanelGroupSegments()
        yield PanelGroupActionButtons(save_action="save_group",delete_action="delete_group")

    def action_delete_group(self) -> None:
        pass

    def action_save_group(self) -> None:
        group_name = self.query_exactly_one(selector="#group_name").value
        group_exists = group.group_profile_exists(group=group_name)

        if group_exists:
            operator = "alter"
        else:
            operator = "add"

        base_segment = get_traits_from_input(operator, self, prefix="base", trait_cls=group.BaseGroupTraits)
        dfp_segment = get_traits_from_input(operator, self, prefix="base", trait_cls=group.DFPGroupTraits)
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
                self.notify(f"Unable to create group, return code: {result}",severity="error")
        else:
            if (result == 0 or result == 4):
                self.notify(f"Group {group_name} updated, return code: {result}",severity="information")
            else:
                self.notify(f"Unable to update group, return code: {result}",severity="error")