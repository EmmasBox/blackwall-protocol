from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Collapsible, Input, Label, RadioButton, Select

from blackwall.api import resource
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


class PanelResourceInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Creation date:",classes="date-labels")
        yield Input(id="base_create_date",disabled=True,classes="date-fields")
        yield Label("Last change date:",classes="date-labels")
        yield Input(id="base_last_change_date",disabled=True,classes="date-fields")
        yield Label("Last reference time:",classes="date-labels")
        yield Input(id="base_last_reference_date",disabled=True,classes="date-fields")

class PanelResourceName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input(max_length=255,id="resource_profile_name",classes="resource-name-field")

class PanelResourceClassAndOwner(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Class:")
        yield Input(max_length=8,id="resource_profile_class",classes="class-field")
        yield Label("Owner:")
        yield Input(max_length=8,restrict=racf_id_regex,id="base_owner",classes="class-field")

class PanelResourceInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="base_installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelResourceAccess(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("UACC:")
        yield Select([("NONE", "NONE"),("READ", "READ"),("EXECUTE", "EXECUTE"),("UPDATE", "UPDATE"),("CONTROL", "CONTROL"),("ALTER", "ALTER")],value="NONE",classes="uacc-select",id="base_universal_access",tooltip="It's advised that you keep this at NONE, UACC read or higher are unsecure, see z/OS RACF Administrator's Guide for more details")
        yield RadioButton(label="Warn on insufficient access",id="base_warn_on_insufficient_access",classes="generic-checkbox-medium")
        yield Label("Notify userid:")
        yield Input(id="base_notify_userid",restrict=racf_id_regex,max_length=8,classes="field-short-generic")

class PanelResourceSecurityLevelAndCategories(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible(title="Security level and category"):
            yield Label("Security level")
            yield Input(max_length=8,id="base_security_level",classes="field-short-generic")
            yield Label("Security category:")
            yield Input(max_length=8,id="base_security_category",classes="field-short-generic")
            yield Label("Security label:")
            yield Input(max_length=8,id="base_security_label",classes="field-short-generic")

class PanelResourceSegments(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible(title="Resource profile segments"):
            yield from generate_trait_section(title="Started task data", prefix="stdata", traits_class=resource.STDATAResourceTraits)
            yield from generate_trait_section(title="ICSF", prefix="icsf", traits_class=resource.ICSFResourceTraits)
            yield from generate_trait_section(title="ICTX", prefix="ictx", traits_class=resource.ICTXResourceTraits)
            yield from generate_trait_section(title="JES", prefix="jes", traits_class=resource.JESResourceTraits)
            yield from generate_trait_section(title="Kerberos", prefix="kerb", traits_class=resource.KerbResourceTraits)
            yield from generate_trait_section(title="EIM", prefix="eim", traits_class=resource.EIMResourceTraits)
            yield from generate_trait_section(title="DLF data", prefix="dlfdata", traits_class=resource.DLFDataResourceTraits)
            yield from generate_trait_section(title="IDTPARMS", prefix="idtparms", traits_class=resource.IDTPARMSResourceTraits)
            yield from generate_trait_section(title="Session", prefix="session", traits_class=resource.SessionResourceTraits)
            yield from generate_trait_section(title="SVFMR", prefix="svfmr", traits_class=resource.SVFMRResourceTraits)
            yield from generate_trait_section(title="Proxy", prefix="proxy", traits_class=resource.ProxyResourceTraits)
            yield from generate_trait_section(title="MF policy", prefix="mfpolicy", traits_class=resource.MFPolicyResourceTraits)
            yield from generate_trait_section(title="SIGVER", prefix="sigver", traits_class=resource.SIGVERResourceTraits)
            yield from generate_trait_section(title="tme", prefix="tme", traits_class=resource.TMEResourceTraits)
            yield from generate_trait_section(title="SSIGNON", prefix="ssignon", traits_class=resource.SSIGNONResourceTraits)
            yield from generate_trait_section(title="Cfdef", prefix="Cfdef", traits_class=resource.CfdefResourceTraits)
            yield from generate_trait_section(title="Class Descriptor Table (CDT) info", prefix="cdtinfo", traits_class=resource.CDTINFOResourceTraits)

class PanelResourceActionButtons(HorizontalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    delete_is_disabled = edit_mode is not True

    def __init__(self, save_action: str, delete_action: str):
        super().__init__()
        self.save_action = save_action
        self.delete_action = delete_action
    
    def compose(self) -> ComposeResult:
        yield Button("Create",id="save",action="save",classes="action-button")
        yield Button("Delete",action="delete",id="delete",variant="error",classes="action-button",disabled=self.delete_is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

@dataclass
class ResourceInfo:
    base_traits: resource.BaseResourceTraits | None = None
    kerb_traits: resource.KerbResourceTraits | None = None
    dlf_traits: resource.DLFDataResourceTraits | None = None
    eim_traits: resource.EIMResourceTraits | None = None
    jes_traits: resource.JESResourceTraits | None = None
    icsf_traits: resource.ICSFResourceTraits | None = None
    ictx_traits: resource.ICTXResourceTraits | None = None
    idtparms_traits: resource.IDTPARMSResourceTraits | None = None
    session_traits: resource.SessionResourceTraits | None = None
    svfmr_traits: resource.SVFMRResourceTraits | None = None
    stdata_traits: resource.STDATAResourceTraits | None = None
    proxy_traits: resource.ProxyResourceTraits | None = None
    mfpolicy_traits: resource.MFPolicyResourceTraits | None = None
    sigver_traits: resource.SIGVERResourceTraits | None = None
    tme_traits: resource.TMEResourceTraits | None = None
    cdtinfo_traits: resource.CDTINFOResourceTraits | None = None
    ssignon_traits: resource.SSIGNONResourceTraits | None = None
    cfdef_traits: resource.CfdefResourceTraits | None = None
    mode: PanelMode = PanelMode.create

    resource_name: str = ""
    resource_class: str = ""

class PanelResource(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourceInfo()
        yield PanelResourceName()
        yield PanelResourceClassAndOwner()
        yield PanelResourceInstallationData()
        yield PanelResourceAccess()
        yield PanelResourceSecurityLevelAndCategories()
        yield PanelResourceSegments()
        yield PanelResourceActionButtons(save_action="save_resource_profile", delete_action="delete_resource_profile")

    resource_info: reactive[ResourceInfo] = reactive(ResourceInfo())

    def set_edit_mode(self):
        self.query_exactly_one("#resource_profile_name",Input).disabled = True
        self.query_exactly_one("#resource_profile_class",Input).disabled = True
        self.query_exactly_one("#delete",Button).disabled = False
        self.query_exactly_one("#save",Button).label = f"{get_emoji("💾")} Save"
        self.notify("Switched to edit mode",severity="information")

    def on_mount(self) -> None:
        if resource.resource_profile_exists(resource=self.resource_info.resource_name,resource_class=self.resource_info.resource_class):
            self.query_exactly_one("#resource_profile_name",Input).value = self.resource_info.resource_name
            self.query_exactly_one("#resource_profile_class",Input).value = self.resource_info.resource_class
            if self.resource_info.base_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.base_traits,prefix="base")
            
            if self.resource_info.kerb_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.kerb_traits,prefix="kerb")

            if self.resource_info.dlf_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.dlf_traits,prefix="dlf")

            if self.resource_info.eim_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.eim_traits,prefix="eim")

            if self.resource_info.jes_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.jes_traits,prefix="jes")

            if self.resource_info.icsf_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.icsf_traits,prefix="icsf")

            if self.resource_info.ictx_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.ictx_traits,prefix="ictx")

            if self.resource_info.idtparms_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.idtparms_traits,prefix="idtparms")

            if self.resource_info.session_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.session_traits,prefix="session")

            if self.resource_info.svfmr_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.svfmr_traits,prefix="svfmr")

            if self.resource_info.stdata_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.stdata_traits,prefix="stdata")

            if self.resource_info.proxy_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.proxy_traits,prefix="proxy")

            if self.resource_info.mfpolicy_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.mfpolicy_traits,prefix="mfpolicy")

            if self.resource_info.sigver_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.sigver_traits,prefix="sigver")

            if self.resource_info.tme_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.tme_traits,prefix="tme")
            
            if self.resource_info.cdtinfo_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.cdtinfo_traits,prefix="cdtinfo")

            if self.resource_info.ssignon_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.ssignon_traits,prefix="ssignon")

            if self.resource_info.cfdef_traits is not None:
                set_traits_in_input(self,traits=self.resource_info.cfdef_traits,prefix="cfdef")

            self.set_edit_mode()

    def action_delete_resource_profile_api(self):
        resource_profile_name = self.get_child_by_type(PanelResourceName).get_child_by_id("resource_profile_name",Input).value
        resource_profile_class = self.get_child_by_type(PanelResourceClassAndOwner).get_child_by_id("resource_profile_class",Input).value
        if resource.resource_profile_exists(resource_class=resource_profile_class,resource=resource_profile_name):
            message, return_code = resource.delete_resource_profile(resource_class=resource_profile_class,resource=resource_profile_name)
            
            if (return_code == 0):
                self.notify(f"Resource profile {resource_profile_name} deleted, return code: {return_code}",severity="warning")
            else:
                self.notify(f"{message}, return code: {return_code}",severity="error")

    def action_delete_resource_profile(self) -> None:
        resource_profile_name = self.get_child_by_type(PanelResourceName).get_child_by_id("resource_profile_name",Input).value
        resource_profile_class = self.get_child_by_type(PanelResourceClassAndOwner).get_child_by_id("resource_profile_class",Input).value
        generic_confirmation_modal(self,modal_text=f"Are you sure you want to delete resource profile {resource_profile_name} in {resource_profile_class}?",confirm_action="delete_resource_profile_api",action_widget=self)


    def action_save_resource_profile(self) -> None:
        resource_profile_name = self.get_child_by_type(PanelResourceName).get_child_by_id("resource_profile_name",Input).value
        resource_profile_class = self.get_child_by_type(PanelResourceClassAndOwner).get_child_by_id("resource_profile_class",Input).value
        resource_profile_exists = resource.resource_profile_exists(resource=resource_profile_name,resource_class=resource_profile_class)

        operator = "alter" if resource_profile_exists else "add"

        base_segment = get_traits_from_input(operator,self, prefix="base", trait_cls=resource.BaseResourceTraits)
        kerb_segment = get_traits_from_input(operator,self, prefix="kerb", trait_cls=resource.KerbResourceTraits)
        dlfdata_segment = get_traits_from_input(operator,self, prefix="dlfdata", trait_cls=resource.DLFDataResourceTraits)
        eim_segment = get_traits_from_input(operator,self, prefix="eim", trait_cls=resource.EIMResourceTraits)
        jes_segment = get_traits_from_input(operator,self, prefix="jes", trait_cls=resource.JESResourceTraits)
        icsf_segment = get_traits_from_input(operator,self, prefix="icsf", trait_cls=resource.ICSFResourceTraits)
        ictx_segment = get_traits_from_input(operator,self, prefix="ictx", trait_cls=resource.ICTXResourceTraits)
        idtparms_segment = get_traits_from_input(operator,self, prefix="idtparms", trait_cls=resource.IDTPARMSResourceTraits)
        session_segment = get_traits_from_input(operator,self, prefix="session", trait_cls=resource.SessionResourceTraits)
        svfmr_segment = get_traits_from_input(operator,self, prefix="svfmr", trait_cls=resource.SVFMRResourceTraits)
        stdata_segment = get_traits_from_input(operator,self, prefix="stdata", trait_cls=resource.STDATAResourceTraits)
        proxy_segment = get_traits_from_input(operator,self, prefix="proxy", trait_cls=resource.ProxyResourceTraits)
        mfpolicy_segment = get_traits_from_input(operator,self, prefix="mfpolicy", trait_cls=resource.MFPolicyResourceTraits)
        sigver_segment = get_traits_from_input(operator,self, prefix="sigver", trait_cls=resource.SIGVERResourceTraits)
        tme_segment = get_traits_from_input(operator,self, prefix="tme", trait_cls=resource.TMEResourceTraits)
        cdtinfo_segment = get_traits_from_input(operator,self, prefix="cdtinfo", trait_cls=resource.CDTINFOResourceTraits)
        ssignon_segment = get_traits_from_input(operator,self, prefix="ssignon", trait_cls=resource.SSIGNONResourceTraits)
        cfdef_segment = get_traits_from_input(operator,self, prefix="cfdef", trait_cls=resource.CfdefResourceTraits)

        resource_object = resource.ResourceObject(
            base_traits=base_segment,
            kerb_traits=kerb_segment,
            dlf_traits=dlfdata_segment,
            eim_traits=eim_segment,
            jes_traits=jes_segment,
            icsf_traits=icsf_segment,
            ictx_traits=ictx_segment,
            idtparms_traits=idtparms_segment,
            session_traits=session_segment,
            svfmr_traits=svfmr_segment,
            stdata_traits=stdata_segment,
            proxy_traits=proxy_segment,
            mfpolicy_traits=mfpolicy_segment,
            sigver_traits=sigver_segment,
            tme_traits=tme_segment,
            cdtinfo_traits=cdtinfo_segment,
            ssignon_traits=ssignon_segment,
            cfdef_traits=cfdef_segment,
        )

        result = resource.update_resource_profile(
            resource=resource_profile_name,
            resource_class=resource_profile_class,
            create=not resource_profile_exists,
            resource_object=resource_object,
            )
        
        if not resource_profile_exists:
            if (result == 0 or result == 4):
                self.notify(f"General resource profile {resource_profile_name} created, return code: {result}",severity="information")
                #self.set_edit_mode()
            else:
                send_notification(self,message=f"Unable to create general resource profile, return code: {result}",severity="error")
        else:
            if result == 0:
                self.notify(f"General resource profile {resource_profile_name} updated, return code: {result}",severity="information")
            else:
                send_notification(self,message=f"Unable to update general resource profile, return code: {result}",severity="error")
