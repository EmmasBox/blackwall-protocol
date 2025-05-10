
from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.lazy import Lazy
from textual.reactive import reactive
from textual.widgets import Button, Collapsible, Input, Label, RadioButton, Select

from blackwall.api import user
from blackwall.emoji import get_emoji
from blackwall.modals import generic_confirmation_modal
from blackwall.notifications import send_notification
from blackwall.panels.panel_mode import PanelMode
from blackwall.regex import racf_id_regex

from ..traits_ui import (
    generate_trait_section,
    get_traits_from_input,
    set_traits_in_input,
)


class PanelUserInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Creation date:",classes="date-labels")
        yield Input(id="base_create_date",disabled=True,classes="date-fields")
        yield Label("Last access date:",classes="date-labels")
        yield Input(id="base_last_access_date",disabled=True,classes="date-fields")
        #yield Label("Last access time:",classes="date-labels")
        #yield Input(id="last_acess_time",disabled=True,classes="date-fields")

class PanelUserName(HorizontalGroup):
    """Username and name components"""
    username: reactive[str] = reactive("")

    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    username_is_disabled = edit_mode is True

    def compose(self) -> ComposeResult:
        yield Label("Username*:")
        yield Input(max_length=8,restrict=racf_id_regex,id="username",classes="field-short-generic",tooltip="Username is what the user uses to log on with, this is required. While very few characters can be used at least 4 character long usernames are recommended to avoid collisions",disabled=self.username_is_disabled).data_bind(value=PanelUserName.username)
        yield Label("name:")
        yield Input(max_length=20,id="base_name",classes="name",tooltip="For personal users this is typically used for names i.e. Song So Mi, for system users it can be the name of the subsystem that it is used for")

class PanelUserOwnership(HorizontalGroup):
    """Component that contains ownership field and default group"""
    def compose(self) -> ComposeResult:
        yield Label("Owner:")
        yield Input(max_length=8,restrict=racf_id_regex,id="base_owner",classes="field-short-generic", tooltip="The group or user that owns this user profile. This is required in the RACF database")
        yield Label("Default group*:")
        yield Input(max_length=8,restrict=racf_id_regex,id="base_default_group",classes="field-short-generic", tooltip="All users must belong to a group in the RACF database")
        yield Label("Default group authority:")
        #yield Input(id="base_default_group_authority",classes="field-short-generic",max_length=8)
        yield Select([("USE", "USE"),("CREATE", "CREATE"),("CONNECT", "CONNECT"),("JOIN", "JOIN")],id="base_default_group_authority",value="USE",classes="uacc-select")

class PanelUserInstalldata(HorizontalGroup):
    """Component that contains install data field"""
    def compose(self) -> ComposeResult:
        yield Label("Installation data: ")
        yield Input(max_length=255,id="base_installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a user. You can use installation data to describe whatever you want, such as department or what the user is for")

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
        with Collapsible(title="User attributes"):
            yield RadioButton("Special",id="base_special",tooltip="This is RACF's way of making a user admin. Special users can make other users special, making this a potentially dangerous option",classes="generic-checkbox-small")
            yield RadioButton("Operations",id="base_operations",tooltip="This is a very dangerous attribute that allows you to bypass most security checks on the system, this should only be used during maintenance tasks and removed immediately afterwards",classes="generic-checkbox-small")
            yield RadioButton("Auditor",id="base_auditor",classes="generic-checkbox-small",tooltip="This attribute allows you to change system options and extract data about the RACF database, this one is pretty dangerous but not as dagnerous as special.")
            yield RadioButton("Read only auditor",id="base_audit_responsibility",classes="generic-checkbox-small",tooltip="This attribute allows you to extract data about the RACF database, but you can't change any settings. This one is still dangerous but signifincantly less than the others as nothing can be changed.")

class PanelUserAccess(VerticalGroup):
    """User dataset component"""
    def compose(self) -> ComposeResult:
        with Collapsible(title="Access"):
            yield Label("Security level:")
            yield Input(max_length=8,id="base_security_level",classes="field-short-generic")
            yield Label("Security category:")
            yield Input(max_length=8,id="base_security_category",classes="field-short-generic")
            yield Label("Security label:")
            yield Input(max_length=8,id="base_security_label",classes="field-short-generic")
            yield Label("UACC:")
            yield Select([("NONE", "NONE"),("READ", "READ"),("EXECUTE", "EXECUTE"),("UPDATE", "UPDATE"),("CONTROL", "CONTROL"),("ALTER", "ALTER")],id="base_universal_access",value="NONE",classes="uacc-select")
            yield RadioButton(label="Audit logging (UAUDIT)",id="base_audit_logging",classes="generic-checkbox-small")

class PanelUserDatasets(VerticalGroup):
    """User dataset component"""
    def compose(self) -> ComposeResult:
        with Collapsible(title="Datasets"):
            yield Label("Model dataset:")
            yield Input(max_length=255,id="base_model_data_set",classes="field-long-generic")
            yield RadioButton(label="Group dataset access",id="base_group_data_set_access",classes="generic-checkbox-medium")

class PanelUserSegments(VerticalGroup):
    """Component where the user can add segments such as the OMVS segment"""
    def compose(self) -> ComposeResult:
        with Collapsible(title="User segments"):
            yield from generate_trait_section(title="TSO", prefix="tso", traits_class=user.TSOUserTraits)
            yield from generate_trait_section(title="z/OS Unix (OMVS)", prefix="omvs", traits_class=user.OMVSUserTraits)
            yield from generate_trait_section(title="Work attributes", prefix="workattr", traits_class=user.WorkattrUserTraits)
            yield from generate_trait_section(title="CICS", prefix="cics", traits_class=user.CICSUserTraits)
            yield from generate_trait_section(title="KERB", prefix="kerb", traits_class=user.KerbUserTraits)
            yield from generate_trait_section(title="Language", prefix="language", traits_class=user.LanguageUserTraits)
            yield from generate_trait_section(title="OPERPARM", prefix="operparm", traits_class=user.OperparmUserTraits)
            yield from generate_trait_section(title="OVM", prefix="ovm", traits_class=user.OvmUserTraits)
            yield from generate_trait_section(title="NDS", prefix="nds", traits_class=user.NDSUserTraits)
            yield from generate_trait_section(title="Netview", prefix="netview", traits_class=user.NetviewUserTraits)
            yield from generate_trait_section(title="MFA", prefix="mfa", traits_class=user.MfaUserTraits)
            yield from generate_trait_section(title="DCE", prefix="dce", traits_class=user.DCEUserTraits)
            yield from generate_trait_section(title="DFP", prefix="dfp", traits_class=user.DFPUserTraits)
            yield from generate_trait_section(title="EIM", prefix="eim", traits_class=user.EIMUserTraits)
            yield from generate_trait_section(title="Proxy", prefix="proxy", traits_class=user.ProxyUserTraits)
            yield from generate_trait_section(title="Lotus Notes", prefix="lnotes", traits_class=user.LnotesUserTraits)

class PanelUserActionButtons(HorizontalGroup):
    """Action buttons"""
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    delete_is_disabled = edit_mode is not True

    def __init__(self, save_action: str, delete_action: str):
        super().__init__()
        self.save_action = save_action
        self.delete_action = delete_action

    def compose(self) -> ComposeResult:
        if self.edit_mode == PanelMode.create:
            yield Button("Create", tooltip="This will update the user, or create it if the user doesn't exist",action="save",classes="action-button",id="save")
        elif self.edit_mode == PanelMode.edit:
            yield Button(f"{get_emoji("💾")} Save", tooltip="This will update the user, or create it if the user doesn't exist",action="save",classes="action-button",id="save")
        yield Button("Delete", tooltip="This will delete the user permanently from the RACF database",id="delete",action="delete",variant="error",classes="action-button",disabled=self.delete_is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

@dataclass
class UserInfo:
    base_traits: user.BaseUserTraits | None = None
    tso_traits: user.TSOUserTraits | None = None
    omvs_traits: user.OMVSUserTraits | None = None
    cics_traits: user.CICSUserTraits | None = None
    kerb_traits: user.KerbUserTraits | None = None
    eim_traits: user.EIMUserTraits | None = None
    lang_traits: user.LanguageUserTraits | None = None
    dce_traits: user.DCEUserTraits | None = None
    dfp_traits: user.DFPUserTraits | None = None
    nds_traits: user.NDSUserTraits | None = None
    lnotes_traits: user.LnotesUserTraits | None = None
    mfa_traits: user.MfaUserTraits | None = None
    ovm_traits: user.OvmUserTraits | None = None
    proxy_traits: user.ProxyUserTraits | None = None
    workattr_traits: user.WorkattrUserTraits | None = None
    netview_traits: user.NetviewUserTraits | None = None
    operparm_traits: user.OperparmUserTraits | None = None

    mode: PanelMode = PanelMode.create
    username: str = ""


class PanelUser(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelUserInfo()
        yield PanelUserName()
        yield PanelUserOwnership()
        yield PanelUserInstalldata()
        yield PanelUserPassword()
        yield PanelUserPassphrase()
        yield PanelUserAccess()
        yield PanelUserDatasets()
        yield PanelUserAttributes()
        yield PanelUserSegments()
        yield PanelUserActionButtons(save_action="save_user", delete_action="delete_user")
    
    user_info: reactive[UserInfo] = reactive(UserInfo())
    
    def on_mount(self) -> None:
        if user.user_exists(self.user_info.username):
            self.query_exactly_one("#username",Input).value = self.user_info.username.upper()
            if self.user_info.base_traits is not None:
                set_traits_in_input(self,traits=self.user_info.base_traits,prefix="base")
            
            if self.user_info.tso_traits is not None:
                set_traits_in_input(self,traits=self.user_info.tso_traits,prefix="tso")

            if self.user_info.omvs_traits is not None:
                set_traits_in_input(self,traits=self.user_info.omvs_traits,prefix="omvs")
                
            if self.user_info.cics_traits is not None:
                set_traits_in_input(self,traits=self.user_info.cics_traits,prefix="cics")
            
            if self.user_info.mfa_traits is not None:
                set_traits_in_input(self,traits=self.user_info.mfa_traits,prefix="mfa")

            if self.user_info.lang_traits is not None:
                set_traits_in_input(self,traits=self.user_info.lang_traits,prefix="language")
            
            if self.user_info.dce_traits is not None:
                set_traits_in_input(self,traits=self.user_info.dce_traits,prefix="dce")

            if self.user_info.dfp_traits is not None:
                set_traits_in_input(self,traits=self.user_info.dfp_traits,prefix="dfp")

            if self.user_info.netview_traits is not None:
                set_traits_in_input(self,traits=self.user_info.netview_traits,prefix="netview")

            if self.user_info.lnotes_traits is not None:
                set_traits_in_input(self,traits=self.user_info.lnotes_traits,prefix="lnotes")

            if self.user_info.ovm_traits is not None:
                set_traits_in_input(self,traits=self.user_info.ovm_traits,prefix="ovm")

            if self.user_info.nds_traits is not None:
                set_traits_in_input(self,traits=self.user_info.nds_traits,prefix="nds")

            if self.user_info.workattr_traits is not None:
                set_traits_in_input(self,traits=self.user_info.workattr_traits,prefix="workattr")

            if self.user_info.proxy_traits is not None:
                set_traits_in_input(self,traits=self.user_info.proxy_traits,prefix="proxy")

            if self.user_info.eim_traits is not None:
                set_traits_in_input(self,traits=self.user_info.eim_traits,prefix="eim")
            
            if self.user_info.operparm_traits is not None:
                set_traits_in_input(self,traits=self.user_info.operparm_traits,prefix="operparm")

            self.set_edit_mode()

    def set_edit_mode(self):
        #user_name_panel = self.get_child_by_type(PanelUserName)
        #user_name_panel.mode = PanelMode.edit
        self.query_exactly_one("#username",Input).disabled = True
        self.query_exactly_one("#delete",Button).disabled = False
        self.query_exactly_one("#save",Button).label = f"{get_emoji("💾")} Save"
        self.notify("Switched to edit mode",severity="information")

    def action_delete_user_api(self):
        username = self.get_child_by_type(PanelUserName).get_child_by_id("username",Input).value
        if user.user_exists(username=username):
            message, return_code = user.delete_user(username)
            
            if (return_code == 0):
                self.notify(f"User {username} deleted, return code: {return_code}",severity="warning")
            else:
                self.notify(f"{message}, return code: {return_code}",severity="error")

    def action_delete_user(self) -> None:
        username = self.get_child_by_type(PanelUserName).get_child_by_id("username",Input).value
        generic_confirmation_modal(self,modal_text=f"Are you sure you want to delete user {username}?",confirm_action="delete_user_api",action_widget=self)

    def action_save_user(self) -> None:
        username = self.get_child_by_type(PanelUserName).get_child_by_id("username",Input).value
        user_exists = user.user_exists(username=username)

        operator = "alter" if user_exists else "add"
        
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

        user_object = user.UserObject(
            base_traits=base_segment,
            tso_traits=tso_segment,
            omvs_traits=omvs_segment,
            cics_traits=cics_segment,
            workattr_traits=workattr_segment,
            language_traits=language_segment,
            dfp_traits=dfp_segment,
            dce_traits=dce_segment,
            proxy_traits=proxy_segment,
            operparm_traits=operparm_segment,
            ovm_traits=ovm_segment,
            eim_traits=eim_segment,
            nds_traits=nds_segment,
            lnotes_traits=lnotes_segment,
            mfa_traits=mfa_segment,
            netview_traits=netview_segment,
        )

        result = user.update_user(
            username=username,
            create=not user_exists,
            user_object=user_object,
        )

        if not user_exists:
            if (result == 0 or result == 4):
                self.notify(f"User {username} created, return code: {result}",severity="information")
                self.set_edit_mode()
            else:
                send_notification(self,message=f"Unable to create user, return code: {result}",severity="error")
        else:
            if result == 0:
                self.notify(f"User {username} updated, return code: {result}",severity="information")
            else:
                send_notification(self,message=f"Unable to update user, return code: {result}",severity="error")
