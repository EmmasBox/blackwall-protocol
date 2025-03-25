
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
        yield Button("Create user", classes="welcome-suggestion-button",action="create_user")
        yield Button("Create dataset profile", classes="welcome-suggestion-button",action="create_dataset")
        yield Button("Create general resource profile", classes="welcome-suggestion-button",action="create_resource")
        yield Button("Analyse system health", classes="welcome-suggestion-button",action="create_analysis")

    async def action_create_dataset(self):
        pass

    async def action_create_resource(self):
        pass
    
    async def action_create_user(self):
        pass

    async def action_create_analysis(self):
        pass


class PanelWelcomeMain(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield PanelWelcomeMessage()
        yield PanelWelcomeActions()

class PanelWelcome(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelWelcomeMain()