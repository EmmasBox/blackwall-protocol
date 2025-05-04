from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, ContentSwitcher, Label


class PanelCopyUser(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy user")

class PanelCopyGroup(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy group")

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
        with ContentSwitcher(initial="PanelCopyUser"):
            yield PanelCopyUser()
            yield PanelCopyGroup()
            yield PanelCopyDataset()
            yield PanelCopyResource()

class PanelCopy(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelCopySwitcher()