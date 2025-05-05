from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, ContentSwitcher, Input, Label


class PanelCopyUser(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy user",classes="copy-label")
        yield Input(max_length=8,classes="field-short-generic")
        yield Input(max_length=8,classes="field-short-generic")

class PanelCopyGroup(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy group",classes="copy-label")
        yield Input(max_length=8,classes="field-short-generic")
        yield Input(max_length=8,classes="field-short-generic")

class PanelCopyDataset(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy dataset",classes="copy-label")

class PanelCopyResource(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy resource",classes="copy-label")

class PanelCopySwitcherButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button(label="User",classes="copy-buttons")
        yield Button(label="Group",classes="copy-buttons")
        yield Button(label="Dataset profile",classes="copy-buttons")
        yield Button(label="User",classes="copy-buttons")

class PanelCopySwitcher(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield PanelCopySwitcherButtons()
        with ContentSwitcher(initial="copy_user",classes="copy-switcher"):
            yield PanelCopyUser(id="copy_user")
            yield PanelCopyGroup()
            yield PanelCopyDataset()
            yield PanelCopyResource()

class PanelCopy(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelCopySwitcher()