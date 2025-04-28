from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, DataTable, Input, Label, Select

from blackwall.api import group, permit, resource
from blackwall.emoji import get_emoji
from blackwall.notifications import send_notification
from blackwall.panels.traits_ui import get_traits_from_input
from blackwall.regex import racf_id_regex

PERMIT_COLUMNS = [
    ("ID", "Type", "Access"),
]

class PanelResourcePermitInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Use this panel to create, delete, and update permits for general resource profiles",classes="label-generic")

class PanelResourcePermitSearchField(HorizontalGroup):
    def __init__(self, search_action: str):
        super().__init__()
        self.search_action = search_action

    def compose(self) -> ComposeResult:
        yield Input(id="search_permit_class",placeholder="class...",classes="field-short-generic")
        yield Input(id="search_permit_profile",placeholder="profile name...",classes="search-field")    
        yield Button(label="Get ACL",id="search_permit_button",action="search")

    @on(Input.Submitted)
    async def action_search(self):
        await self.app.run_action(self.search_action,default_namespace=self.parent)

class PanelResourcePermitCreate(HorizontalGroup):
    def __init__(self, update_action: str):
        super().__init__()
        self.update_action = update_action
    
    def compose(self) -> ComposeResult:
        yield Select([("NONE", "NONE"),("READ", "READ"),("EXECUTE", "EXECUTE"),("UPDATE", "UPDATE"),("CONTROL", "CONTROL"),("ALTER", "ALTER")],value="READ",classes="uacc-select",id="base_access")
        yield Input(id="permit_racf_id",placeholder="ID...",max_length=8,restrict=racf_id_regex,classes="field-short-generic", tooltip="User ID or group ID you want this permit change to affect")    
        yield Button(f"{get_emoji("💾")} Save",id="resource_permit_save",action="update")

    @on(Input.Submitted)
    async def action_create(self):
        await self.app.run_action(self.update_action,default_namespace=self.parent)

class PanelResourcePermitList(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Current permits:",classes="label-generic")
        yield DataTable(id="resource_permits_table")

    def on_mount(self) -> None:
        permit_table = self.get_child_by_id("resource_permits_table",DataTable)
        permit_table.zebra_stripes = True
        permit_table.add_columns(*PERMIT_COLUMNS[0]) 

class PanelResourcePermit(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourcePermitInfo()
        yield PanelResourcePermitSearchField(search_action="search")
        yield PanelResourcePermitCreate(update_action="update")
        yield PanelResourcePermitList()

    def get_acl(self, notification: bool) -> None:
        search_profile_field_value = self.get_child_by_type(PanelResourcePermitSearchField).get_child_by_id("search_permit_profile",Input).value
        search_class_field_value = self.get_child_by_type(PanelResourcePermitSearchField).get_child_by_id("search_permit_class",Input).value
        permit_table = self.get_child_by_type(PanelResourcePermitList).get_child_by_id("resource_permits_table",DataTable)
        
        if resource.resource_profile_exists(resource=search_profile_field_value,resource_class=search_class_field_value):
            resource_acl = resource.get_resource_acl(resource=search_profile_field_value,resource_class=search_class_field_value)
            permit_table.clear(columns=False)

            for entry in resource_acl:
                entry_id = entry["base:access_id"]
                entry_access = entry["base:access_type"]

                #Checks if the entry is a user or group
                id_type = "group" if group.group_exists(entry_id) else "user"
                
                #Adds the entry to the datatable
                permit_table.add_row(entry_id,id_type,entry_access)
            if notification:
                self.notify(f"Found profile {search_profile_field_value} in class {search_class_field_value}",severity="information")
        else:
            if notification:
                self.notify(f"Couldn't find profile {search_profile_field_value} in class {search_class_field_value}",severity="error")

    def action_search(self) -> None:
        self.get_acl(notification=True)

    def action_update(self) -> None:
        search_profile_field_value = self.get_child_by_type(PanelResourcePermitSearchField).get_child_by_id("search_permit_profile",Input).value
        search_class_field_value = self.get_child_by_type(PanelResourcePermitSearchField).get_child_by_id("search_permit_class",Input).value

        racf_id_field_value = self.get_child_by_type(PanelResourcePermitCreate).get_child_by_id("permit_racf_id",Input).value

        if resource.resource_profile_exists(resource=search_profile_field_value,resource_class=search_class_field_value):
            base_segment = get_traits_from_input("alter", self, prefix="base", trait_cls=permit.BasePermitTraits)

            return_code = permit.update_resource_permit(profile=search_profile_field_value,class_name=search_class_field_value,racf_id=racf_id_field_value,base=base_segment)

            self.get_acl(notification=False)

            if return_code == 0:
                self.notify("Created permit",severity="information")
            else:
                send_notification(self,message=f"Couldn't create permit, return code: {return_code}",severity="error")
                