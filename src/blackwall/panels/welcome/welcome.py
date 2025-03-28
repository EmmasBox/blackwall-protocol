
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Markdown, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.messages import OpenTab
from blackwall.panels.users.user import PanelUser
from blackwall.panels.dataset.dataset import PanelDataset
from blackwall.panels.resource.resource import PanelResource
from blackwall.panels.analysis.analysis import PanelAnalysis

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
        yield Button("Analyse system health", classes="welcome-suggestion-button",action="create_analysis",disabled=True)

    async def action_create_dataset(self):
        self.post_message(OpenTab(title="Create dataset profile",content=PanelDataset()))

    async def action_create_resource(self):
        self.post_message(OpenTab(title="Create resource profile",content=PanelResource()))
    
    async def action_create_user(self):
        self.post_message(OpenTab(title="Create user",content=PanelUser()))

    async def action_create_analysis(self):
        self.post_message(OpenTab(title="Health check",content=PanelAnalysis()))


class PanelWelcomeMain(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield PanelWelcomeMessage()
        yield PanelWelcomeActions()

class PanelWelcome(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelWelcomeMain()