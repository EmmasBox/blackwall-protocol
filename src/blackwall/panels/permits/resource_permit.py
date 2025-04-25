from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Select, DataTable
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

class PanelResourcePermitSearchField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="search_permit_field",classes="search-field")    
        yield Button(label="Search")

class PanelResourcePermitCreate(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="permit_receiver_field",placeholder="ID...",classes="field-short-generic")    
        yield Select([("NONE", "NONE"),("READ", "READ"),("EXECUTE", "EXECUTE"),("UPDATE", "UPDATE"),("CONTROL", "CONTROL"),("ALTER", "ALTER")],classes="uacc-select",id="permit_access_selector")
        yield Button(label="Save")

class PanelResourcePermitList(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Current permits:")
        yield DataTable()

class PanelResourcePermit(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourcePermitSearchField()
        yield PanelResourcePermitCreate()
        yield PanelResourcePermitList()