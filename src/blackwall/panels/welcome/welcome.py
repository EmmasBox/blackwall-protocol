
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Markdown, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from importlib.resources import files
message = files('blackwall.panels.welcome').joinpath('welcome_message.md').read_text()

class PanelWelcomeMessage(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Markdown(message,classes="welcome-message")

class PanelWelcomeActions(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Try out the program:",classes="welcome-suggestion-header")
        yield Button("Create user", classes="welcome-suggestion-button")
        yield Button("Create dataset profile", classes="welcome-suggestion-button")
        yield Button("Create general resource profile", classes="welcome-suggestion-button")
        yield Button("Analyse system health", classes="welcome-suggestion-button")

class PanelWelcomeMain(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield PanelWelcomeMessage()
        yield PanelWelcomeActions()

class PanelWelcome(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelWelcomeMain()