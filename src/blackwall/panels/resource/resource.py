from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, RadioButton, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.lazy import Lazy

from blackwall.api import resource
from blackwall.panels.panel_mode import PanelMode

from ..traits_ui import generate_trait_section, get_traits_from_input

from blackwall.api import resource

class PanelResourceClassName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input(max_length=255,classes="resource-name-field")
        yield Label("Class:")
        yield Input(max_length=8,classes="class-field")

class PanelResourceInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelResourceSegments(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="Resource profile segments")):
            yield from generate_trait_section(title="stdata", prefix="stdata", traits_class=resource.STDATAResourceTraits)
            yield from generate_trait_section(title="CDT info", prefix="cdtinfo", traits_class=resource.CDTINFOResourceTraits)

class PanelResourceActionButtons(HorizontalGroup):
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

class PanelResource(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourceClassName()
        yield PanelResourceInstallationData()
        yield PanelResourceSegments()
        yield PanelResourceActionButtons(save_action="save_resource_profile", delete_action="delete_resource_profile")

        def action_save_resource_profile(self) -> None:
            pass

        def action_delete_resource_profile(self) -> None:
            pass
