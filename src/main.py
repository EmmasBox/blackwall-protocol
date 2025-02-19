#Project by Emma Skovgaard

from textual.app import App
from textual.widgets import Header, Footer, Tabs, ListView, Input, Label, Tab

try:
    from zoautil_py import zsystem # type: ignore
    zoau_enabled = True
except:
    print("Warning: could not find ZOAU, certain features will be disabled such as diplaying system and LPAR names")    
    zoau_enabled = False

import json

#system information
if zoau_enabled:
    zsystem_info = json.loads(zsystem.zinfo()) # type: ignore
    system_name = zsystem_info["sys_info"]["sys_name"]
    lpar_name = zsystem_info["sys_info"]["lpar_name"]

class Blackwall(App):
    #This portion handles the text in the header bar
    def on_mount(self) -> None:
        self.title = "Blackwall Protocol"
        self.sub_title = "Mainframe Security Administration"

    BINDINGS = [
        ("a", "add", "Add tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear all tabs"),
    ]

    #UI elements
    def compose(self):
        #display system and LPAR name
        if zoau_enabled:
            yield Label(f"You are working on the {system_name} mainframe system in LPAR {lpar_name}")
        yield Input(id="cli")
        yield Header()
        yield Tabs()
        yield ListView()
        yield Footer()

    def action_add(self) -> None:
        """Add a new tab."""
        tabs = self.query_one(Tabs)
        tabs.add_tab("Empty tab")

    def action_remove(self) -> None:
        """Remove active tab."""
        tabs = self.query_one(Tabs)
        active_tab = tabs.active_tab
        if active_tab is not None:
            tabs.remove_tab(active_tab.id)

    def action_clear(self) -> None:
        """Clear the tabs."""
        self.query_one(Tabs).clear()


Blackwall().run()
