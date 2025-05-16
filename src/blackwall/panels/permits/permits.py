from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.suggester import SuggestFromList
from textual.widgets import Button, ContentSwitcher, DataTable, Input, Label, Select

from blackwall.api import dataset, group, permit, resource, user
from blackwall.api.setropts import get_active_classes, refresh_racf
from blackwall.emoji import get_emoji
from blackwall.notifications import send_notification
from blackwall.panels.traits_ui import get_traits_from_input
from blackwall.regex import racf_id_regex

PERMIT_RESOURCE_COLUMNS = [
    ("ID", "Access", "Type", "Installation data"),
]

PERMIT_DATASET_COLUMNS = [
    ("ID", "Access", "Type","Installation data"),
]


class PanelResourcePermitInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Use this panel to create, delete, and update permits for general resource profiles",classes="label-generic")

class PanelResourcePermitSearchField(HorizontalGroup):
    def __init__(self, search_action: str):
        super().__init__()
        self.search_action = search_action

    active_classes = get_active_classes()

    def compose(self) -> ComposeResult:
        yield Input(id="search_permit_resource_class",suggester=SuggestFromList(self.active_classes,case_sensitive=False),placeholder="class...",classes="field-short-generic")
        yield Input(id="search_permit_resource_profile",placeholder="resource profile name...",classes="search-field")    
        yield Button(label="Get ACL",id="search_permit_button",action="search_resource_profile")

    @on(Input.Submitted)
    async def action_search(self):
        await self.app.run_action(self.search_action,default_namespace=self.parent)

class PanelResourcePermitCreate(HorizontalGroup):
    def __init__(self, update_action: str):
        super().__init__()
        self.update_action = update_action
    
    def compose(self) -> ComposeResult:
        yield Select([("NONE", "NONE"),("EXECUTE", "EXECUTE"),("READ", "READ"),("UPDATE", "UPDATE"),("CONTROL", "CONTROL"),("ALTER", "ALTER")],value="READ",classes="uacc-select",id="base_access")
        yield Input(id="permit_racf_id",placeholder="ID...",max_length=8,restrict=racf_id_regex,classes="field-short-generic", tooltip="User ID or group ID you want this permit change to affect")    
        yield Button(f"{get_emoji("💾")} Save",id="resource_permit_save",action="update")

    @on(Input.Submitted)
    async def action_update(self):
        await self.app.run_action(self.update_action,default_namespace=self.parent)

class PanelResourcePermitsList(VerticalGroup):
    BINDINGS = [
        Binding(key="delete",description="Deletes a permit",action=""),
    ]

    def compose(self) -> ComposeResult:
        yield Label("Access list:",classes="label-generic")
        yield DataTable(id="resource_permits_table")

    def on_mount(self) -> None:
        permit_table = self.get_child_by_id("resource_permits_table",DataTable)
        permit_table.zebra_stripes = True
        permit_table.add_columns(*PERMIT_RESOURCE_COLUMNS[0]) 

class PanelPermitsResource(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield PanelResourcePermitInfo()
        yield PanelResourcePermitSearchField(search_action="search_resource_profile")
        yield PanelResourcePermitCreate(update_action="resource_permit_update")
        yield PanelResourcePermitsList()

    def get_resource_profile_acl(self, notification: bool) -> None:
        search_profile_field_value = self.get_child_by_type(PanelResourcePermitSearchField).query_exactly_one("#search_permit_resource_profile",Input).value
        search_class_field_value = self.get_child_by_type(PanelResourcePermitSearchField).query_exactly_one("#search_permit_resource_class",Input).value
        permit_table = self.get_child_by_type(PanelResourcePermitsList).get_child_by_id("resource_permits_table",DataTable)
        
        if resource.resource_profile_exists(resource=search_profile_field_value,resource_class=search_class_field_value):
            resource_acl = resource.get_resource_acl(resource=search_profile_field_value,resource_class=search_class_field_value)
            permit_table.clear(columns=False)

            for entry in resource_acl:
                entry_id = entry["base:access_id"]
                entry_access = entry["base:access_type"]

                #Checks if the entry is a user or group
                id_type = "group" if group.group_exists(entry_id) else "user"
                installation_data = ""
                if id_type == "group":
                    installation_data = group.get_installation_data(group=entry_id)
                else:
                    installation_data = user.get_installation_data(username=entry_id)
                
                #Adds the entry to the datatable
                permit_table.add_row(entry_id,entry_access,id_type,installation_data)
            if notification:
                self.notify(f"Found profile {search_profile_field_value} in class {search_class_field_value}",markup=False,severity="information")
        else:
            if notification:
                self.notify(f"Couldn't find profile {search_profile_field_value} in class {search_class_field_value}",markup=False,severity="error")

    def action_search_resource_profile(self) -> None:
        self.get_resource_profile_acl(notification=True)

    def action_resource_permit_update(self) -> None:
        search_profile_field_value = self.get_child_by_type(PanelResourcePermitSearchField).query_exactly_one("#search_permit_resource_profile",Input).value
        search_class_field_value = self.get_child_by_type(PanelResourcePermitSearchField).query_exactly_one("#search_permit_resource_class",Input).value

        racf_id_field_value = self.get_child_by_type(PanelResourcePermitCreate).get_child_by_id("permit_racf_id",Input).value

        if resource.resource_profile_exists(resource=search_profile_field_value,resource_class=search_class_field_value):
            base_segment = get_traits_from_input(operator="alter", widget=self, prefix="base", trait_cls=permit.BasePermitTraits)

            return_code = permit.update_resource_permit(profile=search_profile_field_value,class_name=search_class_field_value,racf_id=racf_id_field_value,base=base_segment)

            refresh_racf()

            self.get_resource_profile_acl(notification=False)

            if return_code == 0:
                self.notify("Created permit",severity="information")
            else:
                send_notification(self,message=f"Couldn't create permit, return code: {return_code}",severity="error")

    def key_delete(self) -> None:
        search_profile_field_value = self.get_child_by_type(PanelResourcePermitSearchField).query_exactly_one("#search_permit_resource_profile",Input).value
        search_class_field_value = self.get_child_by_type(PanelResourcePermitSearchField).query_exactly_one("#search_permit_resource_class",Input).value

        datatable = self.query_exactly_one("#resource_permits_table", DataTable)
        column_index = datatable.cursor_column
        if column_index == 0:
            current_row = datatable.cursor_coordinate
            cell_info = datatable.get_cell_at(current_row)

            return_code = permit.delete_resource_permit(class_name=search_class_field_value,profile=search_profile_field_value,racf_id=cell_info)
        
            if return_code == 0:
                refresh_racf()

                self.get_resource_profile_acl(notification=False)

                self.notify(f"Permit deleted for {cell_info}")
            else:
                send_notification(self,message=f"Couldn't delete permit, return code: {return_code}",severity="error")

class PanelDatasetPermitInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Use this panel to create, delete, and update permits for dataset profiles",classes="label-generic")

class PanelDatasetPermitSearchField(HorizontalGroup):
    def __init__(self, search_action: str):
        super().__init__()
        self.search_action = search_action

    active_classes = get_active_classes()

    def compose(self) -> ComposeResult:
        yield Input(id="search_permit_dataset_profile",placeholder="dataset profile name...",classes="search-field")    
        yield Button(label="Get ACL",id="search_dataset_permit_button",action="search_dataset_profile")

    @on(Input.Submitted)
    async def action_search(self):
        await self.app.run_action(self.search_action,default_namespace=self.parent)

class PanelDatasetPermitCreate(HorizontalGroup):
    def __init__(self, update_action: str):
        super().__init__()
        self.update_action = update_action
    
    def compose(self) -> ComposeResult:
        yield Select([("NONE", "NONE"),("EXECUTE", "EXECUTE"),("READ", "READ"),("UPDATE", "UPDATE"),("CONTROL", "CONTROL"),("ALTER", "ALTER")],value="READ",classes="uacc-select",id="base_access")
        yield Input(id="permit_racf_id",placeholder="ID...",max_length=8,restrict=racf_id_regex,classes="field-short-generic", tooltip="User ID or group ID you want this permit change to affect")    
        yield Button(f"{get_emoji("💾")} Save",id="resource_permit_save",action="update")

    @on(Input.Submitted)
    async def action_update(self):
        await self.app.run_action(self.update_action,default_namespace=self.parent)

class PanelDatasetPermitsList(VerticalGroup):
    BINDINGS = [
        Binding(key="delete",description="Deletes a permit",action=""),
    ]

    def compose(self) -> ComposeResult:
        yield Label("Access list:",classes="label-generic")
        yield DataTable(id="dataset_permits_table")

    def on_mount(self) -> None:
        permit_table = self.get_child_by_id("dataset_permits_table",DataTable)
        permit_table.zebra_stripes = True
        permit_table.add_columns(*PERMIT_DATASET_COLUMNS[0]) 

class PanelPermitsDataset(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield PanelDatasetPermitInfo()
        yield PanelDatasetPermitSearchField(search_action="search_dataset_profile")
        yield PanelDatasetPermitCreate(update_action="dataset_permit_update")
        yield PanelDatasetPermitsList()

    def get_dataset_profile_acl(self, notification: bool) -> None:
        search_profile_field_value = self.get_child_by_type(PanelDatasetPermitSearchField).query_exactly_one("#search_permit_dataset_profile",Input).value
        permit_table = self.get_child_by_type(PanelDatasetPermitsList).get_child_by_id("dataset_permits_table",DataTable)
        
        if dataset.dataset_profile_exists(dataset=search_profile_field_value):
            resource_acl = dataset.get_dataset_acl(dataset=search_profile_field_value)
            permit_table.clear(columns=False)

            for entry in resource_acl:
                entry_id = entry["base:access_id"]
                entry_access = entry["base:access_type"]

                #Checks if the entry is a user or group
                id_type = "group" if group.group_exists(entry_id) else "user"
                installation_data = ""
                if id_type == "group":
                    installation_data = group.get_installation_data(group=entry_id)
                else:
                    installation_data = user.get_installation_data(username=entry_id)

                #Adds the entry to the datatable
                permit_table.add_row(entry_id,entry_access,id_type,installation_data)
            if notification:
                self.notify(f"Found dataset profile {search_profile_field_value}",markup=False,severity="information")
        else:
            if notification:
                self.notify(f"Couldn't find dataset profile {search_profile_field_value}",markup=False,severity="error")

    def action_search_dataset_profile(self) -> None:
        self.get_dataset_profile_acl(notification=True)

    def action_dataset_permit_update(self) -> None:
        search_profile_field_value = self.get_child_by_type(PanelDatasetPermitSearchField).query_exactly_one("#search_permit_dataset_profile",Input).value

        racf_id_field_value = self.get_child_by_type(PanelDatasetPermitCreate).get_child_by_id("permit_racf_id",Input).value

        if dataset.dataset_profile_exists(dataset=search_profile_field_value):
            base_segment = get_traits_from_input(operator="alter", widget=self, prefix="base", trait_cls=permit.BasePermitTraits)

            return_code = permit.update_dataset_permit(dataset=search_profile_field_value,racf_id=racf_id_field_value,base=base_segment)

            refresh_racf()

            self.get_dataset_profile_acl(notification=False)

            if return_code == 0:
                self.notify("Created permit",severity="information")
            else:
                send_notification(self,message=f"Couldn't create permit, return code: {return_code}",severity="error")

    def key_delete(self) -> None:
        search_profile_field_value = self.get_child_by_type(PanelDatasetPermitSearchField).query_exactly_one("#search_permit_dataset_profile",Input).value

        datatable = self.query_exactly_one("#dataset_permits_table", DataTable)
        column_index = datatable.cursor_column
        if column_index == 0:
            current_row = datatable.cursor_coordinate
            cell_info = datatable.get_cell_at(current_row)

            return_code = permit.delete_dataset_permit(dataset=search_profile_field_value,racf_id=cell_info)
        
            if return_code == 0:
                refresh_racf()

                self.get_dataset_profile_acl(notification=False)

                self.notify(f"Dataset permit deleted for {cell_info}")
            else:
                send_notification(self,message=f"Couldn't delete dataset permit, return code: {return_code}",severity="error")

class PanelPermitsSwitcherButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button(id="permit_resource_panel_button",label="Resource profile",classes="search-buttons",name="permit_resource_panel")
        yield Button(id="permit_dataset_panel_button",label="Dataset profile",classes="search-buttons",name="permit_dataset_panel")

class PanelPermits(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelPermitsSwitcherButtons()
        with ContentSwitcher(initial="permit_resource_panel",id="permit_switcher",classes="permit-switcher"):
            yield PanelPermitsResource(id="permit_resource_panel")
            yield PanelPermitsDataset(id="permit_dataset_panel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.name  
                