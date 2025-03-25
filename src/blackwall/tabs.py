
from textual.app import ComposeResult
from textual.widgets import TabPane, TabbedContent
from textual.containers import HorizontalGroup
from textual.reactive import reactive

from .panels.welcome.welcome import PanelWelcome
from .panels.users.user import PanelUser, UserInfo
from .panels.search.search import PanelSearch
from .panels.analysis.analysis import PanelAnalysis
from .panels.dataset.dataset import PanelDataset
from .panels.resource.resource import PanelResource

from blackwall.messages import OpenTab

class TabSystem(HorizontalGroup):
    BINDINGS = [
        ("u", "open_user", "Open user tab"),
        ("f", "open_search", "Open search tab"),
        ("l", "open_analysis", "Open analysis tab"),
        ("x", "open_dataset", "Open dataset profile tab"),
        ("g", "open_resource", "Open resource profile tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear all tabs"),
    ]

    def compose(self) -> ComposeResult:
        yield TabbedContent()

    def on_mount(self) -> None:
        self.post_message(OpenTab("Welcome!",PanelWelcome()))

    async def on_open_tab(self, message: OpenTab):
        message.stop()
        tabs = self.query_one(TabbedContent)
        new_tab = TabPane(message.title,message.content)
        await tabs.add_pane(new_tab)
        tabs.active = new_tab.id

    #Add new tab
    async def action_open_user(self) -> None:
        """Add a new user administration tab."""
        self.post_message(OpenTab("User management",PanelUser()))

    async def action_open_dataset(self) -> None:
        """Add a new dataset profile management tab."""
        self.post_message(OpenTab("Dataset profile mangement",PanelDataset()))

    async def action_open_resource(self) -> None:
        """Add a new general resource profile management tab."""
        self.post_message(OpenTab("Resource management",PanelResource()))

    def action_open_search(self) -> None:
        """Add a new search tab."""
        self.post_message(OpenTab("Search",PanelSearch()))

    def action_open_analysis(self) -> None:
        """Add a new analysis tab."""
        self.post_message(OpenTab("Health check",PanelAnalysis()))

    #Remove current tab
    def action_remove(self) -> None:
        """Remove active tab."""
        tabs = self.query_one(TabbedContent)
        active_pane = tabs.active_pane
        if active_pane is not None:
            tabs.remove_pane(active_pane.id)

    #Clear all tabs
    def action_clear(self) -> None:
        """Clear the tabs."""
        self.query_one(TabbedContent).clear_panes()