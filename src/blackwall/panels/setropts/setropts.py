
from dataclasses import dataclass
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll, Right

from blackwall.api import setropts
from blackwall.panels.traits_ui import generate_trait_inputs, set_traits_in_input
from blackwall.panels.panel_mode import PanelMode

@dataclass
class SetroptsInfo:
    mode: PanelMode = PanelMode.read

class PanelSetroptsMode(Right):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.read,recompose=True)

    def __init__(self, switch_action: str):
        super().__init__()
        self.switch_action = switch_action


    def compose(self) -> ComposeResult:
        if self.edit_mode is PanelMode.read:
            readable_mode = "read"
        elif self.edit_mode is PanelMode.edit:
            readable_mode = "edit"
        
        yield Label(f"Mode: {readable_mode}")
        yield Button("Switch",tooltip="Toggle between read and edit mode",action="switch")

    async def action_switch(self):
        await self.app.run_action(self.switch_action,default_namespace=self.parent)

class PanelSetroptsFields(VerticalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.read,recompose=True)
    def compose(self) -> ComposeResult:
        if self.edit_mode is PanelMode.read:
            inputs_disabled = True
        elif self.edit_mode is PanelMode.edit:
            inputs_disabled = False

        yield from generate_trait_inputs(prefix="base",traits_class=setropts.BaseSetroptsTraits,disabled=inputs_disabled)


class PanelSetroptsActionButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Save",classes="action-button")

class PanelSetropts(VerticalScroll):
    setropts_info: reactive[SetroptsInfo] = reactive(SetroptsInfo())

    def watch_setropts_info(self, value: SetroptsInfo):
        mode_section = self.query_exactly_one(PanelSetroptsMode)
        mode_section = self.query_exactly_one(PanelSetroptsFields)
        #valid modes: edit and read
        mode_section.edit_mode = value.mode

    def on_mount(self) -> None:
        racf_options = setropts.get_racf_options()
        set_traits_in_input(self,traits=racf_options,prefix="base",)

    def compose(self) -> ComposeResult:
        yield PanelSetroptsMode(switch_action="switch")
        yield PanelSetroptsFields()
        yield PanelSetroptsActionButtons()

    def action_switch(self) -> None:
        if self.setropts_info.mode is PanelMode.read:
            self.setropts_info = SetroptsInfo(mode=PanelMode.edit) 
            readable_mode = "edit"
        elif self.setropts_info.mode is PanelMode.edit:
            self.setropts_info = SetroptsInfo(mode=PanelMode.read) 
            readable_mode = "read"

        
        self.notify(f"Switched to {readable_mode}")
