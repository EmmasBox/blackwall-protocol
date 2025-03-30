
from dataclasses import dataclass
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Label, Button
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.api import setropts
from blackwall.panels.traits_ui import generate_trait_inputs

class PanelSetroptsFields(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("RACF system options:")
        yield from generate_trait_inputs(prefix="base",traits_class=setropts.BaseSetroptsTraits)

class PanelSetroptsActionButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Save",classes="action-button")

class PanelSetropts(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelSetroptsFields()
        yield PanelSetroptsActionButtons()
