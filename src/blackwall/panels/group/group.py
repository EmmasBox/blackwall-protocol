from dataclasses import dataclass

from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.lazy import Lazy

from blackwall.api import group
from blackwall.panels.panel_mode import PanelMode

class PanelName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Group name:")
        yield Input(id="group_name",classes="field-short-generic ")

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

class PanelGroups(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield PanelName()
        yield PanelGroupActionButtons(save_action="",delete_action="")