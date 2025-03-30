
from dataclasses import dataclass
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, RadioButton, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

class PanelSetroptsFields(VerticalGroup):
    def compose(self) -> ComposeResult:
        pass

class PanelSetroptsActionButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Save",classes="action-button")

class PanelSetropts(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelSetroptsFields()
        yield PanelSetroptsActionButtons()
