
from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Label

from blackwall.api.setropts import (
    BaseSetroptsTraits,
    get_racf_options,
    update_racf_options,
)
from blackwall.emoji import get_emoji
from blackwall.modals import generic_confirmation_modal
from blackwall.panels.panel_mode import PanelMode
from blackwall.panels.traits_ui import (
    generate_trait_inputs,
    get_traits_from_input,
    set_traits_in_input,
    toggle_inputs,
)


@dataclass
class SetroptsInfo:
    mode: PanelMode = PanelMode.read

class PanelSetroptsNotice(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Warning: this panel controls and displays RACF system options. It is not recommended to touch this unless you absolutely know what you are doing!",classes="setropts-warning")

class PanelSetroptsMode(VerticalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.read,recompose=True)

    def __init__(self, switch_action: str):
        super().__init__()
        self.switch_action = switch_action


    def compose(self) -> ComposeResult:
        if self.edit_mode is PanelMode.read:
            readable_mode = "read"
        elif self.edit_mode is PanelMode.edit:
            readable_mode = "edit"
        else:
            readable_mode = "read"
        
        yield Label(f"Mode: {readable_mode}",classes="setropts-mode-label")
        yield Button("Switch",tooltip="Toggle between read and edit mode",action="switch",classes="action-button")

    async def action_switch(self):
        await self.app.run_action(self.switch_action,default_namespace=self.parent)

class PanelSetroptsFields(VerticalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.read)
    base_traits: reactive[BaseSetroptsTraits] = reactive(BaseSetroptsTraits())

    def compose(self) -> ComposeResult:
        yield from generate_trait_inputs(prefix="base",traits_class=BaseSetroptsTraits)

    def watch_base_traits(self):
        set_traits_in_input(self,traits=self.base_traits,prefix="base")

    def watch_edit_mode(self):
        if self.edit_mode is PanelMode.read:
            toggle_inputs(self,prefix="base",traits=self.base_traits,disabled=True)
        elif self.edit_mode is PanelMode.edit:
            toggle_inputs(self,prefix="base",traits=self.base_traits,disabled=False)


class PanelSetroptsActionButtons(VerticalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.read)

    def __init__(self, save_action: str):
        super().__init__()
        self.save_action = save_action

    def compose(self) -> ComposeResult:
        yield Label("Attention: changing system settings can be dangerous!",classes="setropts-warning")
        if self.edit_mode is PanelMode.read:
            yield Button(f"{get_emoji("💾")} Save",id="save",action="save",variant="warning",classes="action-button",disabled=True)
        elif self.edit_mode is PanelMode.edit:
            yield Button(f"{get_emoji("💾")} Save",id="save",action="save",variant="warning",classes="action-button",disabled=False)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

class PanelSetropts(VerticalScroll):
    setropts_info: reactive[SetroptsInfo] = reactive(SetroptsInfo())
    base_traits: reactive[BaseSetroptsTraits] = reactive(BaseSetroptsTraits())

    def watch_setropts_info(self, value: SetroptsInfo):
        mode_section = self.get_child_by_type(PanelSetroptsMode)
        mode_section = self.get_child_by_type(PanelSetroptsFields)
        #valid modes: edit and read
        mode_section.edit_mode = value.mode
  
    def on_mount(self) -> None:
        racf_options = get_racf_options()
        self.get_child_by_type(PanelSetroptsFields).base_traits = BaseSetroptsTraits.from_dict(prefix="base",source=racf_options["profile"]["base"])

    def compose(self) -> ComposeResult:
        yield PanelSetroptsNotice()
        yield PanelSetroptsMode(switch_action="switch")
        yield PanelSetroptsFields()
        yield PanelSetroptsActionButtons(save_action="save")

    def action_save_setropts_api(self) -> None:
        base_traits = get_traits_from_input(prefix="base",operator="alter",trait_cls=BaseSetroptsTraits,widget=self)
        message, return_code = update_racf_options(base=base_traits)
        if return_code == 0 or return_code == 4:
            self.notify(f"Updated system settings, return code: {return_code}",severity="warning")
        else:
            self.notify(f"Couldn't update system settings, return code: {return_code}",severity="error")

    def action_save(self) -> None:
        generic_confirmation_modal(self,modal_text="Are you abosulutely sure you want to change the RACF system options?",action_widget=self,confirm_action="save_setropts_api")

    def action_switch(self) -> None:
        if self.setropts_info.mode is PanelMode.read:
            self.setropts_info = SetroptsInfo(mode=PanelMode.edit) 
            self.query_exactly_one("#save",Button).disabled = False
            readable_mode = "edit"
        elif self.setropts_info.mode is PanelMode.edit:
            self.setropts_info = SetroptsInfo(mode=PanelMode.read) 
            readable_mode = "read"
            self.query_exactly_one("#save",Button).disabled = True
        else:
            readable_mode = "read"

        self.notify(f"Switched to {readable_mode}")
