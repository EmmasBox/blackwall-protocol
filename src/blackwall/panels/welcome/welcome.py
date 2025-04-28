
import importlib.util
from importlib.resources import files
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Grid, VerticalGroup, VerticalScroll
from textual.widgets import Button, Label, Markdown

from blackwall.messages import OpenTab
from blackwall.panels.analysis.analysis import PanelAnalysis
from blackwall.panels.dataset.dataset import PanelDataset
from blackwall.panels.group.group import PanelGroup
from blackwall.panels.resource.resource import PanelResource
from blackwall.panels.search.search import PanelSearch
from blackwall.panels.setropts.setropts import PanelSetropts
from blackwall.panels.users.user import PanelUser
from blackwall.settings import get_site_setting, get_user_setting

message = files('blackwall.panels.welcome').joinpath('welcome_message.md').read_text()

logo_allowed = get_user_setting(section="display",setting="logo")
site_logo_path = get_site_setting(section="welcome",setting="logo_path")

if Path(f"{site_logo_path}").exists():
    logo_path = f"{site_logo_path}"
else:
    logo_path = "OMP_CBTTape_original-color.png"

class PanelWelcomeLogo(VerticalGroup):
    def __init__(self, logo_path: Path | str):
        super().__init__()
        self.logo_path = logo_path

    def compose(self) -> ComposeResult:
        if logo_allowed is not False:
            textual_image_enabled = importlib.util.find_spec('textual_image')
            if textual_image_enabled:
                from textual_image.widget import SixelImage
                image = Path(f'{logo_path}')
                yield SixelImage(image, classes="logo-image")

class PanelWelcomeMessage(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Markdown(message,classes="welcome-message")

class PanelWelcomeActions(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Try out the program:",classes="welcome-suggestion-header")
        yield Button("Search RACF", classes="welcome-suggestion-button",action="search")
        yield Button("Create user", classes="welcome-suggestion-button",action="create_user")
        yield Button("Create group", classes="welcome-suggestion-button",action="create_group")
        yield Button("Create dataset profile", classes="welcome-suggestion-button",action="create_dataset")
        yield Button("Create general resource profile", classes="welcome-suggestion-button",action="create_resource")
        yield Button("View system options", classes="welcome-suggestion-button",action="view_options")
        #yield Button("Analyse system health", classes="welcome-suggestion-button",action="create_analysis")

    async def action_search(self):
        self.post_message(OpenTab(title="Search",content=PanelSearch()))

    async def action_create_user(self):
        self.post_message(OpenTab(title="Create user",content=PanelUser()))

    async def action_create_group(self):
        self.post_message(OpenTab(title="Create group",content=PanelGroup()))

    async def action_create_dataset(self):
        self.post_message(OpenTab(title="Create dataset profile",content=PanelDataset()))

    async def action_create_resource(self):
        self.post_message(OpenTab(title="Create resource profile",content=PanelResource()))

    async def action_view_options(self):
        self.post_message(OpenTab(title="RACF options",content=PanelSetropts()))

    async def action_create_analysis(self):
        self.post_message(OpenTab(title="Health check",content=PanelAnalysis()))

class PanelWelcomeContent(Grid):
    def compose(self) -> ComposeResult:
        yield PanelWelcomeMessage()
        yield PanelWelcomeLogo(logo_path=logo_path)
        yield PanelWelcomeActions()

class PanelWelcome(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelWelcomeContent()