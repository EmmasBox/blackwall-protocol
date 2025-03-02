from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, RadioButton, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, Right, VerticalScroll

try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except: 
    racfu_enabled = False

from .api import user

class PanelUserInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Created: ")

class PanelUserName(HorizontalGroup):
    """Username and name components"""
    def compose(self) -> ComposeResult:
        yield Label("Username*: ")
        yield Input(max_length=8,id="username",classes="username",tooltip="Username is what the user uses to log on with, this is required.")
        yield Label("name: ")
        yield Input(max_length=20,id="name",classes="name",tooltip="For personal users this is typically used for names i.e. Valerie, for system users it can be the subsystem that it is used for")

class PanelUserOwnership(HorizontalGroup):
    """Component that contains ownership field and default group"""
    def compose(self) -> ComposeResult:
        yield Label("Owner*: ")
        yield Input(max_length=8,id="owner",classes="owner", tooltip="The group or user that owns this user profile. This is required in the RACF database")
        yield Label("Default group*: ")
        yield Input(max_length=8,id="default_group",classes="owner", tooltip="All users must belong to a group in the RACF database")

class PanelUserPassword(VerticalGroup):
    #Import css
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
                yield RadioButton("TSO enabled",id="user_segment_tso")
            with Collapsible(title="OMVS"):
                yield RadioButton("OMVS",id="user_segment_omvs")
                yield Label("UID: ")
                yield Input(max_length=30,id="uid",classes="username",type="integer")
                yield Label("Home directory: ")
                yield Input(max_length=255,id="home_directory",classes="username")
                yield Label("Shell path: ")
                yield Input(max_length=255,id="shell",classes="username")
            with Collapsible(title="CSDATA"):    
                yield RadioButton("CSDATA",id="user_segment_csdata")
            with Collapsible(title="KERB"):   
                yield RadioButton("KERB",id="user_segment_kerb")
            with Collapsible(title="LANGUAGE"):   
                yield RadioButton("LANGUAGE",id="user_segment_language")
            with Collapsible(title="OPERPARM"):   
                yield RadioButton("OPERPARM",id="user_segment_operparm")
            with Collapsible(title="OVM"):   
                yield RadioButton("OVM",id="user_segment_ovm")
            with Collapsible(title="NDS"): 
                yield RadioButton("NDS",id="user_segment_nds")
            with Collapsible(title="DCE"): 
                yield RadioButton("DCE",id="user_segment_dce")
            with Collapsible(title="DFP"): 
                yield RadioButton("DFP",id="user_segment_dfp")
            with Collapsible(title="CICS"): 
                yield RadioButton("CICS",id="user_segment_cics")

class PanelUserSave(Right):
    def action_save_user(self) -> None:
        if  racfu_enabled:
            username = self.parent.query_exactly_one(selector="#username").value
            name = self.parent.query_exactly_one(selector="#name").value
            owner = self.parent.query_exactly_one(selector="#owner").value
            default_group = self.parent.query_exactly_one(selector="#default_group").value
            if user.user_create(
                username=username,
                base=user.BaseUserTraits(owner=owner,name=name,default_group=default_group)
                ):
                self.notify(f"User {username.value} created",severity="information")
            else:
                self.notify("Unable to create user",severity="error")

        else:
            self.notify("Error: RACFU features disabled, no user was created",severity="error")

    """Save user button"""
    def compose(self) -> ComposeResult:
        yield Button("Save", tooltip="This will update the user, or create it if the user doesn't exist",action="save_user",classes="save-button")

class PanelUser(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelUserInfo()
        yield PanelUserName()
        yield PanelUserOwnership()
        yield PanelUserPassword()
        yield PanelUserPassphrase()
        yield PanelUserAttributes()
        yield PanelUserSegments()
        yield PanelUserSave()