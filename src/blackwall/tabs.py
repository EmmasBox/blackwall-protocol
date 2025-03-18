
from textual.app import ComposeResult
from textual.widgets import TabPane, TabbedContent
from textual.containers import HorizontalGroup

from .panels.users.user import PanelUser, UserInfo
from .panels.search.search import PanelSearch
from .panels.analysis.analysis import PanelAnalysis
from .panels.dataset.dataset import PanelDataset
from .panels.resource.resource import PanelResource

class TabSystem(HorizontalGroup):
    BINDINGS = [
        ("u", "open_user_administration", "Open user tab"),
        ("f", "open_search", "Open search tab"),
        ("l", "open_analysis", "Open analysis tab"),
        ("x", "open_dataset", "Open dataset profile tab"),
        ("g", "open_resource", "Open resource profile tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear all tabs"),
    ]

    def compose(self) -> ComposeResult:
        yield TabbedContent()

    #Add new tab
    async def action_open_user_administration(self) -> None:
        """Add a new user administration tab."""
        tabs = self.query_one(TabbedContent)
        new_user_panel = PanelUser()
        await tabs.add_pane(TabPane("User management",new_user_panel))
        #new_user_panel.user_info = UserInfo(
        #    username="",
        #    name="",
        #)

    async def action_open_dataset(self) -> None:
        """Add a new dataset profile management tab."""
        tabs = self.query_one(TabbedContent)
        await tabs.add_pane(TabPane("Dataset profile mangement",PanelDataset()))

    async def action_open_resource(self) -> None:
        """Add a new general resource profile management tab."""
        tabs = self.query_one(TabbedContent)
        await tabs.add_pane(TabPane("Resource profile mangement",PanelResource()))

    def action_open_search(self) -> None:
        """Add a new search tab."""
        tabs = self.query_one(TabbedContent)
        tabs.add_pane(TabPane("Search",PanelSearch()))

    def action_open_analysis(self) -> None:
        """Add a new analysis tab."""
        tabs = self.query_one(TabbedContent)
        tabs.add_pane(TabPane("Health check",PanelAnalysis()))

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