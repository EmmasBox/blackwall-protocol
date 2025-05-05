from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, ContentSwitcher, Input, Label


class PanelCopyUser(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy user")
        yield Input(max_length=8,classes="field-short-generic")
        yield Input(max_length=8,classes="field-short-generic")

class PanelCopyGroup(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy group")
        yield Input(max_length=8,classes="field-short-generic")
        yield Input(max_length=8,classes="field-short-generic")

class PanelCopyDataset(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy dataset")

class PanelCopyResource(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy resource")

class PanelCopySwitcherButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button(label="User")
        yield Button(label="Group")
        yield Button(label="Dataset profile")
        yield Button(label="User")

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