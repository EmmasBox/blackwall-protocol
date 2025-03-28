
from textual.app import ComposeResult
from textual.widgets import TabPane, TabbedContent
from textual.containers import HorizontalGroup
from .panels.welcome.welcome import PanelWelcome
from .panels.users.user import PanelUser, UserInfo
from .panels.search.search import PanelSearch
from .panels.analysis.analysis import PanelAnalysis
from .panels.dataset.dataset import PanelDataset
from .panels.resource.resource import PanelResource
from .panels.history.history import PanelHistory

from blackwall.messages import OpenTab

class TabSystem(HorizontalGroup):
    BINDINGS = [
        ("ctrl+u", "open_user", "Open user tab"),
        ("ctrl+f", "open_search", "Open search tab"),
        ("ctrl+a", "open_analysis", "Open analysis tab"),
        ("ctrl+d", "open_dataset", "Open dataset profile tab"),
        ("ctrl+g", "open_resource", "Open resource profile tab"),
        ("ctrl+h", "open_history", "Open history tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear all tabs"),
    ]
    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.tabs = TabbedContent()

    def compose(self) -> ComposeResult:
        yield self.tabs

    def on_mount(self) -> None:
        self.post_message(OpenTab("Welcome!",PanelWelcome()))

    async def on_open_tab(self, message: OpenTab):
        message.stop()
        tabs = self.query_one(TabbedContent)
        new_tab = TabPane(message.title,message.content)
        await tabs.add_pane(new_tab)
        #Workaround, because switching tabs does not work when pressing a button I've had to disable the current tab and then re-enable it
        old_tab = tabs.active
        tabs.disable_tab(old_tab)
        def focus_tab():
            tabs.active = new_tab.id
            tabs.enable_tab(old_tab)
        self.call_after_refresh(focus_tab)

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

    def action_open_history(self) -> None:
        """Add a new history tab."""
        self.post_message(OpenTab("Command history",PanelHistory()))

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