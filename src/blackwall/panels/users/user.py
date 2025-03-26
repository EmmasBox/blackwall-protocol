
from collections.abc import Generator
from dataclasses import dataclass, fields, Field
from types import UnionType
from typing import get_args
from textual.lazy import Lazy
from textual.widget import Widget
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, RadioButton, Collapsible, Select
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.api import user
from blackwall.panels.panel_mode import PanelMode

from ..traits_ui import generate_trait_inputs, get_traits_from_input

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

    if edit_mode is True:
        is_disabled = True
    else:
        is_disabled = False

    def compose(self) -> ComposeResult:
        yield Label("Username*: ")
        yield Input(max_length=8,id="username",classes="username",tooltip="Username is what the user uses to log on with, this is required. While very few characters can be used at least 4 character long usernames are recommended to avoid collisions",disabled=self.is_disabled).data_bind(value=PanelUserName.username)
        yield Label("name: ")
        yield Input(max_length=20,id="base_name",classes="name",tooltip="For personal users this is typically used for names i.e. Song So Mi, for system users it can be the name of the subsystem that it is used for").data_bind(value=PanelUserName.name)

class PanelUserOwnership(HorizontalGroup):
    """Component that contains ownership field and default group"""
    def compose(self) -> ComposeResult:
        yield Label("Owner: ")
        yield Input(max_length=8,id="base_owner",classes="owner", tooltip="The group or user that owns this user profile. This is required in the RACF database")
        yield Label("Default group*: ")
        yield Input(max_length=8,id="base_default_group",classes="owner", tooltip="All users must belong to a group in the RACF database")

class PanelUserInstalldata(HorizontalGroup):
    """Component that contains install data field"""
    def compose(self) -> ComposeResult:
        yield Label("Installation data: ")
        yield Input(max_length=254,id="base_installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a user. You can use installation data to describe whatever you want, such as department or what the user is for")

class PanelUserPassword(VerticalGroup):
    """Change/add password component"""
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="Password")):
            yield Label("Passwords can only be 8 characters long")
            yield Label("New password:")
            yield Input(max_length=8,id="base_password",classes="password",password=True)

class PanelUserPassphrase(VerticalGroup):
    """Change/add passphrase component"""
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="Passphrase")):
            yield Label("Passphrases need to be between 12 and 100 characaters long")
            yield Label("New passphrase:")
            yield Input(max_length=100,id="base_passphrase",classes="passphrase",password=True)
    
class PanelUserAttributes(VerticalGroup):
    """User attributes component"""
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="User attributes")):
            yield RadioButton("Special",id="base_special",tooltip="This is RACF's way of making a user admin. Special users can make other users special, making this a potentially dangerous option")
            yield RadioButton("Operations",id="base_operations",tooltip="This is a very dangerous attribute that allows you to bypass most security checks on the system, this should only be used during maintenance tasks and removed immediately afterwards")
            yield RadioButton("Auditor",id="base_auditor")

class PanelUserLevelAndCategory(VerticalGroup):
    """User attributes component"""
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="Security level and category")):
            yield Label("Security level:")
            yield Input(max_length=8,id="base_security_level",classes="field-short-generic")
            yield Label("Security category:")
            yield Input(max_length=8,id="base_security_category",classes="field-short-generic")
            yield Label("Security label:")
            yield Input(max_length=8,id="base_security_label",classes="field-short-generic")

class PanelUserDatasetsAndUACC(VerticalGroup):
    """User attributes component"""
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="Datasets and UACC")):
            yield Label("UACC:")
            yield Select([("NONE", 1),("READ", 2),("EXECUTE", 3),("UPDATE", 4),("CONTROL", 5),("ALTER", 6)],id="universal_access",value=1,classes="uacc-select")
            yield Label("model dataset:")
            yield Input(max_length=255,id="base_model_data_set",classes="field-long-generic")
            yield Label("Group dataset access:")
            yield Input(max_length=8,id="base_group_data_set_access",classes="field-short-generic")

class PanelUserSegments(VerticalGroup):
    """Component where the user can add segments such as the OMVS segment"""
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="User segments")):
            yield from generate_trait_inputs(title="TSO", prefix="tso", traits_class=user.TSOUserTraits)
            yield from generate_trait_inputs(title="OMVS", prefix="omvs", traits_class=user.OMVSUserTraits)
            yield from generate_trait_inputs(title="Work attributes", prefix="workattr", traits_class=user.WorkattrUserTraits)
            yield from generate_trait_inputs(title="CICS", prefix="cics", traits_class=user.CICSUserTraits)
            yield from generate_trait_inputs(title="KERB", prefix="kerb", traits_class=user.KerbUserTraits)
            yield from generate_trait_inputs(title="Language", prefix="language", traits_class=user.LanguageUserTraits)
            yield from generate_trait_inputs(title="OPERPARM", prefix="operparm", traits_class=user.OperparmUserTraits)
            yield from generate_trait_inputs(title="OVM", prefix="ovm", traits_class=user.OvmUserTraits)
            yield from generate_trait_inputs(title="NDS", prefix="nds", traits_class=user.NDSUserTraits)
            yield from generate_trait_inputs(title="Netview", prefix="netview", traits_class=user.NetviewUserTraits)
            yield from generate_trait_inputs(title="MFA", prefix="mfa", traits_class=user.MfaUserTraits)
            yield from generate_trait_inputs(title="DCE", prefix="dce", traits_class=user.DCEUserTraits)
            yield from generate_trait_inputs(title="DFP", prefix="dfp", traits_class=user.DFPUserTraits)
            yield from generate_trait_inputs(title="EIM", prefix="eim", traits_class=user.EIMUserTraits)
            yield from generate_trait_inputs(title="Proxy", prefix="proxy", traits_class=user.ProxyUserTraits)
            yield from generate_trait_inputs(title="Lotus Notes", prefix="lnotes", traits_class=user.LnotesUserTraits)

class PanelUserActionButtons(HorizontalGroup):
    """Action buttons"""
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    if edit_mode is True:
        delete_is_disabled = False
    else:
        delete_is_disabled = True

    def __init__(self, save_action: str, delete_action: str):
        super().__init__()
        self.save_action = save_action
        self.delete_action = delete_action

    def compose(self) -> ComposeResult:
        if self.edit_mode == PanelMode.create:
            yield Button("Create", tooltip="This will update the user, or create it if the user doesn't exist",action="save",classes="action-button",id="save")
        elif self.edit_mode == PanelMode.edit:
            yield Button("Save", tooltip="This will update the user, or create it if the user doesn't exist",action="save",classes="action-button",id="save")
        yield Button("Delete", tooltip="This will delete the user permanently from the RACF database",id="delete",action="delete",classes="action-button",disabled=self.delete_is_disabled)

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
        yield PanelUserDatasetsAndUACC()
        yield PanelUserAttributes()
        yield PanelUserLevelAndCategory()
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
        user_exists = user.user_exists(username=username)

        if user_exists:
            operator = "alter"
        else:
            operator = "add"
        
        base_segment = get_traits_from_input(operator, self, prefix="base", trait_cls=user.BaseUserTraits)
        tso_segment = get_traits_from_input(operator, self, prefix="tso", trait_cls=user.TSOUserTraits)
        omvs_segment = get_traits_from_input(operator, self, prefix="omvs", trait_cls=user.OMVSUserTraits)
        cics_segment = get_traits_from_input(operator, self, prefix="cics", trait_cls=user.CICSUserTraits)
        workattr_segment = get_traits_from_input(operator, self, prefix="workattr", trait_cls=user.WorkattrUserTraits)
        language_segment = get_traits_from_input(operator, self, prefix="language", trait_cls=user.LanguageUserTraits)
        dfp_segment = get_traits_from_input(operator, self, prefix="dfp", trait_cls=user.DFPUserTraits)
        dce_segment = get_traits_from_input(operator, self, prefix="dce", trait_cls=user.DCEUserTraits)
        proxy_segment = get_traits_from_input(operator, self, prefix="proxy", trait_cls=user.ProxyUserTraits)
        operparm_segment = get_traits_from_input(operator, self, prefix="operparm", trait_cls=user.OperparmUserTraits)
        ovm_segment = get_traits_from_input(operator, self, prefix="ovm", trait_cls=user.OvmUserTraits)
        eim_segment = get_traits_from_input(operator, self, prefix="eim", trait_cls=user.EIMUserTraits)
        nds_segment = get_traits_from_input(operator, self, prefix="nds", trait_cls=user.NDSUserTraits)
        lnotes_segment = get_traits_from_input(operator, self, prefix="lnotes", trait_cls=user.LnotesUserTraits)
        mfa_segment = get_traits_from_input(operator, self, prefix="mfa", trait_cls=user.MfaUserTraits)
        netview_segment = get_traits_from_input(operator, self, prefix="netview", trait_cls=user.NetviewUserTraits)
        result = user.update_user(
            username=username,
            create=not user_exists,
            base=base_segment,
            tso=tso_segment,
            omvs=omvs_segment,
            cics=cics_segment,
            workattr=workattr_segment,
            language=language_segment,
            dfp=dfp_segment,
            dce=dce_segment,
            proxy=proxy_segment,
            operparm=operparm_segment,
            ovm=ovm_segment,
            eim=eim_segment,
            nds=nds_segment,
            lnotes=lnotes_segment,
            mfa=mfa_segment,
            netview=netview_segment
        )

        if not user_exists:
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
