
from textual.app import ComposeResult
from textual.widgets import Button, TabPane, TabbedContent
from textual.containers import HorizontalGroup

from .panels.users.user import PanelUser
from .panels.search.search import PanelSearch
from .panels.analysis.analysis import PanelAnalysis

class TabSystem(HorizontalGroup):
    BINDINGS = [
        ("u", "open_user_administration", "Open user tab"),
        ("f", "open_search", "Open search tab"),
        ("l", "open_analysis", "Open analysis tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear all tabs"),
    ]

    def compose(self) -> ComposeResult:
        yield TabbedContent()

    #Add new tab
    def action_open_user_administration(self) -> None:
        """Add a new user administration tab."""
        tabs = self.query_one(TabbedContent)
        tabs.add_pane(TabPane("User management",PanelUser()))

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