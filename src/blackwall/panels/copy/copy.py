from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, ContentSwitcher, Input, Label

from blackwall.regex import racf_id_regex


class PanelCopyUser(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy user",classes="copy-label")
        yield Input(max_length=8,restrict=racf_id_regex,classes="field-short-generic")
        yield Label("TO",classes="copy-label")
        yield Input(max_length=8,restrict=racf_id_regex,classes="field-short-generic")
        yield Button(label="Copy user",id="copy_user_confirm",action="")

class PanelCopyGroup(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy group",classes="copy-label")
        yield Input(max_length=8,restrict=racf_id_regex,classes="field-short-generic")
        yield Label("TO",classes="copy-label")
        yield Input(max_length=8,restrict=racf_id_regex,classes="field-short-generic")
        yield Button(label="Copy group",id="copy_group_confirm",action="")

class PanelCopyDataset(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy dataset profile",classes="copy-label")
        yield Input(max_length=255,classes="field-long-generic")
        yield Label("TO",classes="copy-label")
        yield Input(max_length=255,classes="field-long-generic")
        yield Button(label="Copy dataset profile",id="copy_dataset_confirm",action="")

class PanelCopyResource(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Copy resource",classes="copy-label")
        yield Input(max_length=8,placeholder="class...",classes="field-short-generic")
        yield Input(max_length=255,placeholder="resource profile...",classes="field-long-generic")
        yield Label("TO",classes="copy-label")
        yield Input(max_length=8,placeholder="class...",classes="field-short-generic")
        yield Input(max_length=255,placeholder="resource profile...",classes="field-long-generic")
        yield Button(label="Copy resource profile",id="copy_resource_confirm",action="")

class PanelCopySwitcherButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button(id="copy_user_panel",label="User",classes="copy-buttons")
        yield Button(id="copy_group_panel",label="Group",classes="copy-buttons")
        yield Button(id="copy_dataset_panel",label="Dataset profile",classes="copy-buttons")
        yield Button(id="copy_resource_panel",label="Resource profile",classes="copy-buttons")

class PanelCopySwitcher(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield PanelCopySwitcherButtons()
        with ContentSwitcher(initial="copy_user_panel",classes="copy-switcher"):
            yield PanelCopyUser(id="copy_user_panel")
            yield PanelCopyGroup(id="copy_group_panel")
            yield PanelCopyDataset(id="copy_dataset_panel")
            yield PanelCopyResource(id="copy_resource_panel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id  

class PanelCopy(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelCopySwitcher()