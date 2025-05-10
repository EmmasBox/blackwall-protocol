
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import TabbedContent, TabPane

from blackwall.emoji import get_emoji
from blackwall.messages import OpenTab
from blackwall.panels.copy.copy import PanelCopy
from blackwall.panels.errors.history import PanelErrorHistory
from blackwall.panels.permits.resource_permit import PanelResourcePermit
from blackwall.settings import get_user_setting

from .panels.analysis.analysis import PanelAnalysis
from .panels.backout.backout import PanelBackout
from .panels.command_output.command_output import PanelCommandOutput
from .panels.dataset.dataset import PanelDataset
from .panels.group.group import PanelGroup
from .panels.resource.resource import PanelResource
from .panels.search.search import PanelSearch
from .panels.setropts.setropts import PanelSetropts
from .panels.users.user import PanelUser
from .panels.welcome.welcome import PanelWelcome

people_list = [
    "🧔",
    "🙋",
    "🙎",
    "🙍",
    "🙅",
    "🙆",
]

class TabSystem(HorizontalGroup):
    BINDINGS = [
        ("ctrl+u", "open_user", "Open user tab"),
        ("ctrl+g", "open_groups", "Open group profile tab"),
        ("ctrl+d", "open_dataset", "Open dataset profile tab"),
        ("ctrl+r", "open_resource", "Open resource profile tab"),
        ("ctrl+l", "open_command_output", "Open command output tab"),
        ("ctrl+f", "open_search", "Open search tab"),
        #("ctrl+a", "open_analysis", "Open analysis tab"),
        ("ctrl+o", "open_options", "Open RACF options tab"),
        ("ctrl+n", "open_resource_permits", "Open resource permits tab"),
        #("ctrl+k", "open_copy", "Open copy tab"),
        #("ctrl+b", "open_backout", "Open backout tab"),
        ("ctrl+w", "remove", "Remove active tab"),
        ("ctrl+shift+w", "clear", "Clear all tabs"),
    ]
    def __init__(self, *children, name = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, classes=classes, disabled=disabled, markup=markup)
        self.tabs = TabbedContent(id="tab_system")

    def compose(self) -> ComposeResult:
        yield self.tabs

    def on_mount(self) -> None:
        default_tab = get_user_setting(section="tabs",setting="default_tab")
        if default_tab is not None:
            if default_tab == "user":
                self.post_message(OpenTab(f"{get_emoji(people_list)} User management",PanelUser()))
            elif default_tab == "group":
                self.post_message(OpenTab(f"{get_emoji("👥")} Group management",PanelGroup()))
            elif default_tab == "dataset":
                self.post_message(OpenTab(f"{get_emoji("📁")} Dataset profile mangement",PanelDataset()))
            elif default_tab == "resource":
                self.post_message(OpenTab(f"{get_emoji("☕")} Resource management",PanelResource()))
            elif default_tab == "commands":
                self.post_message(OpenTab(f"{get_emoji("📃")} Command history",PanelCommandOutput()))
            elif default_tab == "options":
                self.post_message(OpenTab("RACF options",PanelSetropts()))
            elif default_tab == "search":
                self.post_message(OpenTab(f"{get_emoji("🔎")} Search",PanelSearch()))
            else:
                self.post_message(OpenTab("Welcome!",PanelWelcome()))
        else:
            self.post_message(OpenTab("Welcome!",PanelWelcome()))

    async def on_open_tab(self, message: OpenTab):
        message.stop()
        tabs = self.get_child_by_id("tab_system",TabbedContent)
        new_tab = TabPane(message.title,message.content)
        await tabs.add_pane(new_tab)
        #Workaround, because switching tabs does not work when pressing a button I've had to disable the current tab and then re-enable it
        old_tab = tabs.active
        tabs.disable_tab(old_tab)
        def focus_tab():
            if new_tab.id is not None:
                tabs.active = new_tab.id
            tabs.enable_tab(old_tab)
        self.call_after_refresh(focus_tab)

    #Add new tab
    async def action_open_user(self) -> None:
        """Add a new user administration tab."""
        self.post_message(OpenTab(f"{get_emoji(people_list)} User management",PanelUser()))

    async def action_open_dataset(self) -> None:
        """Add a new dataset profile management tab."""
        self.post_message(OpenTab(f"{get_emoji("📁")} Dataset profile mangement",PanelDataset()))
    
    async def action_open_resource(self) -> None:
        """Add a new general resource profile management tab."""
        self.post_message(OpenTab(f"{get_emoji("☕")} Resource management",PanelResource()))
    
    async def action_open_groups(self) -> None:
        """Add a new group management tab."""
        self.post_message(OpenTab(f"{get_emoji("👥")} Group management",PanelGroup()))

    def action_open_search(self) -> None:
        """Add a new search tab."""
        self.post_message(OpenTab(f"{get_emoji("🔎")} Search",PanelSearch()))
    
    def action_open_analysis(self) -> None:
        """Add a new analysis tab."""
        self.post_message(OpenTab(f"{get_emoji("📊")} Health check",PanelAnalysis()))
    
    def action_open_command_output(self) -> None:
        """Add a new history tab."""
        self.post_message(OpenTab(f"{get_emoji("📃")} Command history",PanelCommandOutput()))

    def action_open_options(self) -> None:
        """Add a new RACF options tab."""
        self.post_message(OpenTab("RACF options",PanelSetropts()))

    def action_open_resource_permits(self) -> None:
        """Add a new resource permits tab."""
        self.post_message(OpenTab("Resource permits",PanelResourcePermit()))

    def action_open_copy(self) -> None:
        """Add a new copy panel tab."""
        self.post_message(OpenTab("Copy",PanelCopy()))

    def action_open_error_log(self) -> None:
        """Add a new error log panel tab."""
        self.post_message(OpenTab("Error history",PanelErrorHistory()))

    def action_open_backout(self) -> None:
        """Add a new backout panel tab."""
        self.post_message(OpenTab(f"{get_emoji("↪")} Backout changes",PanelBackout()))

    #Remove current tab
    def action_remove(self) -> None:
        """Remove active tab."""
        tabs = self.get_child_by_id("tab_system",TabbedContent)
        active_pane = tabs.active_pane
        if active_pane is not None and active_pane.id is not None:
            tabs.remove_pane(active_pane.id)

    #Clear all tabs
    def action_clear(self) -> None:
        """Clear the tabs."""
        self.get_child_by_id("tab_system",TabbedContent).clear_panes()