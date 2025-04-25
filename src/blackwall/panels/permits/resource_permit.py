from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Select, DataTable
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.emoji import get_emoji

class PanelResourcePermitInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Use this panel to create, delete, and update permits for general resource profiles",classes="label-generic")

class PanelResourcePermitSearchField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="search_permit_class",placeholder="class...",classes="field-short-generic")
        yield Input(id="search_permit_profile",placeholder="profile name...",classes="search-field")    
        yield Button(label="Search")

class PanelResourcePermitCreate(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="permit_receiver_field",placeholder="ID...",classes="field-short-generic", tooltip="User ID or group ID you want this permit change to affect")    
        yield Select([("NONE", "NONE"),("READ", "READ"),("EXECUTE", "EXECUTE"),("UPDATE", "UPDATE"),("CONTROL", "CONTROL"),("ALTER", "ALTER")],value="READ",classes="uacc-select",id="permit_access_selector")
        yield Button(f"{get_emoji("💾")} Save",id="resource_permit_save")

class PanelResourcePermitList(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Current permits:",classes="label-generic")
        yield DataTable(id="resource_permits_list")

class PanelResourcePermit(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourcePermitInfo()
        yield PanelResourcePermitSearchField()
        yield PanelResourcePermitCreate()
        yield PanelResourcePermitList()