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

class PanelGroups(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield PanelName()