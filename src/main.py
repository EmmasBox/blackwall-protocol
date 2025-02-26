#Project by Emma Skovgaard

from textual.app import App
from textual.widgets import Header, Footer, ListView, Input, Label, TabPane, TabbedContent
from textual.containers import VerticalScroll, Container

try:
    from zoautil_py import zsystem # type: ignore
    zoau_enabled = True
except:
    print("##BLKWL_ERROR_1 Warning: could not find ZOAU, certain features will be disabled such as diplaying system and LPAR names")    
    zoau_enabled = False

import json
from panel_user import PanelUser
from theme import cynosure_theme

#system information
if zoau_enabled:
    zsystem_info = json.loads(zsystem.zinfo()) # type: ignore
    system_name = zsystem_info["sys_info"]["sys_name"]
    lpar_name = zsystem_info["sys_info"]["lpar_name"]

class Blackwall(App):
    #Import css
    CSS_PATH = "UI.css"

    #This portion handles the text in the header bar
    def on_mount(self) -> None:
        self.title = "Blackwall Protocol"
        self.sub_title = "Mainframe Security Administration"
        self.register_theme(cynosure_theme)
        self.theme = "cynosure"

    BINDINGS = [
        ("a", "add", "Add tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear all tabs"),
    ]

    #UI elements
    def compose(self):
        #display system and LPAR name
        with Container():
            if zoau_enabled:
                yield Label(f"You are working on the {system_name} mainframe system in LPAR {lpar_name}")
            yield Input(id="cli",max_length=250)
            yield Header()
            with TabbedContent():
                with TabPane("User administration"):
                    with VerticalScroll():
                        yield PanelUser()
            yield ListView()
            yield Footer()

    #Add new tab
    def action_add(self) -> None:
        """Add a new tab."""
        tabs = self.query_one(TabbedContent)
        tabs.add_pane(TabPane("Empty Tab"))

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

Blackwall().run()
