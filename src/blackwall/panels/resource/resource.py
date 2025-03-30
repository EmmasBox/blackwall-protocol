from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, RadioButton, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.lazy import Lazy

from blackwall.api import resource
from blackwall.panels.panel_mode import PanelMode

from ..traits_ui import generate_trait_inputs, get_traits_from_input

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

class PanelResourceActionButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Save",classes="action-button")
        yield Button("Delete",classes="action-button")

class PanelResourceSegments(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="Resource profile segments")):
            yield from generate_trait_inputs(title="stdata", prefix="stdata", traits_class=resource.STDATAResourceTraits)
            yield from generate_trait_inputs(title="CDT info", prefix="cdtinfo", traits_class=resource.CDTINFOResourceTraits)

class PanelResource(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourceClassName()
        yield PanelResourceInstallationData()
        yield PanelResourceSegments()
        yield PanelResourceActionButtons()
