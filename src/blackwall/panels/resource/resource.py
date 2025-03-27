from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, RadioButton, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.api import resource
from blackwall.panels.panel_mode import PanelMode

class PanelResourceClass(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Class:")
        yield Input(max_length=8,classes="class-field")

class PanelResourceName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input(max_length=255,classes="resource-name-field")

class PanelResourceClassName(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield PanelResourceClass()
        yield PanelResourceName()

class PanelResourceInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelResourceActionButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Save",classes="action-button")
        yield Button("Delete",classes="action-button")

class PanelResource(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourceClassName()
        yield PanelResourceInstallationData()
        yield PanelResourceActionButtons()
