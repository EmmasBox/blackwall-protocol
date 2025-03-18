
from dataclasses import dataclass
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, RadioButton, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.api import user
from blackwall.panels.panel_mode import PanelMode

class PanelUserInfo(HorizontalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    def compose(self) -> ComposeResult:
        if self.edit_mode != PanelMode.create:
            yield Label("Created: ")
            yield Label("Last logon: ")

class PanelUserName(HorizontalGroup):
    """Username and name components"""
    username: reactive[str] = reactive("")
    name: reactive[str] = reactive("")

    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    if edit_mode == True:
        is_disabled = True
    else:
        is_disabled = False

    def compose(self) -> ComposeResult:
        yield Label("Username*: ")
        yield Input(max_length=8,id="username",classes="username",tooltip="Username is what the user uses to log on with, this is required. While very few characters can be used at least 4 character long usernames are recommended to avoid collisions",disabled=self.is_disabled).data_bind(value=PanelUserName.username)
        yield Label("name: ")
        yield Input(max_length=20,id="name",classes="name",tooltip="For personal users this is typically used for names i.e. Song So Mi, for system users it can be the name of the subsystem that it is used for").data_bind(value=PanelUserName.name)

class PanelUserOwnership(HorizontalGroup):
    """Component that contains ownership field and default group"""
    def compose(self) -> ComposeResult:
        yield Label("Owner: ")
        yield Input(max_length=8,id="owner",classes="owner", tooltip="The group or user that owns this user profile. This is required in the RACF database")
        yield Label("Default group*: ")
        yield Input(max_length=8,id="default_group",classes="owner", tooltip="All users must belong to a group in the RACF database")

class PanelUserInstalldata(HorizontalGroup):
    """Component that contains install data field"""
    def compose(self) -> ComposeResult:
        yield Label("Installation data: ")
        yield Input(max_length=254,id="installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a user. You can use installation data to describe whatever you want, such as department or what the user is for")

class PanelUserPassword(VerticalGroup):
    """Change/add password component"""
    def compose(self) -> ComposeResult:
        with Collapsible(title="Password"):
            yield Label("Passwords can only be 8 characters long")
            yield Label("New password:")
            yield Input(max_length=8,id="password",classes="password",password=True)
            yield Label("Repeat password*:")
            yield Input(max_length=8,id="password_repeat",classes="password",password=True)

class PanelUserPassphrase(VerticalGroup):
    """Change/add passphrase component"""
    def compose(self) -> ComposeResult:
        with Collapsible(title="Passphrase"):
            yield Label("Passphrases need to be between 12 and 100 characaters long")
            yield Label("New passphrase:")
            yield Input(max_length=100,id="passphrase",classes="passphrase",password=True)
            yield Label("Repeat passphrase*:")
            yield Input(max_length=100,id="passphrase_repeat",classes="passphrase",password=True)
    
class PanelUserAttributes(VerticalGroup):
    """User attributes component"""
    def compose(self) -> ComposeResult:
        with Collapsible(title="User attributes"):
            yield RadioButton("Special",id="user_attribute_special",tooltip="This is RACF's way of making a user admin. Special users can make other users special, making this a potentially dangerous option")
            yield RadioButton("Operations",id="user_attribute_operations",tooltip="This is a very dangerous attribute that allows you to bypass most security checks on the system, this should only be used during maintenance tasks and removed immediately afterwards")
            yield RadioButton("Auditor",id="user_attribute_auditor")
            yield RadioButton("Read only auditor (ROAUDIT)",id="user_attribute_roaudit")

class PanelUserSegments(VerticalGroup):
    """Component where the user can add segments such as the OMVS segment"""
    def compose(self) -> ComposeResult:
        with Collapsible(title="User segments"):
            with Collapsible(title="TSO"):
                yield Label("logon procedure:")
                yield Input(max_length=8,id="logon_procedure")
                yield Label("account number:")
                yield Input(max_length=8,id="account_number")
                yield Label("logon command:")
                yield Input(max_length=16,id="logon_command")
                yield Label("hold class:")
                yield Input(max_length=8,id="hold_class")
                yield Label("job class:")
                yield Input(max_length=8,id="job_class")
                yield Label("message class:")
                yield Input(max_length=8,id="message_class")
                yield Label("sysout class:")
                yield Input(max_length=8,id="sysout_class")
                yield Label("max region size:")
                yield Input(id="max_region_size",type="integer")
            with Collapsible(title="OMVS"):
                yield Label("UID:")
                yield Input(max_length=30,id="uid",classes="username",type="integer")
                yield RadioButton(label="auto uid",value=False)
                yield Label("Home directory: ")
                yield Input(max_length=255,id="home_directory",classes="username")
                yield Label("Shell path: ")
                yield Input(max_length=255,id="default_shell",classes="username")
                yield Label("Max CPU time: ")
                yield Input(id="max_cpu_time")
                yield Label("Max threads: ")
                yield Input(id="max_threads")
                yield Label("Max processes: ")
                yield Input(id="max_processes")
                yield Label("Max shared memory: ")
                yield Input(id="max_shared_memory")
                yield Label("Max non-shared memory: ")
                yield Input(id="max_non_shared_memory")
                yield Label("Max files per process: ")
                yield Input(id="max_files_per_process")
                yield Label("Max files mapping pages: ")
                yield Input(id="max_file_mapping_pages")
            with Collapsible(title="CSDATA"):    
                yield RadioButton("CSDATA",id="user_segment_csdata")
            with Collapsible(title="KERB"):   
                yield RadioButton("KERB",id="user_segment_kerb")
            with Collapsible(title="LANGUAGE"):   
                yield Label("Primary language: ")
                yield Input(id="language_primary")
                yield Label("Secondary language: ")
                yield Input(id="language_secondary")
            with Collapsible(title="OPERPARM"):   
                yield RadioButton("OPERPARM",id="user_segment_operparm")
            with Collapsible(title="OVM"):   
                yield RadioButton("OVM",id="user_segment_ovm")
            with Collapsible(title="NDS"): 
                yield Label("NDS username: ")
                yield Input(id="nds_username")
            with Collapsible(title="DCE"): 
                yield RadioButton("DCE",id="user_segment_dce")
            with Collapsible(title="DFP"): 
                yield RadioButton("DFP",id="user_segment_dfp")
            with Collapsible(title="CICS"): 
                yield RadioButton("CICS",id="user_segment_cics")

class PanelUserActionButtons(HorizontalGroup):
    """Action buttons"""
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    if edit_mode == True:
        is_disabled = True
    else:
        is_disabled = False

    def __init__(self, save_action: str, delete_action: str):
        super().__init__()
        self.save_action = save_action
        self.delete_action = delete_action

    def compose(self) -> ComposeResult:
        if self.edit_mode == PanelMode.create:
            yield Button("Create", tooltip="This will update the user, or create it if the user doesn't exist",action="save",classes="action-button",id="save")
        elif self.edit_mode == PanelMode.edit:
            yield Button("Save", tooltip="This will update the user, or create it if the user doesn't exist",action="save",classes="action-button",id="save")
        yield Button("Delete", tooltip="This will delete the user permanently from the RACF database",id="delete",action="delete",classes="action-button",disabled=self.is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

@dataclass
class UserInfo:
    mode: PanelMode = PanelMode.create
    username: str = ""
    name: str = ""
    owner: str = ""
    dfltgrp: str = ""
    installation_data: str = ""

class PanelUser(VerticalScroll):
    user_info: reactive[UserInfo] = reactive(UserInfo)

    def compose(self) -> ComposeResult:
        yield PanelUserInfo()
        yield PanelUserName()
        yield PanelUserOwnership()
        yield PanelUserInstalldata()
        yield PanelUserPassword()
        yield PanelUserPassphrase()
        yield PanelUserAttributes()
        yield PanelUserSegments()
        yield PanelUserActionButtons(save_action="save_user", delete_action="delete_user")
    
    def watch_user_info(self, value: UserInfo):
        user_name_panel = self.query_exactly_one(PanelUserName)
        #valid modes: create, edit, and read
        user_name_panel.mode = value.mode
        user_name_panel.username = value.username
        user_name_panel.name = value.name
        user_name_panel.owner = value.owner
        user_name_panel.dfltgrp = value.dfltgrp
        user_name_panel.installation_data = value.installation_data

    def set_edit_mode(self):
        user_name_panel = self.query_exactly_one(PanelUserName)
        user_name_panel.mode = PanelMode.edit
        self.query_exactly_one(selector="#username").disabled = True
        self.query_exactly_one(selector="#delete").disabled = False
        self.query_exactly_one(selector="#save").label = "Save"
        self.notify(f"Switched to edit mode",severity="information")

    def action_delete_user(self) -> None:
        pass

    def action_save_user(self) -> None:
        username = self.query_exactly_one(selector="#username").value
        name = self.query_exactly_one(selector="#name").value
        owner = self.query_exactly_one(selector="#owner").value
        default_group = self.query_exactly_one(selector="#default_group").value
        installation_data = self.query_exactly_one(selector="#installation_data").value
        if installation_data == "":
            installation_data = None
        password = self.query_exactly_one(selector="#password").value
        password_repeat = self.query_exactly_one(selector="#password_repeat").value
        if password == "" or password != password_repeat:
            password = None
        passphrase = self.query_exactly_one(selector="#passphrase").value
        passphrase_repeat = self.query_exactly_one(selector="#passphrase_repeat").value
        if passphrase == "" or passphrase != passphrase_repeat:
            passphrase = None

        special = self.query_exactly_one(selector="#user_attribute_special").value
        operations = self.query_exactly_one(selector="#user_attribute_operations").value
        auditor = self.query_exactly_one(selector="#user_attribute_auditor").value

        result = user.update_user(
            username=username,
            create=not user.user_exists(username=username),
            base=user.BaseUserTraits(
                owner=owner,
                name=name,
                default_group=default_group,
                password=password,
                passphrase=passphrase,
                special=special,
                operations=operations,
                auditor=auditor,
                installation_data=installation_data
                                        )
        )

        if not user.user_exists(username=username):
            if (result == 0 or result == 4):
                self.notify(f"User {username} created, return code: {result}",severity="information")
                self.set_edit_mode()
            else:
                self.notify(f"Unable to create user, return code: {result}",severity="error")
        else:
            if (result == 0 or result == 4):
                self.notify(f"User {username} updated, return code: {result}",severity="information")
            else:
                self.notify(f"Unable to update user, return code: {result}",severity="error")
