
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Markdown, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from importlib.resources import files
message = files('blackwall.panels.welcome').joinpath('welcome_message.md').read_text()

class PanelWelcome(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Markdown(message)